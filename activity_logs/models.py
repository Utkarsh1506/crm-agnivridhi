from django.db import models
from django.conf import settings


class ActivityLog(models.Model):
    """
    Tracks all critical actions in the CRM system
    """
    ACTION_TYPES = [
        ('CREATE', 'Created'),
        ('UPDATE', 'Updated'),
        ('DELETE', 'Deleted'),
        ('APPROVE', 'Approved'),
        ('REJECT', 'Rejected'),
        ('ASSIGN', 'Assigned'),
        ('STATUS_CHANGE', 'Status Changed'),
        ('LOGIN', 'Logged In'),
        ('LOGOUT', 'Logged Out'),
        ('EXPORT', 'Exported Data'),
        ('PAYMENT', 'Payment Action'),
    ]
    
    ENTITY_TYPES = [
        ('CLIENT', 'Client'),
        ('BOOKING', 'Booking'),
        ('APPLICATION', 'Application'),
        ('PAYMENT', 'Payment'),
        ('EDIT_REQUEST', 'Edit Request'),
        ('USER', 'User'),
        ('DOCUMENT', 'Document'),
        ('SCHEME', 'Scheme'),
        ('SERVICE', 'Service'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='activity_logs',
        help_text='User who performed the action'
    )
    
    action = models.CharField(
        max_length=20,
        choices=ACTION_TYPES,
        help_text='Type of action performed'
    )
    
    entity_type = models.CharField(
        max_length=20,
        choices=ENTITY_TYPES,
        null=True,
        blank=True,
        help_text='Type of entity affected'
    )
    
    entity_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='ID of the entity affected'
    )
    
    description = models.TextField(
        help_text='Detailed description of the action'
    )
    
    old_value = models.TextField(
        null=True,
        blank=True,
        help_text='Previous value (for updates)'
    )
    
    new_value = models.TextField(
        null=True,
        blank=True,
        help_text='New value (for updates)'
    )
    
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text='IP address of the user'
    )
    
    user_agent = models.TextField(
        null=True,
        blank=True,
        help_text='Browser/device information'
    )
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text='When the action was performed'
    )
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['entity_type', 'entity_id']),
            models.Index(fields=['action']),
            models.Index(fields=['-timestamp']),
        ]
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'
    
    def __str__(self):
        user_name = self.user.username if self.user else 'Unknown'
        return f"{user_name} - {self.get_action_display()} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    
    @classmethod
    def log_action(cls, user, action, description, entity_type=None, entity_id=None, 
                   old_value=None, new_value=None, request=None):
        """
        Convenience method to create activity logs
        
        Usage:
            ActivityLog.log_action(
                user=request.user,
                action='APPROVE',
                entity_type='PAYMENT',
                entity_id=payment.id,
                description=f'Approved payment #{payment.id}',
                request=request
            )
        """
        ip_address = None
        user_agent = None
        
        if request:
            # Get IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                ip_address = request.META.get('REMOTE_ADDR')
            
            # Get user agent
            user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        return cls.objects.create(
            user=user,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            old_value=old_value,
            new_value=new_value,
            ip_address=ip_address,
            user_agent=user_agent
        )
