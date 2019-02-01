from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns
# from login import models
from .views import editRide

class Ride(models.Model):
    status = (
        ('open', 'o'),
        ('confirmed', 'cf'),
        ('completed', 'cp'),
    )

    ride_id = models.AutoField(primary_key=True)
    owner_name = models.ForeignKey('login.User', on_delete=models.CASCADE)
    destination_add = models.CharField(max_length=128, unique=False)
    arrive_time = models.DateTimeField(auto_now=True)
    passenger = models.PositiveIntegerField()
    vehicle_type = models.CharField(max_length=128, unique=False, blank=True)
    if_shared = models.BooleanField(default=False)
    special_info = models.CharField(max_length=256, unique=False)
    status = models.CharField(max_length=32, choices=status, default='open')
    driver_name = models.CharField(max_length=128, unique=False, blank=True)

    def get_absolute_url(self):
         """
         Returns the url to access a particular instance of Ride.
         """
         return reverse('viewDetail', kwargs={'ride_id': self.ride_id})

    def confirm_url(self):
        '''  for driver to confirm
        :return:
        '''
        return reverse('confirmRide', kwargs={'ride_id': self.ride_id})


class Share(models.Model):
    ride = models.ForeignKey('Ride', on_delete=models.CASCADE)
    sharer_name = models.CharField(max_length=128, unique=False)
