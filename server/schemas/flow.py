from schema import BaseSchema
from marshmallow_sqlalchemy.fields import Nested
from models.flow import FlowModel
from models.log import LogModel
from schemas.log import LogSchema


class FlowSchema(BaseSchema):   
    class Meta(BaseSchema.Meta):
        model = FlowModel

    logs = Nested(LogSchema, many=True)