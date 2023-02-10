from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField #library for verifying phonenumbers, including international
from django.db.models.signals import post_save
from django.dispatch import receiver
from enum import Enum

class Parameter_Types(Enum):
    temp = 1
    ph = 2
    salinity = 3
    ammonia = 4
    #todo add more

 #todo tank & general notification class(es)
class Profile(models.Model): # for additional fields attached to User
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # username, password, email, first_name, last_name included in User
    phone_num = PhoneNumberField(blank=True)
    # one to many relationship to Tank model

@receiver(post_save, sender=User) # uses signals to create connected profile when a User is created
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User) # uses signals to save profile when its User is saved
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save() #not sure if p should be capital, needs testing


class Tank(models.Model):
   user = models.ForeignKey(Profile, on_delete=models.CASCADE) # many to one
   name = models.CharField(max_length=20) #required, but optional to user, will use generated name if they don't enter one
   types = [
       ('Fr', 'Freshwater'),
       ('Sa', 'Saltwater'),
   ]    # may split or add more types later
   type = models.CharField(max_length=2, choices=types)
   volume = models.IntegerField(max_length=10, blank=True)
   module_id = models.CharField(max_length=10, blank=True)
   # one to one relationship to parameters model

class Log_Data(models.Model):
    type = models.IntegerField(choices=Parameter_Types) # needs testing
    value = models.DecimalField(max_digits=5) # actual recorded number
    time_stamp = models.DateTimeField()# should come from user input or Rpi


class Parameters(models.Model):
    tank = models.OneToOneField(Tank, on_delete=models.CASCADE)  # one to one
    # unit: fahrenheit
    temp_max = models.DecimalField(max_digits=5)
    temp_min = models.DecimalField(max_digits=5)
    # unit: ph
    ph_max = models.DecimalField(max_digits=5)
    ph_min = models.DecimalField(max_digits=5)
    # unit: specific gravity (relative density to water, 2.0 = twice the density of water)
    salinity_max = models.DecimalField(max_digits=5, blank=True)
    salinity_min = models.DecimalField(max_digits=5, blank=True)
    # unit: ppm (parts per million)
    ammonia_max = models.DecimalField(max_digits=5, blank=True)
    ammonia_min = models.DecimalField(max_digits=5, blank=True)
    #todo more parameters

