import datetime

from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField  # library for verifying phonenums, including international
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail


# send_mail(
#     'Subject here',
#     'Here is the message.',
#     'from@example.com',
#     ['to@example.com'],
#     fail_silently=False,
# )


# todo tank & general notification class(es)
class Profile(models.Model):  # for additional fields attached to User
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # username, password, email, first_name, last_name included in User
    phone_num = PhoneNumberField(blank=True)
    email_notifications = models.BooleanField(default=True)
    phone_notifications = models.BooleanField(default=False)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # many to one\

    # required, but optional to user, will use generated name if they don't enter one
    name = models.CharField(max_length=20)
    types = [
        ('Fr', 'Freshwater'),
        ('Sa', 'Saltwater'),
    ]  # may split or add more types later

    type = models.CharField(max_length=2, choices=types)
    volume = models.IntegerField()
    module_id = models.CharField(max_length=10, blank=True)
    send_notifications = models.BooleanField(default=True)
    last_notification_time = models.DateTimeField(blank=True)

    # one to one relationship to parameters model

    def __str__(self):
        return '%s\'s tank: %s' % (self.user.email, self.name)


class LogData(models.Model):
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE)  # many to one
    types = [
        ('te', 'temp'),
        ('ph', 'ph'),
        ('sa', 'salinity'),
        ('am', 'ammonia'),
    ]
    type = models.IntegerField(choices=types)
    value = models.DecimalField(max_digits=7, decimal_places=3)  # actual recorded number
    time_stamp = models.DateTimeField()  # should come from user input or Rpi
    is_manual = models.BooleanField(default=False)


    def __str__(self):
        return 'Tank %s data: %s, %s, %s' % (self.tank.pk, self.type, self.value, self.time_stamp.isoformat())

# 1 notification per day per tank
@receiver(post_save, sender=LogData)  # uses signals to check new data when its model is created.
def check_log_data(sender, instance: LogData, created, **kwargs):
    if created:
        data = instance
        param_range = data.tank.parameters.get_dict_of_range().get(data.types[data.type][1])
        profile = data.tank.user.profile
        today = datetime.date.today().isoformat()
        last_notification = data.tank.last_notification_time.date().isoformat()
        tank_notifications = data.tank.send_notifications and (not data.is_manual) and last_notification != today
        if tank_notifications and (data.value < param_range[0] or data.value > param_range[1]): # value is out of bounds
            if profile.email_notifications:
                print("when email should be sent")
                subject = "AquaWatch: tank, %s, has a parameter out of expected range", data.tank.name
                send_mail(
                    subject,
                    'Here is the message.',
                    'from@example.com',
                    [data.tank.user.email],
                    fail_silently=False,
                )
            if profile.phone_notifications:
                print("when text should be sent")




class Parameters(models.Model):
    tank = models.OneToOneField(Tank, on_delete=models.CASCADE)  # one to one
    # unit: fahrenheit
    temp_max = models.DecimalField(max_digits=7, decimal_places=3, default=0.0)
    temp_min = models.DecimalField(max_digits=7, decimal_places=3, default=0.0)
    # unit: ph
    ph_max = models.DecimalField(max_digits=7, decimal_places=3, default=0.0)
    ph_min = models.DecimalField(max_digits=7, decimal_places=3, default=0.0)
    # unit: specific gravity (relative density to water, 2.0 = twice the density of water)
    salinity_max = models.DecimalField(max_digits=7, decimal_places=3, default=0.0)
    salinity_min = models.DecimalField(max_digits=7, decimal_places=3, default=0.0)
    # unit: ppm (parts per million)
    ammonia_max = models.DecimalField(max_digits=7, decimal_places=3, default=0.0)
    ammonia_min = models.DecimalField(max_digits=7, decimal_places=3, default=0.0)

    # todo more parameters

    freshwater_dict = {  # "type": [type_min, type_max] format
        "temp": [72, 82],
        "ph": [6.5, 7.5],
        "salinity": [.997, 1.03],
        "ammonia": [0.0, 0.0],
    }
    saltwater_dict = {  # "type": [type_min, type_max] format
        "temp": [72, 78],
        "ph": [8.1, 8.4],
        "salinity": [1.020, 1.025],
        "ammonia": [0.0, 0.0],
    }
    def get_dict_of_range(self):
        param_dict = {  # "type": [type_min, type_max] format
            "temp": [self.temp_min, self.temp_max],
            "ph": [self.ph_min, self.ph_max],
            "salinity": [self.salinity_min, self.salinity_max],
            "ammonia": [self.ammonia_min, self.ammonia_max],
        }
        return param_dict

    # intended to get w/ helper, change, then set w/ helper
    def set_dict_of_range(self, param_dict: dict[str, list[float, float]]):
        if list(param_dict.keys()) != list(self.get_dict_of_range().keys()):
            raise ValueError("The dict must match keys and types with get_dict_of_range()")
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

@receiver(post_save, sender=Tank)  # uses signals to create connected profile when a User is created
def create_user_profile(sender, instance, created, **kwargs):

    if created:
        new_param = Parameters.objects.create(tank=instance)
        if new_param.tank.type == 0:
            new_param.set_dict_of_range(Parameters.freshwater_dict)
        elif new_param.tank.type == 1:
            new_param.set_dict_of_range(Parameters.saltwater_dict)
        new_param.save()

@receiver(post_save, sender=Tank)
def save_user_profile(sender, instance, **kwargs):
    instance.parameters.save()  # test