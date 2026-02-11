from django.db import models
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL

class Insurer(models.Model):
    company_name = models.CharField(max_length=50)
    registration_no = models.CharField(max_length=100, unique=True)
    contact_email = models.EmailField(unique=True)
    head_office_address = models.TextField()

    def __str__(self):
        return self.company_name

class Agent(models.Model):
    name = models.CharField(max_length=50)
    license_no = models.CharField(max_length=100, unique=True)
    phone_no = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    region = models.CharField(max_length=30)

    insurer = models.ForeignKey(Insurer, on_delete=models.CASCADE, related_name="agent")

    def __str__(self):
        return self.name
    
class ServiceProvider(models.Model):
    PROVIDER_TYPES = [
        ('hospital','Hospital'),
        ('garage','Garage'),
    ]

    name = models.CharField(max_length=50)
    provider_type = models.CharField(max_length=20, choices=PROVIDER_TYPES)
    licence_no = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=30)
    contact_no = models.CharField(max_length=15)

    def __str__(self):
        return self.name
    
class Surveyor(models.Model):
    name = models.CharField(max_length=50)
    license_no = models.CharField(max_length=100, unique=True)
    region = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
    
class Policy(models.Model):
    POLICY_TYPES = [
        ('health','Health'),
        ('motor','Motor'),
    ]

    STATUS_CHOICES = [
        ('active','Active'),
        ('expired','Expired'),
        ('cancelled','Cancelled'),
    ]

    policy_number = models.CharField(max_length=100, unique=True)
    policy_holder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='policies')
    insurer = models.ForeignKey(Insurer, on_delete=models.CASCADE, related_name='policies')
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='policies')

    policy_type = models.CharField(max_length=10, choices=POLICY_TYPES)
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)

    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.policy_number
    


