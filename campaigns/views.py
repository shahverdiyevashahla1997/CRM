from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count, Sum, Q, DecimalField, ExpressionWrapper, F
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Campaign
from .forms import CampaignForm

class CampaignListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Campaign
    template_name = "common/list.html"
    context_object_name = "objects"
    permission_required = "campaigns.view_campaign"
    extra_context = {"page_title": "Рекламные кампании", "create_url": "campaigns:create", "detail_url": "campaigns:detail"}

class CampaignDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Campaign
    template_name = "common/detail.html"
    permission_required = "campaigns.view_campaign"
    extra_context = {"page_title": "Рекламная кампания", "edit_url": "campaigns:edit", "delete_url": "campaigns:delete"}

class CampaignCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = "common/form.html"
    permission_required = "campaigns.add_campaign"
    success_url = reverse_lazy("campaigns:list")
    extra_context = {"page_title": "Создать кампанию"}

class CampaignUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Campaign
    form_class = CampaignForm
    template_name = "common/form.html"
    permission_required = "campaigns.change_campaign"
    success_url = reverse_lazy("campaigns:list")
    extra_context = {"page_title": "Редактировать кампанию"}

class CampaignDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Campaign
    template_name = "common/confirm_delete.html"
    permission_required = "campaigns.delete_campaign"
    success_url = reverse_lazy("campaigns:list")

class CampaignStatsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Campaign
    template_name = "campaigns/stats.html"
    context_object_name = "campaigns"
    permission_required = "campaigns.view_campaign"

    def get_queryset(self):
        return Campaign.objects.select_related("service").annotate(
            lead_count=Count("leads", distinct=True),
            active_count=Count("leads__active_client", distinct=True),
            contract_income=Sum("leads__active_client__contract__amount"),
        ).order_by("name")
