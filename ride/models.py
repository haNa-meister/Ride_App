from django.db import models
from login.models import User
# Create your models here.


class Ride(models.Model):
    status = (
        ('open', 'o'),
        ('confirmed', 'cf'),
        ('completed', 'cp'),
    )

    ride_id = models.AutoField(primary_key=True)
    owner_name = models.ForeignKey('login.User', on_delete=models.CASCADE)
    destination_add = models.CharField(max_length=128, unique=False)
    arrive_time = models.DateTimeField()
    passenger = models.PositiveIntegerField()
    vehicle_type = models.CharField(max_length=128, unique=False, blank=True)
    if_shared = models.BooleanField()
    special_info = models.CharField(max_length=256, unique=False)
    status = models.CharField(max_length=32, choices=status)
    driver_name = models.CharField(max_length=128, unique=False, blank=True)


class Share(models.Model):
    ride = models.ForeignKey('Ride', on_delete=models.CASCADE)
    sharer_name = models.CharField(max_length=128, unique=False)
