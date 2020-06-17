from flask_restful import Resource
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.flow import FlowModel
from models.user import UserModel

from schemas.flow import FlowSchema
from services.locales import gettext

flow_schema = FlowSchema()
flow_list_schema = FlowSchema(many=True)


class FlowList(Resource):
    @classmethod
    def get(cls):
        return {"flows": flow_list_schema.dump(FlowModel.find_all())}, 200
    
    @classmethod
    # @jwt_required
    def post(cls):
        # user_id = get_jwt_identity()
        # user = UserModel.find_by_id(user_id)
        
        # if not user:
        #     return {"message": gettext("flow_error_creating")}, 404
        
        flow_json = request.get_json()
        flow = flow_schema.load(flow_json)
        
        name = flow.name

        if FlowModel.find_by_name(name):
            return {"message": gettext("flow_name_exists").format(name)}, 400
        
        try:
            flow.save_to_db()
            print("success")
            flow.run()
        except:
            return {"message": gettext("flow_error_inserting")}, 500

        return flow_schema.dump(flow), 201
    

class Flow(Resource):
    @classmethod
    def get(cls, flow_id: int):
        flow = FlowModel.find_by_id(flow_id)
        if flow:
            return flow_schema.dump(flow), 200
        return {"message": gettext("flow_not_found")}, 404
    
    @classmethod
    def patch(cls, flow_id: int):
        flow_json = request.get_json()
        flow = FlowModel.find_by_id(flow_id)
        
        if flow:
            flow.name = flow_json["name"]
            flow.report = flow_json["report"]
        else:
            flow_json["flow_id"] = flow_id
            
            flow = flow_schema.load(flow_json)

        flow.save_to_db()

        return flow_schema.dump(flow), 200
    
    @classmethod
    def delete(cls, flow_id: int):
        flow = FlowModel.find_by_id(flow_id)
        if flow:
            flow.delete_from_db()

        return {"message": gettext("flow_deleted")}