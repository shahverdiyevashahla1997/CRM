from django.contrib import admin
from .models import ActiveClient

@admin.register(ActiveClient)
class ActiveClientAdmin(admin.ModelAdmin):
    list_display = ('lead', 'contract', 'activated_at')
    search_fields = ('lead__full_name', 'contract__name')
