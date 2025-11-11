from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import os

class Document(models.Model):
    """
    Documents generated and stored for clients (DPR, Pitch Deck, Projections, etc.)
    """
    
    class DocumentType(models.TextChoices):
        DPR = 'DPR', _('Detailed Project Report')
        PITCH_DECK = 'PITCH_DECK', _('Pitch Deck')
        FINANCIAL_PROJECTION = 'FINANCIAL_PROJECTION', _('Financial Projections')
        FUND_UTILIZATION = 'FUND_UTILIZATION', _('Fund Utilisation Report')
        APPLICATION_FORM = 'APPLICATION_FORM', _('Scheme Application Form')
        CERTIFICATE = 'CERTIFICATE', _('Certificate/Registration')
        INVOICE = 'INVOICE', _('Invoice/Receipt')
        OTHER = 'OTHER', _('Other Document')
    
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', _('Draft')
        GENERATED = 'GENERATED', _('Generated')
        SENT = 'SENT', _('Sent to Client')
        DOWNLOADED = 'DOWNLOADED', _('Downloaded by Client')
    
    # Document Details
    document_type = models.CharField(
        max_length=25,
        choices=DocumentType.choices,
        help_text=_('Type of document')
    )
    
    title = models.CharField(
        max_length=200,
        help_text=_('Document title')
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        help_text=_('Document description')
    )
    
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.DRAFT,
        help_text=_('Document status')
    )
    
    # Relationships
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name='documents',
        help_text=_('Client this document belongs to')
    )
    
    application = models.ForeignKey(
        'applications.Application',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents',
        help_text=_('Associated application (if applicable)')
    )
    
    booking = models.ForeignKey(
        'bookings.Booking',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents',
        help_text=_('Associated booking (if applicable)')
    )
    
    # File Details
    file = models.FileField(
        upload_to='documents/%Y/%m/',
        help_text=_('Uploaded/generated document file')
    )
    
    file_size = models.IntegerField(
        default=0,
        help_text=_('File size in bytes')
    )
    
    file_format = models.CharField(
        max_length=10,
        default='PDF',
        help_text=_('File format (PDF, DOCX, etc.)')
    )
    
    # Generation Details
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='documents_generated',
        help_text=_('User who generated/uploaded the document')
    )
    
    template_used = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_('Template used for generation')
    )
    
    generation_data = models.JSONField(
        default=dict,
        help_text=_('Data used for document generation')
    )
    
    # Download Tracking
    download_count = models.IntegerField(
        default=0,
        help_text=_('Number of times document was downloaded')
    )
    
    last_downloaded_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Last download timestamp')
    )
    
    last_downloaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents_downloaded',
        help_text=_('User who last downloaded the document')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['client', 'document_type']),
            models.Index(fields=['application']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_document_type_display()}) - {self.client.company_name}"
    
    def save(self, *args, **kwargs):
        """Calculate file size on save"""
        if self.file:
            self.file_size = self.file.size
            _, ext = os.path.splitext(self.file.name)
            self.file_format = ext.upper().replace('.', '')
        super().save(*args, **kwargs)
    
    def record_download(self, user):
        """Record a document download"""
        from django.utils import timezone
        self.download_count += 1
        self.last_downloaded_at = timezone.now()
        self.last_downloaded_by = user
        if self.status == self.Status.GENERATED:
            self.status = self.Status.DOWNLOADED
        self.save()
    
    def get_file_size_display(self):
        """Get human-readable file size"""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
