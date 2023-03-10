# test_models.py
import datetime

from django.test import TestCase
from hello.models import *


class UserProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        email = "hello@gmail.com"
        f_name = "Joe"
        l_name = "Smith"
        password = "1jhd91hd91"
        User.objects.create(username=email, email=email, first_name=f_name, last_name=l_name, password=password)

    def test_profile_creation(self):
        user = User.objects.get(id=1)
        user.save()
        self.assertEqual(Profile.objects.get(user=user).user.pk, 1)

    def test_profile_update(self):
        user = User.objects.get(id=1)
        user.pk = 3
        email = "goodbye@gmail.com"
        user.email = email
        user.username = email
        user.save()
        self.assertEqual(Profile.objects.get(user=user).user.pk, 3)


    def test__str__(self):
        user = User.objects.get(id=1)
        profile = Profile.objects.get(user=user)
        expected_object_name = '%s\'s profile' % (profile.user.email)
        self.assertEqual(str(profile), expected_object_name)

class TankModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        email = "hello@gmail.com"
        f_name = "Joe"
        l_name = "Smith"
        password = "1jhd91hd91"
        user = User.objects.create(username=email, email=email, first_name=f_name, last_name=l_name, password=password)
        Tank.objects.create(user=user, name="Office Tank", type="Fr", volume=50)

    def test__str__(self):
        tank = Tank.objects.get(id=1)
        expected_object_name = '%s\'s tank: %s' % (tank.user.email, tank.name)
        self.assertEqual(str(tank), expected_object_name)

class LogDataModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        email = "hello@gmail.com"
        f_name = "Joe"
        l_name = "Smith"
        password = "1jhd91hd91"
        user = User.objects.create(username=email, email=email, first_name=f_name, last_name=l_name, password=password)
        tank = Tank.objects.create(user=user, name="Office Tank", type="Fr", volume=50)
        LogData.objects.create(tank=tank, type=1, value=-0.003, time_stamp=datetime.datetime.now())

    def test__str__(self):
        log_data = LogData.objects.get(id=1)
        expected_object_name = 'Tank %s data: %s, %s, %s' % (log_data.tank.pk, log_data.type,
                                                             log_data.value, log_data.time_stamp.isoformat())
        self.assertEqual(str(log_data), expected_object_name)

class ParametersModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        email = "hello@gmail.com"
        f_name = "Joe"
        l_name = "Smith"
        password = "1jhd91hd91"
        user = User.objects.create(username=email, email=email, first_name=f_name, last_name=l_name, password=password)
        tank = Tank.objects.create(user=user, name="Office Tank", type="Fr", volume=50)
        Parameters.objects.create(tank=tank,
                                  temp_min=75, temp_max=82,
                                  ph_min=7.43, ph_max=8.29,
                                  salinity_min=0.995, salinity_max=1.000,
                                  ammonia_min=0, ammonia_max=0)

    def test_parameter_dict_of_tuples(self):
        param = Parameters.objects.get(id=1)

        invalid_dict = {
            "temp": (.5, 2.0),
            "notsalinity": (1.2, 5.2)
        }
        with self.assertRaises(ValueError):
            param.set_dict_of_tuples(invalid_dict)

        original_dict = param.get_dict_of_tuples()
        original_dict.get("temp")[0] = 70
        param.set_dict_of_tuples(original_dict)
        param.save()
        self.assertEqual(param.temp_min, 70)



    def test__str__(self):
        param = Parameters.objects.get(id=1)
        expected_object_name = 'Tank %s Parameters' % (param.tank.pk)
        self.assertEqual(str(param), expected_object_name)