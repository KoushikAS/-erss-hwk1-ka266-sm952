from rest_framework import serializers
from .models import *


class RidesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ('rideId', 'source', 'destination', 'status')
