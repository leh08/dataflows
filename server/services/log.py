import logging
import traceback
from backend.models.log import Log
from backend.database import db_session


class SQLAlchemyHandler(logging.Handler):
    # A very basic logger that commits a LogRecord to the SQL Db
    def emit(self, record):
        trace = None
        exc = record.exc_info
        if exc:
            trace = traceback.format_exc(exc)
        log = Log(
            logger=record.name,
            level=record.levelname,
            trace=trace,
            msg=record.msg,
            file=record.file,
            status=record.status,
            flow_id=record.flow_id,
            )
        db_session.add(log)
        db_session.commit()