from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import  JSONParser
from django.http.response import JsonResponse

from models import *
from serializers import *

# Create your views here.


@csrf_exempt
def RidesApi(request, id=0):
    if request.method == 'GET':
        rides = Rides.objects.all()
        rides_serialized = RidesSerializers(rides, many = True)
        return JsonResponse(rides_serialized.data,safe=False)
    elif request.method == 'POST':
        ride_data = JSONParser().parse(request)
        ride_serializer = RidesSerializers(ride_data)
        if ride_serializer.is_valid():
            ride_serializer.save()
            return JsonResponse("Successful", safe = False)
        else:
            return JsonResponse("Failed", safe = False)


