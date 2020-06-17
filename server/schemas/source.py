from schema import BaseSchema
from marshmallow_sqlalchemy.fields import Nested
from models.source import SourceModel
from schemas.authorization import AuthorizationSchema

class SourceSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = SourceModel
        
    authorizations = Nested(AuthorizationSchema, many=True)