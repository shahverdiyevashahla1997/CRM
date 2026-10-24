from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, FormView
from contracts.models import Contract
from contracts.forms import ContractForm
from leads.models import Lead
from .models import ActiveClient
from .forms import ActiveClientCreateForm

class ActiveClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ActiveClient
    template_name = "active_clients/list.html"
    context_object_name = "objects"
    permission_required = "active_clients.view_activeclient"
    extra_context = {"page_title": "Активные клиенты"}

class ActiveClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = ActiveClient
    template_name = "active_clients/detail.html"
    permission_required = "active_clients.view_activeclient"
    extra_context = {"page_title": "Активный клиент"}

class ActiveClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "common/form.html"
    form_class = ActiveClientCreateForm
    permission_required = "active_clients.add_activeclient"
    success_url = reverse_lazy("active_clients:list")
    extra_context = {"page_title": "Перевести в активные"}

    def get_initial(self):
        initial = super().get_initial()
        lead_id = self.request.GET.get("lead")
        if lead_id and Lead.objects.filter(pk=lead_id).exclude(active_client__isnull=False).exists():
            initial["lead"] = lead_id
        return initial

    @transaction.atomic
    def form_valid(self, form):
        lead = form.cleaned_data["lead"]
        if ActiveClient.objects.filter(lead=lead).exists():
            form.add_error("lead", "Этот клиент уже активирован.")
            return self.form_invalid(form)
        contract = Contract.objects.create(
            name=form.cleaned_data["contract_name"],
            service=form.cleaned_data["service"],
            document=form.cleaned_data.get("document"),
            signed_date=form.cleaned_data["signed_date"],
            start_date=form.cleaned_data["start_date"],
            end_date=form.cleaned_data["end_date"],
            amount=form.cleaned_data["amount"],
            lead=lead,
        )
        ActiveClient.objects.create(lead=lead, contract=contract)
        messages.success(self.request, "Клиент переведён в активные, контракт создан.")
        return super().form_valid(form)

class ActiveClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ActiveClient
    form_class = None
    template_name = "active_clients/edit.html"
    permission_required = "active_clients.change_activeclient"
    success_url = reverse_lazy("active_clients:list")

    def get_form_class(self):
        from django import forms
        class ActiveClientEditForm(forms.ModelForm):
            class Meta:
                model = ActiveClient
                fields = []
        return ActiveClientEditForm

class ActiveClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ActiveClient
    template_name = "common/confirm_delete.html"
    permission_required = "active_clients.delete_activeclient"
    success_url = reverse_lazy("active_clients:list")
