from django.shortcuts import render
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.template import loader
from login import models as login_model
from . import models
from . import forms
from django.urls import reverse
from django.utils.timezone import now
# Create your views here.

def get_ride_dic(re, aswho = 'owner', action = None, share_id=None):
    dic = {}
    dic['ride_id'] = re.ride_id
    dic['vehicle_type'] = re.vehicle_type
    dic['owner_name'] = re.owner_name.name
    dic['stuatus'] = re.status
    dic['destination'] = re.destination_add
    dic['arrive_time'] = re.arrive_time
    dic['passenger_number'] = re.passenger
    if aswho == 'owner':
        dic['get_absolute_url'] = re.get_absolute_url()
    elif aswho == 'driver':
        if action and action == 'complete':
            dic['get_absolute_url'] = re.complete_url()
        else:
            dic['get_absolute_url'] = re.confirm_url()
    elif aswho == 'share':
        dic['get_absolute_url'] = re.join_url(share_id)

    dic['special_info'] = re.special_info
    return dic


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
            new_ride.total_number = passenger
            new_ride.save()
            print('new ride is created now jump to profile')
            return render(request, 'login/profile.html', locals())
        print('new ride is not correct')
        return render(request, 'ride/requestRide.html', locals())

    req_form = forms.reqForm()
    return render(request, 'ride/requestRide.html', locals())

def request_share_ride(request):
    message = ''
    user = login_model.User.objects.get(name=request.session.get('user_name'))
    if request.method == 'POST':
        req_form = forms.reqShareForm(request.POST)
        if req_form.is_valid():
            destination = req_form.cleaned_data['destination_add']
            early_arrive = req_form.cleaned_data['early_arrive_time']
            late_arrive = req_form.cleaned_data['late_arrive_time']
            passenger = req_form.cleaned_data['passenger']
            vehicle_type = req_form.cleaned_data['vehicle_type']

            if passenger <= 0:
                message = 'passenger should be positive'
                return render(request, 'ride/requestShare.html', locals())
            new_ride = models.Share()
            new_ride.passenger = passenger
            if vehicle_type:
                new_ride.vehicle_type = vehicle_type

            new_ride.early_arrive_time = early_arrive
            new_ride.late_arrive_time = late_arrive
            new_ride.destination_add = destination
            new_ride.sharer_name = user
            new_ride.save()
            dic = {'aswho':'share', 'share_id': new_ride.share_id}
            print('new share {} is created now jump to search page'.format(new_ride.share_id))
            print(reverse('searchRideforShare', kwargs=dic))
            return redirect(reverse('searchRideforShare', kwargs=dic))
        print('new share is not correct')
        return render(request, 'ride/requestShare.html', locals())


def editRide(request, ride_id):
    message = ''
    user = login_model.User.objects.get(name=request.session.get('user_name'))
    ride = models.Ride.objects.get(ride_id=ride_id)
    if request.method == 'POST':
        if ride.owner_name != user:
            message = 'you are not owner of this ride.'
            return render(request, 'ride/editRide.html', locals())
        status = ride.status
        if status != 'open': #open
            message = 'you can not edit a confirmed or complete ride.'
            return render(request, 'ride/editRide.html', locals())
        editRide_form = forms.editRideForm(request.POST)
        if editRide_form.is_valid():

            destination = editRide_form.cleaned_data['destination_add']
            arrive = editRide_form.cleaned_data['arrive_time']
            old_passange = ride.passenger
            passenger = editRide_form.cleaned_data['passenger']
            special_info = editRide_form.cleaned_data['special_info']
            if_shared = editRide_form.cleaned_data['if_shared']
            vehicle_type = editRide_form.cleaned_data['vehicle_type']

            if passenger:
                if passenger <= 0:
                    message = 'passenger should be positive'
                    return render(request, 'ride/editRide.html', locals())
                ride.passenger = passenger
                ride.total_number += passenger - old_passange

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
    owner_requests = models.Ride.objects.filter(owner_name=user, status='open').order_by('ride_id')
    pass_in = []
    # print(owner_requests[0].status)
    for re in owner_requests:
        dic = get_ride_dic(re)
        pass_in.append(dic)

    driver_rides = models.Ride.objects.filter(driver_name=user, status='confirmed').order_by('ride_id')
    driver_list = []
    for re in driver_rides:
        dic = get_ride_dic(re, aswho='driver', action ='complete')
        driver_list.append(dic)

    return render(request, 'ride/viewRides.html', {'request_list': pass_in, 'driver_list': driver_list})


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


def searchRide(request, aswho, share_id=None):

    available_rides = []
    if aswho=='driver':
        user = login_model.User.objects.get(name=request.session.get('user_name'))
        if aswho == 'driver' and not user.driver:
            raise PermissionDenied("Your are not a driver")
        available_rides = models.Ride.objects.filter(status='open',
                                                     vehicle_type=user.vehiclePlate,
                                                     passenger__lt=user.vehicleCapacity)
    elif aswho == 'share':
        share_request = models.Share.objects.get(share_id=share_id)
        available_rides = models.Ride.objects.filter(status='open',
                                                     vehicle_type=share_request.vehicle_type).exclude(owner_name=share_request.sharer_name)
    pass_in = []
    for re in available_rides:
        dic = {}
        if aswho == 'share':
            dic = get_ride_dic(re, aswho, share_id=share_id)
        else:
            dic = get_ride_dic(re, aswho)
        pass_in.append(dic)

    return render(request, 'ride/searchAsDriver.html', {'request_list': pass_in, 'aswho':str(aswho)})

def confirmRide(request, ride_id):
    user = login_model.User.objects.get(name=request.session.get('user_name'))
    ride = models.Ride.objects.get(ride_id=ride_id)
    message = ''
    if request.method == 'POST':
        if 'Back' in request.POST:
            return redirect('/searchRide/driver/')
        elif 'Confirm' in request.POST:
            ride.driver_name = user
            ride.status = 'confirmed'
            ride.empty_seats = user.vehicleCapacity - ride.passenger
            ride.save()
            return redirect('/searchRide/driver/')
        elif 'Complete' in request.POST:
            ride.status = 'completed'
            return redirect('/searchRide/driver/')

    return render(request, 'ride/confirmRide.html', locals())

def completeRide(request, ride_id):
    user = login_model.User.objects.get(name=request.session.get('user_name'))
    ride = models.Ride.objects.get(ride_id=ride_id)
    message = ''
    if user != ride.driver_name:
        raise PermissionDenied('you are not driver of this ride.')

    if request.method == 'POST':
        if 'Back' in request.POST:
            return redirect('/viewRide/')
        elif 'Complete' in request.POST:
            ride.status = 'completed'
            ride.save()
            return redirect('/viewRide/')

    return render(request, 'ride/completeRide.html', locals())


def joinRide(request, ride_id, share_id):
    user = login_model.User.objects.get(name=request.session.get('user_name'))
    ride = models.Ride.objects.get(ride_id=ride_id)
    share = models.Share.objects.get(share_id=share_id)

    if user != share.sharer_name:
        raise PermissionDenied('you are not own of this share request.')

    if request.method == 'POST':
        if 'Back' in request.POST:
            dic = {'aswho':'share', 'share_id': share_id}
            return redirect(reverse('searchRideforShare', kwargs=dic))
        elif 'Join' in request.POST:
            share.ride = ride
            share.save()
            ride.total_number += share.passenger
            ride.save()
            return redirect('/profile/')

    return render(request, 'ride/joinRide.html', locals())