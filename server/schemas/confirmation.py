from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.confirmation import ConfirmationModel


class ConfirmationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ConfirmationModel
        load_only = ["user"]
        dump_only = ["id", "expired_at", "confirmed"]
        include_fk = True