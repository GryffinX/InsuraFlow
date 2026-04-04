from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):

    ROLES = [
        ('customer','Customer'),
        ('agent','Agent'),
        ('surveyor','Surveyor'),
        ('provider','Provider'),
        ('admin','Admin'),
    ]

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    dob = models.DateField(null=True,blank=True)
    role = models.CharField(max_length=20, choices=ROLES, default='customer')
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
    ]

    def save(self, *args, **kwargs):
        if self.role == 'admin':
            self.is_verified = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
