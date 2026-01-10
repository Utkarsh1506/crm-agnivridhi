from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal

class Service(models.Model):
    """
    Services offered by Agnivridhi
    """
    
    class Category(models.TextChoices):
        FUNDING = 'FUNDING', _('Funding Services')
        INCORPORATION = 'INCORPORATION', _('Incorporation Services')
        CERTIFICATION = 'CERTIFICATION', _('Certification Services')
        GROWTH = 'GROWTH', _('Growth Services')
        CSR = 'CSR', _('CSR Services')
        CONSULTING = 'CONSULTING', _('Consulting Services')
    
    name = models.CharField(
        max_length=200,
        help_text=_('Service name')
    )
    
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        help_text=_('Service category')
    )
    
    description = models.TextField(
        help_text=_('Detailed service description')
    )
    
    short_description = models.TextField(
        max_length=500,
        help_text=_('Brief service description (for listings)')
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text=_('Service price in INR')
    )
    
    duration_days = models.IntegerField(
        default=30,
        help_text=_('Expected completion duration in days')
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text=_('Service is active and available for booking')
    )
    
    features = models.JSONField(
        default=list,
        help_text=_('List of features included in service')
    )
    
    deliverables = models.JSONField(
        default=list,
        help_text=_('List of deliverables for this service')
    )

    faqs = models.JSONField(
        default=list,
        help_text=_('FAQ entries for this service')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ['category', 'name']
        indexes = [
            models.Index(fields=['category', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} - ₹{self.price}"


class Booking(models.Model):
    """
    Service bookings made by clients
    """
    
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending Payment')
        PAID = 'PAID', _('Paid - In Progress')
        COMPLETED = 'COMPLETED', _('Completed')
        CANCELLED = 'CANCELLED', _('Cancelled')
        REFUNDED = 'REFUNDED', _('Refunded')
    
    class Priority(models.TextChoices):
        LOW = 'LOW', _('Low')
        MEDIUM = 'MEDIUM', _('Medium')
        HIGH = 'HIGH', _('High')
        URGENT = 'URGENT', _('Urgent')
    
    # Booking ID
    booking_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        help_text=_('Auto-generated unique booking ID')
    )
    
    # Relationships
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text=_('Client who made the booking')
    )
    
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name='bookings',
        help_text=_('Service booked')
    )
    
    # Booking Details
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        help_text=_('Current booking status')
    )
    
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        help_text=_('Booking priority level')
    )
    
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text=_('Booking amount in INR')
    )
    
    discount_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text=_('Discount percentage applied')
    )
    
    final_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text=_('Final amount after discount')
    )
    
    # Dates
    booking_date = models.DateTimeField(
        auto_now_add=True,
        help_text=_('Date when booking was created')
    )
    
    payment_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Date when payment was completed')
    )
    
    expected_completion_date = models.DateField(
        null=True,
        blank=True,
        help_text=_('Expected service completion date')
    )
    
    actual_completion_date = models.DateField(
        null=True,
        blank=True,
        help_text=_('Actual service completion date')
    )
    
    # Requirements
    requirements = models.TextField(
        blank=True,
        null=True,
        help_text=_('Client requirements and specifications')
    )
    
    # Assignment
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_bookings',
        limit_choices_to={'role__in': ['ADMIN', 'MANAGER', 'SALES']},
        help_text=_('Staff member assigned to fulfill booking')
    )
    
    # Progress Tracking
    progress_percent = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_('Completion progress percentage')
    )
    
    internal_notes = models.TextField(
        blank=True,
        null=True,
        help_text=_('Internal notes (not visible to client)')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='bookings_created',
        help_text=_('User who created this booking')
    )
    
    class Meta:
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')
        ordering = ['-booking_date']
        indexes = [
            models.Index(fields=['booking_id']),
            models.Index(fields=['client', 'status']),
            models.Index(fields=['assigned_to', 'status']),
            models.Index(fields=['-booking_date']),
        ]
    
    def __str__(self):
        return f"{self.booking_id} - {self.client.company_name} - {self.service.name}"
    
    def save(self, *args, **kwargs):
        """Generate booking ID and calculate final amount"""
        if not self.booking_id:
            self.booking_id = self.generate_booking_id()
        
        # Calculate final amount after discount
        if self.amount:
            discount_amount = (self.amount * self.discount_percent) / 100
            self.final_amount = self.amount - discount_amount
        
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_booking_id():
        """Generate unique booking ID: BKG-YYYYMMDD-XXXX"""
        import secrets
        import string
        from datetime import datetime
        date_str = datetime.now().strftime('%Y%m%d')
        random_str = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        return f"BKG-{date_str}-{random_str}"
    
    def get_payment_status(self):
        """Get payment status for this booking"""
        try:
            return self.payment.status
        except:
            return 'UNPAID'
    
    def is_overdue(self):
        """Check if booking is overdue"""
        from django.utils import timezone
        if self.expected_completion_date and self.status not in ['COMPLETED', 'CANCELLED', 'REFUNDED']:
            return self.expected_completion_date < timezone.now().date()
        return False
