import os

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

DATABASE_URL = os.getenv('DATABASE_URL') or os.environ["SQLALCHEMY_DATABASE_URI"]

jobstores = {
    'default': SQLAlchemyJobStore(url=DATABASE_URL)
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(8)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

