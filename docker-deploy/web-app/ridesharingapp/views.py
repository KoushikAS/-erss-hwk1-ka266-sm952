from django.http.response import JsonResponse, HttpResponse

from django.shortcuts import render, redirect
from .serializers import *
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


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


def check_ride_exists(request, rideId):
    if not Ride.objects.filter(rideId=rideId).exists():
        messages.error(request, f"Ride Id Does not exists.")
        return redirect('home')


def get_homepage(request):
    return render(request, 'homepage.html')


def get_driver_homepage(request):
    check_driver_view(request)

    driver = Driver.objects.get(user=request.user)
    currentRide = None

    if Ride.objects.filter(driver_id=driver.id, status=Ride.RideStatus.CONFIRMED).exists():
        currentRide = Ride.objects.get(driver_id=driver.id, status=Ride.RideStatus.CONFIRMED)

    return render(request, 'driver-home.html', {'currentRide': currentRide})


def get_nav(request):
    return render(request, 'nav.html')


# Save user details
def save_user(request, action, instance):
    if request.POST:
        form = RegisterUserForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, action.capitalize() + " User is successful. Can you log in now!")
            return redirect('loginuser')
        else:
            messages.error(request, f'Invalid Entry')
    else:
        form = RegisterUserForm(instance=instance)
    return render(request, 'user-form.html', {'form': form, 'pageAction': action.capitalize() + ' User'})


# Register new user
def create_user(request):
    return save_user(request, 'register', None)


# Edit User
def edit_user(request):
    check_user_authentication(request)
    return save_user(request, 'edit', request.user)


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


def save_driver_db(request, form):
    """ Registering the new driver with current logged in user details"""
    new_driver = form.save(commit=False)
    new_driver.user = request.user
    new_driver.save()
    form.save_m2m()


# Saving Driver details
def save_driver(request, action):
    if action == 'edit':
        instance = Driver.objects.get(user=request.user)
    else:
        instance = None

    if request.POST:
        form = RegisterDriverForm(request.POST, instance=instance)
        if form.is_valid():
            save_driver_db(request, form)
            request.session['driverView'] = True
            messages.info(request, f"Successfully " + action.capitalize() + " the Driver.")
            return redirect('home')
        else:
            messages.error(request, 'Invalid Entries in the form.')
            return redirect(action + 'driver')
    else:
        form = RegisterDriverForm(instance=instance)

    return render(request, 'driver-form.html', {'form': form, 'pageAction': action.capitalize() + ' Driver'})


# Register as Driver
def driver_registration(request):
    check_user_authentication(request)
    return save_driver(request, 'register')


# Editing Driver details
def edit_driver(request):
    check_user_authentication(request)
    check_driver_view(request)
    return save_driver(request, 'edit')


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
    check_user_authentication(request)
    rides = Ride.objects.filter(rideOwner__owner=request.user.id).all()
    rides_serialized = RideSerializers(rides, many=True)
    return render(request, 'view-rides.html', {'rides': rides_serialized.data})


# Ride Selection: View Rides accessible to the Driver
def view_rides_driver(request):
    check_user_authentication(request)
    check_driver_view(request)
    rides = Ride.objects.filter(status=Ride.RideStatus.OPEN).all()
    rides_serialized = RideSerializers(rides, many=True)
    return render(request, 'view-rides.html', {'rides': rides_serialized.data})


# Ride Requesting
def create_ride(request):
    check_user_authentication(request)
    form = RideForm(request.POST)
    if form.is_valid():
        party = Party(owner=request.user, passengers=form.cleaned_data['passengers'])
        party.save()
        ride = Ride(source=form.cleaned_data['source'],
                    destination=form.cleaned_data['destination'],
                    destinationArrivalTimeStamp=form.cleaned_data['destinationArrivalTimeStamp'],
                    maxPassengers=form.cleaned_data['maxPassengers'],
                    availablePassengers=form.cleaned_data['maxPassengers'] - form.cleaned_data['passengers'],
                    rideOwner=party,
                    isSharable=form.cleaned_data['isSharable'])
        ride.save()
        return redirect('viewride', rideId=ride.rideId)
    else:
        messages.error(request, 'Invalid Entries in the form.')
    return render(request, 'create-ride.html', {'form': form})


# Ride Requesting Editing
def edit_ride(request, rideId):
    check_user_authentication(request)
    try:
        ride = Ride.objects.get(rideId=rideId)
    except Ride.DoesNotExist:
        messages.error(request, f"Ride not found!")
        return redirect('home')
    if request.user.id != ride.rideOwner_id:
        messages.error(request, f"Not authorized!")
        return redirect('home')
    if ride.isRideEditable():
        data = {
            'source': ride.source,
            'destination': ride.destination,
            'destinationArrivalTimeStamp': ride.destinationArrivalTimeStamp,
            'passengers': ride.rideOwner.passengers,
            'maxPassengers': ride.maxPassengers,
            'isSharable': ride.isSharable
        }
        edit_form = RideForm(initial=data)
        if request.POST:
            try:
                party = Party.objects.get(owner=request.user)
            except Party.DoesNotExist:
                messages.error(request, f"Party not found!")
                return redirect('home')
            form = RideForm(request.POST)
            if form.is_valid():
                party.passengers = form.cleaned_data['passengers']
                party.save()
                ride.source = form.cleaned_data['source']
                ride.destination = form.cleaned_data['destination']
                ride.maxPassengers = form.cleaned_data['maxPassengers']
                ride.availablePassengers = form.cleaned_data['maxPassengers'] - form.cleaned_data['passengers']
                ride.destinationArrivalTimeStamp = form.cleaned_data['destinationArrivalTimeStamp']
                ride.rideOwner = party
                ride.isSharable = form.cleaned_data['isSharable']
                ride.save()
                return redirect('viewride', rideId=ride.rideId)
            else:
                messages.error(request, 'Invalid Entries in the form.')
    else:
        messages.error(request, f"Ride Is already confirmed.")
        return redirect('home')
    return render(request, 'edit-ride.html', {'form': edit_form})


def is_driver_in_ride(userId, ride):
    if ride.rideOwner.owner_id == userId:
        return True
    else:
        parties = ride.rideShared.all()
        for party in parties:
            if party.owner_id == userId:
                return True
        return False


# Ride Status Viewing: View Individual Ride
def view_ride(request, rideId):
    check_user_authentication(request)
    check_ride_exists(request, rideId)
    ride = Ride.objects.get(rideId=rideId)
    ride_serialized = RideSerializers(ride, many=False)
    ownerParty = Party.objects.get(id=ride.rideOwner_id)

    canConfirmRide = False
    canEdit = False
    canCompleteRide = False
    canJoinRide = False

    if ownerParty.owner_id == request.user.id and ride.status == Ride.RideStatus.OPEN:
        canEdit = True

    if request.session.get('driverView') and not is_driver_in_ride(request.user.id, ride):

        if ride.status == Ride.RideStatus.OPEN :
            canConfirmRide = True

        if ride.status == Ride.RideStatus.CONFIRMED and Driver.objects.filter(id=ride.driver_id).exists():
            canCompleteRide = True

    if ride.isSharable is True and ride.status == Ride.RideStatus.OPEN and ownerParty.owner_id != request.user.id:
        canJoinRide = True

    if ride.driver:
        driver = Driver.objects.get(id=ride.driver_id);
        driverUser = User.objects.get(id=driver.user_id);
        driverName = driverUser.username
    else:
        driver = None
        driverName = None

    return render(request, 'view-ride.html',
                  {'ride': ride_serialized.data, 'canEdit': canEdit, 'driver': driver, 'driverName': driverName,
                   'canConfirmRide': canConfirmRide, 'canCompleteRide': canCompleteRide, 'canJoinRide': canJoinRide})


# Ride Searching Driver: Similar to Ride Selection but with filters and open rides driver
def ride_searching_driver(request):
    return HttpResponse("Page Under Development")


# Ride Searching Sharer: Similar to Ride Selection but with filters and open rides driver
def ride_searching_sharer(request):
    return HttpResponse("Page Under Development")


# Ride Complete: when driver completes the ride
def ride_complete(request, rideId):
    check_user_authentication(request)
    check_driver_view(request)
    check_ride_exists(request, rideId)

    ride = Ride.objects.get(rideId=rideId)

    if ride.status != Ride.RideStatus.CONFIRMED:
        messages.error(request, f"Ride Is already Completed.")
        return redirect('driverhome')

    driver = Driver.objects.get(user=request.user)
    if ride.driver != driver:
        messages.error(request, f"This Ride is not started by you.")
        return redirect('driverhome')

    ride.status = Ride.RideStatus.COMPLETED
    ride.save()
    messages.success(request, " Successfully Completed the ride!")
    return redirect('driverhome')


# Ride Confirmed: when driver confirms the ride
def ride_confirmed(request, rideId):
    check_user_authentication(request)
    check_driver_view(request)
    check_ride_exists(request, rideId)

    ride = Ride.objects.get(rideId=rideId)

    if is_driver_in_ride(request.user.i, ride):
        messages.error(request, f"Not authorized to confirm your own ride!")
        return redirect('home')

    if ride.status != Ride.RideStatus.OPEN:
        messages.error(request, f"Ride Is already confirmed.")
        return redirect('driverhome')

    driver = Driver.objects.get(user=request.user)
    if ride.maxPassengers > driver.max_passengers:
        messages.error(request, f"This Ride is not compatible with your car.")
        return redirect('driverhome')

    ride.driver = driver
    ride.status = Ride.RideStatus.CONFIRMED
    ride.save()
    messages.success(request, " Successfully Confirmed the ride!")
    return redirect('driverhome')


# Join a sharable Ride.
def join_ride(request, rideId):
    check_user_authentication(request)
    check_ride_exists(rideId)

    if request.POST:
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            ride = Ride.objects().get(id=rideId)

            if ride.availablePassengers > form.cleaned_data['passengers']:
                messages.error(request, f"Party can only accommodate " + ride.availablePassengers + ". Please try "
                                                                                                    "another ride!")
                return redirect('home')

            party = Party(owner=request.user, passengers=form.cleaned_data['passengers'])
            party.save()
            ride.availablePassengers = ride.availablePassengers - form.cleaned_data['passengers']
            ride.rideShared.add(party)
            messages.success(request, " Successfully Joined the ride.")
            return redirect('home')
        else:
            messages.error(request, f'Invalid Entry')
    else:
        form = RegisterUserForm()
    return render(request, 'party-form.html', {'form': form, 'rideId': rideId})


def open_rides_sharer(request):
    check_user_authentication(request)
    canReset = False
    form = OpenRidesForm()
    rides = Ride.objects.filter(status=Ride.RideStatus.OPEN, isSharable=True).all()
    if request.POST:
        if 'reset_btn' in request.POST:
            rides = Ride.objects.filter(status=Ride.RideStatus.OPEN, isSharable=True).all()
            canReset = False
        elif 'search_btn' in request.POST:
            form = OpenRidesForm(request.POST)
            if form.is_valid():
                rides = Ride.objects.filter(status=Ride.RideStatus.OPEN,
                                            isSharable=True,
                                            destination__startswith=form.cleaned_data['destination'],
                                            destinationArrivalTimeStamp__gte=form.cleaned_data['earliestArrivalTime'],
                                            destinationArrivalTimeStamp__lte=form.cleaned_data['latestArrivalTime'],
                                            availablePassengers__gte=form.cleaned_data['passengers']) \
                                    .order_by('destinationArrivalTimeStamp')
            else:
                messages.error(request, f'Invalid Entry')
            canReset = True
    rides_serialized = RideSerializers(rides, many=True)
    return render(request, 'view-open-rides.html', {'rides': rides_serialized.data, 'form': form, 'canReset': canReset})


def delete_ride(request, rideId):
    check_user_authentication(request)
    try:
        ride = Ride.objects.get(rideId=rideId)
    except Ride.DoesNotExist:
        messages.error(request, f"Ride not found!")
    if request.user.id != ride.rideOwner_id:
        messages.error(request, f"Not authorized!")
    else:
        if ride.isRideEditable():
            ride.rideOwner.delete()
            ride.delete()
        else:
            messages.error(request, f"Ride Is already confirmed.!")
    return redirect('home')
