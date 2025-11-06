from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, SiteSettings


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User Admin interface
    """
    list_display = ('username', 'email', 'role', 'is_owner', 'designation', 'employee_id', 'is_active', 'is_staff')
    list_filter = ('role', 'is_owner', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'employee_id')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'email', 'phone', 'profile_picture')}),
    (_('Role & Organization'), {'fields': ('role', 'is_owner', 'designation', 'employee_id', 'manager')}),
        (_('Communication Preferences'), {'fields': ('whatsapp_opt_in', 'email_opt_in')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        (_('Important Dates'), {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'phone'),
        }),
    )
    
    readonly_fields = ('last_login', 'date_joined')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Admins see all users, Managers see their team
        if request.user.is_admin:
            return qs
        elif request.user.is_manager:
            return qs.filter(manager=request.user)
        return qs.filter(pk=request.user.pk)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'session_cookie_age',
        'session_expire_at_browser_close',
        'session_idle_timeout',
        'session_cookie_secure',
        'csrf_cookie_secure',
        'secure_ssl_redirect',
        'secure_hsts_seconds',
        'updated_at',
    )
    fieldsets = (
        (_('Session Settings'), {
            'fields': (
                'session_cookie_age',
                'session_expire_at_browser_close',
                'session_idle_timeout',
            )
        }),
        (_('Security Settings (HTTPS)'), {
            'classes': ('collapse',),
            'fields': (
                'session_cookie_secure',
                'csrf_cookie_secure',
                'secure_ssl_redirect',
                'secure_hsts_seconds',
                'secure_hsts_include_subdomains',
                'secure_hsts_preload',
            )
        }),
        (_('Metadata'), {
            'classes': ('collapse',),
            'fields': ('updated_at',),
        })
    )
    readonly_fields = ('updated_at',)

    def has_add_permission(self, request):
        # Allow only one settings instance
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)

