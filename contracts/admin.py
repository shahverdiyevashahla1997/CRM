from django.contrib import admin
from .models import Contract

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'signed_date', 'amount', 'lead')
    list_filter = ('service', 'signed_date')
    search_fields = ('name', 'lead__full_name')
