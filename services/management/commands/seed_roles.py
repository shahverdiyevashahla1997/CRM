from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from services.models import Service
from campaigns.models import Campaign
from leads.models import Lead
from contracts.models import Contract
from active_clients.models import ActiveClient

ROLE_PERMISSIONS = {
    "Оператор": [(Lead, ["view", "add", "change"]), (Campaign, ["view"])],
    "Маркетолог": [(Service, ["view", "add", "change"]), (Campaign, ["view", "add", "change"])],
    "Менеджер": [
        (Lead, ["view"]),
        (Campaign, ["view"]),
        (Contract, ["view", "add", "change"]),
        (ActiveClient, ["view", "add", "change"]),
    ],
    "Просмотр статистики": [(Campaign, ["view"])],
}

class Command(BaseCommand):
    help = "Создаёт стандартные группы CRM и назначает им разрешения."

    def handle(self, *args, **options):
        for group_name, model_rules in ROLE_PERMISSIONS.items():
            group, _ = Group.objects.get_or_create(name=group_name)
            permissions = []
            for model, actions in model_rules:
                content_type = ContentType.objects.get_for_model(model)
                for action in actions:
                    codename = f"{action}_{model._meta.model_name}"
                    permissions.append(Permission.objects.get(content_type=content_type, codename=codename))
            if group_name == "Просмотр статистики":
                permissions.append(Permission.objects.get(content_type=ContentType.objects.get_for_model(Campaign), codename="view_campaign"))
            group.permissions.set(permissions)
            self.stdout.write(self.style.SUCCESS(f"Группа «{group_name}» настроена."))
