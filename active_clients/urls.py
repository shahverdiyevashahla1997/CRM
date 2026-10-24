from django.urls import path
from . import views
app_name = "active_clients"
urlpatterns = [
    path("", views.ActiveClientListView.as_view(), name="list"),
    path("create/", views.ActiveClientCreateView.as_view(), name="create"),
    path("<int:pk>/", views.ActiveClientDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.ActiveClientUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.ActiveClientDeleteView.as_view(), name="delete"),
]
