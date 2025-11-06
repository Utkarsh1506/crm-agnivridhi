"""
Context processor to inject pending applications count into all templates
"""
from .models import Application


def pending_applications_count(request):
    """
    Add pending_count to template context for admin/manager users
    """
    pending_count = 0
    
    if request.user.is_authenticated:
        if hasattr(request.user, 'is_admin') and (request.user.is_admin or request.user.is_manager):
            pending_count = Application.objects.filter(
                status__in=['SUBMITTED', 'UNDER_REVIEW']
            ).count()
    
    return {
        'pending_count': pending_count
    }
