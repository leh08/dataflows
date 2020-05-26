from schema import BaseSchema
from models.confirmation import ConfirmationModel


class ConfirmationSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = ConfirmationModel
        load_only = ["user"]