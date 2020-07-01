from models.source import SourceModel

import s3fs
import io


class FileSystem:
    def __init__(
        self,
        name: str = "S3",
        authorization_name: str = None
    ):
        self.name = name
        self.client = self.get_client(authorization_name)
        
    def get_client(self, authorization_name):
        if self.name == "S3":
            if authorization_name:
                source = SourceModel.find_by_name(self.name)
                authorization = source.find_authorization_by_name(authorization_name)
                credential = authorization.credential if authorization else None
                fs = s3fs.S3FileSystem(
                    key=credential["aws_access_key_id"],
                    secret=credential["aws_secret_access_key"]
                )
                
            else:
                fs = s3fs.S3FileSystem(anon=False)
            
        else:
            ValueError("A filesystem, " + self.name + ", wasn't set up to run in this system.")
        
        return fs 
    
    def cloud_download(self, blob_key: str):
        ## download
        with self.client.open(blob_key, 'rb') as file:     
            stream = file.read()
            
        return stream
    
    def cloud_upload(self, data: str, blob_key: str):      
        ## prepare data
        try:
            stream = io.BytesIO(data.encode())
            
        except AttributeError:
            stream = data
        
        ## upload
        with self.client.open(blob_key, 'wb') as file:
            file.write(stream)
        
        return blob_key