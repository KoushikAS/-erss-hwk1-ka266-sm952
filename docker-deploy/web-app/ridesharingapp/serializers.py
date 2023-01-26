from rest_framework import serializers
from models import *

class RidesSerializers(serializers.ModelSerializer):
    class Meta:
        model=Rides
        fields=('RideId','Source','Destination')

