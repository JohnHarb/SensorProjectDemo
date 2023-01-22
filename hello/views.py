from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View 
from django.http import JsonResponse
from hello.models import *
from django.contrib.auth import authenticate, login, logout

class signUp(View):
  def get(self, request):
   return render(request,'hello/signup.html')
  
  def post(self, request):
    fname = request.POST["fname"]
    lname = request.POST["lname"]
    email = request.POST["email"]
    password = request.POST["password"]
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
    return redirect('/signin/')
 
class home(View):
  def get(self, request):
   return render(request,'hello/home.html')

class profile(View):
  def get(self, request):
    user = request.user
    tNum = str(len(Tank.objects.filter(user=user)))
    sNum = str(len(Sensor.objects.filter(user=user)))
    return render(request,'hello/profile.html', {"name": user.first_name + " " + user.last_name, "email": user.email, "tanks": tNum, "sensors": sNum})

class aboutus(View):
  def get(self, request):
   return render(request,'hello/aboutus.html')

class signOut(View):
  def get(self, request):
    logout(request)
    return redirect('/signin/')
