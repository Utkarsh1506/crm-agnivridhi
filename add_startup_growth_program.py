"""
Add Startup Growth Program scheme with correct fields
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from schemes.models import Scheme
from decimal import Decimal

print("=" * 70)
print("ADDING STARTUP GROWTH PROGRAM")
print("=" * 70)

startup_growth_scheme = {
    'name': 'Startup Growth Program',
    'full_name': 'Agnivridhi Startup Growth & Acceleration Program',
    'scheme_code': 'AGNV-SGP-2025',
    'category': 'GRANT',
    'status': 'ACTIVE',
    'description': '''Agnivridhi's proprietary startup growth program designed to accelerate early-stage and growth-stage startups through comprehensive business support, mentorship, and funding assistance.

This program provides end-to-end support including:
- Business model validation and optimization
- Market entry strategy and execution
- Financial management and planning
- Legal and compliance setup
- Access to funding opportunities (loans, grants, investors)
- Mentorship from industry experts
- Networking opportunities

Ideal for startups in their early stages (Seed to Series A) looking for structured growth support and funding access.''',
    'benefits': '''1. Comprehensive Business Support
   - 6-month structured growth program
   - Weekly mentorship sessions
   - Business model refinement
   
2. Financial Assistance
   - Support in accessing ₹10 Lakh to ₹1 Crore funding
   - Connections to banks, NBFCs, and investors
   - Financial modeling and projections
   
3. Operational Setup
   - Company incorporation assistance
   - Legal and compliance setup
   - Accounting and taxation setup
   
4. Market Access
   - Go-to-market strategy
   - Sales and marketing support
   - Customer acquisition assistance
   
5. Network & Resources
   - Access to investor network
   - Industry mentor connections
   - Co-working space partnerships
   
6. Post-Program Support
   - Continued advisory (3 months)
   - Funding round support
   - Growth tracking''',
    'eligible_sectors': ['MANUFACTURING', 'TECHNOLOGY', 'SERVICES', 'AGRICULTURE', 'HEALTHCARE', 'EDUCATION', 'FINTECH', 'ECOMMERCE', 'SOCIAL_ENTERPRISE'],
    'eligible_business_types': ['PROPRIETORSHIP', 'PARTNERSHIP', 'LLP', 'PRIVATE_LIMITED', 'OPC', 'STARTUP'],
    'min_turnover': None,  # No minimum
    'max_turnover': Decimal('500'),  # Max 5 Crore
    'min_company_age': 0,  # Can be brand new
    'max_company_age': 5,  # Within 5 years
    'min_funding': Decimal('10'),  # 10 Lakh
    'max_funding': Decimal('100'),  # 1 Crore
    'interest_rate': Decimal('0'),  # Grant-based, no interest
    'subsidy_percent': None,
    'required_documents': [
        'Business registration certificate',
        'Founder ID proofs (Aadhaar/PAN)',
        'Business pitch deck (10-15 slides)',
        'Financial projections (3 years)',
        'Product demo or prototype',
        'Team CVs/profiles',
        'Business plan summary'
    ],
    'official_website': 'https://agnivridhi.com',
    'application_url': 'https://agnivridhi.com/startup-growth-program',
    'processing_time_days': 28,  # 4 weeks
    'eligibility_notes': '''Eligibility Criteria:
- Early-stage startup (registered within last 5 years)
- Innovative business model with scalability potential
- Founder commitment to full program participation
- Minimum viable product (MVP) or prototype ready
- Clear revenue model and growth plan
- Team of 2-5 members preferred
- Open to all sectors

Application Process:
Step 1: Initial Application (Submit online form with business overview)
Step 2: Screening - 2 weeks (Business model evaluation and team assessment)
Step 3: Interview - 1 week (Founder interview and business presentation)
Step 4: Selection - 1 week (Final selection and enrollment)
Step 5: Program Commencement (Onboarding and mentor assignment)

Total Timeline: 4 weeks from application to enrollment''',
    'exclusion_criteria': '''Not eligible for:
- Companies older than 5 years
- Non-innovative or traditional business models
- Companies with turnover exceeding ₹5 Crore
- Part-time founders (requires full-time commitment)
- Companies without product/prototype
- Businesses in prohibited sectors (alcohol, tobacco, gambling)'''
}

try:
    scheme, created = Scheme.objects.get_or_create(
        scheme_code=startup_growth_scheme['scheme_code'],
        defaults=startup_growth_scheme
    )
    
    if created:
        print(f"✓ Successfully added: {scheme.name}")
        print(f"  Full Name: {scheme.full_name}")
        print(f"  Code: {scheme.scheme_code}")
        print(f"  Category: {scheme.get_category_display()}")
        print(f"  Funding Range: ₹{scheme.min_funding} Lakh - ₹{scheme.max_funding} Lakh")
        print(f"  Processing Time: {scheme.processing_time_days} days")
        print(f"  Status: {scheme.get_status_display()}")
    else:
        print(f"→ Already exists: {scheme.name}")
        print(f"  (Scheme code: {scheme.scheme_code})")
    
    print(f"\n{'='*70}")
    print("SCHEME SETUP COMPLETE!")
    print(f"{'='*70}")
    print(f"\nTotal Active Schemes: {Scheme.objects.filter(status='ACTIVE').count()}")
    
    # List all schemes
    print(f"\n{'='*70}")
    print("ALL ACTIVE SCHEMES:")
    print(f"{'='*70}")
    for s in Scheme.objects.filter(status='ACTIVE').order_by('category', 'name'):
        print(f"  • {s.name} ({s.get_category_display()})")
    
except Exception as e:
    print(f"✗ Error: {str(e)}")
    import traceback
    traceback.print_exc()

print(f"\n{'='*70}")
