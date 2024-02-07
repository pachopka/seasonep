import os
from datasetmanipulation.abstr import DataSetAbstr

# Transcription dataset class
class DataSetTranscriptions(DataSetAbstr):

    def __init__(self) -> None:
        super().__init__()

        self.DIR_TRANSCRIPTED = os.path.join(self.DIR_PATH, 'dataset/transcripted')
        # Transcription files extension
        self.transcr_ext = ".txt"
        # Redis key
        self.DOC_PREFIX = 'transcription:'
        # Redis: fieldname to embed
        self.EMBED_NAME = 'transcription_text'


    # Prepare data
    def prepare(self) -> list:
        # Loop over the directory with transcripted files
        for filename in os.listdir(self.DIR_TRANSCRIPTED):
            # Check if we have transcriptions files
            if filename.endswith(self.transcr_ext):
                file_path = os.path.join(self.DIR_TRANSCRIPTED, filename)
                with open(file_path, 'r') as file:
                    file_content = file.read()
                    transcripted_text = DataSetAbstr.filter_data_string(file_content)
                    transcription = {
                        "filename":filename[0:-4],
                        "transcription_text":transcripted_text
                    }
                    # Append transcription info to dataset
                    self.datasetresult.append(transcription)
        
        return self.datasetresult