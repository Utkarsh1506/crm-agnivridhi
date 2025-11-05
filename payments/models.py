from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

class Payment(models.Model):
    """
    Payment transactions via Razorpay
    """
    
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        INITIATED = 'INITIATED', _('Initiated')
        AUTHORIZED = 'AUTHORIZED', _('Authorized')
        CAPTURED = 'CAPTURED', _('Captured')
        FAILED = 'FAILED', _('Failed')
        REFUNDED = 'REFUNDED', _('Refunded')
        PARTIAL_REFUND = 'PARTIAL_REFUND', _('Partially Refunded')
    
    # Razorpay Details
    razorpay_order_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_('Razorpay order ID (optional for offline/manual payments)')
    )
    
    razorpay_payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_('Razorpay payment ID (after successful payment)')
    )
    
    razorpay_signature = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text=_('Razorpay signature for verification')
    )
    
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
    
    # Additional Info
    PAYMENT_VIA_CHOICES = (
        ('UPI_QR', _('UPI QR')),
        ('BANK_TRANSFER', _('Bank Transfer')),
        ('CASH', _('Cash')),
        ('CARD', _('Card')),
        ('OTHER', _('Other')),
    )

    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_VIA_CHOICES,
        blank=True,
        null=True,
        help_text=_('Payment method/channel')
    )

    # Manual payment capture fields
    reference_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_('Transaction reference number (UTR/UPI Ref/Receipt No.)')
    )

    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='received_payments',
        help_text=_('Sales employee who recorded/received this payment')
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
    
    razorpay_response = models.JSONField(
        default=dict,
        help_text=_('Full Razorpay webhook response')
    )
    
    error_message = models.TextField(
        blank=True,
        null=True,
        help_text=_('Error message if payment failed')
    )
    
    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['razorpay_order_id']),
            models.Index(fields=['razorpay_payment_id']),
            models.Index(fields=['client', 'status']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"Payment {self.razorpay_order_id} - ₹{self.amount} - {self.status}"
    
    def is_successful(self):
        """Check if payment is successful"""
        return self.status in ['AUTHORIZED', 'CAPTURED']
    
    def can_refund(self):
        """Check if payment can be refunded"""
        return self.is_successful() and self.refund_amount < self.amount
