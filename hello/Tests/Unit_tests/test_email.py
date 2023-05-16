from django.core import mail
from django.test import TestCase
from hello.models import *

class EmailTest(TestCase):
    def test_send_email(self):
        # Send message.
        result = mail.send_mail(
            'Subject', 'message.',
            'from@gmail.com', ['to@gmail.com'],
            fail_silently=False,
        )
        print(result)

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Subject')

    def test_check_log_data(self):
        email = "hello@gmail.com"
        f_name = "Joe"
        l_name = "Smith"
        password = "1jhd91hd91"
        user = User.objects.create(username=email, email=email, first_name=f_name, last_name=l_name, password=password)
        tank = Tank.objects.create(user=user, name="Office Tank", type="Fr", volume=50)
        user.save()
        tank.save()

        user.profile.email_notifications = True
        user.save()

        self.assertEqual(len(mail.outbox), 1)
        mail.outbox.clear()

        # Within param range: no email expected
        logdata = LogData.objects.create(tank=tank, type=1, value=7.3, time_stamp=datetime.datetime.now())
        logdata.save()
        self.assertEqual(len(mail.outbox), 0)

        # Out of param range: email expected
        logdata = LogData.objects.create(tank=tank, type=1, value=-0.003, time_stamp=datetime.datetime.now())
        logdata.save()

        # Test that one email has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first email is correct.
        self.assertEqual(mail.outbox[0].subject, 'AquaWatch: tank, Office Tank, has a parameter out of expected range')

        print(mail.outbox[0].message())

        # Out of param range BUT already sent a notification today so no email expected
        logdata = LogData.objects.create(tank=tank, type=2, value=-3.5, time_stamp=datetime.datetime.now())
        logdata.save()

        self.assertEqual(len(mail.outbox), 1)

    def test_sign_up_email(self):
        email = "hello@gmail.com"
        f_name = "Joe"
        l_name = "Smith"
        password = "1jhd91hd91"

        self.assertEqual(len(mail.outbox), 0)

        user = User.objects.create(username=email, email=email, first_name=f_name, last_name=l_name, password=password)
        user.save()

        self.assertEqual(len(mail.outbox), 1)
