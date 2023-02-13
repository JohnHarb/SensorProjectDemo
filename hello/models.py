from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import \
    PhoneNumberField  # library for verifying phonenumbers, including international
from django.db.models.signals import post_save
from django.dispatch import receiver
from enum import Enum


class Parameter_Types(Enum):
    temp = 1
    ph = 2
    salinity = 3
    ammonia = 4
    # todo add more


# todo tank & general notification class(es)
class Profile(models.Model):  # for additional fields attached to User
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # username, password, email, first_name, last_name included in User
    phone_num = PhoneNumberField(blank=True)

    # one to many relationship to Tank model
    def __str__(self):
        return '%s\'s profile' % (self.user.email)


@receiver(post_save, sender=User)  # uses signals to create connected profile when a User is created
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)  # uses signals to save profile when its User is saved
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()  # not sure if p should be capital, needs testing


class Tank(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)  # many to one\

    # required, but optional to user, will use generated name if they don't enter one
    name = models.CharField( max_length=20)
    types = [
        ('Fr', 'Freshwater'),
        ('Sa', 'Saltwater'),
    ]  # may split or add more types later

    type = models.CharField(max_length=2, choices=types)
    volume = models.IntegerField(max_length=10)
    module_id = models.CharField(max_length=10, blank=True)
    # one to one relationship to parameters model

    def __str__(self):
        return '%s\'s tank: %s' % (self.user.email, self.name)


class LogData(models.Model):
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE)  # many to one
    type = models.IntegerField(choices=Parameter_Types)  # needs testing
    value = models.DecimalField(max_digits=5)  # actual recorded number
    time_stamp = models.DateTimeField()  # should come from user input or Rpi

    def __str__(self):
        return 'Tank %s data: %s, %s, %s' % (self.tank.pk, self.type, self.value, self.time_stamp.isoformat())


class Parameters(models.Model):
    tank = models.OneToOneField(Tank, on_delete=models.CASCADE)  # one to one
    # unit: fahrenheit
    temp_max = models.DecimalField(max_digits=5)
    temp_min = models.DecimalField(max_digits=5)
    # unit: ph
    ph_max = models.DecimalField(max_digits=5)
    ph_min = models.DecimalField(max_digits=5)
    # unit: specific gravity (relative density to water, 2.0 = twice the density of water)
    salinity_max = models.DecimalField(max_digits=5)
    salinity_min = models.DecimalField(max_digits=5)
    # unit: ppm (parts per million)
    ammonia_max = models.DecimalField(max_digits=5)
    ammonia_min = models.DecimalField(max_digits=5)
    # todo more parameters

    def get_dict_of_tuples(self):
        param_dict = {  # "type": (type_min, type_max) format
            "temp": (self.temp_min, self.temp_max),
            "ph": (self.ph_min, self.ph_max),
            "salinity": (self.salinity_min, self.salinity_max),
            "ammonia": (self.ammonia_min, self.ammonia_max),
        }
        return param_dict

    # intended to get w/ helper, change, then set w/ helper
    def set_dict_of_tuples(self, param_dict: dict[str, tuple[float, float]]):
        if param_dict.keys != self.get_dict_of_tuples().keys():
            raise ValueError("The dict must match keys and types with get_dict_of_tuples()")
        else:
            self.temp_min = param_dict.get('temp')[0]
            self.temp_max = param_dict.get('temp')[1]
            self.ph_min = param_dict.get('ph')[0]
            self.ph_max = param_dict.get('ph')[1]
            self.salinity_min = param_dict.get('salinity')[0]
            self.salinity_max = param_dict.get('salinity')[1]
            self.ammonia_min = param_dict.get('ammonia')[0]
            self.ammonia_max = param_dict.get('ammonia')[1]

    def __str__(self):
        return 'Tank %s Parameters' % (self.tank.pk)

