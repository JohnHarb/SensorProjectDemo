import re as regex
from django.shortcuts import render,redirect
from hello import models
from django.core.exceptions import FieldDoesNotExist, ObjectDoesNotExist

def deleteTank(tank_to_delete):
    try:
        models.Tank.objects.get( name = tank_to_delete).delete()
    except models.Tank.DoesNotExist:
        return "Tank does not exist to delete" 
    
    return "Tank successfully deleted"


