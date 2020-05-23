from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from models.flow import FlowModel
from models.log import LogModel
from schemas.log import LogSchema


class FlowSchema(SQLAlchemyAutoSchema):
    logs = Nested(LogSchema, many=True)
    
    class Meta:
        model = FlowModel
        dump_only = ["id"]
        include_fk = True
        load_instance = True