from django.contrib import admin
from .models import Scheme


@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    """
    Scheme Admin interface
    """
    list_display = ('name', 'scheme_code', 'category', 'status', 'min_funding', 'max_funding')
    list_filter = ('category', 'status')
    search_fields = ('name', 'full_name', 'scheme_code', 'description')
    ordering = ('category', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'full_name', 'scheme_code', 'category', 'status')
        }),
        ('Description', {
            'fields': ('description', 'benefits')
        }),
        ('Eligibility - Business Criteria', {
            'fields': ('eligible_sectors', 'eligible_business_types', 'min_company_age', 'max_company_age')
        }),
        ('Eligibility - Financial Criteria', {
            'fields': ('min_turnover', 'max_turnover', 'min_funding', 'max_funding')
        }),
        ('Financial Details', {
            'fields': ('interest_rate', 'subsidy_percent', 'processing_time_days')
        }),
        ('Required Documents', {
            'fields': ('required_documents',)
        }),
        ('Additional Information', {
            'fields': ('eligibility_notes', 'exclusion_criteria'),
            'classes': ('collapse',)
        }),
        ('External Links', {
            'fields': ('official_website', 'application_url'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
