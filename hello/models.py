import datetime

from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField  # library for verifying phonenums, including international
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from sms import send_sms
from django.conf import settings

# send_mail(
#     'Subject here',
#     'Here is the message.',
#     'from@example.com',
#     ['to@example.com'],
#     fail_silently=False,
# )


# todo tank & general notification class(es)
from web_project.settings import DEFAULT_FROM_EMAIL


class Profile(models.Model):  # for additional fields attached to User
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # username, password, email, first_name, last_name included in User
    phone_num = PhoneNumberField(blank=True, null=True)
    email_notifications = models.BooleanField(default=True)
    phone_notifications = models.BooleanField(default=False)

    # one to many relationship to Tank model
    def __str__(self):
        return '%s\'s profile' % (self.user.email)


@receiver(post_save, sender=User)  # uses signals to create connected profile when a User is created & send signup email
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        new_profile = Profile.objects.create(user=instance)
        print("when signup email should be sent")
        subject = f"AquaWatch: Sign-Up"
        message = f"Welcome to Aquawatch!"
        send_mail(
            subject,
            message,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )



@receiver(post_save, sender=User)  # uses signals to save profile when its User is saved
def save_user_profile(sender, instance, **kwargs):
    profile = Profile.objects.get(user=instance)
    profile.save()


class Tank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 

    name = models.CharField(max_length=20)
    types = [
        ('Fr', 'Freshwater'),
        ('Sa', 'Saltwater'),
    ] 

    type = models.CharField(max_length=2, choices=types)
    volume = models.IntegerField()
    module_id = models.CharField(max_length=10, blank=True)
    send_notifications = models.BooleanField(default=True)
    last_notification_time = models.DateTimeField(blank=True, null=True)

    parameters = models.OneToOneField('Parameters', on_delete=models.CASCADE, null=True, related_name='tank_for_parameters')

    def __str__(self):
        return '%s\'s tank: %s' % (self.user.email, self.name)

class Parameters(models.Model):
    temp_enabled = models.BooleanField(default=True)
    ph_enabled = models.BooleanField(default=True)
    salinity_enabled = models.BooleanField(default=True)
    ammonia_enabled = models.BooleanField(default=True)
    
    tank = models.OneToOneField('Tank', on_delete=models.CASCADE, related_name='parameters_for_tank')

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
        "temp": [72.0, 82.0],
        "ph": [6.5, 7.5],
        "salinity": [.997, 1.03],
        "ammonia": [0.0, 0.0],
    }
    saltwater_dict = {  # "type": [type_min, type_max] format
        "temp": [72.0, 78.0],
        "ph": [8.1, 8.4],
        "salinity": [1.020, 1.025],
        "ammonia": [0.0, 0.0],
    }

    def get_dict_of_enabled(self):
        param_dict = {  # "type": boolean format
            "temp": self.temp_enabled,
            "ph": self.ph_enabled,
            "salinity": self.salinity_enabled,
            "ammonia": self.ammonia_enabled,
        }
        return param_dict

    def get_dict_of_range(self):
        param_dict = {  # "type": [type_min, type_max] format
            "temp": [self.temp_min.__float__(), self.temp_max.__float__()],
            "ph": [self.ph_min.__float__(), self.ph_max.__float__()],
            "salinity": [self.salinity_min.__float__(), self.salinity_max.__float__()],
            "ammonia": [self.ammonia_min.__float__(), self.ammonia_max.__float__()],
        }
        return param_dict

    #intended to get w/ helper, change, then set w/ helper
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
        is_enabled = data.tank.parameters.get_dict_of_enabled().get(data.types[data.type][1])
        profile = data.tank.user.profile
        today = datetime.date.today().isoformat()
        last_notification = data.tank.last_notification_time
        if last_notification is not None:
            last_notification = last_notification.date().isoformat()
        tank_notifications = data.tank.send_notifications and (not data.is_manual) and last_notification != today and is_enabled
        if tank_notifications and (data.value < param_range[0] or data.value > param_range[1]): # value is out of bounds
            if profile.phone_notifications or profile.email_notifications:
                data.tank.last_notification_time = datetime.datetime.today()
            if profile.email_notifications:
                print("when email should be sent")
                subject = f"AquaWatch: tank, {data.tank.name}, has a parameter out of expected range"
                message = f"Parameter, {data.types[data.type][1]}, is out of range. \nReported value: {data.value}"
                send_mail(
                    subject,
                    message,
                    'from@example.com',
                    [data.tank.user.email],
                    fail_silently=False,
                )
            if profile.phone_notifications:
                print("when text should be sent")
                message = f"AquaWatch: Tank: {data.tank.name},Parameter: {data.types[data.type][1]}, is out of range. \nReported value: {data.value}"
                #send_sms(      this is not working properly on my end
                #    message,
                #   '+12065550100',
                #    [data.tank.user.profile.phone_num],
                #    fail_silently=False
                #)





@receiver(post_save, sender=Tank)  # uses signals to create connected param when a tank is created
def create_tank_params(sender, instance, created, **kwargs):
    if created:
        new_param = Parameters.objects.create(tank=instance)
        if new_param.tank.type == "Fr":
            new_param.set_dict_of_range(Parameters.freshwater_dict)
        elif new_param.tank.type == "Sa":
            new_param.set_dict_of_range(Parameters.saltwater_dict)
        new_param.save()
        instance.parameters = new_param  # Set the parameters field for the Tank instance
        instance.save()  # Save the Tank instance


@receiver(post_save, sender=Tank)
def save_rank_params(sender, instance, **kwargs):
    param = Parameters.objects.get(tank=instance)
    param.save()