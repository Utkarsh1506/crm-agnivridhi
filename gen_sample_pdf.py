#!/usr/bin/env python
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')

import django
django.setup()

import sys
print("Starting PDF generation...", file=sys.stderr)

try:
    from django.utils import timezone
    from agreements.models import Agreement
    from clients.models import Client
    from django.contrib.auth import get_user_model
    from django.template.loader import render_to_string
    from xhtml2pdf import pisa
    from io import BytesIO
    from django.conf import settings

    User = get_user_model()
    print("✓ Imports successful", file=sys.stderr)

    test_user, _ = User.objects.get_or_create(username="sample_startup", defaults={"email": "startup@example.com"})
    print(f"✓ Test user: {test_user.username}", file=sys.stderr)

    client, _ = Client.objects.get_or_create(user=test_user, defaults={"company_name": "Startup Solutions Pvt Ltd", "is_approved": True})
    print(f"✓ Client: {client.company_name}", file=sys.stderr)

    admin_user = User.objects.filter(is_superuser=True).first() or User.objects.first()
    print(f"✓ Admin: {admin_user.username}", file=sys.stderr)

    agreement, _ = Agreement.objects.get_or_create(
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
            "commission_percentage": 5,
            "date_of_agreement": timezone.now().date(),
            "created_by": admin_user
        }
    )
    print(f"✓ Agreement: {agreement.agreement_number}", file=sys.stderr)

    html_string = render_to_string('agreements/pdf/funding_agreement.html', {'agreement': agreement, 'today': timezone.now().date()})
    print(f"✓ Template rendered ({len(html_string)} chars)", file=sys.stderr)

    result = BytesIO()
    pisa.CreatePDF(BytesIO(html_string.encode('utf-8')), result, encoding='utf-8')

    pdf_path = os.path.join(settings.BASE_DIR, 'static', 'sample_agreement_formatted.pdf')
    
    # Remove old file if exists
    try:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
    except:
        pass
    
    with open(pdf_path, 'wb') as f:
        f.write(result.getvalue())

    file_size = os.path.getsize(pdf_path) / 1024
    print(f"\n✅ PDF Created: {pdf_path} ({file_size:.2f} KB)")

except Exception as e:
    print(f"❌ Error: {str(e)}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)
