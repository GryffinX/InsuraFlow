from django.db import models
from django.conf import settings
from insurance.models import Policy, ServiceProvider, Surveyor

# Create your models here.

User = settings.AUTH_USER_MODEL

class Claim(models.Model):
    STATUS_CHOICES = [
        ('filed','Filed'),
        ('under_review','Under Review'),
        ('approved','Approved'),
        ('rejected','Rejected'),
        ("settled", "Settled"),
    ]

    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='claims')
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='claims')
    claim_date = models.DateField(auto_now_add=True)
    claim_amount = models.DecimalField(max_digits=12, decimal_places=2)
    claim_reason = models.TextField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='filed')

    def _str__(self):
        return f"Claim: {self.id} - Policy Number: {self.policy.policy_number}"
    
class InspectionReport(models.Model):
    DAMAGE_LEVELS = [
        ('low','Low'),
        ('medium','Medium'),
        ('high','High'),
    ]

    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='inspection')
    surveyor = models.ForeignKey(Surveyor, on_delete=models.SET_NULL, null=True, related_name='insprection')
    inspection_date = models.DateField(auto_now_add=True)
    damage_level = models.CharField(max_length=15, choices=DAMAGE_LEVELS)
    estimated_loss = models.DecimalField(max_digits=12, decimal_places=2)
    remarks = models.TextField()

    def __str__(self):
        return f"Inspection for Claim: {self.claim.id}"
    

class Settlement(models.Model):

    PAYMENT_MODES = [
        ('bank','Bank'),
        ('upi','UPI'),
        ('cheque','Cheque'),
    ]

    PAYMENT_STATUS = [
        ('pending','Pending'),
        ('paid','Paid'),
    ]

    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='settlement')
    approved_amount = models.DecimalField(max_digits=12, decimal_places=2)
    settlement_date = models.DateField(auto_now_add=True)
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODES)
    payment_status = models.CharField(max_length=15, choices=PAYMENT_STATUS, default='pending')

    def __str__(self):
        return f"Settlement for Claim: {self.claim.id} - Amount: {self.approved_amount}"

    

