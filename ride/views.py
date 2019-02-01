from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from login import models as login_model
from . import models
from . import forms
from django.urls import reverse

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
        return render(request, 'ride/requestRide.html', locals())

    req_form = forms.reqForm()
    return render(request, 'ride/requestRide.html', locals())


def editRide(request, ride_id):
    message = ''
    user = login_model.User.objects.get(name=request.session.get('user_name'))
    ride = models.Ride.objects.get(ride_id=ride_id)
    if request.method == 'POST':
        editRide_form = forms.editRideForm(request.POST)
        if editRide_form.is_valid():
            destination = editRide_form.cleaned_data['destination_add']
            arrive = editRide_form.cleaned_data['arrive_time']
            passenger = editRide_form.cleaned_data['passenger']
            special_info = editRide_form.cleaned_data['special_info']
            if_shared = editRide_form.cleaned_data['if_shared']
            vehicle_type = editRide_form.cleaned_data['vehicle_type']

            if passenger:
                if passenger <= 0:
                    message = 'passenger should be positive'
                    return render(request, 'ride/editRide.html', locals())
                ride.passenger = passenger

            if destination:
                ride.destination_add = destination
            if arrive:
                ride.arrive_time = arrive
            if special_info:
                ride.special_info = special_info
            if if_shared:
                ride.if_shared = if_shared
            if vehicle_type:
                ride.vehicle_type = vehicle_type

            ride.save()
            return redirect(reverse('viewDetail', kwargs={'ride_id': ride.ride_id}))
        return render(request, 'ride/editRide.html', locals())

    editRide_form = forms.editRideForm
    return render(request, 'ride/editRide.html', locals())


def viewRide(request):
    user = login_model.User.objects.get(name=request.session.get('user_name'))
    owner_requests = models.Ride.objects.filter(owner_name=user)
    pass_in = []
    for re in owner_requests:
        dic = {}
        dic['ride_id'] = re.ride_id
        dic['owner_name'] = re.owner_name.name
        dic['get_absolute_url'] = re.get_absolute_url()
        pass_in.append(dic)
    share_request = models.Share.objects.filter(sharer_name=user.name)

    for sh in share_request:
        re = sh.ride
        dic = {}
        dic['ride_id'] = re.ride_id
        dic['owner_name'] = re.owner_name.name
        pass_in.append(dic)

    return render(request, 'ride/viewRides.html', {'request_list': pass_in})


def viewDetail(request, ride_id):
    ride = models.Ride.objects.get(ride_id=ride_id)
    user = login_model.User.objects.get(name=request.session.get('user_name'))
    message = ''
    if request.method == 'POST':
        if 'Back' in request.POST:
            return redirect('/viewRide/')
        elif 'Edit' in request.POST:
            return redirect(reverse('editRide', kwargs={'ride_id': ride.ride_id}))
        elif 'Delete' in request.POST:
            if ride.owner_name.name != user.name:
                message = 'You are not the owner of this ride!!!'
                return render(request, 'ride/viewDetail.html', locals())
            else:
                ride.delete()
                return  redirect('/viewRide/')

    return render(request, 'ride/viewDetail.html', locals())


def searchRideAsDriver():
    return


def searchRideAsSharer():
    return