from django.contrib import admin
from .models import Agreement


class AgreementAdmin(admin.ModelAdmin):
    list_display = [
        'agreement_number', 
        'agreement_type', 
        'service_receiver_name',
        'date_of_agreement',
        'total_amount_pitched',
        'received_amount_stage1',
        'commission_percentage',
        'is_active',
        'created_by',
        'created_at'
    ]
    list_filter = ['agreement_type', 'is_active', 'is_completed', 'created_at']
    search_fields = ['agreement_number', 'service_receiver_name', 'service_description']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    
    fieldsets = (
        ('Agreement Information', {
            'fields': ('agreement_number', 'agreement_type', 'date_of_agreement')
        }),
        ('Service Receiver Details', {
            'fields': ('service_receiver_name', 'service_receiver_address', 'service_receiver_designation')
        }),
        ('Service Details', {
            'fields': ('service_description',)
        }),
        ('Financial Details', {
            'fields': (
                'total_amount_pitched',
                'received_amount_stage1',
                'pending_amount_stage2',
                'commission_percentage',
                'commission_stage'
            )
        }),
        ('Related Parties', {
            'fields': ('client', 'employee')
        }),
        ('Additional Information', {
            'fields': ('notes', 'is_active', 'is_completed')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(Agreement, AgreementAdmin)
