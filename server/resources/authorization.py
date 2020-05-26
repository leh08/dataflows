from flask_restful import Resource
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.authorization import AuthorizationModel
from schemas.authorization import AuthorizationSchema
from services.locales import gettext

authorization_schema = AuthorizationSchema()
authorization_list_schema = AuthorizationSchema(many=True)


class AuthorizationList(Resource):
    @classmethod
    def get(cls):
        return {"authorizations": authorization_list_schema.dump(AuthorizationModel.find_all())}, 200
    

class Authorization(Resource):
    @classmethod
    def get(cls, authorization_id: int):
        authorization = AuthorizationModel.find_by_id(authorization_id)
        if authorization:
            return authorization_schema.dump(authorization), 200
        return {"message": gettext("authorization_not_found")}, 404    
    
    @classmethod
    @jwt_required
    def post(cls):
        user_id = get_jwt_identity()
        authorization_json = request.get_json()
        authorization_json["user_id"] = user_id

        authorization = authorization_schema.load(authorization_json)
            
        name = authorization.name
        
        if AuthorizationModel.find_by_name(name):
            return {"message": gettext("authorization_name_exists").format(name)}, 400

        try:
            authorization.save_to_db()
        except:
            return {"message": gettext("authorization_error_inserting")}, 500

        return authorization_schema.dump(authorization), 201
    
    @classmethod
    def put(cls, authorization_id: int):
        authorization_json = request.get_json()
        authorization = AuthorizationModel.find_by_id(authorization_id)

        if authorization:
            authorization.report = authorization_json["report"]
        else:
            authorization_json["authorization_id"] = authorization_id
            
            authorization = authorization_schema.load(authorization_json)

        authorization.save_to_db()

        return authorization_schema.dump(authorization), 200
    
    @classmethod
    def delete(cls, authorization_id: int):
        authorization = AuthorizationModel.find_by_id(authorization_id)
        if authorization:
            authorization.delete_from_db()

        return {"message": gettext("authorization_deleted")}