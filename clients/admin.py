from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Client Admin interface
    """
    list_display = ('client_id', 'company_name', 'business_type', 'sector', 'annual_turnover', 
                    'funding_required', 'assigned_sales', 'status', 'created_at')
    list_filter = ('business_type', 'sector', 'status', 'created_at')
    search_fields = ('client_id', 'company_name', 'contact_person', 'contact_email', 'contact_phone', 
                     'registration_number', 'gst_number', 'pan_number')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Client ID', {'fields': ('client_id',)}),
        ('Company Information', {
            'fields': ('company_name', 'business_type', 'sector', 'company_age', 
                      'registration_number', 'gst_number', 'pan_number')
        }),
        ('Financial Information', {
            'fields': ('annual_turnover', 'funding_required', 'existing_loans')
        }),
        ('Contact Information', {
            'fields': ('contact_person', 'contact_email', 'contact_phone', 'alternate_phone')
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'pincode'),
            'classes': ('collapse',)
        }),
        ('Assignment & Status', {
            'fields': ('assigned_sales', 'assigned_manager', 'status')
        }),
        ('Additional Information', {
            'fields': ('business_description', 'funding_purpose', 'notes'),
            'classes': ('collapse',)
        }),
        ('User Account', {
            'fields': ('user',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('client_id', 'created_at', 'updated_at')
    
    autocomplete_fields = ['assigned_sales', 'assigned_manager', 'created_by', 'user']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Role-based filtering
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'role'):
            if request.user.role in ['ADMIN', 'MANAGER']:
                return qs
            elif request.user.role == 'SALES':
                return qs.filter(assigned_sales=request.user)
        return qs.none()
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new client
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
