from schema import BaseSchema
from models.flow import FlowModel
from models.log import LogModel


class LogSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = LogModel