from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.


class User(models.Model):

    gender = (
        ('m', 'male'),
        ('f', 'female'),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128, unique=False)
    email = models.EmailField(unique=False)
    sex = models.CharField(max_length=32, choices=gender)
    vehicleMake = models.CharField(max_length=128, unique=False, default='')
    vehiclePlate = models.CharField(max_length=128, unique=False, default='')
    vehicleCapacity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(2)])
    driver = models.BooleanField(default=False)

