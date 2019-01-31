"""Ride_App URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from login import views as login_views
from ride import views as ride_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', login_views.index),
    url(r'^login/', login_views.login),
    url(r'^register/', login_views.register),
    url(r'^logout/', login_views.logout),
    url(r'^profile/', login_views.profile),
    url(r'^registerDriver/', login_views.registerDriver),
    url(r'^editProfile/', login_views.editProfile),
    url(r'^reqRide/', ride_views.reqRide),
    url(r'^editRide/', ride_views.editRide),
    url(r'^viewRide/', ride_views.viewRide),
    url(r'^searchRideAsDriver/', ride_views.searchRideAsDriver),
    url(r'^searchRideAsSharer/', ride_views.searchRideAsSharer),
]
