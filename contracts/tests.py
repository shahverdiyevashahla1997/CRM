from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse

from services.models import Service
from contracts.models import Contract


class ContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="contract_tester",
            password="TestPassword123!",
        )
        cls.user.user_permissions.add(
            Permission.objects.get(
                content_type__app_label="contracts",
                codename="view_contract",
            ),
            Permission.objects.get(
                content_type__app_label="contracts",
                codename="add_contract",
            ),
        )
        cls.service = Service.objects.create(
            name="Тестовая услуга",
            price="100.00",
        )

    def test_contract_string_representation(self):
        contract = Contract.objects.create(
            name="Тестовый контракт",
            service=self.service,
            signed_date="2026-10-20",
            start_date="2026-10-20",
            end_date="2027-10-20",
            amount="1200.00",
        )
        self.assertEqual(str(contract), "Тестовый контракт")

    def test_contract_creation_page_requires_login(self):
        response = self.client.get(reverse("contracts:create"))
        self.assertEqual(response.status_code, 302)

    def test_authorized_user_can_open_contract_creation_page(self):
        self.client.login(
            username="contract_tester",
            password="TestPassword123!",
        )
        response = self.client.get(reverse("contracts:create"))
        self.assertEqual(response.status_code, 200)
