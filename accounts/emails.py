import jwt
from django.core.mail import send_mail
from django.conf import settings
from .models import *

def send_otp_via_email(email, otp):
    subject = "One-Time Password (OTP) for Authentication"
    message = f"Your OTP is: {otp}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    user_obj = User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()




def send_password_reset_email(email):
    user = User.objects.get(email=email)
    token = jwt.encode({'email': email}, settings.SECRET_KEY, algorithm='HS256')
    
    subject = "Password Reset Request"
    message = f"Click the link to reset your password: http://127.0.0.1:8000/reset-password?token={token}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)