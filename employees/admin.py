"""
Django Admin configuration for Employee model.
Provides admin interface for employee management.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Q
from .models import Employee, EmployeeVerificationLog, EmployeeIDSequence


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """
    Admin interface for Employee management.
    Features:
    - Read-only employee ID
    - QR code preview
    - Photo thumbnail
    - Status indicator
    - Bulk actions
    """
    
    # Display list
    list_display = [
        'employee_id_link',
        'full_name',
        'designation',
        'department',
        'status_badge',
        'date_of_joining',
        'created_at',
        'barcode_preview',
    ]
    
    # Filters and search
    list_filter = [
        'status',
        'department',
        'date_of_joining',
        'created_at',
    ]
    search_fields = [
        'employee_id',
        'full_name',
        'designation',
        'department',
    ]
    
    # Ordering
    ordering = ['-created_at']
    
    # Pagination
    list_per_page = 25
    
    # Field grouping
    fieldsets = (
        ('Employee Identification', {
            'fields': ('employee_id', 'uuid', 'full_name'),
        }),
        ('Professional Information', {
            'fields': ('designation', 'department', 'employee_photo'),
        }),
        ('Status & Timeline', {
            'fields': ('status', 'date_of_joining', 'date_of_exit'),
        }),
        ('Verification System', {
            'fields': ('barcode', 'verification_token'),
            'description': 'Auto-generated fields for employee identification.',
        }),
        ('Audit Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    # Read-only fields
    readonly_fields = [
        'employee_id',
        'uuid',
        'barcode',
        'verification_token',
        'created_at',
        'updated_at',
    ]
    
    # Actions
    actions = [
        'deactivate_employees',
        'activate_employees',
    ]
    
    def employee_id_link(self, obj):
        """Display employee ID as a clickable link."""
        url = reverse('admin:employees_employee_change', args=[obj.pk])
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.employee_id
        )
    employee_id_link.short_description = 'Employee ID'
    
    def status_badge(self, obj):
        """Display status as a colored badge."""
        colors = {
            'ACTIVE': '#28a745',    # Green
            'INACTIVE': '#dc3545',  # Red
        }
        color = colors.get(obj.status, '#6c757d')
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def barcode_preview(self, obj):
        """Display barcode thumbnail."""
        if obj.barcode:
            return format_html(
                '<img src="{}" width="80" height="50" style="border: 1px solid #ddd;" />',
                obj.barcode.url
            )
        return format_html(
            '<span style="color: #999;">Generating...</span>'
        )
    barcode_preview.short_description = 'Barcode'
    
    # Admin actions
    def deactivate_employees(self, request, queryset):
        """Bulk deactivate employees."""
        count = 0
        for employee in queryset:
            if employee.deactivate():
                count += 1
        
        self.message_user(
            request,
            f'{count} employee(s) deactivated.'
        )
    deactivate_employees.short_description = 'Deactivate selected employees'
    
    def activate_employees(self, request, queryset):
        """Bulk activate employees."""
        count = 0
        for employee in queryset:
            if employee.reactivate():
                count += 1
        
        self.message_user(
            request,
            f'{count} employee(s) activated.'
        )
    activate_employees.short_description = 'Activate selected employees'


@admin.register(EmployeeVerificationLog)
class EmployeeVerificationLogAdmin(admin.ModelAdmin):
    """
    Admin interface for verification logs.
    Audit trail of all verification attempts.
    """
    
    list_display = [
        'employee',
        'timestamp',
        'ip_address',
        'user_agent_preview',
    ]
    
    list_filter = [
        'timestamp',
        'employee',
    ]
    
    search_fields = [
        'employee__employee_id',
        'employee__full_name',
        'ip_address',
    ]
    
    readonly_fields = [
        'employee',
        'timestamp',
        'ip_address',
        'user_agent',
    ]
    
    ordering = ['-timestamp']
    list_per_page = 50
    
    def user_agent_preview(self, obj):
        """Display truncated user agent."""
        ua = obj.user_agent[:50]
        return f"{ua}..." if len(obj.user_agent) > 50 else ua
    user_agent_preview.short_description = 'User Agent'
    
    def has_add_permission(self, request):
        """Prevent manual log creation."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Prevent log deletion (audit trail)."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Prevent log modification."""
        return False


@admin.register(EmployeeIDSequence)
class EmployeeIDSequenceAdmin(admin.ModelAdmin):
    """
    Admin interface for Employee ID sequence tracker.
    """
    
    list_display = [
        'prefix',
        'last_sequence_number',
        'get_next_employee_id',
        'updated_at',
    ]
    
    readonly_fields = [
        'prefix',
        'last_sequence_number',
        'updated_at',
        'get_next_employee_id',
    ]
    
    def get_next_employee_id(self, obj):
        """Display next employee ID that will be assigned."""
        return obj.get_next_employee_id()
    get_next_employee_id.short_description = 'Next Employee ID'
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of sequence tracker."""
        return False
