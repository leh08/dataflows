from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import pre_dump
from models.user import UserModel


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ["password"]
        dump_only = ["id", 'confirmation']
        load_instance = True
        
    @pre_dump
    def _pre_dump(self, user: UserModel):
        user.confirmation = [user.most_recent_confirmation]
        return user