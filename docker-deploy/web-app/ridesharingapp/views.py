from django.http.response import JsonResponse, HttpResponse

from .serializers import RidesSerializers
from .models import Ride


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


def say_hello(request):
    return HttpResponse("Hello World")


def get_rides(request):
    # Should Do User Validation
    rides = Ride.objects.all()
    rides_serialized = RidesSerializers(rides, many=True)
    return JsonResponse(rides_serialized.data, safe=False)
