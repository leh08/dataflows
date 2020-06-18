import logging
import logging.config

logging.config.fileConfig('configs/logs/config_logger.ini')

def create_logger(flow, status='In Progress'):
    logger = logging.getLogger('Flow.' + flow.name)
    
    return logging.LoggerAdapter(
        logger,
        extra = {
            "status": status,
            "flow_id": flow.id,
        }
    )