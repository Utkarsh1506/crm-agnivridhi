from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class EditRequest(models.Model):
    """
    Edit/Update requests that require Admin approval
    """
    
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending Approval')
        APPROVED = 'APPROVED', _('Approved')
        REJECTED = 'REJECTED', _('Rejected')
        APPLIED = 'APPLIED', _('Applied Successfully')
    
    class EntityType(models.TextChoices):
        CLIENT = 'CLIENT', _('Client')
        BOOKING = 'BOOKING', _('Booking')
        APPLICATION = 'APPLICATION', _('Application')
        USER = 'USER', _('User')
    
    # Request Details
    entity_type = models.CharField(
        max_length=20,
        choices=EntityType.choices,
        help_text=_('Type of entity being edited')
    )
    
    entity_id = models.IntegerField(
        help_text=_('ID of the entity being edited')
    )
    
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING,
        help_text=_('Request status')
    )
    
    # Changes Requested
    field_name = models.CharField(
        max_length=100,
        help_text=_('Name of the field to be changed')
    )
    
    current_value = models.TextField(
        blank=True,
        null=True,
        help_text=_('Current value of the field')
    )
    
    requested_value = models.TextField(
        help_text=_('Requested new value')
    )
    
    reason = models.TextField(
        help_text=_('Reason for requesting the change')
    )
    
    # Approval Details
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_edit_requests',
        limit_choices_to={'role': 'ADMIN'},
        help_text=_('Admin who approved/rejected the request')
    )
    
    approval_notes = models.TextField(
        blank=True,
        null=True,
        help_text=_('Admin notes on approval/rejection')
    )
    
    approval_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Date when request was approved/rejected')
    )
    
    # Requester
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='edit_requests_made',
        help_text=_('User who made the request')
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_('Request creation timestamp')
    )
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Edit Request')
        verbose_name_plural = _('Edit Requests')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['entity_type', 'entity_id']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['requested_by', 'status']),
        ]
    
    def __str__(self):
        return f"Edit Request - {self.entity_type} #{self.entity_id} - {self.field_name}"
    
    def approve(self, admin_user, notes=''):
        """Approve the edit request"""
        from django.utils import timezone
        self.status = self.Status.APPROVED
        self.approved_by = admin_user
        self.approval_notes = notes
        self.approval_date = timezone.now()
        self.save()
    
    def reject(self, admin_user, notes=''):
        """Reject the edit request"""
        from django.utils import timezone
        self.status = self.Status.REJECTED
        self.approved_by = admin_user
        self.approval_notes = notes
        self.approval_date = timezone.now()
        self.save()
    
    def apply_changes(self):
        """Apply the approved changes to the entity"""
        if self.status != self.Status.APPROVED:
            raise ValueError("Only approved requests can be applied")
        
        # Get the model and instance
        from django.apps import apps
        model = apps.get_model('clients' if self.entity_type == 'CLIENT' else 
                               'bookings' if self.entity_type == 'BOOKING' else
                               'applications' if self.entity_type == 'APPLICATION' else
                               'accounts', 
                               self.entity_type.capitalize())
        
        instance = model.objects.get(pk=self.entity_id)
        setattr(instance, self.field_name, self.requested_value)
        instance.save()
        
        self.status = self.Status.APPLIED
        self.save()
