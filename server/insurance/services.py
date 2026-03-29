from django.core.exceptions import ValidationError
from .models import Policy

def activate_policy(policy: Policy) -> Policy:
    if policy.status == "active":
        raise ValidationError({"error": "Policy is already active"})
    
    policy.status = "active"
    policy.save()
    return policy

def cancel_policy(policy: Policy) -> Policy:
    if policy.status == "cancelled":
        raise ValidationError({"error": "Policy is already cancelled"})
    
    policy.status = "cancelled"
    policy.save()
    return policy
