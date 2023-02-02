from django.urls import path
from . import views

urlpatterns =[
    path('hello/', views.say_hello),
    path('getrides/',views.get_rides),
    path('getdrivers/',views.get_drivers),
    # path('getusers/',views.get_users),
    path('', views.get_homepage, name = 'home'),
    path('register/user/', views.create_user, name = 'registeruser'),
    path('login/user/', views.login_user, name = 'loginuser'),
    path('logout/user/', views.logout_user, name = 'logoutuser'),
    path('register/driver/', views.driver_registration, name = 'registerdriver'),
    path('rides/view/', views.view_rides, name = 'viewrides'),
    path('rides/view/<int:rideId>', views.view_ride, name = 'viewride'),
    path('rides/create', views.create_ride, name = 'createride'),
    path('rides/edit', views.create_ride, name = 'editride'),
    path('rides/open/driver', views.create_ride, name = 'openridesdriver'),
    path('rides/open/sharer', views.create_ride, name = 'openridessharer'),
    path('driver/ride/confirmed', views.ride_confirmed, name='confirmride'),
    path('driver/ride/complete/', views.ride_complete, name='completeride'),
]