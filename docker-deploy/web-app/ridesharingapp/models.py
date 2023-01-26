from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    userId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    emailId = models.CharField(max_length=500, unique= True)


class Driver(User):
    vehicle = models.CharField(max_length=500)


class Ride(models.Model):
    class RideStatus(models.TextChoices):
        NEW = 'NEW', _('New')
        ACCEPTED = 'ACCEPTED', _('Accepted')
        RIDING = 'RIDING', _('RIDING')
        FINISHED = 'FINISHED', _('FINISHED')

    rideId = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, related_name='driver', on_delete=models.CASCADE)
    rideShared = models.ManyToManyField(User, blank=True)
    source = models.CharField(max_length=500)
    destination = models.CharField(max_length=500)
    status = models.CharField(
        max_length=8,
        choices=RideStatus.choices,
        default=RideStatus.NEW,
    )

    def isEditable(self):
        return self.RideStatus == self.RideStatus.NEW
