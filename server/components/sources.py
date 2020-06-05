from services.filesystem import FileSystem


class Source:
    def __init__(self, name):
        self.name = name
    
    def create_source(self):
        """ Get a source API for retrieve a report """
        source_name = self.name
        credential = self.authorization.credential
    
        if source_name == "S3":
            return FileSystem(credential=credential)
        
        else:
            raise ValueError("A source, " + source_name + ", wasn't set up to run in this system.")