from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from login import models as login_model
from . import models
from . import forms

# Create your views here.


def reqRide(request):
    message = ''
    user = login_model.User.objects.get(name=request.session.get('user_name'))
    if request.method == 'POST':
        req_form = forms.reqForm(request.POST)
        if req_form.is_valid():
            destination = req_form.cleaned_data['destination_add']
            arrive = req_form.cleaned_data['arrive_time']
            passenger = req_form.cleaned_data['passenger']
            special_info = req_form.cleaned_data['special_info']
            if_shared = req_form.cleaned_data['if_shared']
            vehicle_type = req_form.cleaned_data['vehicle_type']

            if passenger <= 0:
                message = 'passenger should be positive'
                return render(request, 'ride/requestRide.html', locals())

            new_ride = models.Ride()
            new_ride.passenger = passenger
            if vehicle_type:
                new_ride.vehicle_type = vehicle_type
            new_ride.if_shared = if_shared
            new_ride.special_info = special_info
            new_ride.arrive_time = arrive
            new_ride.destination_add = destination
            new_ride.owner_name = user
            new_ride.save()
            return render(request, 'login/profile.html', locals())
        return

    req_form = forms.reqForm()
    return render(request, 'ride/requestRide.html', locals())


def editRide():
    return

def viewRide():
    return


def searchRideAsDriver():
    return


def searchRideAsSharer():
    return