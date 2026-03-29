from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Claim

def submit_claim(claim: Claim) -> Claim:
    if claim.status != "filed":
        raise ValidationError({"error": "Only new claims can be submitted"})
    
    claim.status = "under_review"
    claim.save()
    return claim

def approve_claim(claim: Claim) -> Claim:
    if claim.status != "under_review":
        raise ValidationError({"error": "Claim must be under review to be approved"})
    
    claim.status = "approved"
    claim.save()
    return claim

def reject_claim(claim: Claim) -> Claim:
    if claim.status != "under_review":
        raise ValidationError({"error": "Claim must be under review to be rejected"})
    
    claim.status = "rejected"
    claim.save()
    return claim

def settle_claim(claim: Claim) -> Claim:
    if claim.status != "approved":
        raise ValidationError({"error": "Claim must be approved to be settled"})

    claim.status = "settled"
    claim.save()
    return claim
