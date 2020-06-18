from flows.amazon.s3 import S3

def create_flow(cls, flow_dict):
    source_name = flow_dict['source_name']
    
    if source_name == "S3":
        return S3(**flow_dict)
    
    else:
        raise ValueError("A Flow, " + source_name + ", wasn't set up to run in this system.")