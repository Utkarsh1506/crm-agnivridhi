"""
Context processors for common template variables across the app.
"""
from django.urls import reverse


def dashboard_link(request):
    """
    Provide the correct dashboard URL based on the user's role.
    Avoids repeated redirects when navigating back to dashboard.
    """
    if not request.user.is_authenticated:
        return {'dashboard_url': reverse('accounts:login')}
    
    user = request.user
    
    # Owners (either role OWNER or admin flagged is_owner) get Owner Dashboard
    if getattr(user, 'is_owner', False) or getattr(user, 'role', None) == 'OWNER':
        return {'dashboard_url': reverse('accounts:owner_dashboard')}
    
    # Superuser gets dedicated dashboard
    if user.is_superuser:
        return {'dashboard_url': reverse('accounts:superuser_dashboard')}
    
    role = getattr(user, 'role', None)
    if role == 'ADMIN':
        return {'dashboard_url': reverse('accounts:admin_dashboard')}
    elif role == 'MANAGER':
        return {'dashboard_url': reverse('accounts:manager_dashboard')}
    elif role == 'SALES':
        return {'dashboard_url': reverse('accounts:sales_dashboard')}
    elif role == 'CLIENT':
        return {'dashboard_url': reverse('accounts:client_portal')}
    
    # Fallback to generic dashboard
    return {'dashboard_url': reverse('accounts:dashboard')}
