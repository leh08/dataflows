from schema import BaseSchema
from marshmallow_sqlalchemy.fields import Nested
from models.flow import FlowModel
from models.source import SourceModel
from models.authorization import AuthorizationModel
from models.log import LogModel


class FlowSchema(BaseSchema):   
    class Meta(BaseSchema.Meta):
        model = FlowModel
        
    source = Nested('SourceSchema', exclude=['authorizations'])
    authorization = Nested('AuthorizationSchema', exclude=['source_id', 'created_at'])
    logs = Nested('LogSchema', many=True)