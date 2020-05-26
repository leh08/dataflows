from flask_restful import Resource
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.source import SourceModel
from schemas.source import SourceSchema
from services.locales import gettext

source_schema = SourceSchema()
source_list_schema = SourceSchema(many=True)


class SourceList(Resource):
    @classmethod
    def get(cls):
        return {"sources": source_list_schema.dump(SourceModel.find_all())}, 200
    

class Source(Resource):
    @classmethod
    def get(cls, source_id: int):
        source = SourceModel.find_by_id(source_id)
        if source:
            return source_schema.dump(source), 200
        return {"message": gettext("source_not_found")}, 404    
    
    @classmethod
    @jwt_required
    def post(cls):
        user_id = get_jwt_identity()
        source_json = request.get_json()
        source_json["user_id"] = user_id

        source = source_schema.load(source_json)
            
        name = source.name
        
        if SourceModel.find_by_name(name):
            return {"message": gettext("source_name_exists").format(name)}, 400

        try:
            source.save_to_db()
        except:
            return {"message": gettext("source_error_inserting")}, 500

        return source_schema.dump(source), 201
    
    @classmethod
    def put(cls, source_id: int):
        source_json = request.get_json()
        source = SourceModel.find_by_id(source_id)

        if source:
            source.report = source_json["report"]
        else:
            source_json["source_id"] = source_id
            
            source = source_schema.load(source_json)

        source.save_to_db()

        return source_schema.dump(source), 200
    
    @classmethod
    def delete(cls, source_id: int):
        source = SourceModel.find_by_id(source_id)
        if source:
            source.delete_from_db()

        return {"message": gettext("source_deleted")}