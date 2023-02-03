from django.urls import path
from . import views

urlpatterns =[
    path('nav/', views.get_nav),
    path('getrides/',views.get_rides),
    path('getdrivers/',views.get_drivers),
    path('getusers/',views.get_users),
    path('', views.get_homepage, name = 'home'),
    path('user/register/', views.create_user, name = 'registeruser'),
    path('user/edit/', views.edit_user, name='edituser'),
    path('user/login/', views.login_user, name = 'loginuser'),
    path('user/logout/', views.logout_user, name = 'logoutuser'),
    path('driver/register/', views.driver_registration, name = 'registerdriver'),
    path('driver/edit/', views.edit_driver, name='editdriver'),
    path('driver/unregister/', views.delete_driver, name='unregisterdriver'),
    path('rides/view/', views.view_rides, name = 'viewrides'),
    path('rides/view/<int:rideId>', views.view_ride, name = 'viewride'),
    path('rides/create', views.create_ride, name = 'createride'),
    path('rides/edit/<int:rideId>', views.edit_ride, name = 'editride'),
    path('rides/open/driver', views.create_ride, name = 'openridesdriver'),
    path('rides/open/sharer', views.create_ride, name = 'openridessharer'),
    path('driver/ride/confirmed', views.ride_confirmed, name='confirmride'),
    path('driver/ride/complete/', views.ride_complete, name='completeride'),
]