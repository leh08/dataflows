from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.flow import FlowModel
from models.log import LogModel


class LogSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LogModel
        dump_only = ["id"]
        include_fk = True
        load_instance = True