from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from insurance.models import Policy, Provider, UserPolicy

User = get_user_model()


class PolicyApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="Pass123!",
            role="admin",
        )

        self.provider_user = User.objects.create_user(
            username="provider-one",
            email="provider-one@example.com",
            password="Pass123!",
            role="provider",
            is_verified=True,
        )
        self.provider = Provider.objects.create(
            user=self.provider_user,
            company_name="Provider One",
            registration_no="REG-001",
            contact_email="provider-one@company.com",
            head_office_address="Mumbai",
        )

        self.other_provider_user = User.objects.create_user(
            username="provider-two",
            email="provider-two@example.com",
            password="Pass123!",
            role="provider",
            is_verified=True,
        )
        self.other_provider = Provider.objects.create(
            user=self.other_provider_user,
            company_name="Provider Two",
            registration_no="REG-002",
            contact_email="provider-two@company.com",
            head_office_address="Delhi",
        )

        self.agent = User.objects.create_user(
            username="agent",
            email="agent@example.com",
            password="Pass123!",
            role="agent",
            is_verified=True,
        )

        self.customer = User.objects.create_user(
            username="customer",
            email="customer@example.com",
            password="Pass123!",
            role="customer",
            is_verified=True,
        )

        self.policy = Policy.objects.create(
            title="Family Health Shield",
            description="Base coverage",
            policy_type="health",
            coverage_amount="50000.00",
            premium_amount="1200.00",
            provider=self.provider,
            is_active=True,
        )

    def test_provider_can_create_policy(self):
        self.client.force_authenticate(user=self.provider_user)

        response = self.client.post(
            "/api/policies/",
            {
                "title": "Motor Secure Plus",
                "description": "Comprehensive motor cover",
                "policy_type": "motor",
                "coverage_amount": "90000",
                "premium_amount": "1800",
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_policy = Policy.objects.get(title="Motor Secure Plus")
        self.assertEqual(created_policy.provider, self.provider)

    def test_admin_can_create_policy(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            "/api/policies/",
            {
                "title": "Admin Created Policy",
                "description": "Platform managed plan",
                "policy_type": "life",
                "coverage_amount": "100000",
                "premium_amount": "2200",
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Policy.objects.filter(title="Admin Created Policy").exists())

    def test_agent_cannot_create_policy(self):
        self.client.force_authenticate(user=self.agent)

        response = self.client.post(
            "/api/policies/",
            {
                "title": "Agent Policy",
                "description": "Should be blocked",
                "policy_type": "travel",
                "coverage_amount": "15000",
                "premium_amount": "400",
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_provider_can_update_owned_policy(self):
        self.client.force_authenticate(user=self.provider_user)

        response = self.client.patch(
            f"/api/policies/{self.policy.id}/",
            {"title": "Updated Family Health Shield"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.policy.refresh_from_db()
        self.assertEqual(self.policy.title, "Updated Family Health Shield")

    def test_provider_cannot_update_other_provider_policy(self):
        foreign_policy = Policy.objects.create(
            title="Other Provider Policy",
            description="Should stay unchanged",
            policy_type="health",
            coverage_amount="75000.00",
            premium_amount="900.00",
            provider=self.other_provider,
            is_active=True,
        )

        self.client.force_authenticate(user=self.provider_user)
        response = self.client.patch(
            f"/api/policies/{foreign_policy.id}/",
            {"title": "Blocked Update"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        foreign_policy.refresh_from_db()
        self.assertEqual(foreign_policy.title, "Other Provider Policy")

    def test_delete_policy_removes_user_policy_records(self):
        owned_policy = UserPolicy.objects.create(
            user=self.customer,
            policy=self.policy,
            policy_number="UP-100001",
            start_date="2026-01-01",
            end_date="2027-01-01",
            status="active",
        )

        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f"/api/policies/{self.policy.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Policy.objects.filter(id=self.policy.id).exists())
        self.assertFalse(UserPolicy.objects.filter(id=owned_policy.id).exists())
