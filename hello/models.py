from django.db import models
from django.contrib.auth.models import User

class Sensor(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)  
  sname = models.CharField(max_length=20)


class Tank(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)    
  tname = models.CharField(max_length=20)

class Animal(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)  
  tank = models.ForeignKey(Tank, on_delete=models.CASCADE)
  atypes = [
        ('F', 'Fish'),
        ('T', 'Turtle'),
        ('O', 'Octopus'),
        ('L', 'Lobster'),
        ('S', 'Shrimp'),
    ] 
  animalType = models.CharField(max_length=1, choices=atypes)
  aname = models.CharField(max_length=20)
  

