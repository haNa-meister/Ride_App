from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from django.utils.timezone import now
from . import models
from . import forms
from ride import forms as ride_form

# Create your views here.


def index(request):
    pass
    return render(request, '../templates/login/index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect("/profile/")
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        massage = ''
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/profile/')
                else:
                    message = 'Invalid Password'

            except:
                message = 'Invalid Username'
        return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = ''
        print('register_form.is_valid:' + str(register_form.is_valid()))
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # correct password
                message = 'different password for twice typing'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # unique username
                    message = 'Not a unique username'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                new_user = models.User()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                redirect('/profile/')
                return render(request, 'login/profile.html', locals())

    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/index/")
    request.session.flush()
    return redirect("/index/")


def profile(request):
    print('user: {}'.format(request.session.get('user_name')))
    user = models.User.objects.get(name=request.session.get('user_name'))
    if request.POST:
        if 'edit' in request.POST:
            editProfile_form = forms.EditProfileForm()
            return render(request, 'login/editProfile.html', locals())
        elif 'regDriver' in request.POST:
            reg_form = forms.RegisterDriverForm()
            if user.driver:
                message = 'You are already a driver'
                return render(request, 'login/profile.html', locals())
            else:
                return render(request, 'login/registerDriver.html', locals())
        elif 'reqRide' in request.POST:
            req_form = ride_form.reqForm(initial={'arrive_time': str(now())})
            return render(request, 'ride/requestRide.html', locals())
        elif 'reqShare' in  request.POST:
            req_form = ride_form.reqShareForm(initial={'early_arrive_time': str(now())})
            return render(request, 'ride/requestShare.html', locals())
        elif 'viewRide' in request.POST:
            return redirect('/viewRide/')
        elif 'searchRideAsDriver' in request.POST:
            return redirect('/searchRide/driver/')
    else:
        return render(request, 'login/profile.html', locals())


def registerDriver(request):
    message = ''
    print('user:{} register as Drive'.format(request.session.get('user_name')))
    user = models.User.objects.get(name=request.session.get('user_name'))

    if request.method == 'POST':
        reg_form = forms.RegisterDriverForm(request.POST)
        if reg_form.is_valid():
            vehicleMake = reg_form.cleaned_data['vehicleMake']
            vehiclePlate = reg_form.cleaned_data['vehiclePlate']
            vehicleCapacity = reg_form.cleaned_data['vehicleCapacity']
            user.vehicleMake = vehicleMake
            user.vehiclePlate = vehiclePlate
            user.vehicle_capacity = vehicleCapacity
            user.driver = True
            user.save()
            return render(request, 'login/profile.html', locals())

    reg_form = forms.RegisterDriverForm()
    return render(request, 'login/registerDriver.html', locals())


def editProfile(request):
    message = ''
    user = models.User.objects.get(name=request.session.get('user_name'))
    if request.method == 'POST':
        editProfile_form = forms.EditProfileForm(request.POST)
        if editProfile_form.is_valid():
            email = editProfile_form.cleaned_data['email']
            sex = editProfile_form.cleaned_data['sex']
            vehicleMake = editProfile_form.cleaned_data['vehicleMake']
            vehiclePlate = editProfile_form.cleaned_data['vehiclePlate']
            vehicleCapacity = editProfile_form.cleaned_data['vehicleCapacity']
            if user.driver:
                if vehicleMake:
                    user.vehicleMake = editProfile_form.cleaned_data['vehicleMake']
                if vehiclePlate:
                    user.vehiclePlate = editProfile_form.cleaned_data['vehiclePlate']
                if vehicleCapacity:
                    user.vehicleCapacity = editProfile_form.cleaned_data['vehicleCapacity']
            elif vehiclePlate or vehicleMake or vehicleCapacity:
                message = 'You are not a driver yet'
                return render(request, 'login/editProfile.html', locals())

            if email:
                user.email = editProfile_form.cleaned_data['email']
            user.save()
            return render(request, 'login/profile.html', locals())

    print('not vaild')
    editProfile_form = forms.EditProfileForm()
    return render(request, 'login/editProfile.html', locals())
