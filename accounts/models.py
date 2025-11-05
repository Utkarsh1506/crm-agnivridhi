from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom User model with role-based access control
    Roles: Admin, Manager, Sales Employee, Client
    """
    
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        MANAGER = 'MANAGER', _('Manager')
        SALES = 'SALES', _('Sales Employee')
        CLIENT = 'CLIENT', _('Client')
    
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CLIENT,
        help_text=_('User role determines access permissions')
    )
    
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text=_('Contact phone number with country code')
    )
    
    designation = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_('Job designation/title')
    )
    
    employee_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True,
        help_text=_('Unique employee ID for staff members')
    )
    
    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='team_members',
        limit_choices_to={'role__in': ['ADMIN', 'MANAGER']},
        help_text=_('Manager assigned to this user')
    )
    
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        help_text=_('User profile picture')
    )
    
    whatsapp_opt_in = models.BooleanField(
        default=True,
        help_text=_('User consent for WhatsApp notifications')
    )
    
    email_opt_in = models.BooleanField(
        default=True,
        help_text=_('User consent for email notifications')
    )
    
    is_owner = models.BooleanField(
        default=False,
        help_text=_('Marks this Admin as the company owner for special dashboard access')
    )
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['role', 'is_active']),
            models.Index(fields=['employee_id']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def get_full_name(self):
        """Returns the full name of the user"""
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    @property
    def is_admin(self):
        """Check if user is Admin"""
        return self.role == self.Role.ADMIN
    
    @property
    def is_manager(self):
        """Check if user is Manager"""
        return self.role == self.Role.MANAGER
    
    @property
    def is_sales(self):
        """Check if user is Sales Employee"""
        return self.role == self.Role.SALES
    
    @property
    def is_client(self):
        """Check if user is Client"""
        return self.role == self.Role.CLIENT
    
    @property
    def is_staff_member(self):
        """Check if user is staff (Admin, Manager, or Sales)"""
        return self.role in [self.Role.ADMIN, self.Role.MANAGER, self.Role.SALES]
    
    def can_manage_users(self):
        """Check if user can create/edit other users"""
        return self.role in [self.Role.ADMIN, self.Role.MANAGER]
    
    def can_approve_edits(self):
        """Check if user can approve edit requests"""
        return self.role == self.Role.ADMIN
    
    def save(self, *args, **kwargs):
        """Override save to set staff status based on role"""
        if self.role in [self.Role.ADMIN, self.Role.MANAGER, self.Role.SALES]:
            self.is_staff = True
        else:
            self.is_staff = False
        
        # Do NOT auto-elevate Admin role to superuser.
        # Keep superuser separate so tech team can use it independently.
        # Ensure superusers remain staff regardless of role.
        if self.is_superuser:
            self.is_staff = True
        
        super().save(*args, **kwargs)
