from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse

from services.models import Service
from campaigns.models import Campaign


class CampaignTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="campaign_tester",
            password="TestPassword123!",
        )
        cls.user.user_permissions.add(
            Permission.objects.get(
                content_type__app_label="campaigns",
                codename="view_campaign",
            ),
            Permission.objects.get(
                content_type__app_label="campaigns",
                codename="add_campaign",
            ),
        )
        cls.service = Service.objects.create(
            name="Тестовая услуга",
            price="100.00",
        )

    def test_campaign_string_representation(self):
        campaign = Campaign.objects.create(
            name="Тестовая кампания",
            service=self.service,
            channel="social",
            budget="500.00",
        )
        self.assertEqual(str(campaign), "Тестовая кампания")

    def test_campaign_creation_page_requires_login(self):
        response = self.client.get(reverse("campaigns:create"))
        self.assertEqual(response.status_code, 302)

    def test_authorized_user_can_open_campaign_creation_page(self):
        self.client.login(
            username="campaign_tester",
            password="TestPassword123!",
        )
        response = self.client.get(reverse("campaigns:create"))
        self.assertEqual(response.status_code, 200)
