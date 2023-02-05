from django.forms import ModelForm
from django import forms
from .models import Driver, Ride, Party
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=101)
    last_name = forms.CharField(max_length=101)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class LoginUserForm(ModelForm):
    emailId = forms.EmailField()

    class Meta:
        model = User
        fields = ['emailId']


class RegisterDriverForm(ModelForm):
    class Meta:
        model = Driver
        fields = ['vehicle_type', 'license_no', 'special_info']
        labels = {'vehicle_type': 'Vehicle Type', 'license_no': 'License Number', 'special_info': 'Special Vehicle Information'}


class PartyForm(ModelForm):
    class Meta:
        model = Party
        fields = ['passengers']


class RideForm(ModelForm):
    passengers = forms.IntegerField(max_value=6, min_value=1)
    destinationArrivalTimeStamp = forms.DateTimeField(label='Destination Arrival Time')

    class Meta:
        model = Ride
        fields = ['source', 'destination', 'destinationArrivalTimeStamp', 'passengers', 'vehicleType', 'isSharable',
                  'specialRequests']
        labels = {'vehicleType': 'Vehicle Type', 'isSharable': 'Willing to share?',
                  'specialRequests': 'Any special requests?', }


class OpenRidesForm(forms.Form):
    destination = forms.CharField(max_length=500, required=False)
    passengers = forms.IntegerField(max_value=6, min_value=1, required=False)
    earliestArrivalTime = forms.DateTimeField(label='Earliest Arrival Time', required=False)
    latestArrivalTime = forms.DateTimeField(label='Latest Arrival Time', required=False)
