from django.db import models
from django.conf import settings
from clients.models import Client  # adjust if your app name different

class Invoice(models.Model):
    INVOICE_TYPE_CHOICES = [
        ('proforma', 'Proforma Invoice'),
        ('tax', 'Tax Invoice'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('final', 'Final'),
    ]

    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_type = models.CharField(
        max_length=20,
        choices=INVOICE_TYPE_CHOICES,
        default='proforma'
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='invoices')

    issue_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)

    # Item fields (single line item for now)
    item_description = models.CharField(max_length=255)
    hsn_sac = models.CharField(max_length=20, blank=True, null=True)
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=18)  # in %
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # quantity * rate

    # Tax fields (IGST for now)
    igst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    place_of_supply = models.CharField(max_length=100, blank=True, null=True)
    place_of_supply_code = models.CharField(max_length=5, blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_invoices'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.invoice_number} - {self.client.company_name}"
