from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal

class Scheme(models.Model):
    """
    Government schemes and funding programs (CGTMSE, PMEGP, Startup India, etc.)
    """
    
    class Category(models.TextChoices):
        LOAN = 'LOAN', _('Loan/Credit Guarantee')
        GRANT = 'GRANT', _('Grant/Subsidy')
        REGISTRATION = 'REGISTRATION', _('Registration/Certification')
        SUBSIDY = 'SUBSIDY', _('Capital/Interest Subsidy')
        TAX_BENEFIT = 'TAX_BENEFIT', _('Tax Benefits')
    
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', _('Active')
        INACTIVE = 'INACTIVE', _('Inactive')
        UPCOMING = 'UPCOMING', _('Upcoming')
        EXPIRED = 'EXPIRED', _('Expired')
    
    # Basic Information
    name = models.CharField(
        max_length=200,
        help_text=_('Scheme name (e.g., CGTMSE, PMEGP)')
    )
    
    full_name = models.CharField(
        max_length=300,
        help_text=_('Full official name of the scheme')
    )
    
    scheme_code = models.CharField(
        max_length=50,
        unique=True,
        help_text=_('Unique scheme code')
    )
    
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        help_text=_('Scheme category')
    )
    
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.ACTIVE,
        help_text=_('Current scheme status')
    )
    
    # Description
    description = models.TextField(
        help_text=_('Detailed scheme description')
    )
    
    benefits = models.TextField(
        help_text=_('Key benefits of the scheme')
    )
    
    # Eligibility Criteria
    eligible_sectors = models.JSONField(
        default=list,
        help_text=_('List of eligible business sectors')
    )
    
    eligible_business_types = models.JSONField(
        default=list,
        help_text=_('List of eligible business types (Pvt Ltd, LLP, etc.)')
    )
    
    min_turnover = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Minimum annual turnover required (in lakhs)')
    )
    
    max_turnover = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Maximum annual turnover allowed (in lakhs)')
    )
    
    min_company_age = models.IntegerField(
        null=True,
        blank=True,
        help_text=_('Minimum company age in years')
    )
    
    max_company_age = models.IntegerField(
        null=True,
        blank=True,
        help_text=_('Maximum company age in years')
    )
    
    # Funding Details
    min_funding = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Minimum funding available (in lakhs)')
    )
    
    max_funding = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Maximum funding available (in lakhs)')
    )
    
    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Interest rate (if applicable)')
    )
    
    subsidy_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Subsidy percentage (if applicable)')
    )
    
    # Documents Required
    required_documents = models.JSONField(
        default=list,
        help_text=_('List of required documents')
    )
    
    # URLs
    official_website = models.URLField(
        blank=True,
        null=True,
        help_text=_('Official scheme website')
    )
    
    application_url = models.URLField(
        blank=True,
        null=True,
        help_text=_('Application portal URL')
    )
    
    # Additional Information
    processing_time_days = models.IntegerField(
        default=30,
        help_text=_('Expected processing time in days')
    )
    
    eligibility_notes = models.TextField(
        blank=True,
        null=True,
        help_text=_('Additional eligibility notes and conditions')
    )
    
    exclusion_criteria = models.TextField(
        blank=True,
        null=True,
        help_text=_('Cases where scheme is not applicable')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Scheme')
        verbose_name_plural = _('Schemes')
        ordering = ['category', 'name']
        indexes = [
            models.Index(fields=['scheme_code']),
            models.Index(fields=['status', 'category']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.category})"
    
    def check_client_eligibility(self, client):
        """
        Check if a client is eligible for this scheme
        Returns: (is_eligible: bool, reasons: list)
        """
        reasons = []
        
        # Check sector
        if self.eligible_sectors and client.sector not in self.eligible_sectors:
            reasons.append(f"Business sector '{client.get_sector_display()}' not eligible")
        
        # Check business type
        if self.eligible_business_types and client.business_type not in self.eligible_business_types:
            reasons.append(f"Business type '{client.get_business_type_display()}' not eligible")
        
        # Check turnover range
        if self.min_turnover and client.annual_turnover < self.min_turnover:
            reasons.append(f"Annual turnover below minimum (₹{self.min_turnover} lakhs required)")
        
        if self.max_turnover and client.annual_turnover > self.max_turnover:
            reasons.append(f"Annual turnover exceeds maximum (₹{self.max_turnover} lakhs limit)")
        
        # Check company age
        if self.min_company_age and client.company_age < self.min_company_age:
            reasons.append(f"Company age below minimum ({self.min_company_age} years required)")
        
        if self.max_company_age and client.company_age > self.max_company_age:
            reasons.append(f"Company age exceeds maximum ({self.max_company_age} years limit)")
        
        # Check funding requirement
        if self.min_funding and client.funding_required < self.min_funding:
            reasons.append(f"Funding requirement below minimum (₹{self.min_funding} lakhs)")
        
        if self.max_funding and client.funding_required > self.max_funding:
            reasons.append(f"Funding requirement exceeds maximum (₹{self.max_funding} lakhs)")
        
        is_eligible = len(reasons) == 0
        return is_eligible, reasons
    
    def get_recommended_for_client(self, client):
        """
        Get AI recommendation score (0-100) for this scheme
        Higher score = better match
        """
        score = 0
        
        # Perfect match criteria (high weight)
        if self.eligible_sectors and client.sector in self.eligible_sectors:
            score += 30
        
        if self.eligible_business_types and client.business_type in self.eligible_business_types:
            score += 20
        
        # Funding range match
        if self.min_funding and self.max_funding:
            if self.min_funding <= client.funding_required <= self.max_funding:
                score += 25
        
        # Turnover range match
        if self.min_turnover and self.max_turnover:
            if self.min_turnover <= client.annual_turnover <= self.max_turnover:
                score += 15
        
        # Company age match
        if self.min_company_age and self.max_company_age:
            if self.min_company_age <= client.company_age <= self.max_company_age:
                score += 10
        
        return score
