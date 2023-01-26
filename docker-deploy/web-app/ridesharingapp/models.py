from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    userId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    emailId = models.CharField(max_length=500, unique=True)


class Vehicle(models.Model):
    class VehicleType(models.TextChoices):
        FOUR_SEATER = 'FOUR_SEATER', _('4 Seats')
        SIX_SEATER = 'SIX_SEATER', _('6 Seats')

    type = models.CharField(max_length=15,
                            choices=VehicleType.choices,
                            default=VehicleType.FOUR_SEATER, )
    max_passengers = models.IntegerField()
    license_no = models.CharField(max_length=500)


class Driver(User):
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)


class Party(models.Model):
    owner = models.ForeignKey(User, related_name='party_owner', on_delete=models.CASCADE)
    passengers = models.IntegerField()


class Ride(models.Model):
    class RideStatus(models.TextChoices):
        OPEN = 'OPEN', _('Open')
        CONFIRMED = 'CONFIRMED', _('Confirmed')
        COMPLETED = 'COMPLETED', _('Completed')

    rideId = models.AutoField(primary_key=True)
    driver = models.ForeignKey(Driver, related_name='driver', on_delete=models.CASCADE)
    rideOwner = models.ForeignKey(Party, related_name='ride_owner', on_delete=models.CASCADE)
    isSharable = models.BooleanField(default=False)
    rideShared = models.ManyToManyField(Party, blank=True)
    source = models.CharField(max_length=500)
    destination = models.CharField(max_length=500)
    destinationArrivalTimeStamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=10,
        choices=RideStatus.choices,
        default=RideStatus.OPEN,
    )

    def isRideEditable(self):
        return self.RideStatus == self.RideStatus.OPEN
