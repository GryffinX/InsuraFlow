from django.urls import path
from .views import RegisterView, UserDetailView, VerifyOTPView, ResendOTPView

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/me/", UserDetailView.as_view()),
    path("auth/verify-otp/", VerifyOTPView.as_view()),
    path("auth/resend-otp/", ResendOTPView.as_view()),
]