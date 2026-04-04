from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, UserDetailView, UserViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/me/", UserDetailView.as_view()),
    path("", include(router.urls)),
]
