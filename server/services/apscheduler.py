from datetime import datetime, date, time, timedelta

def schedule(self):
    params = dict()
    
    if self.frequency == 'Daily':
        params['days'] = 1
        params['next_run_time'] = datetime.combine(date.today() + timedelta(1), time(self.time_unit))
        
    else:
        raise ValueError("A frequency, " + self.frequency + ", wasn't set up to run in this system.")
        
    scheduler.add_job(self.run, id=str(self.id), trigger='interval', **params)