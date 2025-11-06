from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

class Payment(models.Model):
    """
    Manual payment records - No payment gateway integration
    All payments recorded manually by sales employees
    """
    
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending Verification')
        CAPTURED = 'CAPTURED', _('Payment Received')
        FAILED = 'FAILED', _('Failed/Disputed')
        REFUNDED = 'REFUNDED', _('Refunded')
    
    # Relationships
    booking = models.OneToOneField(
        'bookings.Booking',
        on_delete=models.CASCADE,
        related_name='payment',
        help_text=_('Associated booking')
    )
    
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name='payments',
        help_text=_('Client making payment')
    )
    
    # Amount Details
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text=_('Payment amount in INR')
    )
    
    currency = models.CharField(
        max_length=3,
        default='INR',
        help_text=_('Currency code')
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        help_text=_('Payment status')
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_('Payment creation timestamp')
    )
    
    payment_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Successful payment timestamp')
    )
    
    # Refund Details
    refund_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text=_('Refunded amount')
    )
    
    refund_reason = models.TextField(
        blank=True,
        null=True,
        help_text=_('Reason for refund')
    )
    
    refund_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Refund processing date')
    )
    
    # Additional Info - Manual Payment Fields
    PAYMENT_VIA_CHOICES = (
        ('UPI_QR', _('UPI QR')),
        ('BANK_TRANSFER', _('Bank Transfer (NEFT/RTGS/IMPS)')),
        ('CASH', _('Cash')),
        ('CHEQUE', _('Cheque/DD')),
        ('CARD', _('Card (POS/Swipe)')),
        ('OTHER', _('Other')),
    )

    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_VIA_CHOICES,
        default='OTHER',
        help_text=_('Payment method/channel')
    )

    # Manual payment capture fields
    reference_id = models.CharField(
        max_length=100,
        default='',
        help_text=_('Transaction reference number (UTR/UPI Ref/Receipt No/Cheque No)')
    )

    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='received_payments',
        help_text=_('Sales employee who recorded this payment')
    )

    notes = models.TextField(
        blank=True,
        null=True,
        help_text=_('Internal notes about this payment')
    )

    proof = models.FileField(
        upload_to='payment_proofs/',
        blank=True,
        null=True,
        help_text=_('Optional proof/screenshot of payment')
    )
    
    error_message = models.TextField(
        blank=True,
        null=True,
        help_text=_('Error message if payment failed/disputed')
    )
    
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_payments',
        help_text=_('Manager/Admin who approved this payment')
    )
    
    approval_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('When payment was approved')
    )
    
    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reference_id']),
            models.Index(fields=['client', 'status']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['payment_method']),
        ]
    
    def __str__(self):
        ref = self.reference_id or f"#{self.pk or 'NEW'}"
        return f"Payment {ref} - ₹{self.amount} - {self.status}"
    
    def is_successful(self):
        """Check if payment is successful"""
        return self.status == 'CAPTURED'
    
    def can_refund(self):
        """Check if payment can be refunded"""
        return self.is_successful() and self.refund_amount < self.amount
    
    def approve(self, approved_by_user):
        """Approve manual payment"""
        from django.utils import timezone
        self.status = self.Status.CAPTURED
        self.approved_by = approved_by_user
        self.approval_date = timezone.now()
        if not self.payment_date:
            self.payment_date = timezone.now()
        self.save()
        
        # Update booking status
        if self.booking:
            self.booking.status = 'PAID'
            self.booking.payment_date = self.payment_date
            self.booking.save()
    
    def reject(self, rejected_by_user, reason=''):
        """Reject/dispute manual payment"""
        from django.utils import timezone
        self.status = self.Status.FAILED
        self.error_message = reason
        self.approved_by = rejected_by_user
        self.approval_date = timezone.now()
        self.save()
