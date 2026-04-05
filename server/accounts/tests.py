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

    def test_admin_registration_success_with_secret_key(self):
        data = {
            "username": "adminuser",
            "email": "admin@example.com",
            "password": "Password123!",
            "role": "admin",
            "secret_key": "admin-secret-2026",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="admin@example.com")
        self.assertEqual(user.role, "admin")
        self.assertTrue(user.is_verified)

    def test_admin_registration_rejects_invalid_secret_key(self):
        data = {
            "username": "badadmin",
            "email": "badadmin@example.com",
            "password": "Password123!",
            "role": "admin",
            "secret_key": "wrong-secret",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("details", response.data)
        self.assertIn("secret_key", response.data["details"])

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
