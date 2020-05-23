from flask_restful import Resource
from models.log import LogModel
from schemas.log import LogSchema
from services.locales import gettext

log_schema = LogSchema()
log_list_schema = LogSchema(many=True)


class LogList(Resource):
    @classmethod
    def get(cls):
        return {"logs": log_list_schema.dump(LogModel.find_all())}, 200
        

class Log(Resource):
    @classmethod
    def get(cls, log_id: int):
        log = LogModel.find_by_id(log_id)
        if log:
            return log_schema.dump(log), 200
        return {"message": gettext("log_not_found")}, 404    
