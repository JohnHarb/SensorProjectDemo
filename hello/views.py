from django.shortcuts import render, redirect
from django.views import View 
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from hello.models import *
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
 
class home(View):
  def get(self, request):
    tanks = Tank.objects.filter(user=request.user)
    #sensors = Sensor.objects.filter(user=request.user)
    #return render(request,'hello/home.html', {"tanks": tanks, "sensors": sensors})

class profile(View):
  def get(self, request):
    user = request.user
    tNum = str(len(Tank.objects.filter(user=user)))
    return render(request,'hello/profile.html', {"name": user.first_name + " " + user.last_name, "email": user.email, "tanks": tNum})

class aboutUs(View):
  def get(self, request):
   return render(request,'hello/aboutus.html')

class signOut(View):
  def get(self, request):
    logout(request)
    return redirect('/signin/')
"""
class tankManage(View):
  def get(self, request):
    tanks = Tank.objects.filter(user=request.user).values()
    return JsonResponse(json.dumps(list(tanks)), safe=False)

  def post(self, request):
    tname = request.POST["tname"]
    sensor = request.POST["sensor"]
    if len(Tank.objects.filter(user = request.user, tname = tname)) == 1:
      messages.error(request, "tank exists already")
      return redirect('/home/')
    if sensor != 'none':
      sensorToAdd = Sensor.objects.filter(id=sensor)[0]
      if len(Tank.objects.filter(user = request.user, sensor=sensorToAdd)) == 1:
        messages.error(request, "sensor assigned already")
        return redirect('/home/')
      newTank = Tank(tname=tname, user=request.user, sensor=sensorToAdd)
    else:
      newTank = Tank(tname=tname, user=request.user)
    newTank.save()
    return redirect('/home/')"""