import datetime
import time

from django_q.tasks import async_task, schedule
from django_q.models import Schedule
from models import *

#  check if modules that were sending logdatas stopped sending data if so send a connection issue notification
def check_module_logging():
    tanks = list(Tank.objects.all())
    for tank in tanks:
        data = LogData.objects.filter(is_manual=False, tank=tank)
        most_recent= data.objects.order_by('time_stamp').first()
        if most_recent is not None:
            now = datetime.datetime.now()
            minutes_since_update = datetime.timedelta(now, most_recent.time_stamp).total_seconds() % 60
            if 30 < minutes_since_update < 62:  # replace with something more reliable
                # send notification: can't connect to module; internet, power, or hardware issue
                pass

#  change to start after n mins so it doesn't send notifications on server start, before everything is going
schedule('tasks.check_module_logging', schedule_type=Schedule.minutes, minutes=30)
