from django.http.response import JsonResponse, HttpResponse

from django.shortcuts import render, redirect
from .serializers import *
from .models import *
from .forms import *


# Just for testing purpose
def say_hello(request):
    return HttpResponse("Hello World")

#Just for testing purpose
def get_rides(request):
    # Should Do User Validation
    rides = Ride.objects.all()
    rides_serialized = RideSerializers(rides, many=True)
    return JsonResponse(rides_serialized.data, safe=False)


# Just for Testing purpose
def get_drivers(request):
    # Should Do User Validation
    drivers = Driver.objects.all()
    drivers_serialized = DriverSerializers(drivers, many=True)
    return JsonResponse(drivers_serialized.data, safe=False)


# Just for Testing purpose
def get_users(request):
    # Should Do User Validation
    users = User.objects.all()
    users_serialized = UserSerializers(users, many=True)
    return JsonResponse(users_serialized.data, safe=False)


def get_homepage(request):
    return render(request, 'homepage.html')


# register user
def create_user(request):
    if request.POST:
        form = UserForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'register-user-page.html', {'form': UserForm})


def login_user(request):
    return HttpResponse("Page Under Development")


def logout_user(request):
    return HttpResponse("Page Under Development")


def driver_registration(request):
    return HttpResponse("Page Under Development")


# Ride Selection: View Rides accessible to the user
def view_rides(request):
    return HttpResponse("Page Under Development")


# Ride Requesting
def create_ride(request):
    return HttpResponse("Page Under Development")


# Ride Requesting Editing
def edit_ride(request):
    return HttpResponse("Page Under Development")


# Ride Status Viewing: View Individual Ride
def view_ride(request):
    return HttpResponse("Page Under Development")


# Ride Searching Driver: Similar to Ride Selection but with filters and open rides driver
def ride_searching_driver(request):
    return HttpResponse("Page Under Development")


# Ride Searching Sharer: Similar to Ride Selection but with filters and open rides driver
def ride_searching_sharer(request):
    return HttpResponse("Page Under Development")
