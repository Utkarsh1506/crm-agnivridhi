from django.contrib import admin
from .models import ClientActivity, ServiceOffering, ClientServiceEnrollment


@admin.register(ClientActivity)
class ClientActivityAdmin(admin.ModelAdmin):
    """
    Client Activity Admin
    """
    list_display = ('client', 'activity_type', 'title', 'status', 'priority', 
                    'is_visible_to_client', 'created_by', 'created_at')
    list_filter = ('activity_type', 'status', 'priority', 'is_visible_to_client', 'created_at')
    search_fields = ('client__company_name', 'title', 'description')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('client', 'activity_type', 'title', 'description')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'is_visible_to_client')
        }),
        ('Relationships', {
            'fields': ('application', 'booking', 'document', 'service_offering', 'scheme'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('due_date', 'completed_at')
        }),
        ('Metadata', {
            'fields': ('created_by', 'notes')
        }),
    )
    
    readonly_fields = ('completed_at', 'created_at', 'updated_at')
    autocomplete_fields = ['client', 'application', 'booking', 'document', 
                           'service_offering', 'scheme', 'created_by']
    
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


@admin.register(ServiceOffering)
class ServiceOfferingAdmin(admin.ModelAdmin):
    """
    Service Offering Admin
    """
    list_display = ('name', 'service_type', 'pricing_type', 'base_price', 
                    'is_active', 'is_featured', 'display_order')
    list_filter = ('service_type', 'pricing_type', 'is_active', 'is_featured')
    search_fields = ('name', 'description', 'short_description')
    ordering = ('display_order', 'name')
    
    fieldsets = (
        ('Service Details', {
            'fields': ('service_type', 'name', 'description', 'short_description', 'icon')
        }),
        ('Pricing', {
            'fields': ('pricing_type', 'base_price')
        }),
        ('Features', {
            'fields': ('key_features',)
        }),
        ('Display Options', {
            'fields': ('is_active', 'is_featured', 'display_order')
        }),
    )


@admin.register(ClientServiceEnrollment)
class ClientServiceEnrollmentAdmin(admin.ModelAdmin):
    """
    Client Service Enrollment Admin
    """
    list_display = ('client', 'service', 'status', 'agreed_price', 
                    'enrolled_at', 'expected_completion', 'recommended_by')
    list_filter = ('status', 'enrolled_at', 'expected_completion')
    search_fields = ('client__company_name', 'service__name', 'notes')
    ordering = ('-created_at',)
    date_hierarchy = 'enrolled_at'
    
    fieldsets = (
        ('Enrollment Details', {
            'fields': ('client', 'service', 'status')
        }),
        ('Pricing', {
            'fields': ('agreed_price',)
        }),
        ('Dates', {
            'fields': ('enrolled_at', 'expected_completion', 'completed_at')
        }),
        ('Metadata', {
            'fields': ('recommended_by', 'notes')
        }),
    )
    
    readonly_fields = ('completed_at', 'created_at', 'updated_at')
    autocomplete_fields = ['client', 'service', 'recommended_by']
    
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
