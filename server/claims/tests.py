from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from insurance.models import Insurer, Agent, Policy, ServiceProvider
from .models import Claim, Settlement
from . import services

User = get_user_model()

class ClaimTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = User.objects.create_user(
            username="customer", email="cust@test.com", password="Pass123!", role="customer"
        )
        self.admin = User.objects.create_user(
            username="admin", email="admin@test.com", password="Pass123!", role="admin"
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
            coverage_amount=10000, premium_amount=500, end_date="2030-01-01"
        )
        self.provider = ServiceProvider.objects.create(
            name="Hosp1", provider_type="hospital", licence_no="L1", 
            address="Addr", city="City", contact_no="999"
        )
        self.claim = Claim.objects.create(
            policy=self.policy, service_provider=self.provider, 
            claim_amount=5000, claim_reason="Medical", status="filed"
        )

    def test_submit_claim_service(self):
        services.submit_claim(self.claim)
        self.assertEqual(self.claim.status, "under_review")

    def test_approve_claim_admin(self):
        self.claim.status = "under_review"
        self.claim.save()
        
        self.client.force_authenticate(user=self.admin)
        url = f"/api/claims/{self.claim.id}/approve/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.claim.refresh_from_db()
        self.assertEqual(self.claim.status, "approved")

    def test_approve_claim_customer_forbidden(self):
        self.claim.status = "under_review"
        self.claim.save()
        
        self.client.force_authenticate(user=self.customer)
        url = f"/api/claims/{self.claim.id}/approve/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_settlement_validation(self):
        self.client.force_authenticate(user=self.admin)
        url = "/api/settlements/"
        data = {
            "claim_id": self.claim.id,
            "approved_amount": 6000, # More than claim amount (5000)
            "payment_mode": "bank"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("approved_amount", response.data["details"])
