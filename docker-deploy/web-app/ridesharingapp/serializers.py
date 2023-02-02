from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class DriverSerializers(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class RideSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'
