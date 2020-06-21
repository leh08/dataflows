from schema import BaseSchema
from marshmallow_sqlalchemy.fields import Nested
from models.flow import FlowModel
from schemas.authorization import AuthorizationSchema
from schemas.log import LogSchema


class FlowSchema(BaseSchema):   
    class Meta(BaseSchema.Meta):
        model = FlowModel

    authorization = Nested(AuthorizationSchema)
    logs = Nested(LogSchema, many=True)