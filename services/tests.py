from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db import IntegrityError, transaction
from django.urls import reverse

from services.models import Service


class ServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="service_tester",
            password="TestPassword123!",
        )
        cls.user.user_permissions.add(
            Permission.objects.get(
                content_type__app_label="services",
                codename="view_service",
            ),
            Permission.objects.get(
                content_type__app_label="services",
                codename="add_service",
            ),
        )

    def test_service_string_representation(self):
        service = Service.objects.create(
            name="Консультация",
            description="Тестовая услуга",
            price="150.00",
        )
        self.assertEqual(str(service), "Консультация")

    def test_service_creation_page_requires_login(self):
        response = self.client.get(reverse("services:create"))
        self.assertEqual(response.status_code, 302)

    def test_authorized_user_can_open_service_creation_page(self):
        self.client.login(
            username="service_tester",
            password="TestPassword123!",
        )
        response = self.client.get(reverse("services:create"))
        self.assertEqual(response.status_code, 200)

    def test_service_name_must_be_unique(self):
        Service.objects.create(
            name="Консультация",
            price="150.00",
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Service.objects.create(
                    name="Консультация",
                    price="200.00",
                )
