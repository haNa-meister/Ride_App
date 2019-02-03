import random

import datetime
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from login.models import User

def fake_users():
    User.objects.all().delete()
    for i in range(0, 20):
        dic = {}
        dic['name'] = 'user_{}'.format(i)
        dic['password'] = '1'
        dic['email'] = 'fake@nonexist.com'
        dic['sex'] = 'm'

        if i < 10:
            dic['driver'] = True
            dic['vehicleMake'] = 'vM_{}'.format(i)
            dic['vehiclePlate'] = 0
            dic['vehicleCapacity'] = random.randint(2,20)
        else:
            dic['driver'] = False
        u = User.objects.create(**dic)


class Command(BaseCommand):
    help = 'testcases: creat 20 users with pwd 1'

    def handle(self, *args, **options):
        fake_users()
        self.stdout.write(self.style.SUCCESS('fake user created'))