"""
Script to add government schemes to database
Run: python add_schemes.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from schemes.models import Scheme

# Government schemes data
schemes_data = [
    {
        'name': 'Credit Guarantee Scheme (CGTMSE)',
        'full_name': 'Credit Guarantee Fund Trust for Micro and Small Enterprises',
        'scheme_code': 'CGTMSE-2025',
        'category': 'LOAN',
        'description': 'Collateral-free loans up to ₹2 crore for MSMEs with credit guarantee from CGTMSE. No security required, simplified process.',
        'benefits': 'No collateral, Lower interest rates, Quick processing, Credit guarantee cover up to 85% of loan amount',
        'status': 'ACTIVE',
        'min_funding': 10.00,  # ₹10 lakhs
        'max_funding': 200.00,  # ₹2 crore
        'interest_rate': 9.5,
        'eligible_sectors': ['MANUFACTURING', 'SERVICES', 'TRADING'],
        'eligible_business_types': ['PRIVATE_LIMITED', 'LLP', 'PARTNERSHIP', 'PROPRIETORSHIP'],
        'min_turnover': 5.00,  # ₹5 lakhs
        'max_turnover': 500.00,  # ₹5 crore
        'min_company_age': 1,
        'max_company_age': 50,
        'required_documents': [
            'Business plan',
            'Financial statements (2 years)',
            'KYC documents',
            'Project report',
            'Bank statements'
        ],
        'official_website': 'https://www.cgtmse.in/',
        'application_url': 'https://www.cgtmse.in/login.aspx',
        'processing_time_days': 30,
        'eligibility_notes': 'Applicable to new and existing MSMEs. Maximum loan amount ₹2 crore.',
    },
    {
        'name': 'Prime Minister Employment Generation Programme (PMEGP)',
        'full_name': 'Prime Minister Employment Generation Programme',
        'scheme_code': 'PMEGP-2025',
        'category': 'GRANT',
        'description': 'Subsidy up to ₹25 lakhs for new manufacturing and service ventures. Government provides 15-35% subsidy on project cost.',
        'benefits': '25-35% subsidy, Easy loan approval, Training support, Marketing assistance, Employment generation',
        'status': 'ACTIVE',
        'min_funding': 1.00,  # ₹1 lakh
        'max_funding': 25.00,  # ₹25 lakhs
        'subsidy_percent': 25.0,  # 25-35% subsidy
        'eligible_sectors': ['MANUFACTURING', 'SERVICES', 'AGRICULTURE'],
        'eligible_business_types': ['PROPRIETORSHIP', 'PARTNERSHIP', 'LLP', 'PRIVATE_LIMITED'],
        'min_turnover': 0.00,
        'max_turnover': 50.00,
        'min_company_age': 0,  # For new businesses
        'max_company_age': 5,
        'required_documents': [
            'Project report',
            'Educational certificates',
            'Caste certificate (if applicable)',
            'Aadhar card',
            'Bank account details',
            'Land documents (if applicable)'
        ],
        'official_website': 'https://www.kviconline.gov.in/pmegpeportal/',
        'application_url': 'https://www.kviconline.gov.in/pmegpeportal/jsp/pmegponline.jsp',
        'processing_time_days': 45,
        'eligibility_notes': 'Eligible for individuals above 18 years. Priority for SC/ST/OBC/Women/Ex-servicemen.',
    },
    {
        'name': 'Startup India Seed Fund Scheme (SISFS)',
        'full_name': 'Startup India Seed Fund Scheme',
        'scheme_code': 'SISFS-2025',
        'category': 'GRANT',
        'description': 'Seed funding up to ₹50 lakhs for innovative startups recognized by DPIIT. 100% grant, no repayment required.',
        'benefits': '100% grant (no repayment), Mentorship support, Incubation facilities, Networking opportunities',
        'status': 'ACTIVE',
        'min_funding': 5.00,  # ₹5 lakhs
        'max_funding': 50.00,  # ₹50 lakhs
        'subsidy_percent': 100.0,  # Full grant
        'eligible_sectors': ['TECHNOLOGY', 'HEALTHCARE', 'EDUCATION', 'AGRICULTURE'],
        'eligible_business_types': ['PRIVATE_LIMITED', 'LLP'],
        'min_turnover': 0.00,
        'max_turnover': 100.00,  # ₹1 crore
        'min_company_age': 0,
        'max_company_age': 2,  # Must be < 2 years old
        'required_documents': [
            'DPIIT recognition certificate',
            'Business plan',
            'Pitch deck',
            'Financial projections',
            'Team profile',
            'Product/service prototype'
        ],
        'official_website': 'https://www.startupindia.gov.in/content/sih/en/seed-fund-scheme.html',
        'application_url': 'https://www.startupindia.gov.in/content/sih/en/reources/seed-fund/apply-for-seed-fund.html',
        'processing_time_days': 60,
        'eligibility_notes': 'Must be DPIIT recognized startup, less than 2 years old, with innovative business model.',
    },
    {
        'name': 'SIDBI Stand-Up India Scheme',
        'full_name': 'Stand-Up India Scheme by SIDBI',
        'scheme_code': 'SIDBI-STANDUP-2025',
        'category': 'LOAN',
        'description': 'Loans ₹10 lakhs to ₹1 crore for SC/ST/Women entrepreneurs to set up greenfield enterprises in manufacturing, services, or trading.',
        'benefits': 'Preferential interest rates, Handholding support, No collateral for loans up to ₹50 lakhs, Extended repayment period',
        'status': 'ACTIVE',
        'min_funding': 10.00,  # ₹10 lakhs
        'max_funding': 100.00,  # ₹1 crore
        'interest_rate': 8.5,
        'eligible_sectors': ['MANUFACTURING', 'SERVICES', 'TRADING'],
        'eligible_business_types': ['PRIVATE_LIMITED', 'LLP', 'PARTNERSHIP', 'PROPRIETORSHIP'],
        'min_turnover': 0.00,
        'max_turnover': 1000.00,
        'min_company_age': 0,
        'max_company_age': 30,
        'required_documents': [
            'Category certificate (SC/ST/Women)',
            'Business plan',
            'Financial projections',
            'KYC documents',
            'Project report',
            'Bank statements'
        ],
        'official_website': 'https://www.standupmitra.in/',
        'application_url': 'https://www.standupmitra.in/Home/ApplyNow',
        'processing_time_days': 30,
        'eligibility_notes': 'Exclusively for SC/ST/Women entrepreneurs. At least one borrower should be SC/ST/Woman.',
    },
    {
        'name': 'Mudra Loan Scheme - Shishu/Kishore/Tarun',
        'full_name': 'Micro Units Development & Refinance Agency Loan Scheme',
        'scheme_code': 'MUDRA-2025',
        'category': 'LOAN',
        'description': 'Collateral-free loans up to ₹10 lakhs for micro-enterprises. Three categories: Shishu (up to ₹50k), Kishore (₹50k-₹5L), Tarun (₹5L-₹10L).',
        'benefits': 'No collateral, Low interest rates, Quick disbursement, Flexible repayment, 3 categories for different needs',
        'status': 'ACTIVE',
        'min_funding': 0.50,  # ₹50,000
        'max_funding': 10.00,  # ₹10 lakhs
        'interest_rate': 10.0,
        'eligible_sectors': ['MANUFACTURING', 'SERVICES', 'TRADING', 'AGRICULTURE'],
        'eligible_business_types': ['PROPRIETORSHIP', 'PARTNERSHIP', 'LLP', 'PRIVATE_LIMITED'],
        'min_turnover': 0.00,
        'max_turnover': 50.00,
        'min_company_age': 0,
        'max_company_age': 50,
        'required_documents': [
            'Business plan',
            'Identity proof',
            'Address proof',
            'Bank statements (6 months)',
            'Quotations/estimates',
            'Income proof'
        ],
        'official_website': 'https://www.mudra.org.in/',
        'application_url': 'https://udyamimitra.in/',
        'processing_time_days': 15,
        'eligibility_notes': 'Available to individuals and micro-enterprises in non-farm sectors. Income generating activities only.',
    }
]

def add_schemes():
    """Add government schemes to database"""
    print("=" * 60)
    print("🏛️  ADDING GOVERNMENT SCHEMES TO DATABASE")
    print("=" * 60)
    print()
    
    # Check if schemes already exist
    existing_count = Scheme.objects.count()
    print(f"📊 Current schemes in database: {existing_count}")
    print()
    
    added_count = 0
    updated_count = 0
    skipped_count = 0
    
    for data in schemes_data:
        scheme_code = data['scheme_code']
        scheme_name = data['name']
        
        # Check if scheme already exists
        existing = Scheme.objects.filter(scheme_code=scheme_code).first()
        
        if existing:
            print(f"⚠️  Scheme already exists: {scheme_name}")
            
            # Ask if user wants to update
            update = input("   Update? (y/n): ").lower().strip()
            if update == 'y':
                for key, value in data.items():
                    setattr(existing, key, value)
                existing.save()
                print(f"✅ Updated: {scheme_name}")
                updated_count += 1
            else:
                print(f"⏭️  Skipped: {scheme_name}")
                skipped_count += 1
        else:
            # Create new scheme
            scheme = Scheme.objects.create(**data)
            print(f"✅ Created: {scheme_name}")
            print(f"   Code: {scheme.scheme_code}")
            print(f"   Category: {scheme.get_category_display()}")
            print(f"   Funding: ₹{scheme.min_funding:,.0f} - ₹{scheme.max_funding:,.0f}")
            added_count += 1
        
        print()
    
    # Summary
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"✅ Added: {added_count} schemes")
    print(f"🔄 Updated: {updated_count} schemes")
    print(f"⏭️  Skipped: {skipped_count} schemes")
    print()
    
    total_schemes = Scheme.objects.count()
    print(f"🎉 Total schemes in database: {total_schemes}")
    print()
    
    # Display all schemes
    print("=" * 60)
    print("📋 ALL SCHEMES IN DATABASE")
    print("=" * 60)
    for scheme in Scheme.objects.all().order_by('category', 'name'):
        print(f"{scheme.scheme_code:20} | {scheme.name:50} | {scheme.get_category_display():10}")
    
    print()
    print("=" * 60)
    print("✅ DONE! Schemes ready for AI recommendations.")
    print("=" * 60)
    print()
    print("🔗 Next steps:")
    print("   1. Start server: python manage.py runserver")
    print("   2. Login as client")
    print("   3. View AI scheme recommendations")
    print("   4. Test eligibility matching")
    print()

if __name__ == '__main__':
    try:
        add_schemes()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
