# Generated by Django 2.1.5 on 2019-02-04 20:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254)),
                ('sex', models.CharField(choices=[('m', 'male'), ('f', 'female')], max_length=32)),
                ('vehicleMake', models.CharField(default='', max_length=128)),
                ('vehiclePlate', models.CharField(default='', max_length=128)),
                ('vehicleCapacity', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(2)])),
                ('driver', models.BooleanField(default=False)),
            ],
        ),
    ]
