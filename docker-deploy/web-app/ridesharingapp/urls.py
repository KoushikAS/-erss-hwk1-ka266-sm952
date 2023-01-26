from django.urls import path
from . import views

urlpatterns =[
    path('hello/', views.say_hello),
    path('getrides/',views.get_rides),
    path('getdrivers/',views.get_drivers),
    path('getusers/',views.get_users),
]