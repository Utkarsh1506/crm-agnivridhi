from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import EditRequest


@admin.register(EditRequest)
class EditRequestAdmin(admin.ModelAdmin):
    """
    Edit Request Admin interface
    """
    list_display = ('entity_type', 'entity_id', 'field_name', 'status', 
                    'requested_by', 'approved_by', 'created_at')
    list_filter = ('status', 'entity_type', 'created_at')
    search_fields = ('field_name', 'requested_by__username', 'approved_by__username')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (_('Request Details'), {
            'fields': ('entity_type', 'entity_id', 'status')
        }),
        (_('Changes Requested'), {
            'fields': ('field_name', 'current_value', 'requested_value', 'reason')
        }),
        (_('Approval Details'), {
            'fields': ('approved_by', 'approval_notes', 'approval_date')
        }),
        (_('Requester'), {
            'fields': ('requested_by',)
        }),
    )
    
    readonly_fields = ('approval_date', 'created_at', 'updated_at')
    
    autocomplete_fields = ['requested_by', 'approved_by']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'role'):
            if request.user.role == 'ADMIN':
                return qs
            else:
                # Non-admins see only their own requests
                return qs.filter(requested_by=request.user)
        return qs.none()
    
    actions = ['approve_requests', 'reject_requests']
    
    def approve_requests(self, request, queryset):
        for edit_request in queryset.filter(status='PENDING'):
            edit_request.approve(request.user, 'Approved via admin action')
        self.message_user(request, f"{queryset.count()} requests approved.")
    approve_requests.short_description = "Approve selected requests"
    
    def reject_requests(self, request, queryset):
        for edit_request in queryset.filter(status='PENDING'):
            edit_request.reject(request.user, 'Rejected via admin action')
        self.message_user(request, f"{queryset.count()} requests rejected.")
    reject_requests.short_description = "Reject selected requests"
