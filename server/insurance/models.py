from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_profile', null=True, blank=True)
    company_name = models.CharField(max_length=50)
    registration_no = models.CharField(max_length=100, unique=True)
    contact_email = models.EmailField(unique=True)
    head_office_address = models.TextField()

    def __str__(self):
        return self.company_name

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent_profile', null=True, blank=True)
    name = models.CharField(max_length=50)
    license_no = models.CharField(max_length=100, unique=True)
    phone_no = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    region = models.CharField(max_length=30)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name="agents", null=True, blank=True)

    def __str__(self):
        return self.name

class Surveyor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='surveyor_profile', null=True, blank=True)
    name = models.CharField(max_length=50)
    license_no = models.CharField(max_length=100, unique=True)
    region = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Policy(models.Model):
    POLICY_TYPES = [
        ('health', 'Health'),
        ('motor', 'Motor'),
        ('life', 'Life'),
        ('travel', 'Travel'),
    ]

    title = models.CharField(max_length=100, default="New Policy")
    description = models.TextField(blank=True, default="")
    policy_type = models.CharField(max_length=10, choices=POLICY_TYPES)
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='policies', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class UserPolicy(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_policies', null=True, blank=True)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='instances', null=True, blank=True)
    policy_number = models.CharField(max_length=100, unique=True)
    
    purchase_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')

    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_policies')

    def __str__(self):
        return f"{self.user.email if self.user else 'No User'} - {self.policy_number}"

# Keeping ServiceProvider as it might be used by Claims
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
