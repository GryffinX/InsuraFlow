from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = "/api/auth/register/"
        self.login_url = "/api/auth/login/"

    def test_registration_success(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Password123!",
            "role": "customer"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get()
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.role, "customer")

    def test_registration_weak_password(self):
        data = {
            "username": "testuser2",
            "email": "test2@example.com",
            "password": "123",
            "role": "customer"
        }
        response = self.client.post(self.register_url, data)
        # Custom exception handler should return 400 with details
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Validation Error")

    def test_login_success(self):
        User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="Password123!"
        )
        data = {
            "email": "test@example.com",
            "password": "Password123!"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
