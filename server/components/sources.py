from services.filesystem import FileSystem

def get_source(source_name, credential):
    """ Get a source API for retrieve a report """

    if source_name == "S3":
        return FileSystem(credential=credential)
        
    else:
        raise ValueError("A source, " + source_name + ", wasn't set up to run in this system.")
