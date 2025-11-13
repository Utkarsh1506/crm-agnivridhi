from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class ClientActivity(models.Model):
    """
    Client-facing activity timeline - shows updates, milestones, tasks
    This is what clients see on their dashboard to track progress
    """
    
    class ActivityType(models.TextChoices):
        # Application Process
        APPLICATION_SUBMITTED = 'APPLICATION_SUBMITTED', 'Application Submitted'
        APPLICATION_UNDER_REVIEW = 'APPLICATION_UNDER_REVIEW', 'Application Under Review'
        DOCUMENTS_REQUESTED = 'DOCUMENTS_REQUESTED', 'Documents Requested'
        DOCUMENTS_RECEIVED = 'DOCUMENTS_RECEIVED', 'Documents Received'
        APPLICATION_APPROVED = 'APPLICATION_APPROVED', 'Application Approved'
        APPLICATION_REJECTED = 'APPLICATION_REJECTED', 'Application Rejected'
        
        # Milestones
        MILESTONE_ACHIEVED = 'MILESTONE_ACHIEVED', 'Milestone Achieved'
        MEETING_SCHEDULED = 'MEETING_SCHEDULED', 'Meeting Scheduled'
        MEETING_COMPLETED = 'MEETING_COMPLETED', 'Meeting Completed'
        
        # Tasks
        TASK_ASSIGNED = 'TASK_ASSIGNED', 'Task Assigned to Client'
        TASK_COMPLETED = 'TASK_COMPLETED', 'Task Completed'
        
        # Services
        SERVICE_RECOMMENDED = 'SERVICE_RECOMMENDED', 'Service Recommended'
        SERVICE_ENROLLED = 'SERVICE_ENROLLED', 'Service Enrolled'
        
        # Schemes
        SCHEME_RECOMMENDED = 'SCHEME_RECOMMENDED', 'Scheme Recommended'
        SCHEME_APPLIED = 'SCHEME_APPLIED', 'Applied for Scheme'
        
        # Payments
        PAYMENT_RECEIVED = 'PAYMENT_RECEIVED', 'Payment Received'
        PAYMENT_PENDING = 'PAYMENT_PENDING', 'Payment Pending'
        
        # General Updates
        GENERAL_UPDATE = 'GENERAL_UPDATE', 'General Update'
        IMPORTANT_NOTICE = 'IMPORTANT_NOTICE', 'Important Notice'
    
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
    
    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'
        URGENT = 'URGENT', 'Urgent'
    
    # Basic Information
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name='activities',
        help_text=_('Client this activity belongs to')
    )
    
    activity_type = models.CharField(
        max_length=30,
        choices=ActivityType.choices,
        help_text=_('Type of activity/update')
    )
    
    title = models.CharField(
        max_length=200,
        help_text=_('Activity title (shown in timeline)')
    )
    
    description = models.TextField(
        help_text=_('Detailed description of the activity')
    )
    
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING,
        help_text=_('Current status of the activity')
    )
    
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        help_text=_('Priority level')
    )
    
    # Visibility
    is_visible_to_client = models.BooleanField(
        default=True,
        help_text=_('Should this be visible to the client?')
    )
    
    # Relationships
    application = models.ForeignKey(
        'applications.Application',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activities',
        help_text=_('Related application (if any)')
    )
    
    booking = models.ForeignKey(
        'bookings.Booking',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activities',
        help_text=_('Related booking (if any)')
    )
    
    document = models.ForeignKey(
        'documents.Document',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activities',
        help_text=_('Related document (if any)')
    )
    
    service_offering = models.ForeignKey(
        'tracking.ServiceOffering',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activities',
        help_text=_('Related service offering (if any)')
    )
    
    scheme = models.ForeignKey(
        'schemes.Scheme',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activities',
        help_text=_('Related scheme (if any)')
    )
    
    # Due Date (for tasks)
    due_date = models.DateField(
        null=True,
        blank=True,
        help_text=_('Due date (for tasks)')
    )
    
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('When the activity was completed')
    )
    
    # Metadata
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='activities_created',
        help_text=_('Sales/User who created this update')
    )
    
    notes = models.TextField(
        blank=True,
        help_text=_('Internal notes (not visible to client)')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Client Activity')
        verbose_name_plural = _('Client Activities')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['client', '-created_at']),
            models.Index(fields=['client', 'is_visible_to_client', '-created_at']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['activity_type']),
        ]
    
    def __str__(self):
        return f"{self.client.company_name} - {self.title}"
    
    def mark_completed(self):
        """Mark activity as completed"""
        from django.utils import timezone
        self.status = self.Status.COMPLETED
        self.completed_at = timezone.now()
        self.save()
    
    def get_icon(self):
        """Get Bootstrap icon for activity type"""
        icon_map = {
            'APPLICATION_SUBMITTED': 'bi-file-earmark-check',
            'APPLICATION_UNDER_REVIEW': 'bi-hourglass-split',
            'DOCUMENTS_REQUESTED': 'bi-file-earmark-arrow-up',
            'DOCUMENTS_RECEIVED': 'bi-file-earmark-check-fill',
            'APPLICATION_APPROVED': 'bi-check-circle-fill',
            'APPLICATION_REJECTED': 'bi-x-circle-fill',
            'MILESTONE_ACHIEVED': 'bi-trophy-fill',
            'MEETING_SCHEDULED': 'bi-calendar-event',
            'MEETING_COMPLETED': 'bi-calendar-check',
            'TASK_ASSIGNED': 'bi-list-task',
            'TASK_COMPLETED': 'bi-check-square-fill',
            'SERVICE_RECOMMENDED': 'bi-lightbulb',
            'SERVICE_ENROLLED': 'bi-briefcase',
            'SCHEME_RECOMMENDED': 'bi-star',
            'SCHEME_APPLIED': 'bi-send-check',
            'PAYMENT_RECEIVED': 'bi-cash-coin',
            'PAYMENT_PENDING': 'bi-clock-history',
            'GENERAL_UPDATE': 'bi-info-circle',
            'IMPORTANT_NOTICE': 'bi-exclamation-triangle-fill',
        }
        return icon_map.get(self.activity_type, 'bi-circle-fill')
    
    def get_color_class(self):
        """Get Bootstrap color class for activity type"""
        if self.status == self.Status.COMPLETED:
            return 'success'
        elif self.status == self.Status.CANCELLED:
            return 'secondary'
        elif self.priority == self.Priority.URGENT:
            return 'danger'
        elif self.priority == self.Priority.HIGH:
            return 'warning'
        elif 'APPROVED' in self.activity_type:
            return 'success'
        elif 'REJECTED' in self.activity_type:
            return 'danger'
        elif 'PENDING' in self.activity_type:
            return 'warning'
        return 'primary'


class ServiceOffering(models.Model):
    """
    Services offered by Agnivridhi beyond loans/grants
    """
    
    class ServiceType(models.TextChoices):
        WEB_DEVELOPMENT = 'WEB_DEVELOPMENT', 'Website Development'
        DIGITAL_MARKETING = 'DIGITAL_MARKETING', 'Digital Marketing'
        CERTIFICATION = 'CERTIFICATION', 'Business Certifications'
        CONSULTING = 'CONSULTING', 'Business Consulting'
        BRANDING = 'BRANDING', 'Branding & Design'
        TRAINING = 'TRAINING', 'Training & Workshops'
        LEGAL = 'LEGAL', 'Legal Services'
        ACCOUNTING = 'ACCOUNTING', 'Accounting & Taxation'
        IT_SUPPORT = 'IT_SUPPORT', 'IT Support'
        OTHER = 'OTHER', 'Other Services'
    
    # Service Details
    service_type = models.CharField(
        max_length=20,
        choices=ServiceType.choices,
        help_text=_('Type of service')
    )
    
    name = models.CharField(
        max_length=200,
        help_text=_('Service name')
    )
    
    description = models.TextField(
        help_text=_('Detailed description of the service')
    )
    
    short_description = models.CharField(
        max_length=300,
        blank=True,
        help_text=_('Short description for cards/listings')
    )
    
    # Pricing
    pricing_type = models.CharField(
        max_length=20,
        choices=[
            ('FIXED', 'Fixed Price'),
            ('HOURLY', 'Hourly Rate'),
            ('PROJECT', 'Project Based'),
            ('CUSTOM', 'Custom Quote'),
        ],
        default='CUSTOM',
        help_text=_('Pricing model')
    )
    
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Base price (if applicable)')
    )
    
    # Features
    key_features = models.JSONField(
        default=list,
        help_text=_('List of key features/deliverables')
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        help_text=_('Is this service currently offered?')
    )
    
    is_featured = models.BooleanField(
        default=False,
        help_text=_('Show in featured services?')
    )
    
    # Display Order
    display_order = models.IntegerField(
        default=0,
        help_text=_('Order in which to display (lower = higher)')
    )
    
    # Metadata
    icon = models.CharField(
        max_length=50,
        default='bi-briefcase',
        help_text=_('Bootstrap icon class')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Service Offering')
        verbose_name_plural = _('Service Offerings')
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_service_type_display()})"


class ClientServiceEnrollment(models.Model):
    """
    Track which services a client has enrolled in
    """
    
    class Status(models.TextChoices):
        RECOMMENDED = 'RECOMMENDED', 'Recommended'
        INTERESTED = 'INTERESTED', 'Interested'
        ENROLLED = 'ENROLLED', 'Enrolled'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
    
    # Relationships
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name='service_enrollments',
        help_text=_('Client enrolled in service')
    )
    
    service = models.ForeignKey(
        ServiceOffering,
        on_delete=models.CASCADE,
        related_name='enrollments',
        help_text=_('Service offered')
    )
    
    # Status
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.RECOMMENDED,
        help_text=_('Enrollment status')
    )
    
    # Pricing
    agreed_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Agreed price for this service')
    )
    
    # Dates
    enrolled_at = models.DateField(
        null=True,
        blank=True,
        help_text=_('When client enrolled')
    )
    
    expected_completion = models.DateField(
        null=True,
        blank=True,
        help_text=_('Expected completion date')
    )
    
    completed_at = models.DateField(
        null=True,
        blank=True,
        help_text=_('Actual completion date')
    )
    
    # Metadata
    recommended_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='services_recommended',
        help_text=_('Sales who recommended this service')
    )
    
    notes = models.TextField(
        blank=True,
        help_text=_('Additional notes')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Client Service Enrollment')
        verbose_name_plural = _('Client Service Enrollments')
        ordering = ['-created_at']
        unique_together = ['client', 'service']
    
    def __str__(self):
        return f"{self.client.company_name} - {self.service.name}"
