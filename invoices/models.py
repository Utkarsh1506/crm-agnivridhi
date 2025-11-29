from django.db import models
from django.conf import settings
from clients.models import Client
from decimal import Decimal


class Invoice(models.Model):
    """Simple Invoice/Proforma model"""
    
    INVOICE_TYPE_CHOICES = [
        ('proforma', 'Proforma Invoice'),
        ('tax', 'Tax Invoice'),
    ]
    
    # Basic Info
    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_type = models.CharField(max_length=20, choices=INVOICE_TYPE_CHOICES, default='proforma')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='invoices', null=True, blank=True)
    client_name = models.CharField(max_length=255, blank=True, help_text="Manual client name for Proforma")
    
    # Manual Client Details (for Proforma)
    client_contact_person = models.CharField(max_length=255, blank=True, help_text="Contact person name")
    client_address = models.TextField(blank=True, help_text="Full address")
    client_city = models.CharField(max_length=100, blank=True)
    client_state = models.CharField(max_length=100, blank=True)
    client_pincode = models.CharField(max_length=10, blank=True)
    client_gstin = models.CharField(max_length=15, blank=True, help_text="GSTIN (optional)")
    client_mobile = models.CharField(max_length=15, blank=True, help_text="Mobile/Phone")
    
    # Dates
    issue_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    
    # Item Details
    item_description = models.CharField(max_length=500)
    hsn_sac = models.CharField(max_length=20, blank=True, default='998314')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1.00'))
    rate = models.DecimalField(max_digits=10, decimal_places=2, help_text="Rate per unit")
    
    # GST
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('18.00'), help_text="GST % rate")
    taxable_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Tax breakdown (auto-calculated: either CGST+SGST or IGST)
    cgst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    sgst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    igst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Place of supply for tax calculation
    place_of_supply = models.CharField(max_length=100, default='Maharashtra')
    
    # Notes
    notes = models.TextField(blank=True, null=True)
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        client_display = self.client.company_name if self.client else (self.client_name or "No Client")
        return f"{self.invoice_number} - {client_display}"
