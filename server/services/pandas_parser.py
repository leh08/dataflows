from services.filesystem import FileSystem
from typing import Dict
import pandas as pd
import io


class PandasParser():
    """ Perform standard parsing jobs on a csv string """

    def __init__(self):
        """ Configures the parsing required for the test resource """
        self.fs = FileSystem()


    def parse_data(self, stream, extension, HEADER_END: str = None, FOOTER_END: str = None, params: Dict = dict()):
        """ Get the parsed output as a list of tuples representing records
        Pandas probably unnecessary here """

        data = stream.decode()
        
        skiprows = self.get_rows_to_skip(data, HEADER_END)
        skipfooter = self.get_footer_to_skip(data, FOOTER_END)
        params.update(dict(
            na_values = ['n.a.', '#ERROR!','None'],
            skiprows = skiprows,
            skipfooter = skipfooter
        ))
                                   
        df = self.get_dataframe(data, extension, params)
        
        return df

    
    
    def get_dataframe(self, data, extension, params):
        if 'csv' in extension:
            return pd.read_csv(io.StringIO(data), **params)
        
        elif ["xls", "xlsx", "xlsm", "xlsb"] in extension:
            return pd.read_excel(io.StringIO(data),  **params)
    
    
    def get_rows_to_skip(self, data, HEADER_END):
        """ Find the number of rows to skip  based on the header end string """
        
        if HEADER_END is None: 
            return 0
            
        else:
            for count, value in enumerate(data, start=1): 
                if HEADER_END in value:
                    # Then we've found the end of the header        
                    return count

    
    def get_footer_to_skip(self,data, FOOTER_END):
        """ Find the number of rows to skip  based on the footer end string """
        
        if FOOTER_END is None:
            return 0
                
        else:
            for count, value in enumerate(reversed(data),start=1):
                if FOOTER_END in value:
                    return count + 1