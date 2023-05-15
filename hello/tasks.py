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
            if 30 < minutes_since_update < 60:  # replace with something more reliable
                # send notification: can't connect to module; internet, power, or hardware issue
                profile = tank.user.profile
                if profile.email_notifications:
                    print("possible disconnect email")
                    subject = f"AquaWatch: tank, {tank.name}, has lost connection"
                    message = f"Tank, {tank.name}, failed to reach our servers  \nLast contact: {minutes_since_update} minutes ago."
                    send_mail(
                        subject,
                        message,
                        from_email=DEFAULT_FROM_EMAIL,
                        recipient_list=[data.tank.user.email],
                        fail_silently=False,
                    )
                if profile.phone_notifications:
                    print("possible disconnect text")
                    message = f"AquaWatch: tank, {tank.name}, has lost connection, \nLast contact: {minutes_since_update} minutes ago."
                    send_sms(
                        message,
                        '+12065550100',
                        [data.tank.user.profile.phone_num],
                        fail_silently=False
                    )

#  change to start after n mins so it doesn't send notifications on server start, before everything is going
schedule('tasks.check_module_logging', schedule_type=Schedule.minutes, minutes=30)
