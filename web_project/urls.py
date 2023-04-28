"""web_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hello import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.signUp.as_view()),
    path("signin/", views.signIn.as_view()),
    path("home/", views.home.as_view()),
    path("profile/", views.profile.as_view()),
    path('tankhome/<int:tank_id>/', views.TankHomeView.as_view(), name='tankhome'),
    path('tankhome/<int:tank_id>/log_parameter/', views.LogParameterView.as_view(), name='log_parameter'),
    path("addtank/", views.addTank.as_view()),
     path("manualinput/", views.manualInput.as_view()),
    path("aboutus/", views.aboutUs.as_view()),
    path("signout/", views.signOut.as_view()),
    path('tankparams/<int:tank_id>/', views.tankParams.as_view(), name='tank_params'),
    path("deletetank/<int:tank_id>/", views.deleteTank.as_view(), name='tank_delete'),
    path('tank_data/<int:tank_id>/', views.tank_data, name='tank_data'),
    #path("tankmanage/", views.tankManage.as_view()),
]


