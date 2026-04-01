from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, UserDetailView, VerifyOTPView, ResendOTPView,
    PasswordResetRequestView, PasswordResetConfirmView, UserViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/me/", UserDetailView.as_view()),
    path("auth/verify-otp/", VerifyOTPView.as_view()),
    path("auth/resend-otp/", ResendOTPView.as_view()),
    path("auth/password-reset/", PasswordResetRequestView.as_view()),
    path("auth/password-reset-confirm/", PasswordResetConfirmView.as_view()),
    path("", include(router.urls)),
]