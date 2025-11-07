from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import secrets
import string

class Application(models.Model):
    """
    Client applications to government schemes
    """
    
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', _('Draft')
        SUBMITTED = 'SUBMITTED', _('Submitted to Government')
        UNDER_REVIEW = 'UNDER_REVIEW', _('Under Review')
        APPROVED = 'APPROVED', _('Approved')
        REJECTED = 'REJECTED', _('Rejected')
        WITHDRAWN = 'WITHDRAWN', _('Withdrawn')
        ON_HOLD = 'ON_HOLD', _('On Hold')
    
    # Application ID
    application_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        help_text=_('Auto-generated unique application ID')
    )
    
    # Relationships
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name='applications',
        help_text=_('Client making the application')
    )
    
    scheme = models.ForeignKey(
        'schemes.Scheme',
        on_delete=models.PROTECT,
        related_name='applications',
        help_text=_('Scheme being applied to')
    )
    
    # Application Details
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.DRAFT,
        help_text=_('Current application status')
    )
    
    applied_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text=_('Amount applied for (in lakhs)')
    )
    
    approved_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Amount approved (in lakhs)')
    )
    
    # Dates
    application_date = models.DateField(
        auto_now_add=True,
        help_text=_('Date when application was created')
    )
    
    submission_date = models.DateField(
        null=True,
        blank=True,
        help_text=_('Date when application was submitted to government')
    )
    
    approval_date = models.DateField(
        null=True,
        blank=True,
        help_text=_('Date when application was approved')
    )
    
    rejection_date = models.DateField(
        null=True,
        blank=True,
        help_text=_('Date when application was rejected')
    )
    
    # Documents
    documents_submitted = models.BooleanField(
        default=False,
        help_text=_('All required documents submitted')
    )
    
    # Notes
    purpose = models.TextField(
        help_text=_('Purpose/justification for the funding')
    )
    
    internal_notes = models.TextField(
        blank=True,
        null=True,
        help_text=_('Internal notes (not visible to client)')
    )
    
    rejection_reason = models.TextField(
        blank=True,
        null=True,
        help_text=_('Reason for rejection (if applicable)')
    )
    
    # Government References
    government_ref_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_('Government reference/acknowledgment number')
    )
    
    # Assignment
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_applications',
        limit_choices_to={'role__in': ['ADMIN', 'MANAGER', 'SALES']},
        help_text=_('Staff member handling this application')
    )
    
    # Timeline Tracking
    timeline = models.JSONField(
        default=list,
        help_text=_('Application status timeline with timestamps')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='applications_created',
        help_text=_('User who created this application')
    )
    
    class Meta:
        verbose_name = _('Application')
        verbose_name_plural = _('Applications')
        ordering = ['-application_date']
        indexes = [
            models.Index(fields=['application_id']),
            models.Index(fields=['client', 'status']),
            models.Index(fields=['scheme', 'status']),
            models.Index(fields=['assigned_to', 'status']),
            models.Index(fields=['-application_date']),
        ]
        # Note: Removed unique_together constraint to allow multiple applications
        # for the same client-scheme combination (e.g., reapply after rejection)
    
    def __str__(self):
        return f"{self.application_id} - {self.client.company_name} - {self.scheme.name}"
    
    def save(self, *args, **kwargs):
        """Generate application ID and track status changes"""
        if not self.application_id:
            self.application_id = self.generate_application_id()
        
        # Track status changes in timeline
        if self.pk:  # Existing record
            old_instance = Application.objects.get(pk=self.pk)
            if old_instance.status != self.status:
                self.add_timeline_entry(self.status)
        
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_application_id():
        """Generate unique application ID: APP-YYYYMMDD-XXXX"""
        from datetime import datetime
        date_str = datetime.now().strftime('%Y%m%d')
        random_str = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        return f"APP-{date_str}-{random_str}"
    
    def add_timeline_entry(self, status):
        """Add status change to timeline"""
        from django.utils import timezone
        entry = {
            'status': status,
            'timestamp': timezone.now().isoformat(),
            'status_display': self.get_status_display()
        }
        self.timeline.append(entry)
    
    def get_eligibility_check(self):
        """Check if client is eligible for this scheme"""
        return self.scheme.check_client_eligibility(self.client)
    
    def get_days_in_process(self):
        """Calculate days since application submission"""
        from django.utils import timezone
        if self.submission_date:
            return (timezone.now().date() - self.submission_date).days
        return 0
    
    def is_pending(self):
        """Check if application is in pending status"""
        return self.status in ['DRAFT', 'SUBMITTED', 'UNDER_REVIEW', 'ON_HOLD']
