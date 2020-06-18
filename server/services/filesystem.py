from models.source import SourceModel
from typing import Dict
import s3fs
import io


class FileSystem:
    def __init__(
        self,
        name: str = "S3",
        credential: Dict = None,
        authorization_name: str = "Default"
    ):
        self.name = name
        source = SourceModel.find_by_name(name)
        authorization = source.find_authorization_by_name(authorization_name)
        self.credential = credential or authorization.credential if authorization else None
        self.client = self.get_client()
        
    def get_client(self):
        if self.name == "S3":
            if self.credential:
                fs = s3fs.S3FileSystem(
                    key=self.credential["aws_access_key_id"],
                    secret=self.credential["aws_secret_access_key"]
                )
                
            else:
                fs = s3fs.S3FileSystem(anon=True)
            
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