from django.http.response import JsonResponse, HttpResponse

from django.shortcuts import render, redirect
from .serializers import *
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


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


def check_user_authentication(request):
    if request.user.is_authenticated is False:
        messages.info(request, f"Please login again.")
        return redirect('loginuser')


def check_driver_view(request):
    if request.session.get('driverView') is None:
        messages.info(request, f"Please register as a Driver.")
        return redirect('registerdriver')


def get_homepage(request):
    return render(request, 'homepage.html')


# register user
def create_user(request):
    if request.POST:
        form = RegisterUserForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created. You can log in now!')
            return redirect('loginuser')
        else:
            messages.error(request, f'Could not create an account')
    else:
        form = RegisterUserForm(request.POST)

    return render(request, 'register-user-page.html', {'form': form})


def login_user(request):
    if request.POST:
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if Driver.objects.filter(user=user).exists():
                    request.session['driverView'] = True
                else:
                    request.session['driverView'] = False

                messages.info(request, f"You are now logged in as {username}.")
                return redirect('home')
            else:
                messages.error(request, f"User not Authenticated.")
        else:
            messages.error(request, f"Something is wrong with your entry")

    return render(request, 'login-user-page.html', {'form': AuthenticationForm})


def logout_user(request):
    logout(request)
    messages.info(request, f"You have successfully logged out.")

    return redirect('home')


def driver_registration(request):
    check_user_authentication(request)

    if Driver.objects.filter(user=request.user).exists():
        messages.info(request, f"You have already registered as a Driver.")
        return redirect('home')

    if request.POST:
        form = RegisterDriverForm(request.POST)
        if form.is_valid():
            """ Registering the new driver with current logged in user details"""
            new_driver = form.save(commit=False)
            new_driver.user = request.user
            new_driver.save()
            form.save_m2m()

            request.session['driverView'] = True
            messages.info(request, f"Successfully registered as a Driver.")
            return redirect('home')
        else:
            messages.error(request, 'User with this EmailId already exists.')
            return redirect('registerdriver')

    return render(request, 'register-driver-page.html', {'form': RegisterDriverForm})
    # return HttpResponse("Page Under Development")

# View user details
def view_user(request):
    return HttpResponse("Page Under Development")

# Editing user details
def edit_user(request):
    return HttpResponse("Page Under Development")

# View Driver details
def view_driver(request):
    return HttpResponse("Page Under Development")

# Editing Driver details
def edit_driver(request):
    return HttpResponse("Page Under Development")

# Delete Driver details
def delete_driver(request):
    check_user_authentication(request)
    check_driver_view(request)
    Driver.objects.filter(user=request.user).delete()
    request.session['driverView'] = False
    messages.info(request, f"Successfully un-registered as a Driver.")
    return redirect('home')

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
