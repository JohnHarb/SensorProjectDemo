#test_signup.py
import datetime

from django.test import TestCase, Client
from .setup_helper_functions import setUpUsers, createUsers


class TestSignup(TestCase):
    c = None
    users = None

    def setUp(self):
        self.c = Client()
        self.users = createUsers()
        setUpUsers(self.users)

    def test_success(self):
        for user in self.users:
            res = self.c.post("/signup",{"first_name": user["first_name"], "l_name": user["last_name"], "email": user["email"]})
            self.assertEqual(res.context["message"], "", "")

    def test_create_duplicate(self):
        for user in self.users:
            res = self.c.post("/signup",{"first_name": user["first_name"], "last_name": user["last_name"], "email": user["email"]})
            self.assertEqual(res.context["message"], "User already in exists", "Context should notify when creating duplicate user")

    def test_non_email_format(self):
        for user in self.users:
            res = self.c.post("/signup",{"first_name": user["first_name"], "last_name": user["last_name"], "email": user["email"]})
            self.assertEqual(res.context["message"], "email is not in proper format", "context should notify when creating duplicate user")



