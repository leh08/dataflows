import logging


def create_logger(flow, status='In Progress'):
    logger = logging.getLogger('Flow.' + flow.name)
    
    return logging.LoggerAdapter(
        logger,
        extra = {
            "status": status,
            "flow_id": flow.id,
        }
    )