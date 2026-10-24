from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", TemplateView.as_view(template_name="dashboard.html"), name="dashboard"),
    path("services/", include("services.urls")),
    path("campaigns/", include("campaigns.urls")),
    path("leads/", include("leads.urls")),
    path("contracts/", include("contracts.urls")),
    path("active-clients/", include("active_clients.urls")),
]
