from django.http.response import JsonResponse, HttpResponse

from django.shortcuts import render, redirect
from .serializers import *
from .models import *
from .forms import *


# Create your views here.


# @csrf_exempt
# def RidesApi(request, id=0):
#     if request.method == 'GET':
#         rides = Rides.objects.all()
#         rides_serialized = RidesSerializers(rides, many = True)
#         return JsonResponse(rides_serialized.data,safe=False)
#     elif request.method == 'POST':
#         ride_data = JSONParser().parse(request)
#         ride_serializer = RidesSerializers(ride_data)
#         if ride_serializer.is_valid():
#             ride_serializer.save()
#             return JsonResponse("Successful", safe = False)
#         else:
#             return JsonResponse("Failed", safe = False)

# Just for testing purpose
def say_hello(request):
    return HttpResponse("Hello World")


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
    return render(request, 'home/homepage.html')


def create_user(request):
    if request.POST:
        form = UserForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'registeruserpage.html', {'form': UserForm})
