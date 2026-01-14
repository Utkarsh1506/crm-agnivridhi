from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import secrets
import string

class Client(models.Model):
    """
    Client/Company model for businesses seeking funding and consultancy services
    """
    
    class BusinessType(models.TextChoices):
        PVT_LTD = 'PVT_LTD', _('Pvt Ltd Company')
        LLP = 'LLP', _('LLP')
        PROPRIETORSHIP = 'PROPRIETORSHIP', _('Proprietorship')
        PARTNERSHIP = 'PARTNERSHIP', _('Partnership Firm')
        OPC = 'OPC', _('One Person Company')
        STARTUP = 'STARTUP', _('Startup')
        NGO = 'NGO', _('NGO')
        SECTION_8 = 'SECTION_8', _('Section 8 (Schools, Hospitals, etc.)')
        OTHER = 'OTHER', _('Other')
    
    class Sector(models.TextChoices):
        MANUFACTURING = 'MANUFACTURING', _('Manufacturing')
        SERVICE = 'SERVICE', _('Service')
        RETAIL = 'RETAIL', _('Retail/Trading')
        IT_SOFTWARE = 'IT_SOFTWARE', _('IT/Software')
        AGRICULTURE = 'AGRICULTURE', _('Agriculture')
        HEALTHCARE = 'HEALTHCARE', _('Healthcare')
        EDUCATION = 'EDUCATION', _('Education')
        FOOD_BEVERAGE = 'FOOD_BEVERAGE', _('Food & Beverage')
        CONSTRUCTION = 'CONSTRUCTION', _('Construction')
        TEXTILE = 'TEXTILE', _('Textile')
        CHEMICAL = 'CHEMICAL', _('Chemical')
        PHARMA = 'PHARMA', _('Pharma')
        LOGISTICS = 'LOGISTICS', _('Logistics')
        NGO_SOCIAL = 'NGO_SOCIAL', _('NGO/Social Work')
        NGO_CHARITY = 'NGO_CHARITY', _('Charity/Welfare')
        NGO_ENVIRONMENT = 'NGO_ENVIRONMENT', _('Environment/Conservation')
        NGO_HEALTH = 'NGO_HEALTH', _('Health & Sanitation')
        NGO_EDUCATION = 'NGO_EDUCATION', _('Education & Literacy')
        NGO_WOMEN = 'NGO_WOMEN', _('Women Empowerment')
        NGO_CHILD = 'NGO_CHILD', _('Child Welfare')
        OTHER = 'OTHER', _('Other')
    
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', _('Active')
        INACTIVE = 'INACTIVE', _('Inactive')
        PENDING_DOCS = 'PENDING_DOCS', _('Pending Documents')
        ON_HOLD = 'ON_HOLD', _('On Hold')
        COMPLETED = 'COMPLETED', _('Completed')
    
    # User account
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_profile',
        help_text=_('Associated user account for client login')
    )
    
    # Client ID
    client_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        help_text=_('Auto-generated unique client ID')
    )
    
    # Company Information
    company_name = models.CharField(
        max_length=200,
        help_text=_('Registered company/business name')
    )
    
    business_type = models.CharField(
        max_length=20,
        choices=BusinessType.choices,
        blank=True,
        null=True,
        help_text=_('Type of business entity')
    )
    
    sector = models.CharField(
        max_length=20,
        choices=Sector.choices,
        blank=True,
        null=True,
        help_text=_('Primary business sector')
    )
    
    company_age = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True,
        null=True,
        help_text=_('Age of company in years')
    )
    
    registration_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text=_('Company registration number (CIN/LLPIN/etc.)')
    )
    
    gst_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text=_('GST registration number')
    )
    
    pan_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text=_('Company PAN number')
    )
    
    # Financial Information
    annual_turnover = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('Annual turnover in lakhs')
    )
    
    funding_required = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('Total funding required in lakhs')
    )
    
    existing_loans = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text=_('Existing loan amount in lakhs')
    )

    # Revenue Tracking
    total_pitched_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text=_('Total pitched amount (₹) discussed with client (excluding GST)')
    )

    gst_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('18.00'),
        help_text=_('GST percentage to apply')
    )

    gst_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text=_('GST amount (auto-calculated)')
    )

    total_with_gst = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text=_('Total pitched amount including GST')
    )

    received_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text=_('Total amount (₹) received so far from client')
    )

    pending_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text=_('Pending amount (₹) expected from client')
    )
    
    # Contact Information
    contact_person = models.CharField(
        max_length=200,
        help_text=_('Primary contact person name')
    )
    
    contact_email = models.EmailField(
        help_text=_('Primary contact email')
    )
    
    contact_phone = models.CharField(
        max_length=15,
        help_text=_('Primary contact phone')
    )
    
    alternate_phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text=_('Alternate contact phone')
    )
    
    # Address
    address_line1 = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text=_('Address line 1')
    )
    
    address_line2 = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text=_('Address line 2')
    )
    
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_('City')
    )
    
    state = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_('State')
    )
    
    pincode = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        help_text=_('Pincode')
    )
    
    # Assignment
    assigned_sales = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_clients_sales',
        limit_choices_to={'role': 'SALES'},
        help_text=_('Sales employee assigned to this client')
    )
    
    assigned_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_clients_manager',
        limit_choices_to={'role__in': ['ADMIN', 'MANAGER']},
        help_text=_('Manager overseeing this client')
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        help_text=_('Current client status')
    )
    
    # Approval fields
    is_approved = models.BooleanField(
        default=True,
        help_text=_('Whether client is approved by manager')
    )
    
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_clients',
        help_text=_('Manager who approved this client')
    )
    
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Date when client was approved')
    )
    
    rejection_reason = models.TextField(
        blank=True,
        null=True,
        help_text=_('Reason for rejection if not approved')
    )
    
    # Additional Information
    business_description = models.TextField(
        blank=True,
        null=True,
        help_text=_('Brief description of business activities')
    )
    
    funding_purpose = models.TextField(
        blank=True,
        null=True,
        help_text=_('Purpose of funding requirement')
    )
    
    notes = models.TextField(
        blank=True,
        null=True,
        help_text=_('Internal notes (not visible to client)')
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_('Date when client was registered')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_('Last update timestamp')
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='clients_created',
        help_text=_('User who created this client record')
    )
    
    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['client_id']),
            models.Index(fields=['company_name']),
            models.Index(fields=['assigned_sales', 'status']),
            models.Index(fields=['sector', 'annual_turnover']),
        ]
    
    def __str__(self):
        return f"{self.company_name} ({self.client_id})"
    
    def save(self, *args, **kwargs):
        """Generate unique client ID if not exists"""
        # Normalize revenue numbers and keep consistency
        try:
            total = Decimal(self.total_pitched_amount or 0)
            received = Decimal(self.received_amount or 0)
            gst_pct = Decimal(self.gst_percentage or 18)
            
            if received < 0:
                received = Decimal('0.00')
            if total < 0:
                total = Decimal('0.00')
            if gst_pct < 0:
                gst_pct = Decimal('18.00')
            
            # Calculate GST
            self.gst_amount = (total * gst_pct / Decimal('100')).quantize(Decimal('0.01'))
            self.total_with_gst = total + self.gst_amount
            
            # Ensure received does not exceed total with GST
            if self.total_with_gst >= 0 and received > self.total_with_gst:
                self.total_with_gst = received
                self.gst_amount = Decimal('0.00')
                total = received
            
            self.total_pitched_amount = total
            self.received_amount = received
            self.gst_percentage = gst_pct
            
            # Compute pending based on total with GST
            computed_pending = self.total_with_gst - received
            if computed_pending < 0:
                computed_pending = Decimal('0.00')
            self.pending_amount = computed_pending
        except Exception:
            # Fail-safe: ensure fields exist even if parsing fails
            self.total_pitched_amount = self.total_pitched_amount or Decimal('0.00')
            self.received_amount = self.received_amount or Decimal('0.00')
            self.pending_amount = self.pending_amount or Decimal('0.00')
            self.gst_percentage = self.gst_percentage or Decimal('18.00')
            self.gst_amount = self.gst_amount or Decimal('0.00')
            self.total_with_gst = self.total_with_gst or Decimal('0.00')

        if not self.client_id:
            self.client_id = self.generate_client_id()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_client_id():
        """Generate unique client ID: CLI-YYYYMMDD-XXXX"""
        from datetime import datetime
        date_str = datetime.now().strftime('%Y%m%d')
        random_str = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        return f"CLI-{date_str}-{random_str}"
    
    def get_absolute_url(self):
        """Get URL for client detail page"""
        from django.urls import reverse
        return reverse('client_detail', kwargs={'pk': self.pk})
    
    def get_total_applications(self):
        """Get count of all applications"""
        return self.applications.count()
    
    def get_total_bookings(self):
        """Get count of all bookings"""
        return self.bookings.count()
    
    def get_total_paid(self):
        """Get total amount paid by client"""
        from payments.models import Payment
        return Payment.objects.filter(
            booking__client=self,
            status__in=['AUTHORIZED', 'CAPTURED']
        ).aggregate(models.Sum('amount'))['amount__sum'] or 0
    
    def calculate_aggregated_revenue(self):
        """
        Calculate total revenue across all bookings for this client.
        Updates the client-level revenue fields based on booking totals.
        """
        from django.db.models import Sum
        aggregated = self.bookings.aggregate(
            total_pitched=Sum('pitched_amount'),
            total_gst=Sum('gst_amount'),
            total_with_gst=Sum('total_with_gst'),
            total_received=Sum('received_amount'),
            total_pending=Sum('pending_amount')
        )
        
        # Update client fields with aggregated values
        self.total_pitched_amount = aggregated['total_pitched'] or Decimal('0.00')
        self.gst_amount = aggregated['total_gst'] or Decimal('0.00')
        self.total_with_gst = aggregated['total_with_gst'] or Decimal('0.00')
        self.received_amount = aggregated['total_received'] or Decimal('0.00')
        self.pending_amount = aggregated['total_pending'] or Decimal('0.00')
        
        # Calculate average GST percentage if needed
        if self.total_pitched_amount > 0:
            self.gst_percentage = (self.gst_amount / self.total_pitched_amount * Decimal('100.00')).quantize(Decimal('0.01'))
        
        return {
            'total_pitched': self.total_pitched_amount,
            'gst_amount': self.gst_amount,
            'total_with_gst': self.total_with_gst,
            'received_amount': self.received_amount,
            'pending_amount': self.pending_amount
        }
    
    def approve(self, manager_user):
        """Approve the client"""
        from django.utils import timezone
        self.is_approved = True
        self.approved_by = manager_user
        self.approved_at = timezone.now()
        self.rejection_reason = None
        self.save()
    
    def reject(self, manager_user, reason):
        """Reject the client"""
        from django.utils import timezone
        self.is_approved = False
        self.approved_by = manager_user
        self.approved_at = timezone.now()
        self.rejection_reason = reason
        self.save()


class ClientCredential(models.Model):
    """
    Store generated login credentials for new clients
    Only visible to Admin/Owner for security
    """
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name='credentials',
        help_text=_('Client these credentials belong to')
    )
    
    username = models.CharField(
        max_length=150,
        help_text=_('Generated username')
    )
    
    email = models.EmailField(
        help_text=_('Client email')
    )
    
    plain_password = models.CharField(
        max_length=100,
        help_text=_('Plain text password (only stored once)')
    )
    
    is_sent = models.BooleanField(
        default=False,
        help_text=_('Whether credentials have been sent to client')
    )
    
    sent_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('When credentials were sent')
    )
    
    sent_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='credentials_sent',
        help_text=_('Who sent the credentials')
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='credentials_created',
        help_text=_('Who created this client')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Client Credential')
        verbose_name_plural = _('Client Credentials')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Credentials for {self.client.company_name}"
    
    def mark_as_sent(self, user):
        """Mark credentials as sent"""
        from django.utils import timezone
        self.is_sent = True
        self.sent_at = timezone.now()
        self.sent_by = user
        self.save()
