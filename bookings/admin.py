from django.contrib import admin
from .models import Service, Booking


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    Service Admin interface
    """
    list_display = ('name', 'category', 'price', 'duration_days', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('category', 'name')
    
    fieldsets = (
        ('Service Information', {
            'fields': ('name', 'category', 'short_description', 'description')
        }),
        ('Pricing & Duration', {
            'fields': ('price', 'duration_days')
        }),
        ('Features & Deliverables', {
            'fields': ('features', 'deliverables')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Booking Admin interface
    """
    list_display = ('booking_id', 'client', 'service', 'final_amount', 'total_with_gst',
                    'status', 'priority', 'assigned_to', 'booking_date')
    list_filter = ('status', 'priority', 'booking_date')
    search_fields = ('booking_id', 'client__company_name', 'service__name')
    ordering = ('-booking_date',)
    date_hierarchy = 'booking_date'
    
    fieldsets = (
        ('Booking ID', {'fields': ('booking_id',)}),
        ('Booking Details', {
            'fields': ('client', 'service', 'status', 'priority')
        }),
        ('Amount', {
            'fields': ('amount', 'discount_percent', 'final_amount')
        }),
        ('Revenue Tracking', {
            'fields': ('pitched_amount', 'gst_percentage', 'gst_amount', 
                      'total_with_gst', 'received_amount', 'pending_amount'),
            'description': 'Revenue tracking for this specific booking. Updates client total revenue automatically.'
        }),
        ('Dates', {
            'fields': ('booking_date', 'payment_date', 'expected_completion_date', 'actual_completion_date')
        }),
        ('Requirements & Assignment', {
            'fields': ('requirements', 'assigned_to', 'progress_percent')
        }),
        ('Internal Notes', {
            'fields': ('internal_notes',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('booking_id', 'booking_date', 'final_amount', 'gst_amount', 
                       'total_with_gst', 'pending_amount', 'created_at', 'updated_at')
    
    autocomplete_fields = ['client', 'assigned_to', 'created_by']
    
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
