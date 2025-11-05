from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Notification(models.Model):
    """
    Email and WhatsApp notifications sent to users/clients
    """
    
    class Channel(models.TextChoices):
        EMAIL = 'EMAIL', _('Email')
        WHATSAPP = 'WHATSAPP', _('WhatsApp')
        BOTH = 'BOTH', _('Email + WhatsApp')
    
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        SENT = 'SENT', _('Sent Successfully')
        FAILED = 'FAILED', _('Failed')
        QUEUED = 'QUEUED', _('Queued for Sending')
    
    class NotificationType(models.TextChoices):
        WELCOME = 'WELCOME', _('Welcome Message')
        CREDENTIALS = 'CREDENTIALS', _('Login Credentials')
        BOOKING_CONFIRMATION = 'BOOKING_CONFIRMATION', _('Booking Confirmation')
        PAYMENT_SUCCESS = 'PAYMENT_SUCCESS', _('Payment Successful')
        PAYMENT_FAILED = 'PAYMENT_FAILED', _('Payment Failed')
        APPLICATION_SUBMITTED = 'APPLICATION_SUBMITTED', _('Application Submitted')
        APPLICATION_APPROVED = 'APPLICATION_APPROVED', _('Application Approved')
        APPLICATION_REJECTED = 'APPLICATION_REJECTED', _('Application Rejected')
        DOCUMENT_READY = 'DOCUMENT_READY', _('Document Ready for Download')
        EDIT_REQUEST_APPROVED = 'EDIT_REQUEST_APPROVED', _('Edit Request Approved')
        EDIT_REQUEST_REJECTED = 'EDIT_REQUEST_REJECTED', _('Edit Request Rejected')
        REMINDER = 'REMINDER', _('Reminder/Follow-up')
        CUSTOM = 'CUSTOM', _('Custom Message')
    
    # Recipient
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications_received',
        help_text=_('User/client who will receive the notification')
    )
    
    # Channel & Type
    channel = models.CharField(
        max_length=10,
        choices=Channel.choices,
        help_text=_('Communication channel')
    )
    
    notification_type = models.CharField(
        max_length=30,
        choices=NotificationType.choices,
        help_text=_('Type of notification')
    )
    
    # Status
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        help_text=_('Notification status')
    )
    
    # Content
    subject = models.CharField(
        max_length=200,
        help_text=_('Email subject or WhatsApp message title')
    )
    
    message = models.TextField(
        help_text=_('Notification message content')
    )
    
    html_content = models.TextField(
        blank=True,
        null=True,
        help_text=_('HTML content for email (optional)')
    )
    
    # Contact Details
    email_to = models.EmailField(
        blank=True,
        null=True,
        help_text=_('Recipient email address')
    )
    
    whatsapp_to = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text=_('Recipient WhatsApp number')
    )
    
    # Attachments
    attachments = models.JSONField(
        default=list,
        help_text=_('List of attachment file paths')
    )
    
    # Tracking
    sent_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Timestamp when notification was sent')
    )
    
    failed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Timestamp when notification failed')
    )
    
    error_message = models.TextField(
        blank=True,
        null=True,
        help_text=_('Error message if notification failed')
    )
    
    retry_count = models.IntegerField(
        default=0,
        help_text=_('Number of retry attempts')
    )
    
    # External IDs
    email_message_id = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text=_('Email message ID from SMTP server')
    )
    
    whatsapp_message_id = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text=_('WhatsApp message ID from API')
    )
    
    # Related Objects
    related_booking = models.ForeignKey(
        'bookings.Booking',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications',
        help_text=_('Related booking (if applicable)')
    )
    
    related_application = models.ForeignKey(
        'applications.Application',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications',
        help_text=_('Related application (if applicable)')
    )
    
    related_payment = models.ForeignKey(
        'payments.Payment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications',
        help_text=_('Related payment (if applicable)')
    )
    
    # Sender
    sent_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications_sent',
        help_text=_('User who triggered the notification')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'status']),
            models.Index(fields=['notification_type', 'status']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_notification_type_display()} to {self.recipient.email} via {self.channel}"
    
    def mark_sent(self):
        """Mark notification as sent"""
        from django.utils import timezone
        self.status = self.Status.SENT
        self.sent_at = timezone.now()
        self.save()
    
    def mark_failed(self, error):
        """Mark notification as failed"""
        from django.utils import timezone
        self.status = self.Status.FAILED
        self.failed_at = timezone.now()
        self.error_message = str(error)
        self.retry_count += 1
        self.save()
    
    def can_retry(self):
        """Check if notification can be retried"""
        return self.status == self.Status.FAILED and self.retry_count < 3
