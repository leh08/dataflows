from models.authorization import AuthorizationModel
from models.log import LogModel

from flows.amazon.s3 import S3

def create_flow(flow_dict):
    source_name = flow_dict['source_name']
    
    flow_dict['authorization'] = AuthorizationModel.find_by_id(flow_dict['authorization_id']).as_dict()
    logs = LogModel.find_all_by_flow_id(flow_dict['id'])
    flow_dict['logs'] = [log.as_dict() for log in logs]

    if source_name == "S3":
        return S3(**flow_dict)
    
    else:
        raise ValueError("A Flow, " + source_name + ", wasn't set up to run in this system.")