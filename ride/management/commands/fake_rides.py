import random

import datetime
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from ride.models import Ride
from login.models import User

def fake_rides():
    Ride.objects.all().delete()
    user_list = User.objects.all()

    for i in range(0, 30):
        random_user = random.sample(user_list, 1)

        dic = {}
        dic['name'] = 'user_{}'.format(i)
        dic['password'] = '1'
        dic['email'] = 'fake@nonexist.com'
        dic['sex'] = 'm'
        dic['vechicleMake'] = 'vM_{}'.format(i)

        if i < 10:
            dic['driver'] = True
        else:
            dic['driver'] = False
        u = User.objects.create(**dic)


class Command(BaseCommand):
    help = 'testcases: creat 30 rides'

    def handle(self, *args, **options):
        fake_rides()
        self.stdout.write(self.style.SUCCESS('fake rides created'))