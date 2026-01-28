from django.db import models
from django.conf import settings
from clients.models import Client
from employees.models import Employee
from decimal import Decimal


class Agreement(models.Model):
    """Agreement model for Funding and Website services"""
    
    AGREEMENT_TYPE_CHOICES = [
        ('funding', 'Funding Agreement'),
        ('website', 'Website Agreement'),
    ]
    
    STAGE_CHOICES = [
        ('stage_1', 'Stage 1 - Received'),
        ('stage_2', 'Stage 2 - Pending/Commission'),
        ('stage_3', 'Stage 3 - Final Commission'),
    ]
    
    # Basic Info
    agreement_number = models.CharField(max_length=50, unique=True, db_index=True)
    agreement_type = models.CharField(max_length=20, choices=AGREEMENT_TYPE_CHOICES)
    
    # Service Receiver Details
    service_receiver_name = models.CharField(max_length=255, help_text="Name of Service Receiver")
    service_receiver_address = models.TextField(help_text="Complete Address")
    service_receiver_designation = models.CharField(
        max_length=100, 
        default="Director",
        help_text="Designation of Service Receiver (e.g., Director, Proprietor)"
    )
    
    # Agreement Details
    date_of_agreement = models.DateField(help_text="Date of Agreement")
    service_description = models.TextField(help_text="Description of Service")
    
    # Financial Details
    total_amount_pitched = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        help_text="Total Amount Pitched"
    )
    
    received_amount_stage1 = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        help_text="Received Amount without GST (Stage 1)"
    )
    
    pending_amount_stage2 = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        default=Decimal('0.00'),
        blank=True,
        null=True,
        help_text="Pending Amount (Stage 2) - Optional"
    )
    
    commission_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Commission Percentage after Disbursement"
    )
    
    commission_stage = models.CharField(
        max_length=20,
        choices=STAGE_CHOICES,
        default='stage_2',
        help_text="Stage when commission applies"
    )
    
    # Related parties
    client = models.ForeignKey(
        Client, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='agreements'
    )
    
    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='agreements',
        help_text="Employee handling this agreement"
    )
    
    # Additional Notes
    notes = models.TextField(blank=True, null=True)
    
    # Metadata
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_agreements'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Agreement'
        verbose_name_plural = 'Agreements'
        
    def __str__(self):
        return f"{self.agreement_number} - {self.service_receiver_name} ({self.get_agreement_type_display()})"
    
    def has_pending_amount(self):
        """Check if there is pending amount"""
        return self.pending_amount_stage2 and self.pending_amount_stage2 > 0
    
    @property
    def calculated_commission(self):
        """Calculate commission amount based on percentage"""
        if self.has_pending_amount():
            base_amount = self.pending_amount_stage2
        else:
            base_amount = self.received_amount_stage1
        
        return (base_amount * self.commission_percentage) / Decimal('100')
