from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):

    ROLES = [
        ('customer','Customer'),
        ('agent','Agent'),
        ('surveyor','Surveyor'),
        ('admin','Admin'),
    ]

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    dob = models.DateField(null=True,blank=True)
    role = models.CharField(max_length=20, choices=ROLES, default='customer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
    ]

    def __str__(self):
        return self.email
    