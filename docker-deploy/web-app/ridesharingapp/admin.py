from django.contrib import admin

from .models import Ride


# Register your models here.

@admin.register(Ride)
class Ride(admin.ModelAdmin):
    list_display = ['rideId', 'driver', 'rideOwner', 'isSharable', 'source', 'destination',
                    'destinationArrivalTimeStamp', 'status']
