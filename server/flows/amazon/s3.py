from flows.flow import Flow

class S3(Flow):

    def discover(self, report):
        return self.source.client.ls(report)
    
    def extract(self, file_id):
        stream = self.source.cloud_download(file_id)
        return stream       
        
    def transform(self, stream, extension):
        df = self.parser.parse_data(stream, extension)
        return df
    
    def generate_file_name(self, file_id):
        file_name = file_id.split("/")[-1]
        return file_name       
