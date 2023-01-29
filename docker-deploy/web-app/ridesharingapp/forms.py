from django.forms import ModelForm
from django import forms
from .models import User, Vehicle


class RegisterUserForm(ModelForm):
    name = forms.TextInput()
    emailId = forms.EmailField()

    class Meta:
        model = User
        fields = ['name', 'emailId']


class LoginUserForm(ModelForm):
    emailId = forms.EmailField()

    class Meta:
        model = User
        fields = ['emailId']

#
# class RegisterDriverForm(ModelForm):
#     name = forms.TextInput()
#     emailId = forms.EmailField()
#     vehicle.type = forms.ChoiceField(choices = Vehicle.VehicleType)
#     max_passengers = forms.IntegerField()
#     license_no = forms.TextInput()
#
#
#     class Meta:
#         model = Vehicle
#         fields = ['name', 'emailId', 'vehicle.max_passengers', 'vehicle.type', 'vehicle.license_no']
#
