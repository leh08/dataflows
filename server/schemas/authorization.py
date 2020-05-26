from schema import BaseSchema
from models.authorization import AuthorizationModel


class AuthorizationSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = AuthorizationModel
        load_only = ["credential"]