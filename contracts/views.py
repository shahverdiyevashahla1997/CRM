from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Contract
from .forms import ContractForm

class ContractListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Contract
    template_name = "common/list.html"
    context_object_name = "objects"
    permission_required = "contracts.view_contract"
    extra_context = {"page_title": "Контракты", "create_url": "contracts:create", "detail_url": "contracts:detail"}

class ContractDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Contract
    template_name = "common/detail.html"
    permission_required = "contracts.view_contract"
    extra_context = {"page_title": "Контракт", "edit_url": "contracts:edit", "delete_url": "contracts:delete"}

class ContractCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Contract
    form_class = ContractForm
    template_name = "common/form.html"
    permission_required = "contracts.add_contract"
    success_url = reverse_lazy("contracts:list")
    extra_context = {"page_title": "Создать контракт"}

class ContractUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = "common/form.html"
    permission_required = "contracts.change_contract"
    success_url = reverse_lazy("contracts:list")
    extra_context = {"page_title": "Редактировать контракт"}

class ContractDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Contract
    template_name = "common/confirm_delete.html"
    permission_required = "contracts.delete_contract"
    success_url = reverse_lazy("contracts:list")
