from schema import BaseSchema
from marshmallow_sqlalchemy.fields import Nested
from models.flow import FlowModel
from schemas.source import SourceSchema
from schemas.authorization import AuthorizationSchema
from schemas.log import LogSchema


class FlowSchema(BaseSchema):   
    class Meta(BaseSchema.Meta):
        model = FlowModel
        
    source = Nested(SourceSchema, exclude=['authorizations'])
    authorization = Nested(AuthorizationSchema, exclude=['source_id', 'created_at'])
    logs = Nested(LogSchema, many=True)