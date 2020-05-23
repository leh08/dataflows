from marshmallow import Schema
from marshmallow.fields import Field
from werkzeug.datastructures import FileStorage

class FileStorageField(Field):
    default_error_messages = {
        "invalid": "Not a valid file"
    }
    def _deserialize(self, value, attr, data, **kwargs) -> FileStorage:
        if value is None:
            return None
        
        if not isinstance(value, FileStorage):
            self.fail("invalid")
            
        return value
    

class FileSchema(Schema):
    file = FileStorageField(required=True)