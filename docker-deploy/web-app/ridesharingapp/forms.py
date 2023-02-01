from django.forms import ModelForm
from django import forms
from .models import User, Driver


class RegisterUserForm(ModelForm):
    emailId = forms.EmailField()

    class Meta:
        model = User
        fields = ['name', 'emailId']


class LoginUserForm(ModelForm):
    emailId = forms.EmailField()

    class Meta:
        model = User
        fields = ['emailId']


class RegisterDriverForm(ModelForm):
    emailId = forms.EmailField()

    class Meta:
        model = Driver
        fields = ['name', 'emailId', 'vehicle_type', 'max_passengers', 'license_no']
