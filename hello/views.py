from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.views import View 
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from hello.models import *
from .models import Tank
from django.template import RequestContext
from django.core.serializers.json import DjangoJSONEncoder

from .models import LogData
from django.template.defaulttags import register
import json
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def checkemail(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

class signUp(View):
  def get(self, request):
   return render(request,'hello/signup.html')

  def post(self, request):
    fname = request.POST["fname"]
    lname = request.POST["lname"]
    email = request.POST["email"]
    password = request.POST["password"]

    if not checkemail(str(email)):
      messages.error(request, 'invalid email format')
      return redirect('/')
    if len(User.objects.filter(email=email)) > 0:
      messages.error(request, 'account with that email already exists')
      return redirect('/')
    user = User.objects.create_user(username = email, email = email, first_name = fname, last_name = lname, password = password)
    user.save()
    login(request, user)
    return redirect('/home/')

class signIn(View):
  def get(self, request):
    return render(request,'hello/signin.html')

  def post(self, request):
    email = request.POST["email"]
    password = request.POST["password"]
    user = authenticate(request, username=email, password=password)
    if user is not None:
        login(request, user)
        return redirect('/home/')
    messages.error(request, "invalid credentials")
    return redirect('/signin/')
 
def home(request):
    tanks = Tank.objects.all()
    context = {
        'tanks': tanks,
    }
    return render(request, 'hello/Home.html', context)

class profile(View):
  def get(self, request):
    user = request.user
    tNum = str(len(Tank.objects.filter(user=user)))
    return render(request,'hello/profile.html', {"name": user.first_name + " " + user.last_name, "email": user.email, "tanks": tNum})

def tankhome(request, tank_id):
    tank = get_object_or_404(Tank, pk=tank_id)
    
    # Retrieve log data for each parameter
    log_data_temperature = tank.logdata_set.filter(type=LogData.types.index(('te', 'temp'))).order_by('time_stamp')
    log_data_ph = tank.logdata_set.filter(type=LogData.types.index(('ph', 'ph'))).order_by('time_stamp')
    log_data_salinity = tank.logdata_set.filter(type=LogData.types.index(('sa', 'salinity'))).order_by('time_stamp')

    # Prepare data for each parameter
    temperature_timestamps = [data.time_stamp.strftime('%Y-%m-%dT%H:%M:%S') for data in log_data_temperature]
    temperature_values = [float(data.value) for data in log_data_temperature]

    ph_timestamps = [data.time_stamp.strftime('%Y-%m-%dT%H:%M:%S') for data in log_data_ph]
    ph_values = [float(data.value) for data in log_data_ph]

    salinity_timestamps = [data.time_stamp.strftime('%Y-%m-%dT%H:%M:%S') for data in log_data_salinity]
    salinity_values = [float(data.value) for data in log_data_salinity]

    context = {
        'tank': tank,
        'temperature_timestamps': json.dumps(temperature_timestamps),
        'temperature_values': json.dumps(temperature_values),
        'temp_enabled': tank.parameters.temp_enabled if tank.parameters else False,
        'ph_timestamps': json.dumps(ph_timestamps),
        'ph_values': json.dumps(ph_values),
        'ph_enabled': tank.parameters.ph_enabled if tank.parameters else False,
        'salinity_timestamps': json.dumps(salinity_timestamps),
        'salinity_values': json.dumps(salinity_values),
        'salinity_enabled': tank.parameters.salinity_enabled if tank.parameters else False,
    }

    return render(request, 'hello/TankHome.html', context)


class addTank(View):
  def get(self, request):
    return render(request,'hello/addtank.html')

  def post(self, request):
    user = request.user
    tname = request.POST["tname"]
    ttype = request.POST["ttype"]
    volume = request.POST["wcap"]
    module_id = request.POST["mID"]
    if Tank.objects.filter(module_id=module_id).exists():
      messages.error(request, 'The module: %s, is connected to an existing tank' % module_id)
      return render(request, 'hello/addtank.html')
    notifications = "notif" in request.POST

    new_tank = Tank.objects.create(user=user, name=tname, type=ttype, volume=volume, module_id=module_id, send_notifications=notifications)
    new_tank.save()
    print("new tank saved")


    return redirect('/home/')

class aboutUs(View):
  def get(self, request):
   return render(request,'hello/aboutus.html')

class signOut(View):
  def get(self, request):
    logout(request)
    return redirect('/signin/')
  
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Tank, Parameters

from django.shortcuts import get_object_or_404
from .models import Tank, Parameters
from .forms import ParametersForm

class tankParams(View):
  def get(self, request, tank_id):
      tank = get_object_or_404(Tank, id=tank_id)
      parameters = tank.parameters  # Assuming the related name is 'parameters'
      parameter_list = [
          {'name': 'temp', 'label': 'Temperature', 'min_value': parameters.temp_min if parameters else None, 'max_value': parameters.temp_max if parameters else None},
          {'name': 'ph', 'label': 'pH', 'min_value': parameters.ph_min if parameters else None, 'max_value': parameters.ph_max if parameters else None},
          {'name': 'salinity', 'label': 'Salinity', 'min_value': parameters.salinity_min if parameters else None, 'max_value': parameters.salinity_max if parameters else None},
          {'name': 'ammonia', 'label': 'Ammonia', 'min_value': parameters.ammonia_min if parameters else None, 'max_value': parameters.ammonia_max if parameters else None},
      ]
      context = RequestContext(request, {
          'tank': tank,
          'parameters': parameters,
          'parameter_list': parameter_list,
      })
      context.update({'get_enabled': get_enabled})  # Add the custom filter to the context
      return render(request, 'hello/tankparams.html', context.flatten())

    
  def post(self, request, tank_id):
      tank = get_object_or_404(Tank, id=tank_id)
      parameters = tank.parameters
      form = ParametersForm(request.POST, instance=parameters, tank=tank, initial={'tank_id': tank_id})

      if form.is_valid():
          print(form.cleaned_data)
          form.save()
          messages.success(request, 'Parameters saved successfully')
          return redirect('tank_params', tank_id=tank_id)
      else:
          messages.error(request, 'There was an error saving the parameters')
          print(form.errors)

      return self.get(request, tank_id)

@register.filter
def get_enabled(parameters, parameter_name):
    if not parameters:
        return False

    enabled_field = f"{parameter_name.lower()}_enabled"
    return getattr(parameters, enabled_field)