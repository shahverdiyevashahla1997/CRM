from django.contrib import admin
from .models import Campaign

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'channel', 'budget', 'is_active')
    list_filter = ('channel', 'is_active')
    search_fields = ('name',)
