from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
    Document Admin interface
    """
    list_display = ('title', 'document_type', 'client', 'status', 
                    'file_format', 'download_count', 'created_at')
    list_filter = ('document_type', 'status', 'file_format', 'created_at')
    search_fields = ('title', 'client__company_name', 'description')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Document Details', {
            'fields': ('document_type', 'title', 'description', 'status')
        }),
        ('Relationships', {
            'fields': ('client', 'application', 'booking')
        }),
        ('File Details', {
            'fields': ('file', 'file_size', 'file_format')
        }),
        ('Generation Details', {
            'fields': ('generated_by', 'template_used', 'generation_data'),
            'classes': ('collapse',)
        }),
        ('Download Tracking', {
            'fields': ('download_count', 'last_downloaded_at', 'last_downloaded_by'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('file_size', 'file_format', 'download_count', 
                       'last_downloaded_at', 'created_at', 'updated_at')
    
    autocomplete_fields = ['client', 'application', 'booking', 'generated_by', 'last_downloaded_by']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'role'):
            if request.user.role in ['ADMIN', 'MANAGER']:
                return qs
            elif request.user.role == 'SALES':
                return qs.filter(client__assigned_sales=request.user)
        return qs.none()
