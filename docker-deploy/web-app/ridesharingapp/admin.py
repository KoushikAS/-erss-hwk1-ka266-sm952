from django.contrib import admin

from .models import *


# Register your models here.

@admin.register(Ride)
class Ride(admin.ModelAdmin):
    list_display = ['rideId', 'driver', 'rideOwner', 'isSharable', 'source', 'destination',
                    'destinationArrivalTimeStamp', 'status']


@admin.register(Party)
class Party(admin.ModelAdmin):
    list_display = ['owner', 'passengers']
