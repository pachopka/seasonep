import numpy as np
import os
import pandas as pd
import re
import redis
from redis.commands.search.field import TextField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from sentence_transformers import SentenceTransformer

# OS path-related constants
DIR_PATH = os.path.dirname(__file__)
DIR_SUBTITLES = os.path.join(DIR_PATH, 'dataset/subtitles')
DIR_TRANSCRIPTED = os.path.join(DIR_PATH, 'dataset/transcripted')
DIR_AUDIO = os.path.join(DIR_PATH, 'dataset/audio')
DIR_VIDEO = os.path.join(DIR_PATH, 'dataset/video')
# SentenceTransformer-related constants
EMBEDDER = SentenceTransformer('sentence-t5-base')
VECTOR_DIMENSION = 768
# Redis-related constants
CLIENT = redis.Redis(host='localhost', port=6379, decode_responses=True)
INDEX_NAME = 'episodesIdxV'
DOC_EP_PREFIX = 'episode:'
DOC_TR_PREFIX = 'transcription:'

# Redis functions
# Send key:value pairs to Redis via pipelne
def sendtoRedis(data, key) -> None:
    # Redis pipeline
    pipeline = CLIENT.pipeline()

    # Send data to redis via pipeline
    for i, data_item in enumerate(data, start=1):
        redis_key = f'{key}{i:03}'
        pipeline.json().set(redis_key, '$', data_item)

    pipeline.execute()

# Prepare and send vectorized text field output to Redis via pipeline
def vectorizeRedis(ikey, fieldname) -> None:
    keys = sorted(CLIENT.keys(ikey+'*'))

    textfield = CLIENT.json().mget(keys, '$.'+fieldname)
    textfield_data = [item for sublist in textfield for item in sublist]
    embeddings = EMBEDDER.encode(textfield_data).astype(np.float32).tolist()

    # Redis pipeline
    pipeline = CLIENT.pipeline()
    for key, embedding in zip(keys, embeddings):
        pipeline.json().set(key, '$.'+fieldname+'_embeddings', embedding)

    pipeline.execute()

# Create Index to make a vector search possible
def crIndexRedis() -> None:
    schema = (
        TextField('$.season', no_stem=True, as_name='season'),
        TextField('$.subtitle', as_name='subtitle'),
        TextField('$.subtitle_filename', no_stem=True, as_name='filename'),
        VectorField('$.subtitle_embeddings',
            'FLAT', {
                'TYPE': 'FLOAT32',
                'DIM': VECTOR_DIMENSION,
                'DISTANCE_METRIC': 'COSINE',
            },  as_name='vector'
        ),
    )

    # Index Definition
    definition = IndexDefinition(prefix=[DOC_EP_PREFIX], index_type=IndexType.JSON)

    # Index Creation
    CLIENT.ft(INDEX_NAME).create_index(fields=schema, definition=definition)


# Utility function
# Prepare the text fragment
def filterString(input_string) -> str:
    # Remove digits, colons, special sequinses and empty lines
    filtered_string = re.sub(r'[\d:]', '', input_string)
    filtered_string = filtered_string.replace(', --> ,', '')
    filtered_string = filtered_string.replace('<i>', '')
    filtered_string = filtered_string.replace('</i>', '')
    result = " ".join(
        line.strip() for line in filtered_string[1:].splitlines()
        if line.strip() != '')
    
    return result


# Episodes data part of the deal
class Episodes:

    def __init__(self) -> None:
        self.episodes = []

    # Function to extract fragment between two strings
    def extractFragment(self, file_path) -> str|None:
        # UTF8 sometimes not a case...
        with open(file_path, 'r', encoding = "ISO-8859-1") as file:
            file_content = file.read()
            start_index = file_content.find('00:01:')
            end_index = file_content.find('00:02:', start_index)
            if start_index != -1 and end_index != -1:
                fragment = file_content[start_index:end_index+33]
                return fragment
            else:
                return None

    # Prepare data
    def prepare(self) -> None:
        # Loop over the directory with subtitle files
        for filename in os.listdir(DIR_SUBTITLES):
            if filename.endswith(".srt"):
                file_path = os.path.join(DIR_SUBTITLES, filename)
                extracted_fragment = self.extractFragment(file_path)
                subtitles = filterString(extracted_fragment)
                add_data = list(filename[:-4].split(" - "))
                episode = {"tvshow":add_data[0], 
                            "season":add_data[1][1:-3],
                            "episode":add_data[1][4:],
                            "title":add_data[2],
                            "subtitle_filename":filename,
                            "subtitle":subtitles}
                self.episodes.append(episode)

        print('Episodes data has been prepared')

        sendtoRedis(self.episodes, DOC_EP_PREFIX)
        print('Episodes data has been sent to Redis')

        vectorizeRedis(DOC_EP_PREFIX, 'subtitle')
        print('Vector data for Episodes has been sent to Redis')

        crIndexRedis()
        print('Redis Index has been created')


# Transcripted data part of the deal
class Transcriptions:

    def __init__(self) -> None:
        self.transcriptions = []

    # Prepare data
    def prepare(self) -> None:
        # Loop over the directory with transcripted files
        for filename in os.listdir(DIR_TRANSCRIPTED):
            if filename.endswith(".txt"):
                file_path = os.path.join(DIR_TRANSCRIPTED, filename)
                with open(file_path, 'r') as file:
                    file_content = file.read()
                    transcripted_text = filterString(file_content)
                    transcription = {
                        "filename":filename[0:-4],
                        "transcription":transcripted_text
                    }
                    self.transcriptions.append(transcription)
        print('Transcriptions data has been prepared')

        sendtoRedis(self.transcriptions, DOC_TR_PREFIX)
        print('Transcriptions data has been sent to Redis')

        vectorizeRedis(DOC_TR_PREFIX, 'transcription')
        print('Vector data for Transcriptions has been sent to Redis')


episodes = Episodes().prepare()

transcriptions = Transcriptions().prepare()

# Have all needed now
# Search in Redis Index using Vector Search Similarity (VSS)
def shIndexRedisVss() -> list:

    print('Combine and search on Redis')
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
    transcrptions_keys = CLIENT.keys(DOC_TR_PREFIX+'*')
    for tr_key in transcrptions_keys:
        tr_embed = CLIENT.json().get(tr_key, '$.transcription_embeddings')
        tr_filename = CLIENT.json().get(tr_key, '$.filename')
        # Search in Index
        result_docs = CLIENT.ft(INDEX_NAME).search(range_query, { 'query_vector': np.array(tr_embed, dtype=np.float32).tobytes() }).docs
        for doc in result_docs:
            # Flag variable, too much loops...
            check_next = False
            vector_score = round(1 - float(doc.vector_score), 2)
            filename = doc.filename[0:-4].replace(',','')
            # Checking if we already have same filename recorded
            for i, sublist in enumerate(findings):
                if sublist[2] == filename:
                    # There is a better guess now, replace it
                    if sublist[3] < vector_score:
                        findings.pop(i)
                    # Lower score now, continue to the next item
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

# Results are here
results = shIndexRedisVss()

print('Magic done')

# Creating CSV file
exportFrame = pd.DataFrame(results, columns=['Video','Season', 'Filename', 'Score'])
exportFrame.to_csv('dataset/results.csv')
print('Csv file with results was created')
