#!/usr/bin/env python
"""
Script to generate sample agreement PDF
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from django.utils import timezone
from agreements.models import Agreement
from clients.models import Client
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
from django.conf import settings

User = get_user_model()

# Get or create a test user first
test_user, _ = User.objects.get_or_create(
    username="sample_startup",
    defaults={
        "email": "startup@example.com",
        "first_name": "Startup",
        "last_name": "Solutions"
    }
)

# Get or create a test client
client, created = Client.objects.get_or_create(
    user=test_user,
    defaults={
        "company_name": "Startup Solutions Pvt Ltd",
        "business_type": "STARTUP",
        "sector": "IT_SOFTWARE",
        "company_age": 3,
        "gst_number": "07AACTU1234H1Z0",
        "pan_number": "AAACR0123F",
        "annual_turnover": 50,
        "funding_required": 25,
        "is_approved": True
    }
)

# Get admin/superuser
admin_user = User.objects.filter(is_superuser=True).first()
if not admin_user:
    admin_user = User.objects.filter(is_staff=True).first()
if not admin_user:
    admin_user = User.objects.first()

# Create sample agreement
agreement, created = Agreement.objects.get_or_create(
    agreement_number="FA-20260128-001",
    defaults={
        "agreement_type": "funding",
        "client": client,
        "service_description": "STARTUP GROWTH PROGRAM",
        "service_receiver_name": "Startup Solutions Pvt Ltd",
        "service_receiver_address": "123 Tech Park, Bangalore, Karnataka 560001",
        "service_receiver_designation": "CEO",
        "total_amount_pitched": 500000,
        "received_amount_stage1": 200000,
        "pending_amount_stage2": 100000,
        "commission_percentage": 5,
        "has_pending_amount": True,
        "date_of_agreement": timezone.now().date(),
        "created_by": admin_user
    }
)

if created:
    print(f"✓ Created agreement: {agreement.agreement_number}")
else:
    print(f"✓ Using existing agreement: {agreement.agreement_number}")

# Generate PDF
template_name = 'agreements/pdf/funding_agreement.html'
logo_path = os.path.join(settings.BASE_DIR, 'static', 'agni_logo.png')

print("Rendering template...")
html_string = render_to_string(template_name, {
    'agreement': agreement,
    'today': timezone.now().date(),
    'logo_path': logo_path
})

print("Generating PDF...")
result = BytesIO()
pdf_status = pisa.CreatePDF(
    BytesIO(html_string.encode('utf-8')),
    result,
    encoding='utf-8'
)

if not pdf_status.err:
    # Save to static folder
    pdf_path = os.path.join(settings.BASE_DIR, 'static', 'sample_agreement_optimized.pdf')
    with open(pdf_path, 'wb') as f:
        f.write(result.getvalue())
    
    file_size = os.path.getsize(pdf_path) / 1024  # in KB
    print(f"\n✅ SUCCESS!")
    print(f"📄 PDF saved: {pdf_path}")
    print(f"📊 File size: {file_size:.2f} KB")
    print(f"📋 Agreement Number: {agreement.agreement_number}")
    print(f"🏢 Client: {agreement.client.company_name}")
    print(f"💰 Amount: Rs. {agreement.total_amount_pitched:,.0f}/-")
    print(f"📅 Date: {agreement.date_of_agreement}")
else:
    print(f"❌ Error generating PDF: {pdf_status.err}")
    sys.exit(1)
