from schema import BaseSchema
from marshmallow_sqlalchemy.fields import Nested
from models.flow import FlowModel
from models.authorization import AuthorizationModel
from schemas.authorization import AuthorizationSchema
from schemas.log import LogSchema


class FlowSchema(BaseSchema):   
    class Meta(BaseSchema.Meta):
        model = FlowModel

    authorization = Nested(AuthorizationSchema, exclude=['source_id', 'created_at'])
    logs = Nested(LogSchema, exclude=['flow_id'], many=True)