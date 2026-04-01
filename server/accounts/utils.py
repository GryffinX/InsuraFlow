import random
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailOTP

def send_otp_email(user):
    otp_code = str(random.randint(100000, 999999))
    
    # Deactivate any existing OTPs for this user
    EmailOTP.objects.filter(user=user, is_active=True).update(is_active=False)
    
    # Create new OTP
    EmailOTP.objects.create(user=user, otp=otp_code)
    
    subject = 'Your InsuraFlow Verification Code'
    message = f'Your verification code is: {otp_code}. It will expire soon.'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    
    try:
        send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    except Exception as e:
        print(f"ERROR: Failed to send OTP email: {e}")
        # In development, we can still proceed as the OTP is saved in the database
    
    return otp_code
