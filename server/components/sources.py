from services.filesystem import FileSystem
   
def get_source(name):
    """ Get a source API for retrieve a report """
    source_name = name
    credential = authorization.credential

    if source_name == "S3":
        return FileSystem(credential=credential)
    
    else:
        raise ValueError("A source, " + source_name + ", wasn't set up to run in this system.")