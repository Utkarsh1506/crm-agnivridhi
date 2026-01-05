"""
Employee Model for Agnivridhi CRM.
Manages employee records, ID generation, and verification system.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import uuid


class Employee(models.Model):
    """
    Employee model for the Identity & Verification System.
    
    Features:
    - Auto-generated unique employee IDs (0101 format)
    - QR code generation support
    - Employee photo management
    - Active/Inactive status tracking
    - Audit trail with timestamps
    """
    
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', _('Active')
        INACTIVE = 'INACTIVE', _('Inactive')
    
    # Primary Keys & IDs
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text=_('Unique identifier for internal tracking')
    )
    employee_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        db_index=True,
        help_text=_('Auto-generated unique employee ID (e.g., 0101)')
    )
    
    # Employee Information
    full_name = models.CharField(
        max_length=200,
        db_index=True,
        help_text=_('Full legal name of the employee')
    )
    designation = models.CharField(
        max_length=100,
        help_text=_('Job title/designation')
    )
    department = models.CharField(
        max_length=100,
        db_index=True,
        help_text=_('Department name (e.g., Sales, HR, Engineering)')
    )
    
    # Photo & Documents
    employee_photo = models.ImageField(
        upload_to='employees/photos/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],
        help_text=_('Employee portrait photo (JPG, PNG recommended)')
    )
    
    # Status & Timeline
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
        help_text=_('Employment status')
    )
    date_of_joining = models.DateField(
        default=timezone.now,
        help_text=_('Employee joining date')
    )
    date_of_exit = models.DateField(
        null=True,
        blank=True,
        help_text=_('Employee exit/termination date (if applicable)')
    )
    
    # Barcode & Verification
    barcode = models.ImageField(
        upload_to='employees/barcodes/%Y/%m/',
        editable=False,
        null=True,
        blank=True,
        help_text=_('Auto-generated barcode for employee identification')
    )
    verification_token = models.CharField(
        max_length=100,
        unique=True,
        editable=False,
        db_index=True,
        help_text=_('Unique token for verification endpoint')
    )
    
    # Audit Trail
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_('Record creation timestamp')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_('Record last update timestamp')
    )
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees_created',
        help_text=_('User who created this employee record')
    )
    
    class Meta:
        db_table = 'employee'
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['employee_id']),
            models.Index(fields=['status']),
            models.Index(fields=['department']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"
    
    def get_verification_url(self):
        """Generate the public verification URL for this employee."""
        return f"https://agnivridhi.com/employee/verify/{self.employee_id}/"
    
    def get_qr_content(self):
        """
        Return the content to be encoded in the barcode.
        This contains the employee ID for easy scanning.
        """
        return self.employee_id
    
    def is_active_employee(self):
        """Check if employee is currently active."""
        return self.status == self.Status.ACTIVE
    
    def can_be_deactivated(self):
        """Determine if employee can be deactivated."""
        return self.status == self.Status.ACTIVE
    
    def deactivate(self, date_of_exit=None):
        """
        Safely deactivate an employee.
        
        Args:
            date_of_exit: Date of exit (defaults to today)
        """
        if not self.can_be_deactivated():
            return False
        
        self.status = self.Status.INACTIVE
        self.date_of_exit = date_of_exit or timezone.now().date()
        self.save(update_fields=['status', 'date_of_exit', 'updated_at'])
        return True
    
    def reactivate(self):
        """
        Reactivate a previously inactive employee.
        """
        if self.status == self.Status.INACTIVE:
            self.status = self.Status.ACTIVE
            self.date_of_exit = None
            self.save(update_fields=['status', 'date_of_exit', 'updated_at'])
            return True
        return False


class EmployeeIDSequence(models.Model):
    """
    Tracker for Employee ID sequence.
    Ensures thread-safe, auto-incrementing employee ID generation.
    """
    last_sequence_number = models.IntegerField(
        default=0,
        help_text=_('Last assigned sequence number for employee IDs')
    )
    prefix = models.CharField(
        max_length=20,
        default='AGN-EMP-',
        editable=False,
        help_text=_('Prefix for employee IDs')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_('Last update timestamp')
    )
    
    class Meta:
        db_table = 'employee_id_sequence'
        verbose_name = 'Employee ID Sequence'
        verbose_name_plural = 'Employee ID Sequences'
    
    def __str__(self):
        return f"Employee ID Sequence (Next: {self.get_next_employee_id()})"
    
    def get_next_employee_id(self):
        """
        Generate the next employee ID in sequence.
        Format: AGN-EMP-001, AGN-EMP-002, etc.
        
        Returns:
            str: Next employee ID
        """
        self.last_sequence_number += 1
        return f"{self.prefix}{self.last_sequence_number:03d}"


class EmployeeVerificationLog(models.Model):
    """
    Audit log for employee verification attempts.
    Tracks public verification page access for security monitoring.
    """
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='verification_logs',
        help_text=_('Employee being verified')
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text=_('Verification attempt timestamp')
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text=_('IP address of verification attempt')
    )
    user_agent = models.TextField(
        blank=True,
        help_text=_('Browser user agent')
    )
    
    class Meta:
        db_table = 'employee_verification_log'
        verbose_name = 'Employee Verification Log'
        verbose_name_plural = 'Employee Verification Logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['employee', 'timestamp']),
        ]
    
    def __str__(self):
        return f"Verification of {self.employee.employee_id} at {self.timestamp}"
