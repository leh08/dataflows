import logging
import traceback
from models.log import LogModel


class SQLAlchemyHandler(logging.Handler):
    # A very basic logger that commits a LogRecord to the SQL Db
    def emit(self, record):
        trace = None
        exc_info = record.exc_info
        if exc_info:
            trace = traceback.format_exc(exc_info)
        log = LogModel(
            message=record.message,
            status=record.status,
            flow_id=record.flow_id,
        )
        log.save_to_db()