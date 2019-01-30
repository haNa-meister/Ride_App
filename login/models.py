from django.db import models

# Create your models here.


class User(models.Model):

    gender = (
        ('m', 'male'),
        ('f', 'female'),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128, unique=False)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender)
