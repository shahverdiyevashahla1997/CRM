from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Service
from .forms import ServiceForm

class ServiceListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Service
    template_name = "common/list.html"
    context_object_name = "objects"
    permission_required = "services.view_service"
    extra_context = {"page_title": "Услуги", "create_url": "services:create", "detail_url": "services:detail"}

class ServiceDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Service
    template_name = "common/detail.html"
    permission_required = "services.view_service"
    extra_context = {"page_title": "Услуга", "edit_url": "services:edit", "delete_url": "services:delete"}

class ServiceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = "common/form.html"
    permission_required = "services.add_service"
    success_url = reverse_lazy("services:list")
    extra_context = {"page_title": "Создать услугу"}

class ServiceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = "common/form.html"
    permission_required = "services.change_service"
    success_url = reverse_lazy("services:list")
    extra_context = {"page_title": "Редактировать услугу"}

class ServiceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Service
    template_name = "common/confirm_delete.html"
    permission_required = "services.delete_service"
    success_url = reverse_lazy("services:list")
