from django.contrib import admin
from .models import Client, ClientCredential


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Client Admin interface
    """
    list_display = (
        'client_id', 'company_name', 'business_type', 'sector', 'annual_turnover',
        'funding_required', 'total_pitched_amount', 'received_amount', 'pending_amount',
        'assigned_sales', 'status', 'created_at'
    )
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
        ('Revenue Tracking', {
            'fields': ('total_pitched_amount', 'received_amount', 'pending_amount')
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


@admin.register(ClientCredential)
class ClientCredentialAdmin(admin.ModelAdmin):
    """
    ClientCredential Admin interface - for viewing auto-generated login credentials
    """
    list_display = ('client', 'username', 'email', 'is_sent', 'created_at', 'sent_at', 'sent_by')
    list_filter = ('is_sent', 'created_at', 'sent_at')
    search_fields = ('client__company_name', 'username', 'email')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Client & Credentials', {
            'fields': ('client', 'username', 'email', 'plain_password')
        }),
        ('Status', {
            'fields': ('is_sent', 'sent_at', 'sent_by')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at')
        }),
    )
    
    readonly_fields = ('client', 'username', 'email', 'plain_password', 'sent_at', 'sent_by', 'created_by', 'created_at')
    
    def has_add_permission(self, request):
        # Credentials are auto-generated, can't manually add
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Can delete old credentials if needed
        return request.user.is_superuser
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only superuser and admin/owner can view
        if request.user.is_superuser or (hasattr(request.user, 'role') and request.user.role in ['ADMIN', 'OWNER']):
            return qs
        return qs.none()
