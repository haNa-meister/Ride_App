from django.shortcuts import render
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.template import loader
from login import models as login_model
from . import models
from . import forms
from django.urls import reverse
from django.conf import settings
# Create your views here.


def get_rides_share(ride):
    share_info = []
    share_list = models.Share.objects.filter(ride=ride).order_by('early_arrive_time')
    for sh in share_list:
        info = {'sharer': sh.sharer_name.name, 'party_number': sh.passenger}
        share_info.append(info)
    return share_info


def get_ride_dic(re, aswho = 'owner', action = None, share_id=None):
    dic = {}
    dic['ride_id'] = re.ride_id
    dic['vehicle_type'] = re.vehicle_type
    dic['owner_name'] = re.owner_name.name
    dic['stuatus'] = re.status
    dic['destination'] = re.destination_add
    dic['arrive_time'] = re.arrive_time
    dic['passenger_number'] = re.passenger
    if aswho == 'owner' or action == 'view':
        dic['get_absolute_url'] = re.get_absolute_url()
    elif aswho == 'driver':
        if action and action == 'complete':
            dic['get_absolute_url'] = re.complete_url()
        else:
            dic['get_absolute_url'] = re.confirm_url()
    elif aswho == 'share':
        dic['get_absolute_url'] = re.join_url(share_id)

    dic['special_info'] = re.special_info

    dic['share_list'] = get_rides_share(re)

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
    share_requests = models.Share.objects.filter(sharer_name=user).order_by('ride_id')

    pass_in = []
    # print(owner_requests[0].status)
    for re in owner_requests:
        dic = get_ride_dic(re)
        pass_in.append(dic)

    for sh in share_requests:
        if sh.ride and sh.ride.status == 'open':
            dic = get_ride_dic(sh.ride, action='view')
            pass_in.append(dic)

    driver_rides = models.Ride.objects.filter(driver_name=user, status='confirmed').order_by('ride_id')
    driver_list = []
    for re in driver_rides:
        dic = get_ride_dic(re, aswho='driver', action='complete')
        driver_list.append(dic)

    return render(request, 'ride/viewRides.html', {'request_list': pass_in, 'driver_list': driver_list})


def viewDetail(request, ride_id):
    ride = models.Ride.objects.get(ride_id=ride_id)
    user = login_model.User.objects.get(name=request.session.get('user_name'))
    if ride.owner_name == user:
        aswho = 'owner'
    else:
        aswho = 'share'

    message = ''
    if request.method == 'POST':
        if 'Back' in request.POST:
            return redirect('/viewRide/')
        elif 'Leave' in request.POST:
            share = models.Share.objects.get(ride_id=ride_id)
            ride.total_number -= share.passenger
            ride.save()
            share.delete()
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
    share_list = get_rides_share(ride)
    return render(request, 'ride/viewDetail.html', locals())


def searchRide(request, aswho, share_id=None):

    available_rides = []
    if aswho == 'driver':
        user = login_model.User.objects.get(name=request.session.get('user_name'))
        if aswho == 'driver' and not user.driver:
            raise PermissionDenied("Your are not a driver")
        available_rides = models.Ride.objects.filter(status='open', total_number__lt=user.vehicleCapacity,
                                                     vehicle_type=user.vehicleMake)

    elif aswho == 'share':
        share_request = models.Share.objects.get(share_id=share_id)
        st = share_request.early_arrive_time
        et = share_request.late_arrive_time
        available_rides = models.Ride.objects.filter(status='open',
                                                     arrive_time__gte=st,
                                                     arrive_time__lte=et,
                                                     vehicle_type=share_request.vehicle_type).exclude(owner_name=share_request.sharer_name)
    pass_in = []
    print(len(available_rides))
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
            shareList = models.Share.objects.filter(ride=ride)
            userList = []
            owner = ride.owner_name
            userList.append(owner)
            for share in shareList:
                userList.append(share.sharer_name)

            for user in userList:
                sendConfirmEmail(user.email, ride.ride_id, ride.driver_name, user.name)

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

    share_list = get_rides_share(ride)
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


def sendConfirmEmail(email, rideId, driver, username):
    from django.core.mail import EmailMultiAlternatives
    subject = 'Confirm Email from Ride Sharing Web APP'
    content = 'Dear User {}:\n' \
              ' Your Ride with ride ID : {}' \
              ' has been confirmed by Driver: {}!\n' \
              ' Thanks for your support!'.format(username, rideId, driver)

    msg = EmailMultiAlternatives(subject, content, settings.EMAIL_HOST_USER, [email])
    msg.send()
    pass
