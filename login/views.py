from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from . import models
from . import forms

# Create your views here.


def index(request):
    pass
    return render(request, '../templates/login/index.html')


def login(request):
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        massage = ''
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    print('password correct')
                    return redirect('/index/')
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
                if same_email_user:  # unique email address
                    message = 'Not a unique email address'
                    return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    pass
    return render(request, '../templates/logout.html')
