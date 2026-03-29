from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Insurer, Agent, Policy

User = get_user_model()

class PolicyTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username="admin", email="admin@test.com", password="Pass123!", role="admin"
        )
        self.customer = User.objects.create_user(
            username="customer", email="cust@test.com", password="Pass123!", role="customer"
        )
        self.insurer = Insurer.objects.create(
            company_name="InsureCo", registration_no="REG123", contact_email="co@test.com"
        )
        self.agent = Agent.objects.create(
            name="Agent Smith", license_no="LIC123", phone_no="123", 
            email="agent@test.com", region="South", insurer=self.insurer
        )
        self.policy = Policy.objects.create(
            policy_number="POL123", policy_holder=self.customer, 
            insurer=self.insurer, agent=self.agent, policy_type="health",
            coverage_amount=10000, premium_amount=500, end_date="2030-01-01",
            status="active"
        )

    def test_cancel_policy_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = f"/api/policies/{self.policy.id}/cancel/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.policy.refresh_from_db()
        self.assertEqual(self.policy.status, "cancelled")

    def test_activate_policy_forbidden_customer(self):
        self.policy.status = "cancelled"
        self.policy.save()
        
        self.client.force_authenticate(user=self.customer)
        url = f"/api/policies/{self.policy.id}/activate/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_policy_amount_validation(self):
        self.client.force_authenticate(user=self.admin)
        url = "/api/policies/"
        data = {
            "policy_number": "POL_INVALID",
            "policy_holder": self.customer.id,
            "insurer": self.insurer.id,
            "agent": self.agent.id,
            "policy_type": "health",
            "coverage_amount": -100, # Invalid
            "premium_amount": 50,
            "end_date": "2030-01-01"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("coverage_amount", response.data["details"])
