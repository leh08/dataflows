import traceback
from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from models.user import UserModel
from models.confirmation import ConfirmationModel
from schemas.user import UserSchema
from blacklist import BLACKLIST
from services.mailgun import MailGunException
from services.locales import gettext

user_schema = UserSchema()


class User(Resource):
    """
    This resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful when we are manipulating data regarding the users.
    """

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404
        user.delete_from_db()
        return {"message": gettext("user_deleted")}, 200


class Signup(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)

        if UserModel.find_by_email(user.email):
            return {"message": gettext("user_email_exists")}, 400
        
        try:
            user.save_to_db()
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            confirmation = ConfirmationModel(user.id)
            confirmation.save_to_db()
            user.send_confirmation_email()
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "message": gettext("user_signed_up"),
            }, 201
        
        except MailGunException as error:
            user.delete_from_db()
            return {"message": str(error)}, 500
                    
        except:
            traceback.print_exc()
            user.delete_from_db()
            return {"message": gettext("user_error_creating")}, 500
            

class Login(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json)

        user = UserModel.find_by_email(user_data.email)

        # this is what the `authenticate()` function did in security.py
        if user and safe_str_cmp(user.password, user_data.password):
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.confirmed:  
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {
                    "user": user_schema.dump(user),
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }, 200
            return {"message": gettext("user_not_confirmed").format(user.email)}, 40
                
        return {"message": gettext("user_invalid_credentials")}, 401


class Logout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": gettext("user_logged_out").format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200


class CurrentUser(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404
        return user_schema.dump(user), 200


class Resend(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json)

        user = UserModel.find_by_email(user_data.email)
        
        if not user:
            return {"message": gettext("user_not_found")}, 404
        
        try:
            confirmation = user.most_recent_confirmation
            if confirmation:
                if confirmation.confirmed:
                    return {"message": gettext("user_already_confirmed")}, 400
            
                confirmation.force_to_expire()
                
            new_confirmation = ConfirmationModel(user.id)
            new_confirmation.save_to_db()
            user.send_confirmation_email()
            return {"message": gettext("user_resend_successful")}, 201
        
        except MailGunException as error:
            return {"message": str(error)}, 500
        
        except:
            traceback.print_exc()
            return {"message": gettext("user_resend_fail")}, 500