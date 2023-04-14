from django.shortcuts import render, redirect
from django.views import View 
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from hello.models import *
from .models import LogData
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
    # Add code to retrieve temperature data and pass it to the template.
    # You may need to adjust the following example according to your LogData model structure.
    log_data = tank.logdata_set.filter(type=LogData.types.index(('te', 'temp'))).order_by('time_stamp')
    timestamps = [data.time_stamp.strftime('%Y-%m-%dT%H:%M:%S') for data in log_data]
    values = [float(data.value) for data in log_data]

    context = {
        'tank': tank,
        'timestamps': json.dumps(timestamps),
        'values': json.dumps(values),
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

class tankParams(View):
    def get(self, request, tank_id):
        tank = get_object_or_404(Tank, id=tank_id)
        parameters = tank.parameters  # Assuming the related name is 'parameters'
        parameter_list = [
            {'name': 'temp', 'label': 'Temperature'},
            {'name': 'ph', 'label': 'pH'},
            {'name': 'salinity', 'label': 'Salinity'},
            {'name': 'ammonia', 'label': 'Ammonia'},
        ]

        context = {
            'tank': tank,
            'parameters': parameters,
            'parameter_list': parameter_list,
        }
        return render(request, 'hello/tankparams.html', context)

