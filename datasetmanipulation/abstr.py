import os
import re
from abc import ABC

# Abstraction of Dataset class
class DataSetAbstr(ABC):

    def __init__(self) -> None:
        self.DIR_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
        self.datasetresult = []
    
    # Utility function
    # Prepare the text fragment
    def filter_data_string(input_string) -> str:
        # Remove digits, colons, empty lines etc.
        # ----- To be improved -----
        filtered_string = re.sub(r'[\d:]', '', input_string)
        filtered_string = filtered_string.replace(', --> ,', '')
        filtered_string = filtered_string.replace('<i>', '')
        filtered_string = filtered_string.replace('</i>', '')
        result = " ".join(
            line.strip() for line in filtered_string[1:].splitlines()
            if line.strip() != '')
    
        return result

    # Prepare data
    def prepare(self) -> None: 
        pass