import os

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

jobstores = {
    'default': SQLAlchemyJobStore(url=os.environ["SQLALCHEMY_DATABASE_URI"])
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(8)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

