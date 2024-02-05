import numpy as np
import pandas as pd
from dataset_subtitles import DataSetSubtitles
from dataset_transcriptions import DataSetTranscriptions
from redis_tasks import RedisTasks
from redis.commands.search.field import TextField, VectorField

# Sentence Transformer model name and dimension 
SENTRANSFMOD = 'sentence-t5-base'
VECTOR_DIMENSION = 768


# Prepare Redis client
redistasks = RedisTasks()


# Prepare Subtitles dataset
subtitles = DataSetSubtitles()
subtitles_dataset = subtitles.prepare()
if (subtitles_dataset):
    print('Subtitles dataset has been prepared')

    redistasks.send_to_redis(subtitles_dataset, subtitles.DOC_PREFIX)
    print('Subtitles dataset has been sent to Redis')
    
    redistasks.vectorize_redis(subtitles.DOC_PREFIX, subtitles.EMBED_NAME, SENTRANSFMOD)
    print('Vector data for Subtitles dataset has been sent to Redis')

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

else: print('Subtitles dataset has not been prepared')


# Prepare Transcriptions dataset
transcriptions = DataSetTranscriptions()
transcriptions_dataset = transcriptions.prepare()
if (transcriptions_dataset):
    print('Transcriptions dataset has been prepared')

    redistasks.send_to_redis(transcriptions_dataset, transcriptions.DOC_PREFIX)
    print('Transcriptions dataset has been sent to Redis')
    
    redistasks.vectorize_redis(transcriptions.DOC_PREFIX, transcriptions.EMBED_NAME, SENTRANSFMOD)
    print('Vector data for Transcriptions has been sent to Redis')

else: print('Transcriptions dataset has not been prepared')


# Make a vector-based search and return CSV file
if (transcriptions_dataset and subtitles_dataset):
    results = redistasks.search_redis_index_vss(transcriptions.DOC_PREFIX, subtitles.INDEX_NAME)
    if (results):
        print('Magic done')

        # Creating CSV file
        exportFrame = pd.DataFrame(results, columns=['Video', 'Season', 'Filename', 'Score'])
        exportFrame.to_csv('dataset/results.csv')
        print('Csv file with results was created')
    else:
        print('Smth went wrong')
