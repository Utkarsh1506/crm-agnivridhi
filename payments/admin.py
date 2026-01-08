from django.contrib import admin
from .models import Payment, RevenueEntry


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Payment Admin interface
    """
    list_display = ('client', 'booking', 'amount', 'status', 'payment_method', 'reference_id', 'received_by', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at', 'received_by')
    search_fields = ('razorpay_order_id', 'razorpay_payment_id', 'reference_id',
                     'client__company_name', 'booking__booking_id')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Razorpay Details (optional)', {
            'fields': ('razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature')
        }),
        ('Relationships', {
            'fields': ('booking', 'client')
        }),
        ('Amount Details', {
            'fields': ('amount', 'currency', 'status')
        }),
        ('Payment Info', {
            'fields': ('payment_method', 'reference_id', 'received_by', 'payment_date', 'proof', 'notes')
        }),
        ('Refund Details', {
            'fields': ('refund_amount', 'refund_reason', 'refund_date'),
            'classes': ('collapse',)
        }),
        ('Technical Details', {
            'fields': ('razorpay_response', 'error_message'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'refund_date')
    
    autocomplete_fields = ['booking', 'client']
    
    def has_add_permission(self, request):
        # Allow manual additions in admin (for offline payments)
        return True


@admin.register(RevenueEntry)
class RevenueEntryAdmin(admin.ModelAdmin):
    list_display = (
        'client', 'total_pitched_amount', 'received_amount', 'pending_amount',
        'source', 'recorded_by', 'created_at'
    )
    list_filter = ('source', 'created_at', 'recorded_by')
    search_fields = ('client__company_name', 'recorded_by__username')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
