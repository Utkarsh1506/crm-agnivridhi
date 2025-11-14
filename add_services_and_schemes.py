"""
Add comprehensive services and Startup Growth Program scheme
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from bookings.models import Service
from schemes.models import Scheme
from decimal import Decimal

print("=" * 70)
print("ADDING COMPREHENSIVE SERVICES AND SCHEMES")
print("=" * 70)

# Services to add
services_data = [
    # Funding Services
    {
        'name': 'CGTMSE Loan Application',
        'category': 'FUNDING',
        'description': 'Complete assistance in applying for Credit Guarantee Scheme loans',
        'short_description': 'CGTMSE loan application support with documentation',
        'price': Decimal('10000.00'),
        'duration_days': 30,
        'features': ['Documentation preparation', 'Bank liaison', 'Application tracking', 'Post-approval support'],
        'deliverables': ['Complete loan application', 'Supporting documents', 'Bank submission']
    },
    {
        'name': 'PMEGP Loan & Subsidy Application',
        'category': 'FUNDING',
        'description': 'End-to-end support for PMEGP loan and subsidy application',
        'short_description': 'PMEGP application with subsidy claim assistance',
        'price': Decimal('15000.00'),
        'duration_days': 45,
        'features': ['Project report preparation', 'Subsidy calculation', 'Bank coordination', 'DIC approval'],
        'deliverables': ['Project report', 'Subsidy application', 'Bank loan application']
    },
    {
        'name': 'Mudra Loan Application',
        'category': 'FUNDING',
        'description': 'Mudra loan application (Shishu/Kishore/Tarun)',
        'short_description': 'Mudra loan assistance for micro enterprises',
        'price': Decimal('8000.00'),
        'duration_days': 20,
        'features': ['Loan category selection', 'Documentation', 'Bank submission'],
        'deliverables': ['Loan application', 'Business plan', 'Financial projections']
    },
    {
        'name': 'Startup India Seed Fund Application',
        'category': 'FUNDING',
        'description': 'Startup India Seed Fund Scheme (SISFS) application support',
        'short_description': 'SISFS application for early-stage startups',
        'price': Decimal('20000.00'),
        'duration_days': 60,
        'features': ['Pitch deck creation', 'Business model validation', 'Incubator coordination'],
        'deliverables': ['Application package', 'Pitch presentation', 'Financial model']
    },
    {
        'name': 'Stand-Up India Loan Application',
        'category': 'FUNDING',
        'description': 'SIDBI Stand-Up India scheme for SC/ST/Women entrepreneurs',
        'short_description': 'Stand-Up India loan application assistance',
        'price': Decimal('12000.00'),
        'duration_days': 35,
        'features': ['Eligibility check', 'Project report', 'Bank coordination'],
        'deliverables': ['Complete application', 'Project report', 'Supporting documents']
    },
    
    # Incorporation Services
    {
        'name': 'Private Limited Company Registration',
        'category': 'INCORPORATION',
        'description': 'Complete Pvt Ltd company incorporation with MCA',
        'short_description': 'Pvt Ltd company registration with all compliances',
        'price': Decimal('15000.00'),
        'duration_days': 15,
        'features': ['Name approval', 'DIN/DSC', 'MOA/AOA drafting', 'ROC filing'],
        'deliverables': ['Certificate of Incorporation', 'PAN', 'TAN', 'Company documents']
    },
    {
        'name': 'LLP Registration',
        'category': 'INCORPORATION',
        'description': 'Limited Liability Partnership registration',
        'short_description': 'LLP registration with MCA',
        'price': Decimal('12000.00'),
        'duration_days': 12,
        'features': ['Name approval', 'DPIN/DSC', 'LLP Agreement', 'ROC filing'],
        'deliverables': ['LLP Certificate', 'PAN', 'TAN', 'Partnership deed']
    },
    {
        'name': 'One Person Company (OPC) Registration',
        'category': 'INCORPORATION',
        'description': 'OPC registration for solo entrepreneurs',
        'short_description': 'OPC registration with single director',
        'price': Decimal('10000.00'),
        'duration_days': 10,
        'features': ['Name approval', 'DIN/DSC', 'MOA/AOA', 'ROC filing'],
        'deliverables': ['Incorporation certificate', 'PAN', 'TAN']
    },
    {
        'name': 'Partnership Firm Registration',
        'category': 'INCORPORATION',
        'description': 'Partnership firm registration and deed preparation',
        'short_description': 'Partnership firm with deed registration',
        'price': Decimal('8000.00'),
        'duration_days': 7,
        'features': ['Partnership deed drafting', 'Registration', 'PAN application'],
        'deliverables': ['Partnership deed', 'Registration certificate', 'PAN']
    },
    {
        'name': 'Proprietorship Registration',
        'category': 'INCORPORATION',
        'description': 'Sole proprietorship setup with registrations',
        'short_description': 'Proprietorship with GST and licenses',
        'price': Decimal('5000.00'),
        'duration_days': 5,
        'features': ['Business name', 'GST registration', 'Shop Act license'],
        'deliverables': ['GST certificate', 'Shop Act license', 'Bank account support']
    },
    
    # Certification Services
    {
        'name': 'Startup India Registration',
        'category': 'CERTIFICATION',
        'description': 'DPIIT Startup India recognition certificate',
        'short_description': 'Startup India DPIIT recognition',
        'price': Decimal('5000.00'),
        'duration_days': 20,
        'features': ['Eligibility check', 'Application preparation', 'DPIIT submission'],
        'deliverables': ['Recognition certificate', 'Tax benefits', 'IPR support']
    },
    {
        'name': 'MSME/Udyam Registration',
        'category': 'CERTIFICATION',
        'description': 'Udyam registration for MSME benefits',
        'short_description': 'MSME Udyam certificate for businesses',
        'price': Decimal('3000.00'),
        'duration_days': 5,
        'features': ['Online registration', 'Classification', 'Certificate generation'],
        'deliverables': ['Udyam certificate', 'MSME benefits guide']
    },
    {
        'name': 'GST Registration',
        'category': 'CERTIFICATION',
        'description': 'GST registration and compliance setup',
        'short_description': 'GST registration for businesses',
        'price': Decimal('4000.00'),
        'duration_days': 7,
        'features': ['GST application', 'Documentation', 'Portal setup'],
        'deliverables': ['GSTIN certificate', 'Compliance calendar']
    },
    {
        'name': 'Import Export Code (IEC)',
        'category': 'CERTIFICATION',
        'description': 'IEC license for import/export businesses',
        'short_description': 'IEC registration for international trade',
        'price': Decimal('5000.00'),
        'duration_days': 10,
        'features': ['DGFT application', 'Documentation', 'IEC issuance'],
        'deliverables': ['IEC certificate', 'DGFT registration']
    },
    {
        'name': 'ISO Certification Consulting',
        'category': 'CERTIFICATION',
        'description': 'ISO 9001/14001/45001 certification assistance',
        'short_description': 'ISO certification consulting and audit support',
        'price': Decimal('25000.00'),
        'duration_days': 90,
        'features': ['Gap analysis', 'Documentation', 'Audit preparation', 'Certification liaison'],
        'deliverables': ['ISO documentation', 'Audit report', 'Certification support']
    },
    
    # Growth Services
    {
        'name': 'Business Plan Preparation',
        'category': 'GROWTH',
        'description': 'Comprehensive business plan for funding/growth',
        'short_description': 'Professional business plan with financials',
        'price': Decimal('15000.00'),
        'duration_days': 15,
        'features': ['Market research', 'Financial projections', 'Strategy development'],
        'deliverables': ['Business plan document', 'Financial model', 'Pitch deck']
    },
    {
        'name': 'Project Report for Bank Loan',
        'category': 'GROWTH',
        'description': 'Detailed project report (DPR) for bank financing',
        'short_description': 'DPR for loan applications',
        'price': Decimal('12000.00'),
        'duration_days': 10,
        'features': ['Cost estimation', 'Revenue projections', 'Loan requirement analysis'],
        'deliverables': ['Project report', 'Financial statements', 'CMA data']
    },
    {
        'name': 'Financial Projections & Modeling',
        'category': 'GROWTH',
        'description': '3-5 year financial projections for investors',
        'short_description': 'Financial model and projections',
        'price': Decimal('10000.00'),
        'duration_days': 7,
        'features': ['Revenue modeling', 'P&L projections', 'Cash flow analysis'],
        'deliverables': ['Excel financial model', 'Projection statements', 'Break-even analysis']
    },
    {
        'name': 'Pitch Deck Creation',
        'category': 'GROWTH',
        'description': 'Investor pitch deck design and content',
        'short_description': 'Professional pitch presentation for investors',
        'price': Decimal('8000.00'),
        'duration_days': 5,
        'features': ['Market analysis', 'Business model', 'Financial highlights', 'Design'],
        'deliverables': ['PowerPoint pitch deck', 'Investor one-pager']
    },
    {
        'name': 'Market Research & Feasibility Study',
        'category': 'GROWTH',
        'description': 'Market analysis and business feasibility assessment',
        'short_description': 'Market research for business validation',
        'price': Decimal('20000.00'),
        'duration_days': 20,
        'features': ['Industry analysis', 'Competitor research', 'Customer insights', 'Feasibility'],
        'deliverables': ['Research report', 'Market data', 'Feasibility analysis']
    },
    
    # CSR Services
    {
        'name': 'CSR Registration (Section 8 Company)',
        'category': 'CSR',
        'description': 'Section 8 company registration for NGO/NPO',
        'short_description': 'Non-profit company incorporation',
        'price': Decimal('18000.00'),
        'duration_days': 30,
        'features': ['License application', 'MOA/AOA drafting', 'MCA approval', 'Registration'],
        'deliverables': ['Section 8 certificate', 'Incorporation certificate', 'PAN/TAN']
    },
    {
        'name': '12A & 80G Registration',
        'category': 'CSR',
        'description': 'Income tax exemption registration for NGOs',
        'short_description': '12A and 80G tax exemption certificates',
        'price': Decimal('15000.00'),
        'duration_days': 45,
        'features': ['Application preparation', 'IT department liaison', 'Compliance setup'],
        'deliverables': ['12A certificate', '80G certificate', 'Tax exemption']
    },
    {
        'name': 'FCRA Registration',
        'category': 'CSR',
        'description': 'Foreign Contribution Regulation Act registration',
        'short_description': 'FCRA for receiving foreign funding',
        'price': Decimal('25000.00'),
        'duration_days': 60,
        'features': ['Eligibility check', 'Application preparation', 'MHA submission'],
        'deliverables': ['FCRA certificate', 'Foreign funding approval']
    },
    {
        'name': 'CSR Policy & Compliance',
        'category': 'CSR',
        'description': 'CSR policy development and compliance for companies',
        'short_description': 'CSR strategy and reporting',
        'price': Decimal('20000.00'),
        'duration_days': 20,
        'features': ['CSR policy drafting', 'Project identification', 'Compliance reporting'],
        'deliverables': ['CSR policy document', 'Annual CSR report', 'Compliance calendar']
    },
    
    # Consulting Services
    {
        'name': 'Business Strategy Consulting',
        'category': 'CONSULTING',
        'description': 'Strategic consulting for business growth',
        'short_description': 'Growth strategy and business consulting',
        'price': Decimal('30000.00'),
        'duration_days': 30,
        'features': ['SWOT analysis', 'Strategy development', 'Implementation roadmap'],
        'deliverables': ['Strategy document', 'Action plan', 'Performance metrics']
    },
    {
        'name': 'Legal & Compliance Consulting',
        'category': 'CONSULTING',
        'description': 'Legal compliance advisory for businesses',
        'short_description': 'Legal and regulatory compliance support',
        'price': Decimal('25000.00'),
        'duration_days': 15,
        'features': ['Compliance audit', 'Legal documentation', 'Regulatory advisory'],
        'deliverables': ['Compliance report', 'Legal documents', 'Advisory notes']
    },
    {
        'name': 'Tax Planning & Advisory',
        'category': 'CONSULTING',
        'description': 'Tax optimization and planning services',
        'short_description': 'Tax planning and compliance advisory',
        'price': Decimal('15000.00'),
        'duration_days': 10,
        'features': ['Tax assessment', 'Optimization strategies', 'Compliance planning'],
        'deliverables': ['Tax plan', 'Savings report', 'Compliance checklist']
    },
    {
        'name': 'Accounting & Bookkeeping Setup',
        'category': 'CONSULTING',
        'description': 'Accounting system setup and training',
        'short_description': 'Bookkeeping and accounting system implementation',
        'price': Decimal('12000.00'),
        'duration_days': 10,
        'features': ['Software selection', 'Chart of accounts', 'Process setup', 'Training'],
        'deliverables': ['Accounting system', 'SOPs', 'Staff training']
    },
]

print(f"\n{'='*70}")
print(f"Adding {len(services_data)} Services...")
print(f"{'='*70}")

services_added = 0
services_updated = 0

for service_data in services_data:
    service, created = Service.objects.get_or_create(
        name=service_data['name'],
        defaults=service_data
    )
    if created:
        print(f"✓ Added: {service.name} (₹{service.price})")
        services_added += 1
    else:
        print(f"→ Exists: {service.name}")
        services_updated += 1

print(f"\n{'='*70}")
print(f"Services Added: {services_added}")
print(f"Services Already Exist: {services_updated}")
print(f"{'='*70}")

# Add Startup Growth Program scheme
print(f"\n{'='*70}")
print("Adding Startup Growth Program (Agnivridhi's Own Scheme)...")
print(f"{'='*70}")

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
    'eligibility_criteria': '''- Early-stage startup (registered within last 5 years)
- Innovative business model with scalability potential
- Founder commitment to full program participation
- Minimum viable product (MVP) or prototype ready
- Clear revenue model and growth plan
- Team of 2-5 members preferred
- Open to all sectors (Tech, Manufacturing, Services, Social Enterprise)''',
    'funding_min': Decimal('1000000'),  # 10 Lakh
    'funding_max': Decimal('10000000'),  # 1 Crore
    'interest_rate': Decimal('0'),  # Grant/Equity-free support
    'tenure_months': 6,
    'application_process': '''Step 1: Initial Application
- Submit online application form
- Provide business overview and pitch deck
- Team details and background

Step 2: Screening (2 weeks)
- Business model evaluation
- Team assessment
- Feasibility analysis

Step 3: Interview (1 week)
- Founder interview with selection panel
- Business presentation
- Q&A session

Step 4: Selection (1 week)
- Final selection announcement
- Program enrollment
- Documentation

Step 5: Program Commencement
- Onboarding session
- Mentor assignment
- Program kickoff

Timeline: 4 weeks from application to enrollment''',
    'required_documents': [
        'Business registration certificate',
        'Founder ID proofs (Aadhaar/PAN)',
        'Business pitch deck (10-15 slides)',
        'Financial projections (3 years)',
        'Product demo or prototype',
        'Team CVs/profiles',
        'Business plan summary'
    ],
    'application_url': 'https://agnivridhi.com/startup-growth-program',
    'contact_email': 'startups@agnivridhi.com',
    'contact_phone': '+91-XXXXXXXXXX',
    'is_featured': True,
    'tags': ['startup', 'growth', 'acceleration', 'mentorship', 'funding', 'agnivridhi']
}

scheme, created = Scheme.objects.get_or_create(
    scheme_code=startup_growth_scheme['scheme_code'],
    defaults=startup_growth_scheme
)

if created:
    print(f"✓ Added: {scheme.name}")
    print(f"  Category: {scheme.get_category_display()}")
    print(f"  Funding Range: ₹{scheme.funding_min:,.0f} - ₹{scheme.funding_max:,.0f}")
else:
    print(f"→ Already exists: {scheme.name}")

print(f"\n{'='*70}")
print("SETUP COMPLETE!")
print(f"{'='*70}")
print(f"\nTotal Active Services: {Service.objects.filter(is_active=True).count()}")
print(f"Total Active Schemes: {Scheme.objects.filter(status='ACTIVE').count()}")
print(f"\n{'='*70}")
