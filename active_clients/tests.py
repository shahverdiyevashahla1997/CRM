from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse

from services.models import Service
from campaigns.models import Campaign
from leads.models import Lead
from contracts.models import Contract
from active_clients.models import ActiveClient


class ActiveClientTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="active_client_tester",
            password="TestPassword123!",
        )
        cls.user.user_permissions.add(
            Permission.objects.get(
                content_type__app_label="active_clients",
                codename="view_activeclient",
            ),
            Permission.objects.get(
                content_type__app_label="active_clients",
                codename="add_activeclient",
            ),
        )

        cls.service = Service.objects.create(
            name="Тестовая услуга",
            price="100.00",
        )
        cls.campaign = Campaign.objects.create(
            name="Тестовая кампания",
            service=cls.service,
            channel="social",
            budget="500.00",
        )
        cls.lead = Lead.objects.create(
            full_name="Тестовый Клиент",
            phone="+994501234567",
            email="client@example.com",
            campaign=cls.campaign,
        )
        cls.contract = Contract.objects.create(
            name="Тестовый контракт",
            service=cls.service,
            signed_date="2026-10-20",
            start_date="2026-10-20",
            end_date="2027-10-20",
            amount="1200.00",
            lead=cls.lead,
        )

    def test_active_client_string_representation(self):
        client = ActiveClient.objects.create(
            lead=self.lead,
            contract=self.contract,
        )
        self.assertEqual(str(client), "Тестовый Клиент")

    def test_active_client_creation_page_requires_login(self):
        response = self.client.get(reverse("active_clients:create"))
        self.assertEqual(response.status_code, 302)

    def test_authorized_user_can_open_active_client_creation_page(self):
        self.client.login(
            username="active_client_tester",
            password="TestPassword123!",
        )
        response = self.client.get(reverse("active_clients:create"))
        self.assertEqual(response.status_code, 200)

    def test_lead_is_marked_as_active_client_after_activation(self):
        self.assertFalse(self.lead.is_active_client)

        ActiveClient.objects.create(
            lead=self.lead,
            contract=self.contract,
        )

        self.assertTrue(self.lead.is_active_client)
