from django.http.response import JsonResponse, HttpResponse

from django.shortcuts import render, redirect
from .serializers import *
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.core.mail import send_mail


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


def view_user(request):
    check_user_authentication(request)
    if request.session.get('driverView'):
        driver = Driver.objects.get(user=request.user)
    else:
        driver = None
    return render(request, 'view-user.html', {'driver': driver})


def get_homepage(request):
    return render(request, 'homepage.html')


def get_driver_homepage(request):
    check_driver_view(request)

    driver = Driver.objects.get(user=request.user)
    currentRides = []

    currentRides.extend(Ride.objects.filter(driver_id=driver.id, status=Ride.RideStatus.CONFIRMED))

    if len(currentRides) == 0:
        currentRides = None

    return render(request, 'driver-home.html', {'currentRides': currentRides})


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
        instance = Driver.objects.get(user_id=request.user.id)
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
    rides = Ride.objects.filter(Q(rideOwner__owner=request.user.id) | Q(rideShared__owner=request.user.id)).all()
    rides_serialized = RideSerializers(rides, many=True)
    return render(request, 'view-rides.html', {'rides': rides_serialized.data})


# Ride Selection: View Rides accessible to the Driver
def view_rides_driver(request):
    check_user_authentication(request)
    check_driver_view(request)
    driver = Driver.objects.get(user=request.user)
    rides = Ride.objects.filter(status=Ride.RideStatus.OPEN).filter(
        Q(vehicleType=None) | Q(vehicleType=driver.vehicle_type)) \
        .filter(Q(specialRequests=None) | Q(specialRequests=driver.special_info)).all()
    rides_serialized = RideSerializers(rides, many=True)
    return render(request, 'view-rides.html', {'rides': rides_serialized.data})


# Ride Requesting
def create_ride(request):
    check_user_authentication(request)
    form = RideForm()
    if request.POST:
        form = RideForm(request.POST)
        if form.is_valid():
            party = Party(owner=request.user, passengers=form.cleaned_data['passengers'])
            party.save()
            if form.cleaned_data['vehicleType'] == 'SIX_SEATER':
                availableSeats = 6 - form.cleaned_data['passengers']
            else:
                availableSeats = 4 - form.cleaned_data['passengers']
            if availableSeats < 0:
                messages.error(request, 'Invalid number of passengers in the form!')
            else:
                if form.cleaned_data['specialRequests'].strip() == '':
                    specialRequests = None
                else:
                    specialRequests = form.cleaned_data['specialRequests']
                ride = Ride(source=form.cleaned_data['source'],
                            destination=form.cleaned_data['destination'],
                            destinationArrivalTimeStamp=form.cleaned_data['destinationArrivalTimeStamp'],
                            availablePassengers=availableSeats,
                            rideOwner=party,
                            isSharable=form.cleaned_data['isSharable'],
                            vehicleType=form.cleaned_data['vehicleType'],
                            specialRequests=specialRequests)
                ride.save()
                return redirect('viewride', rideId=ride.rideId)
        else:
            messages.error(request, 'Invalid Entries in the form.')
    return render(request, 'create-ride.html', {'form': form})


# Ride Requesting Editing
def edit_ride(request, rideId):
    check_user_authentication(request)
    check_ride_exists(request, rideId)

    ride = Ride.objects.get(rideId=rideId)

    if request.user.id != ride.rideOwner.owner_id:
        messages.error(request, f"Not authorized!")
        return redirect('home')

    if ride.isRideEditable():
        data = {
            'source': ride.source,
            'destination': ride.destination,
            'destinationArrivalTimeStamp': ride.destinationArrivalTimeStamp,
            'passengers': ride.rideOwner.passengers,
            'vehicleType': ride.vehicleType,
            'isSharable': ride.isSharable,
            'specialRequests': ride.specialRequests,
        }
        edit_form = RideForm(initial=data)
        if request.POST:
            try:
                party = Party.objects.get(id=ride.rideOwner_id)
            except Party.DoesNotExist:
                messages.error(request, f"Party not found!")
                return redirect('home')
            form = RideForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['vehicleType'] == 'SIX_SEATER':
                    availableSeats = 6 - form.cleaned_data['passengers']
                else:
                    availableSeats = 4 - form.cleaned_data['passengers']
                if availableSeats < 0:
                    messages.error(request, 'Invalid number of passengers in the form!')
                else:
                    if form.cleaned_data['specialRequests'].strip() == '':
                        specialRequests = None
                    else:
                        specialRequests = form.cleaned_data['specialRequests']
                    party.passengers = form.cleaned_data['passengers']
                    party.save()
                    ride.source = form.cleaned_data['source']
                    ride.destination = form.cleaned_data['destination']
                    ride.availablePassengers = availableSeats
                    ride.destinationArrivalTimeStamp = form.cleaned_data['destinationArrivalTimeStamp']
                    ride.rideOwner = party
                    ride.isSharable = form.cleaned_data['isSharable']
                    ride.vehicleType = form.cleaned_data['vehicleType']
                    ride.specialRequests = specialRequests
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
    parties = []
    parties.append({'ownerName': User.objects.get(id=ownerParty.owner_id).username, 'passengers': ownerParty.passengers,
                    'owner': True})

    canConfirmRide = False
    canEdit = False
    canCompleteRide = False
    canJoinRide = False
    canEditParty = False

    isUserLinked = is_driver_in_ride(request.user.id, ride)

    if ownerParty.owner_id == request.user.id and ride.status == Ride.RideStatus.OPEN:
        canEdit = True

    if request.session.get('driverView') and not isUserLinked:

        if ride.status == Ride.RideStatus.OPEN:
            canConfirmRide = True

        if ride.status == Ride.RideStatus.CONFIRMED and Driver.objects.filter(id=ride.driver_id).exists():
            canCompleteRide = True

    if ride.isSharable is True and ride.status == Ride.RideStatus.OPEN and ownerParty.owner_id != request.user.id and not isUserLinked:
        canJoinRide = True

    if ride.driver:
        driver = Driver.objects.get(id=ride.driver_id)
        driverUser = User.objects.get(id=driver.user_id)
        driverName = driverUser.username
    else:
        driver = None
        driverName = None

    for party in ride.rideShared.all():
        parties.append(
            {'ownerName': User.objects.get(id=party.owner_id).username, 'passengers': party.passengers,
             'owner': False})

    if isUserLinked and ride.rideOwner.owner_id != request.user.id:
        canEditParty = True

    return render(request, 'view-ride.html',
                  {'ride': ride_serialized.data, 'canEdit': canEdit, 'driver': driver, 'driverName': driverName,
                   'canConfirmRide': canConfirmRide, 'canCompleteRide': canCompleteRide, 'canJoinRide': canJoinRide,
                   'canEditParty': canEditParty, 'parties': parties})


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

    ownerParty = Party.objects.get(id=ride.rideOwner_id)

    send_mail('Ride Complete', 'Your ride is completed. Looking to serve you again.', 'ece568project1@gmail.com',
              [User.objects.get(id=ownerParty.owner_id).email], fail_silently=False)
    messages.success(request, " Successfully Completed the ride!")
    return redirect('driverhome')


# Ride Confirmed: when driver confirms the ride
def ride_confirmed(request, rideId):
    check_user_authentication(request)
    check_driver_view(request)
    check_ride_exists(request, rideId)

    ride = Ride.objects.get(rideId=rideId)

    if is_driver_in_ride(request.user.id, ride):
        messages.error(request, f"Not authorized to confirm your own ride!")
        return redirect('home')

    if ride.status != Ride.RideStatus.OPEN:
        messages.error(request, f"Ride Is already confirmed.")
        return redirect('driverhome')

    driver = Driver.objects.get(user=request.user)
    if ride.vehicleType is not None and ride.vehicleType != driver.vehicle_type:
        messages.error(request, f"This Ride is not compatible with your car.")
        return redirect('driverhome')

    if ride.specialRequests is not None and ride.specialRequests.strip() and ride.specialRequests != driver.special_info:
        messages.error(request, f"This Ride is not compatible with your car based on special requests!")
        return redirect('driverhome')

    ride.driver = driver
    ride.status = Ride.RideStatus.CONFIRMED
    ride.save()
    messages.success(request, " Successfully Confirmed the ride!")
    return redirect('driverhome')


# Join a sharable Ride.
def party_ride(request, rideId, ride, instance):
    if request.POST:
        form = PartyForm(request.POST, instance=instance)

        if instance:
            # If Edit Revert the available list
            ride.availablePassengers = ride.availablePassengers + instance.passengers

        if form.is_valid():
            if ride.availablePassengers < form.cleaned_data['passengers']:
                messages.error(request, f"Party can only accommodate " + str(
                    ride.availablePassengers) + ". Please try another ride!")
                return redirect('home')

            # Edit Ride
            if instance:
                party = instance
                party.passengers = form.cleaned_data['passengers']
            else:
                party = Party(owner=request.user, passengers=form.cleaned_data['passengers'])

            party.save()
            ride.availablePassengers = ride.availablePassengers - form.cleaned_data['passengers']
            ride.rideShared.add(party)
            ride.save()
            if instance:
                messages.success(request, " Successfully edited the party!")
            else:
                messages.success(request, " Successfully Joined the ride.")
            return redirect('home')
        else:
            messages.error(request, f'Invalid Entry')
    else:
        form = PartyForm(instance=instance)
    return render(request, 'party-form.html', {'form': form, 'rideId': rideId})


def join_ride(request, rideId):
    check_user_authentication(request)
    check_ride_exists(request, rideId)
    ride = Ride.objects.get(rideId=rideId)
    return party_ride(request, rideId, ride, None)


def editParty(request, rideId):
    check_user_authentication(request)
    check_ride_exists(request, rideId)
    ride = Ride.objects.get(rideId=rideId)

    currentparty = None
    for party in ride.rideShared.all():
        if party.owner_id == request.user.id:
            currentparty = party
            break

    if not currentparty:
        messages.error(request, f'You are not part of shared list.')
        return redirect('home')

    return party_ride(request, rideId, ride, currentparty)


def deleteParty(request, rideId):
    check_user_authentication(request)
    check_ride_exists(request, rideId)
    ride = Ride.objects.get(rideId=rideId)

    currentparty = None
    for party in ride.rideShared.all():
        if party.owner_id == request.user.id:
            currentparty = party
            break

    if not currentparty:
        messages.error(request, f'You are not part of shared list.')
        return redirect('home')

    ride.availablePassengers = ride.availablePassengers + currentparty.passengers
    ride.save()
    currentparty.delete()

    messages.info(request, f"Successfully deleted the party.")
    return redirect('home')


def open_rides_sharer(request):
    check_user_authentication(request)
    canReset = False
    form = OpenRidesForm()
    rides = Ride.objects.filter(status=Ride.RideStatus.OPEN, isSharable=True).order_by(
        'destinationArrivalTimeStamp').all()
    if request.POST:
        if 'reset_btn' in request.POST:
            rides = Ride.objects.filter(status=Ride.RideStatus.OPEN, isSharable=True).order_by(
                'destinationArrivalTimeStamp').all()
            canReset = False
        elif 'search_btn' in request.POST:
            form = OpenRidesForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['earliestArrivalTime'] is not None and form.cleaned_data[
                    'latestArrivalTime'] is not None:
                    rides = Ride.objects.filter(status=Ride.RideStatus.OPEN,
                                                isSharable=True,
                                                destination__startswith='' if form.cleaned_data[
                                                                                  'destination'] is None else
                                                form.cleaned_data['destination'],
                                                destinationArrivalTimeStamp__gte=form.cleaned_data[
                                                    'earliestArrivalTime'],
                                                destinationArrivalTimeStamp__lte=form.cleaned_data['latestArrivalTime'],
                                                availablePassengers__gte=1 if form.cleaned_data[
                                                                                  'passengers'] is None else
                                                form.cleaned_data['passengers']) \
                        .order_by('destinationArrivalTimeStamp')
                elif form.cleaned_data['earliestArrivalTime'] is not None:
                    rides = Ride.objects.filter(status=Ride.RideStatus.OPEN,
                                                isSharable=True,
                                                destination__startswith='' if form.cleaned_data[
                                                                                  'destination'] is None else
                                                form.cleaned_data['destination'],
                                                destinationArrivalTimeStamp__gte=form.cleaned_data[
                                                    'earliestArrivalTime'],
                                                availablePassengers__gte=1 if form.cleaned_data[
                                                                                  'passengers'] is None else
                                                form.cleaned_data['passengers']) \
                        .order_by('destinationArrivalTimeStamp')
                elif form.cleaned_data['latestArrivalTime'] is not None:
                    rides = Ride.objects.filter(status=Ride.RideStatus.OPEN,
                                                isSharable=True,
                                                destination__startswith='' if form.cleaned_data[
                                                                                  'destination'] is None else
                                                form.cleaned_data['destination'],
                                                destinationArrivalTimeStamp__lte=form.cleaned_data['latestArrivalTime'],
                                                availablePassengers__gte=1 if form.cleaned_data[
                                                                                  'passengers'] is None else
                                                form.cleaned_data['passengers']) \
                        .order_by('destinationArrivalTimeStamp')
                else:
                    rides = Ride.objects.filter(status=Ride.RideStatus.OPEN, isSharable=True).order_by(
                        'destinationArrivalTimeStamp').all()
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
    if request.user.id != ride.rideOwner.owner_id:
        messages.error(request, f"Not authorized!")
    else:
        if ride.isRideEditable():
            ride.rideOwner.delete()
            parties = ride.rideShared.all()
            for party in parties:
                party.delete()
            ride.delete()
        else:
            messages.error(request, f"Ride Is already confirmed.!")
    return redirect('home')
