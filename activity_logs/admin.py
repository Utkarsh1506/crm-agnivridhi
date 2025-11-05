from django.contrib import admin
from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'entity_type', 'entity_id', 'description_short', 'timestamp']
    list_filter = ['action', 'entity_type', 'timestamp', 'user']
    search_fields = ['description', 'user__username', 'user__email']
    readonly_fields = ['user', 'action', 'entity_type', 'entity_id', 'description', 
                       'old_value', 'new_value', 'ip_address', 'user_agent', 'timestamp']
    date_hierarchy = 'timestamp'
    
    def description_short(self, obj):
        """Truncate description for list view"""
        if len(obj.description) > 50:
            return obj.description[:50] + '...'
        return obj.description
    description_short.short_description = 'Description'
    
    def has_add_permission(self, request):
        """Activity logs should only be created programmatically"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Only superusers can delete activity logs"""
        return request.user.is_superuser
