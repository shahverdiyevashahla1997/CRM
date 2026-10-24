from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse

from services.models import Service
from campaigns.models import Campaign
from leads.models import Lead


class LeadTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="lead_tester",
            password="TestPassword123!",
        )
        cls.service = Service.objects.create(
            name="Тестовая услуга",
            description="Для автоматических тестов",
            price="100.00",
        )
        cls.campaign = Campaign.objects.create(
            name="Тестовая кампания",
            service=cls.service,
            channel="social",
            budget="500.00",
        )
        cls.user.user_permissions.add(
            Permission.objects.get(
                content_type__app_label="leads",
                codename="view_lead",
            ),
            Permission.objects.get(
                content_type__app_label="leads",
                codename="add_lead",
            ),
        )

    def test_lead_string_representation(self):
        lead = Lead.objects.create(
            full_name="Тестовый Клиент",
            phone="+994501234567",
            email="lead@example.com",
            campaign=self.campaign,
        )
        self.assertEqual(str(lead), "Тестовый Клиент")

    def test_lead_creation_page_requires_login(self):
        response = self.client.get(reverse("leads:create"))
        self.assertEqual(response.status_code, 302)

    def test_authorized_user_can_open_lead_creation_page(self):
        self.client.login(username="lead_tester", password="TestPassword123!")
        response = self.client.get(reverse("leads:create"))
        self.assertEqual(response.status_code, 200)

    def test_lead_is_not_active_client_before_conversion(self):
        lead = Lead.objects.create(
            full_name="Потенциальный Клиент",
            phone="+994501234567",
            email="potential@example.com",
            campaign=self.campaign,
        )
        self.assertFalse(lead.is_active_client)
