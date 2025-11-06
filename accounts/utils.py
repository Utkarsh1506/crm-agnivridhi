"""
Utility functions for accounts app
"""
import csv
from io import StringIO
from django.http import HttpResponse
from datetime import datetime
from .constants import (
    ROLE_SUPERUSER, ROLE_OWNER, ROLE_ADMIN,
    ROLE_MANAGER, ROLE_SALES, ROLE_CLIENT
)


def role_required(*allowed_roles):
    """
    Generic decorator for role-based access control.
    
    Usage:
        @role_required('admin', 'manager')
        def my_view(request):
            ...
    
    Args:
        *allowed_roles: Variable number of role strings (lowercase)
    
    Returns:
        Decorator function that checks user role
    """
    from functools import wraps
    from django.shortcuts import redirect
    from django.http import HttpResponseForbidden
    from django.contrib import messages
    
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Please log in to access this page.")
                return redirect("accounts:login")
            
            # Normalize role for comparison (lowercase)
            user_role = request.user.normalized_role
            
            # Superusers can access everything
            if request.user.is_superuser or user_role == ROLE_SUPERUSER:
                return view_func(request, *args, **kwargs)
            
            # Check if user's role is in allowed roles
            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, f"Access Denied: Your role ({user_role}) doesn't have permission to view this page.")
                return HttpResponseForbidden(
                    "<h3>403 - Access Denied</h3>"
                    "<p>You don't have permission to access this page.</p>"
                    "<p><a href='/dashboard/'>Return to Dashboard</a></p>"
                )
        return wrapper
    return decorator


# Convenience decorators for specific roles
def superuser_required(view_func):
    """Restrict view to superusers only"""
    return role_required(ROLE_SUPERUSER)(view_func)


def owner_required(view_func):
    """Restrict view to owners only"""
    return role_required(ROLE_OWNER)(view_func)


def admin_required(view_func):
    """Restrict view to admins and above"""
    return role_required(ROLE_ADMIN, ROLE_OWNER, ROLE_SUPERUSER)(view_func)


def manager_required(view_func):
    """Restrict view to managers and above"""
    return role_required(ROLE_MANAGER, ROLE_ADMIN, ROLE_OWNER, ROLE_SUPERUSER)(view_func)


def sales_required(view_func):
    """Restrict view to sales and above"""
    return role_required(ROLE_SALES, ROLE_MANAGER, ROLE_ADMIN, ROLE_OWNER, ROLE_SUPERUSER)(view_func)


def client_required(view_func):
    """Restrict view to clients only"""
    return role_required(ROLE_CLIENT)(view_func)


def staff_required(view_func):
    """Restrict view to any staff member (sales, manager, admin, owner, superuser)"""
    return role_required(ROLE_SALES, ROLE_MANAGER, ROLE_ADMIN, ROLE_OWNER, ROLE_SUPERUSER)(view_func)


def export_to_csv(queryset, fields, filename_prefix='export'):
    """
    Generic function to export queryset to CSV
    
    Args:
        queryset: Django queryset to export
        fields: List of field names to include
        filename_prefix: Prefix for the downloaded filename
    
    Returns:
        HttpResponse with CSV content
    """
    response = HttpResponse(content_type='text/csv')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    response['Content-Disposition'] = f'attachment; filename="{filename_prefix}_{timestamp}.csv"'
    
    writer = csv.writer(response)
    
    # Write header row
    headers = []
    for field in fields:
        if isinstance(field, dict):
            headers.append(field.get('label', field.get('name', '')))
        else:
            headers.append(field.replace('_', ' ').title())
    writer.writerow(headers)
    
    # Write data rows
    for obj in queryset:
        row = []
        for field in fields:
            if isinstance(field, dict):
                field_name = field.get('name')
                accessor = field.get('accessor')
                if accessor:
                    # Custom accessor function
                    value = accessor(obj)
                else:
                    # Standard field access
                    value = getattr(obj, field_name, '')
            else:
                value = getattr(obj, field, '')
            
            # Handle special types
            if hasattr(value, 'all'):  # ManyToMany or reverse FK
                value = ', '.join(str(v) for v in value.all())
            elif callable(value):
                value = value()
            
            row.append(str(value))
        writer.writerow(row)
    
    return response


def get_field_value(obj, field_path):
    """
    Get nested field value from object using dot notation
    Example: 'client.company_name' or 'assigned_to.get_full_name'
    """
    parts = field_path.split('.')
    value = obj
    for part in parts:
        if hasattr(value, part):
            value = getattr(value, part)
            if callable(value):
                value = value()
        else:
            return ''
    return value
