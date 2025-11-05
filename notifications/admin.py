from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Notification Admin interface
    """
    list_display = ('notification_type', 'recipient', 'channel', 'status', 
                    'sent_at', 'retry_count', 'created_at')
    list_filter = ('notification_type', 'channel', 'status', 'created_at')
    search_fields = ('subject', 'recipient__username', 'recipient__email', 
                     'email_to', 'whatsapp_to')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (_('Recipient & Type'), {
            'fields': ('recipient', 'notification_type', 'channel', 'status')
        }),
        (_('Content'), {
            'fields': ('subject', 'message', 'html_content')
        }),
        (_('Contact Details'), {
            'fields': ('email_to', 'whatsapp_to')
        }),
        (_('Attachments'), {
            'fields': ('attachments',),
            'classes': ('collapse',)
        }),
        (_('Tracking'), {
            'fields': ('sent_at', 'failed_at', 'error_message', 'retry_count')
        }),
        (_('External IDs'), {
            'fields': ('email_message_id', 'whatsapp_message_id'),
            'classes': ('collapse',)
        }),
        (_('Related Objects'), {
            'fields': ('related_booking', 'related_application', 'related_payment'),
            'classes': ('collapse',)
        }),
        (_('Sender'), {
            'fields': ('sent_by',)
        }),
    )
    
    readonly_fields = ('sent_at', 'failed_at', 'created_at', 'updated_at')
    
    autocomplete_fields = ['recipient', 'sent_by', 'related_booking', 
                           'related_application', 'related_payment']
    
    actions = ['retry_failed_notifications']
    
    def retry_failed_notifications(self, request, queryset):
        count = 0
        for notification in queryset.filter(status='FAILED'):
            if notification.can_retry():
                notification.status = 'PENDING'
                notification.save()
                count += 1
        self.message_user(request, f"{count} notifications queued for retry.")
    retry_failed_notifications.short_description = "Retry failed notifications"
