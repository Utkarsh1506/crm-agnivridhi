from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .constants import (
    ROLE_ADMIN, ROLE_MANAGER, ROLE_SALES, ROLE_CLIENT,
    ROLE_OWNER, ROLE_SUPERUSER
)

class User(AbstractUser):
    """
    Custom User model with role-based access control
    Roles: Superuser, Owner, Admin, Manager, Sales Employee, Client
    """
    
    class Role(models.TextChoices):
        SUPERUSER = ROLE_SUPERUSER.upper(), _('Superuser')
        OWNER = ROLE_OWNER.upper(), _('Owner')
        ADMIN = ROLE_ADMIN.upper(), _('Admin')
        MANAGER = ROLE_MANAGER.upper(), _('Manager')
        SALES = ROLE_SALES.upper(), _('Sales Employee')
        CLIENT = ROLE_CLIENT.upper(), _('Client')
    
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
        return self.role == self.Role.ADMIN.value or self.role == 'ADMIN'
    
    @property
    def is_manager(self):
        """Check if user is Manager"""
        return self.role == self.Role.MANAGER.value or self.role == 'MANAGER'
    
    @property
    def is_sales(self):
        """Check if user is Sales Employee"""
        return self.role == self.Role.SALES.value or self.role == 'SALES'
    
    @property
    def is_client(self):
        """Check if user is Client"""
        return self.role == self.Role.CLIENT.value or self.role == 'CLIENT'
    
    @property
    def is_staff_member(self):
        """Check if user is staff (Admin, Manager, or Sales)"""
        return self.role in [self.Role.ADMIN.value, self.Role.MANAGER.value, self.Role.SALES.value, 'ADMIN', 'MANAGER', 'SALES']
    
    @property
    def normalized_role(self):
        """Return lowercase role string for consistent comparisons"""
        return self.role.lower() if self.role else 'client'
    
    def can_manage_users(self):
        """Check if user can create/edit other users"""
        return self.role in [self.Role.ADMIN, self.Role.MANAGER]
    
    def can_approve_edits(self):
        """Check if user can approve edit requests"""
        return self.role == self.Role.ADMIN
    
    def save(self, *args, **kwargs):
        """Override save to set staff status based on role"""
        if self.role in [self.Role.ADMIN.value, self.Role.MANAGER.value, self.Role.SALES.value, 'ADMIN', 'MANAGER', 'SALES', 'SUPERUSER', 'OWNER']:
            self.is_staff = True
        else:
            self.is_staff = False
        
        # Superusers and owners remain staff regardless of role
        if self.is_superuser or self.is_owner:
            self.is_staff = True
        
        super().save(*args, **kwargs)


class SiteSettings(models.Model):
    """Editable site-wide settings exposed in Django Admin.

    Provides admin UI to configure session/timeouts and security toggles at runtime.
    Middleware can read these values per request to enforce idle timeout and
    per-session expiry without restarting the server.
    """

    # Session configuration
    session_cookie_age = models.PositiveIntegerField(
        default=86400,
        help_text=_('Session lifetime in seconds (e.g., 86400 = 1 day).')
    )
    session_expire_at_browser_close = models.BooleanField(
        default=False,
        help_text=_('Expire session when browser closes (overrides cookie age).')
    )
    session_idle_timeout = models.PositiveIntegerField(
        default=1800,
        help_text=_('Auto logout after this many seconds of inactivity (0 to disable).')
    )

    # Security toggles (informational; some require server settings/HTTPS)
    session_cookie_secure = models.BooleanField(
        default=False,
        help_text=_('Mark session cookie as Secure (HTTPS only). Enable in production over HTTPS.')
    )
    csrf_cookie_secure = models.BooleanField(
        default=False,
        help_text=_('Mark CSRF cookie as Secure (HTTPS only). Enable in production over HTTPS.')
    )
    secure_ssl_redirect = models.BooleanField(
        default=False,
        help_text=_('Redirect all HTTP requests to HTTPS (requires proxy/HTTPS).')
    )
    secure_hsts_seconds = models.PositiveIntegerField(
        default=0,
        help_text=_('HSTS max-age in seconds (0 disables). Enable with caution in production.')
    )
    secure_hsts_include_subdomains = models.BooleanField(
        default=False,
        help_text=_('Include subdomains in HSTS policy.')
    )
    secure_hsts_preload = models.BooleanField(
        default=False,
        help_text=_('Enable HSTS preload (submit domain to browser preload lists).')
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Site Settings')
        verbose_name_plural = _('Site Settings')

    def __str__(self):
        return 'Site Settings'

    @classmethod
    def get(cls):
        """Return the single settings row or None if not created yet."""
        return cls.objects.first()
