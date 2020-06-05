import logging
from models.flow import FlowModel


def create_logger(flow_id, status='In Progress'):
    flow = FlowModel.find_by_id(flow_id)
    logger = logging.getLogger('Flow.' + flow.name)
    
    return logging.LoggerAdapter(
        logger,
        extra = {
            "status": status,
            "flow_id": flow_id,
        }
    )