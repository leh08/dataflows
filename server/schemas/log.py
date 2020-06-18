from schema import BaseSchema
from models.log import LogModel


class LogSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = LogModel