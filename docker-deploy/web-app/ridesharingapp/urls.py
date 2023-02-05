from django.urls import path
from . import views

urlpatterns = [
    path('nav/', views.get_nav),
    path('', views.get_homepage, name='home'),
    path('user/register/', views.create_user, name='registeruser'),
    path('user/edit/', views.edit_user, name='edituser'),
    path('user/login/', views.login_user, name='loginuser'),
    path('user/logout/', views.logout_user, name='logoutuser'),
    path('rides/view/', views.view_rides, name='viewrides'),
    path('rides/view/driver/', views.view_rides_driver, name='viewridesdriver'),
    path('rides/view/<int:rideId>', views.view_ride, name='viewride'),
    path('rides/create/', views.create_ride, name='createride'),
    path('rides/edit/<int:rideId>', views.edit_ride, name='editride'),
    path('rides/delete/<int:rideId>', views.delete_ride, name='deleteride'),
    path('rides/open/driver/', views.create_ride, name='openridesdriver'),
    path('rides/open/join/<int:rideId>', views.join_ride, name='joinride'),
    path('rides/open/sharer/', views.open_rides_sharer, name='openridessharer'),
    path('rides/edit/party/<int:rideId>', views.editParty, name='editParty'),
    path('rides/delete/party/<int:rideId>', views.deleteParty, name='deleteParty'),
    path('driver/home/', views.get_driver_homepage, name='driverhome'),
    path('driver/ride/confirmed/<int:rideId>', views.ride_confirmed, name='confirmride'),
    path('driver/ride/complete/<int:rideId>', views.ride_complete, name='completeride'),
    path('driver/register/', views.driver_registration, name='registerdriver'),
    path('driver/edit/', views.edit_driver, name='editdriver'),
    path('driver/unregister/', views.delete_driver, name='unregisterdriver'),
]
