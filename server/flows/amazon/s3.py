from flows.flow import Flow

from services.struct import Struct


class S3(Flow):
    def discover(self):
        file_ids = []
        
        objects = self.source.client.ls(self.report, detail=True)
        
        for object in objects:
            struct = Struct(**object)
            
            if struct.size > 0:
                file_id = struct.Key.split('/')[-1]
                file_ids.append(file_id)
                    
        return file_ids
    
    def extract(self, file_id):
        if not self.source.client.isdir(self.report):
            stream = self.source.cloud_download(self.report)
            
        else:
            stream = self.source.cloud_download(self.report.rstrip("/") + '/' + file_id)
            
        return stream       
        
    def transform(self, stream, extension):
        df = self.parser.parse_data(stream, extension)
        return df
