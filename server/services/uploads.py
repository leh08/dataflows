import os
from typing import Union
from werkzeug.datastructures import FileStorage

from flask_uploads import UploadSet, DEFAULTS, AUDIO, SCRIPTS, ARCHIVES

FILE_FORMATS = DEFAULTS + AUDIO + SCRIPTS + ARCHIVES
UPLOAD_SET = UploadSet('files', FILE_FORMATS)

def save_file(file: FileStorage, folder: str = None, name: str = None) -> str:
    """Take FileStorage and save it to a folder"""
    return UPLOAD_SET.save(file, folder, name)

def get_path(filename: str = None, folder: str = None) -> str:
    return UPLOAD_SET.path(filename, folder)

def _retrieve_filename(file: Union[str, FileStorage]) -> str:
    if isinstance(file, FileStorage):
        return file.filename
    
    return file

def get_basename(file: Union[str, FileStorage]) -> str:
    filename = _retrieve_filename(file)
    
    return os.path.split(filename)[1]

def get_extension(file: Union[str, FileStorage]) -> str:
    filename = _retrieve_filename(file)
    
    return os.path.splitext(filename)[1]