from schema import BaseSchema
from marshmallow.fields import Nested
from models.user import UserModel
from models.confirmation import ConfirmationModel


class UserSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = UserModel
        load_only = ["password"]