from django.contrib import admin
from .models import Payment


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
