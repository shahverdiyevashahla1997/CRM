from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Lead
from .forms import LeadForm

class LeadListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Lead
    template_name = "leads/list.html"
    context_object_name = "objects"
    permission_required = "leads.view_lead"
    extra_context = {"page_title": "Потенциальные клиенты", "create_url": "leads:create"}

class LeadDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Lead
    template_name = "common/detail.html"
    permission_required = "leads.view_lead"
    extra_context = {"page_title": "Потенциальный клиент", "edit_url": "leads:edit", "delete_url": "leads:delete"}

class LeadCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Lead
    form_class = LeadForm
    template_name = "common/form.html"
    permission_required = "leads.add_lead"
    success_url = reverse_lazy("leads:list")
    extra_context = {"page_title": "Добавить потенциального клиента"}

class LeadUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Lead
    form_class = LeadForm
    template_name = "common/form.html"
    permission_required = "leads.change_lead"
    success_url = reverse_lazy("leads:list")
    extra_context = {"page_title": "Редактировать потенциального клиента"}

class LeadDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Lead
    template_name = "common/confirm_delete.html"
    permission_required = "leads.delete_lead"
    success_url = reverse_lazy("leads:list")
