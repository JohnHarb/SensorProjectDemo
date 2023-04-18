from django.core import mail
from django.test import TestCase

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