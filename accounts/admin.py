from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, SiteSettings


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User Admin interface
    """
    list_display = ('username', 'email', 'role', 'designation', 'employee_id', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'employee_id')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'profile_picture')}),
        ('Role & Organization', {'fields': ('role', 'is_owner', 'designation', 'employee_id', 'manager')}),
        ('Communication Preferences', {'fields': ('whatsapp_opt_in', 'email_opt_in')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
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
        # Superusers and Admins see all users
        if request.user.is_superuser:
            return qs
        # Check role via string comparison to avoid property access issues
        if hasattr(request.user, 'role'):
            role = request.user.role.upper() if request.user.role else ''
            if role in ['ADMIN', 'OWNER']:
                return qs
            elif role == 'MANAGER':
                return qs.filter(manager=request.user)
        # Regular users see only themselves
        return qs.filter(pk=request.user.pk)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'session_cookie_age',
        'session_idle_timeout',
        'updated_at',
    )
    
    readonly_fields = ('updated_at',)

    def has_add_permission(self, request):
        # Allow only one settings instance
        if SiteSettings.objects.exists():
            return False
        return True

