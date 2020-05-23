from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request

from services import uploads
from services.locales import gettext
from schemas.file import FileSchema

file_schema = FileSchema()


class Upload(Resource):
    @classmethod
    def post(cls, flow_name: str):
        """
        Used to upload a file
        If there is a filename conflict, it appends a number at the end.
        """
        data = file_schema.load(request.files) # {"file": FileStorage}
        try:
            file_path = uploads.save_file(data["file"], folder=flow_name)
            basename = uploads.get_basename(file_path)
            return {"message": gettext("file_uploaded").format(basename)}, 200
        
        except UploadNotAllowed:
            extension = uploads.get_extension(data["file"])
            return {"message": gettext("file_illegal_extension").format(extension)}, 400
        