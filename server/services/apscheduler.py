from typing import Union
from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from configurations.schedulers.apscheduler import jobstores, executors, job_defaults

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

scheduler.start()

def schedule(function, frequency: str = "Daily", hour: int = 6, day: Union[int, str] = None, job_id: Union[int, str] = None):    
    if frequency == 'Hourly':
        cron = dict(year='*', month='*', day="*", week='*', day_of_week='*', hour="*", minute=0, second=0)
        
    elif frequency == 'Daily':
        cron = dict(year='*', month='*', day="*", week='*', day_of_week='*', hour=hour, minute=0, second=0)
        
    elif frequency == 'Weekly':
        cron = dict(year='*', month='*', day="*", week="*", day_of_week=day.lower(), hour=hour, minute=0, second=0)
    
    elif frequency == 'Monthly':
        cron = dict(year='*', month='*', day=day, week="*", day_of_week="*", hour=hour, minute=0, second=0)
        
    else:
        raise ValueError("A frequency, " + frequency + ", wasn't set up to run in this system.")

    scheduler.add_job(function, id=str(job_id), trigger='cron', **cron)