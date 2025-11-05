from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """
    Application Admin interface
    """
    list_display = ('application_id', 'client', 'scheme', 'applied_amount', 
                    'status', 'assigned_to', 'application_date')
    list_filter = ('status', 'application_date', 'submission_date')
    search_fields = ('application_id', 'client__company_name', 'scheme__name', 
                     'government_ref_number')
    ordering = ('-application_date',)
    date_hierarchy = 'application_date'
    
    fieldsets = (
        (_('Application ID'), {'fields': ('application_id',)}),
        (_('Application Details'), {
            'fields': ('client', 'scheme', 'status', 'applied_amount', 'approved_amount')
        }),
        (_('Dates'), {
            'fields': ('application_date', 'submission_date', 'approval_date', 'rejection_date')
        }),
        (_('Purpose & Documents'), {
            'fields': ('purpose', 'documents_submitted')
        }),
        (_('Government Reference'), {
            'fields': ('government_ref_number',)
        }),
        (_('Assignment & Notes'), {
            'fields': ('assigned_to', 'internal_notes', 'rejection_reason')
        }),
        (_('Timeline'), {
            'fields': ('timeline',),
            'classes': ('collapse',)
        }),
        (_('Metadata'), {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('application_id', 'application_date', 'timeline', 'created_at', 'updated_at')
    
    autocomplete_fields = ['client', 'scheme', 'assigned_to', 'created_by']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'role'):
            if request.user.role in ['ADMIN', 'MANAGER']:
                return qs
            elif request.user.role == 'SALES':
                return qs.filter(assigned_to=request.user)
        return qs.none()
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
