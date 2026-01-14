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
    
    # Revenue Tracking (for individual booking)
    pitched_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text=_('Pitched amount for this booking (excluding GST)')
    )
    
    gst_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('18.00'),
        help_text=_('GST percentage for this booking')
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
        help_text=_('Total amount including GST for this booking')
    )
    
    received_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text=_('Amount received for this booking')
    )
    
    pending_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text=_('Pending amount for this booking')
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
        
        # Calculate GST and totals for revenue tracking
        if self.pitched_amount and self.gst_percentage is not None:
            self.gst_amount = (self.pitched_amount * self.gst_percentage) / Decimal('100.00')
            self.total_with_gst = self.pitched_amount + self.gst_amount
            self.pending_amount = self.total_with_gst - self.received_amount
        
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
    
    def get_service_stages(self):
        """Get stage definitions based on service category"""
        stage_definitions = {
            'INCORPORATION': [
                {'step': 1, 'name': 'Business Information', 'completed': False, 'current': False},
                {'step': 2, 'name': 'Documentation', 'completed': False, 'current': False},
                {'step': 3, 'name': 'Application Submission', 'completed': False, 'current': False},
                {'step': 4, 'name': 'Government Approval', 'completed': False, 'current': False},
                {'step': 5, 'name': 'Certificate Received', 'completed': False, 'current': False},
            ],
            'CERTIFICATION': [
                {'step': 1, 'name': 'Eligibility Check', 'completed': False, 'current': False},
                {'step': 2, 'name': 'Audit & Assessment', 'completed': False, 'current': False},
                {'step': 3, 'name': 'Corrective Actions', 'completed': False, 'current': False},
                {'step': 4, 'name': 'Final Certification', 'completed': False, 'current': False},
                {'step': 5, 'name': 'Certificate Issuance', 'completed': False, 'current': False},
            ],
            'FUNDING': [
                {'step': 1, 'name': 'Scheme Evaluation', 'completed': False, 'current': False},
                {'step': 2, 'name': 'Documentation Preparation', 'completed': False, 'current': False},
                {'step': 3, 'name': 'Application Filing', 'completed': False, 'current': False},
                {'step': 4, 'name': 'Application Tracking', 'completed': False, 'current': False},
                {'step': 5, 'name': 'Fund Disbursement', 'completed': False, 'current': False},
            ],
            'CONSULTING': [
                {'step': 1, 'name': 'Initial Consultation', 'completed': False, 'current': False},
                {'step': 2, 'name': 'Analysis & Planning', 'completed': False, 'current': False},
                {'step': 3, 'name': 'Implementation', 'completed': False, 'current': False},
                {'step': 4, 'name': 'Monitoring & Review', 'completed': False, 'current': False},
                {'step': 5, 'name': 'Final Recommendations', 'completed': False, 'current': False},
            ],
            'GROWTH': [
                {'step': 1, 'name': 'Business Assessment', 'completed': False, 'current': False},
                {'step': 2, 'name': 'Growth Strategy', 'completed': False, 'current': False},
                {'step': 3, 'name': 'Execution Planning', 'completed': False, 'current': False},
                {'step': 4, 'name': 'Implementation Support', 'completed': False, 'current': False},
                {'step': 5, 'name': 'Success Tracking', 'completed': False, 'current': False},
            ],
            'CSR': [
                {'step': 1, 'name': 'CSR Planning', 'completed': False, 'current': False},
                {'step': 2, 'name': 'Project Design', 'completed': False, 'current': False},
                {'step': 3, 'name': 'Implementation', 'completed': False, 'current': False},
                {'step': 4, 'name': 'Impact Assessment', 'completed': False, 'current': False},
                {'step': 5, 'name': 'Compliance Filing', 'completed': False, 'current': False},
            ],
        }
        
        # Get stages for this service category
        stages = stage_definitions.get(self.service.category, stage_definitions['CONSULTING'])
        
        # Mark stages as completed/current based on progress
        progress_per_stage = 100 / len(stages)
        for i, stage in enumerate(stages):
            if self.progress_percent >= (i + 1) * progress_per_stage:
                stage['completed'] = True
                stage['current'] = False
            elif self.progress_percent > i * progress_per_stage:
                stage['completed'] = False
                stage['current'] = True
            else:
                stage['completed'] = False
                stage['current'] = False
        
        return stages
