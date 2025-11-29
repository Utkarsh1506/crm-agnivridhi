from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'invoice_type', 'client', 'total_amount', 'issue_date', 'created_by']
    list_filter = ['invoice_type', 'issue_date', 'created_at']
    search_fields = ['invoice_number', 'client__company_name', 'item_description']
    readonly_fields = ['invoice_number', 'taxable_amount', 'cgst_amount', 'sgst_amount', 'igst_amount', 'total_amount', 'created_at', 'updated_at']
