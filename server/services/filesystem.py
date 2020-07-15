from typing import Dict
import os
import s3fs
import io


class FileSystem:
    def __init__(
        self,
        name: str = "S3",
        credential: Dict = None,
    ):
        self.name = name
        self.client = self.get_client(credential)
        
    def get_client(self, credential):
        if self.name == "S3":
            if credential:
                return s3fs.S3FileSystem(
                    key=credential.get("aws_access_key_id"),
                    secret=credential.get("aws_secret_access_key")
                )

            else:
                return s3fs.S3FileSystem(key=os.getenv("AWS_ACCESS_KEY_ID"), secret=os.getenv("AWS_SECRET_ACCESS_KEY"))
            
        else:
            ValueError("A filesystem, " + self.name + ", wasn't set up to run in this system.")
    
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
