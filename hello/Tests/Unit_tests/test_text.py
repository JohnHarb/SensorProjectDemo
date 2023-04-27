# from sms import send_sms, message
import sms.utils
from sms import *
from django.test import TestCase
from hello.models import *

class TextTest(TestCase):
    def test_send_text(self):
        # Send message.
        result = send_sms(
             'message text goes here',
            '+14145550000', ['+12154158983'],
            fail_silently=False,
        )
        print(result)

        # Test that one message has been sent.
        self.assertEqual(result, 1)



    def test_check_log_data(self):
        email = "hello@gmail.com"
        f_name = "Joe"
        l_name = "Smith"
        password = "1jhd91hd91"
        user = User.objects.create(username=email, email=email, first_name=f_name, last_name=l_name, password=password)
        tank = Tank.objects.create(user=user, name="Office Tank", type="Fr", volume=50)
        user.save()
        tank.save()

        user.profile.phone_notifications = True
        user.profile.email_notifications = False
        user.profile.phone_num = "+14145550000"
        user.save()

        # Within param range: no text expected
        logdata = LogData.objects.create(tank=tank, type=1, value=7.3, time_stamp=datetime.datetime.now())
        logdata.save()


        # Out of param range: text expected
        logdata = LogData.objects.create(tank=tank, type=1, value=-0.003, time_stamp=datetime.datetime.now())
        logdata.save()



        # Out of param range BUT already sent a notification today so no text expected
        logdata = LogData.objects.create(tank=tank, type=2, value=-3.5, time_stamp=datetime.datetime.now())
        logdata.save()



