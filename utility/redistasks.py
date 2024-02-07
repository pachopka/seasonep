import redis
import numpy as np
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from sentence_transformers import SentenceTransformer

# Redis-related operations class
class RedisTasks():

    def __init__(self) -> None:
        self.client = redis.Redis(host='localhost', port=6379, decode_responses=True)


    # Send key:value pairs to Redis via pipelne
    def send_to_redis(self, data, key) -> None:
        # Redis pipeline
        pipeline = self.client.pipeline()

        # Send data to redis via pipeline
        for i, data_item in enumerate(data, start=1):
            redis_key = f'{key}{i:03}'
            pipeline.json().set(redis_key, '$', data_item)

        pipeline.execute()


    # Prepare and send vectorized text field output to Redis via pipeline
    def vectorize_redis(self, ikey, fieldname, sentransfmod_name) -> None:
        keys = sorted(self.client.keys(ikey+'*'))

        textfield = self.client.json().mget(keys, '$.'+fieldname)
        textfield_data = [item for sublist in textfield for item in sublist]
        embedder = SentenceTransformer(sentransfmod_name)
        embeddings = embedder.encode(textfield_data).astype(np.float32).tolist()

        # Redis pipeline
        pipeline = self.client.pipeline()
        for key, embedding in zip(keys, embeddings):
            pipeline.json().set(key, '$.'+fieldname+'_embeddings', embedding)

        pipeline.execute()


    # Create Index to make a vector search possible
    def create_redis_index(self, schema, prefix, indexname) -> None:

        # Index Definition
        definition = IndexDefinition(prefix=[prefix], index_type=IndexType.JSON)

        # Index Creation
        self.client.ft(indexname).create_index(fields=schema, definition=definition)


    # Search in Redis Index using Vector Search Similarity (VSS)
    def search_redis_index_vss(self, prefix, indexname) -> list:

        #Prepare a query, limit results to 0.60 radius
        range_query = (
            Query('@vector:[VECTOR_RANGE 0.60 $query_vector]=>{$YIELD_DISTANCE_AS: vector_score}') 
            .sort_by('vector_score')
            .return_fields('vector_score', 'id', 'season', 'filename')
            .paging(0, 1)
            .dialect(2)
        )

        findings = []

        # Get keys of all translations entities
        transcrptions_keys = self.client.keys(prefix+'*')

        for tr_key in transcrptions_keys:
            tr_embed = self.client.json().get(tr_key, '$.transcription_text_embeddings')
            tr_filename = self.client.json().get(tr_key, '$.filename')
            # Search in Index
            result_docs = self.client.ft(indexname).search(range_query, { 'query_vector': np.array(tr_embed, dtype=np.float32).tobytes() }).docs
            for doc in result_docs:
                # Flag variable, too much loops...
                check_next = False
                vector_score = round(1 - float(doc.vector_score), 2)
                filename = doc.filename[0:-4].replace(',','')
                # Checking if we already have same filename recorded
                for i, sublist in enumerate(findings):
                    if sublist[2] == filename:
                        # There is a better guess, replace it
                        if sublist[3] < vector_score:
                            findings.pop(i)
                        # Lower score, continue to the next item
                        else:
                            check_next = True
                        break
                if check_next:
                    continue

                findings.append([
                    tr_filename[0],
                    doc.season,
                    filename,
                    vector_score
                ])

        return findings
