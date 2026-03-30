from django.urls import path
from .views import RegisterView, UserDetailView

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/me/", UserDetailView.as_view()),
]