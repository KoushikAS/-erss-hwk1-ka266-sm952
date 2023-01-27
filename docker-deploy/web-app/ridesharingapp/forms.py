from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User


class UserForm(ModelForm):
    name = forms.TextInput()
    emailId = forms.TextInput()

    class Meta:
        model = User
        fields = ['name', 'emailId']

