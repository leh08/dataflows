from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from database import db_session


class BaseSchema(SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = db_session
        load_instance = True
        include_fk = True