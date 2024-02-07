import os
from datasetmanipulation.abstr import DataSetAbstr

# Subtitles dataset class
class DataSetSubtitles(DataSetAbstr):

    def __init__(self) -> None:
        super().__init__()

        self.DIR_SUBTITLES = os.path.join(self.DIR_PATH, 'dataset/subtitles')
        # Subtitles files extension
        self.subt_ext = ".srt"
        # Subtitles files encoding (play with it)
        self.encoding = "ISO-8859-1"
        # Timecodes. Changeable, see to ffmpeg command in dataroutine.sh file
        self.starttime = '00:01:'
        self.endtime = '00:02:'
        # Redis: key
        self.DOC_PREFIX = 'episode:'
        # Redis: index key
        self.INDEX_NAME = 'episodesIdxV'
        # Redis: fieldname to embed
        self.EMBED_NAME = 'subtitle'


    # Utility function
    # Function to extract fragment between two timecode strings
    def extract_fragment(self, file_path) -> str:

        # UTF8 sometimes not a case, so read file with 'Latin-1'
        # ----- To be improved -----
        with open(file_path, 'r', encoding = self.encoding) as file:
            file_content = file.read()
            start_index = file_content.find(self.starttime)
            end_index = file_content.find(self.endtime, start_index)
            if start_index != -1 and end_index != -1:
                fragment = file_content[start_index:end_index+33]
                return fragment
            else:
                return ''


    # Prepare data
    def prepare(self) -> list:
        # Loop over the directory with subtitle files
        for filename in os.listdir(self.DIR_SUBTITLES):
            # Check if we have subtitles files
            if filename.endswith(self.subt_ext):
                file_path = os.path.join(self.DIR_SUBTITLES, filename)
                # Extract subtitles by timecode
                extracted_fragment = self.extract_fragment(file_path)

                if (extracted_fragment) :
                    subtitles = DataSetAbstr.filter_data_string(extracted_fragment)
                    add_data = list(filename[:-4].split(" - "))
                    subtitle_data = {"tvshow":add_data[0], 
                            "season":add_data[1][1:-3],
                            "episode":add_data[1][4:],
                            "subtitle_filename":filename,
                            "subtitle":subtitles}
                    # Append episode data to dataset
                    self.datasetresult.append(subtitle_data)
        
        return self.datasetresult
        