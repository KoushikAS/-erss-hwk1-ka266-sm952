from django.http.response import JsonResponse, HttpResponse

from django.shortcuts import render, redirect
from .serializers import *
from .models import *
from .forms import *
from django.contrib import messages


# Just for testing purpose
def say_hello(request):
    return HttpResponse("Hello World")


# Just for testing purpose
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
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            storage = messages.get_messages(request)
            return redirect('/login/user/')
        else:
            messages.error(request, 'User with this EmailId already exists.')
            return redirect('registeruser')

    return render(request, 'register-user-page.html', {'form': RegisterUserForm})


def login_user(request):
    if request.POST:
        form = LoginUserForm(request.POST)
        email_id = request.POST['emailId']

        if User.objects.filter(emailId=email_id).exists():
            request.session['userId'] = User.objects.get(emailId=email_id).userId
            if Driver.objects.filter(emailId=email_id).exists():
                request.session['driverView'] = True
            else:
                request.session['driverView'] = False

            return redirect('home')
        else:
            messages.error(request, 'EmailId is not been registered in our system.')
            return redirect('loginuser')

    return render(request, 'login-user-page.html', {'form': LoginUserForm})


def logout_user(request):
    del request.session['userId']
    del request.session['driverView']

    return redirect('home')


def driver_registration(request):
    if request.POST:
        form = RegisterDriverForm(request.POST)
        if form.is_valid():
            form.save()
            storage = messages.get_messages(request)
            return redirect('/login/user/')
        else:
            messages.error(request, 'User with this EmailId already exists.')
            return redirect('registerdriver')

    return render(request, 'register-driver-page.html', {'form': RegisterDriverForm})
    #return HttpResponse("Page Under Development")


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


# Ride Complete: when driver completes the ride
def ride_complete(request):
    return HttpResponse("Page Under Development")


# Ride Cnfirmed: when driver confirms the ride
def ride_confirmed(request):
    return HttpResponse("Page Under Development")
