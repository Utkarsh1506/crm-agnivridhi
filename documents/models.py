from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import os

class Document(models.Model):
    """
    Documents generated and stored for clients (DPR, Pitch Deck, Projections, etc.)
    """
    
    class DocumentType(models.TextChoices):
        # Professional documents (uploaded by Sales/Team)
        DPR = 'DPR', 'Detailed Project Report (DPR)'
        PITCH_DECK = 'PITCH_DECK', 'Pitch Deck'
        FINANCIAL_PROJECTION = 'FINANCIAL_PROJECTION', 'Financial Projections'
        FUND_UTILIZATION = 'FUND_UTILIZATION', 'Fund Utilisation Report'
        AGREEMENT = 'AGREEMENT', 'Agreement/Contract'
        
        # Client required documents
        COMPANY_REG = 'COMPANY_REG', 'Company Registration Certificate'
        GST_CERT = 'GST_CERT', 'GST Registration Certificate'
        PAN_CARD = 'PAN_CARD', 'PAN Card'
        MSME_CERT = 'MSME_CERT', 'MSME/Udyam Registration'
        BANK_STATEMENT = 'BANK_STATEMENT', 'Bank Statements (6 months)'
        ITR = 'ITR', 'Income Tax Returns (Last 2 years)'
        BALANCE_SHEET = 'BALANCE_SHEET', 'Balance Sheet & P&L'
        INCORPORATION_CERT = 'INCORPORATION_CERT', 'Certificate of Incorporation'
        MOA_AOA = 'MOA_AOA', 'MOA & AOA'
        BOARD_RESOLUTION = 'BOARD_RESOLUTION', 'Board Resolution'
        
        # Application forms
        APPLICATION_FORM = 'APPLICATION_FORM', 'Scheme Application Form'
        
        # Other
        INVOICE = 'INVOICE', 'Invoice/Receipt'
        OTHER = 'OTHER', 'Other Document'
    
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        GENERATED = 'GENERATED', 'Generated'
        SENT = 'SENT', 'Sent to Client'
        DOWNLOADED = 'DOWNLOADED', 'Downloaded by Client'
    
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


class DocumentChecklist(models.Model):
    """
    Required documents checklist created by Sales for each client
    """
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name='document_checklist',
        help_text='Client for this checklist'
    )
    
    document_type = models.CharField(
        max_length=25,
        choices=Document.DocumentType.choices,
        help_text='Type of required document'
    )
    
    is_required = models.BooleanField(
        default=True,
        help_text='Is this document mandatory?'
    )
    
    is_uploaded = models.BooleanField(
        default=False,
        help_text='Has client uploaded this document?'
    )
    
    uploaded_document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='checklist_items',
        help_text='Link to uploaded document if available'
    )
    
    notes = models.TextField(
        blank=True,
        null=True,
        help_text='Special instructions or notes for this document'
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='checklists_created',
        help_text='Sales employee who created this checklist item'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Document Checklist Item'
        verbose_name_plural = 'Document Checklist Items'
        ordering = ['client', 'is_required', 'document_type']
        unique_together = ['client', 'document_type']
        indexes = [
            models.Index(fields=['client', 'is_uploaded']),
            models.Index(fields=['client', 'is_required']),
        ]
    
    def __str__(self):
        status = "✓" if self.is_uploaded else "✗"
        required = "(Required)" if self.is_required else "(Optional)"
        return f"{status} {self.get_document_type_display()} - {self.client.company_name} {required}"
    
    def mark_as_uploaded(self, document):
        """Mark checklist item as uploaded and link document"""
        self.is_uploaded = True
        self.uploaded_document = document
        self.save()
    
    def get_completion_percentage(client):
        """Get percentage of required documents uploaded for a client"""
        checklist = DocumentChecklist.objects.filter(client=client, is_required=True)
        if not checklist.exists():
            return 0
        total = checklist.count()
        uploaded = checklist.filter(is_uploaded=True).count()
        return int((uploaded / total) * 100)
