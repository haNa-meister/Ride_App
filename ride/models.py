from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns

# from login import models
from .views import editRide

class Ride(models.Model):
    status = (
        ('open', 'open'),
        ('confirmed', 'confirmed'),
        ('completed', 'completed'),
    )

    ride_id = models.AutoField(primary_key=True)
    owner_name = models.ForeignKey('login.User', on_delete=models.CASCADE,
                                   related_name='owner_of_ride'
                                   )
    driver_name = models.ForeignKey('login.User', on_delete=models.SET_NULL,
                                    null=True, blank=True,
                                    related_name='driver_of_ride'
                                    )
    destination_add = models.CharField(max_length=128, unique=False)
    arrive_time = models.DateTimeField(auto_now=False)
    passenger = models.PositiveIntegerField()
    vehicle_type = models.CharField(max_length=128, unique=False, blank=True)
    if_shared = models.BooleanField(default=False)
    special_info = models.CharField(max_length=256, unique=False, blank=True)
    status = models.CharField(max_length=32, choices=status, default='open')
    # driver_name = models.CharField(max_length=128, unique=False, blank=True)
    total_number = models.PositiveIntegerField(default=0)

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

    def complete_url(self):
        '''  for driver to confirm
        :return:
        '''
        return reverse('completeRide', kwargs={'ride_id': self.ride_id})

    def join_url(self, share_id):
        return reverse('joinRide', kwargs={'ride_id': self.ride_id, 'share_id': share_id})


class Share(models.Model):
    share_id = models.AutoField(primary_key=True)
    ride = models.ForeignKey('Ride', null=True, blank=True, on_delete=models.CASCADE)
    sharer_name = models.ForeignKey('login.User', on_delete=models.CASCADE,
                                   related_name='user_of_sharer')
    destination_add = models.CharField(max_length=128, default='non', unique=False)
    early_arrive_time = models.DateTimeField(auto_now=False)
    late_arrive_time = models.DateTimeField(auto_now=False)
    passenger = models.PositiveIntegerField(default=1)
    vehicle_type = models.CharField(max_length=128, unique=False, blank=True)

