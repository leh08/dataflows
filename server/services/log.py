import logging
import logging.config

from models.flow import FlowModel
logging.config.fileConfig('configs/logs/config_logger.ini')

def create_logger(flow_name, status='In Progress', file=None):
    flow = FlowModel.find_by_name(flow_name)
    logger = logging.getLogger('Flow.' + flow.name)
    
    return logging.LoggerAdapter(
        logger,
        extra = {
            "status": status,
            "file": None,
            "flow_id": flow.id,
        }
    )