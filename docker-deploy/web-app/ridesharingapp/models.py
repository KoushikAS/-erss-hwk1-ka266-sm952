from django.db import models

# Create your models here.

class Rides(models.Model):
    RideId = models.AutoField(primary_key = True)
    Source = models.CharField(max_length=500)
    Destination = models.CharField(max_length=500)