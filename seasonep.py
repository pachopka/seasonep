import pandas as pd
from datasetmanipulation.subtitles import DataSetSubtitles
from datasetmanipulation.transcriptions import DataSetTranscriptions
from utility.colorcodes import Colorcodes
from utility.redistasks import RedisTasks
from redis.commands.search.field import TextField, VectorField

# Sentence Transformer model name and dimension 
SENTRANSFMOD = 'sentence-t5-base'
VECTOR_DIMENSION = 768


# Prepare Redis client
redistasks = RedisTasks()

# Prepare Colocodes for print statements
_c = Colorcodes()


# Prepare Subtitles dataset
subtitles = DataSetSubtitles()
subtitles_dataset = subtitles.prepare()
if (subtitles_dataset):
    print(_c.white + _c.background_green + 'Subtitles dataset has been prepared' + _c.reset)

    redistasks.send_to_redis(subtitles_dataset, subtitles.DOC_PREFIX)
    print(_c.white + _c.background_green + 'Subtitles dataset has been sent to Redis' + _c.reset)

    redistasks.vectorize_redis(subtitles.DOC_PREFIX, subtitles.EMBED_NAME, SENTRANSFMOD)
    print(_c.white + _c.background_green + 'Vector data for Subtitles dataset has been sent to Redis' + _c.reset)

    # Prepare Redis index
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
    redistasks.create_redis_index(schema, subtitles.DOC_PREFIX, subtitles.INDEX_NAME)

else: print(_c.white + _c.background_red + 'Subtitles dataset has not been prepared' + _c.reset)


# Prepare Transcriptions dataset
transcriptions = DataSetTranscriptions()
transcriptions_dataset = transcriptions.prepare()
if (transcriptions_dataset):
    print(_c.white + _c.background_green + 'Transcriptions dataset has been prepared' + _c.reset)

    redistasks.send_to_redis(transcriptions_dataset, transcriptions.DOC_PREFIX)
    print(_c.white + _c.background_green + 'Transcriptions dataset has been sent to Redis' + _c.reset)
    
    redistasks.vectorize_redis(transcriptions.DOC_PREFIX, transcriptions.EMBED_NAME, SENTRANSFMOD)
    print(_c.white + _c.background_green + 'Vector data for Transcriptions has been sent to Redis' + _c.reset)

else: print(_c.white + _c.background_red + 'Transcriptions dataset has not been prepared' + _c.reset)


# Make a vector-based search and return CSV file
if (transcriptions_dataset and subtitles_dataset):
    results = redistasks.search_redis_index_vss(transcriptions.DOC_PREFIX, subtitles.INDEX_NAME)
    if (results):
        # Creating CSV file
        exportFrame = pd.DataFrame(results, columns=['Video', 'Season', 'Filename', 'Score'])
        exportFrame.to_csv('dataset/results.csv')
        print(_c.white + _c.background_blue + 'Magic done. Csv file with results was created' + _c.reset)
    else:
        print(_c.white + _c.background_red + 'Step 3: Smth went wrong' + _c.reset)