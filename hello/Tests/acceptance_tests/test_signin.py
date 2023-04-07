#test_signin.py
import datetime
from django.test import TestCase, Client
from ..setup_helper_functions import setUpUsers, createUsers


class TestSignin(TestCase):
    c = None
    users = None

    def setUp(self):
        self.c = Client()
        self.users = createUsers()
        setUpUsers(self.users)

    def test_success(self):
        for user in self.users:
            res = self.c.post("/signin", {"email": user["email"], "password": user["password"]}, follow=True)
            self.assertRedirects(res, "/")

    def test_success_session(self):
        for user in self.users:
            self.c.post("/signin", {"email": user["email"], "password": user["password"]}, follow=True)
            session = self.c.session
            self.assertEqual(session["email"], user["email"], "Correct email not set in session on successful login")

    def test_failure_context_message(self):
        for user in self.users:
            res = self.c.post("/signin", {"email": user["email"], "password": "bad"}, follow=True)
            self.assertIn("message", res.context, "Context must contain message if failure occurs")

    def test_failure_form(self):
        for user in self.users:
            res = self.c.post("/signin", {"email": user["email"], "password": "bad"}, follow=True)
            self.assertEqual(res.context["email"], user["email"], "context must contain input email")
            self.assertEqual(res.context["password"], "bad", "context must contain input password")

    def test_failure_message(self):
        for user in self.users:
            res = self.c.post("/signin", {"email": user["email"], "password": "bad"}, follow=True)
            self.assertEqual(res.context["message"], "message",
                             "context must contain message if user credentials are incorrect")

    def test_wrong_format_for_email(self):
        for user in self.users:
            res = self.c.post("/signin", {"email": "user", "password": user["password"]}, follow=True)
            self.assertEqual(res.context["message"], "Please enter the valid email address for username",
                             "message in context must warn of incorrect email formats in form")


