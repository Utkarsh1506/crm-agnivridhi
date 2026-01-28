#!/usr/bin/env python
"""
Quick test script to verify agreements system is working
"""
import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from django.contrib.auth.models import User
from agreements.models import Agreement
from agreements.views import generate_agreement_number
from clients.models import Client

print("=" * 60)
print("AGREEMENTS SYSTEM - VERIFICATION TEST")
print("=" * 60)

# Test 1: Check if Agreement model exists
print("\n✓ Test 1: Agreement Model")
print(f"  - Model registered: {Agreement._meta.app_label}.{Agreement._meta.model_name}")
print(f"  - Fields: {', '.join([f.name for f in Agreement._meta.get_fields()[:10]])}")

# Test 2: Check agreement number generation
print("\n✓ Test 2: Agreement Number Generation")
for agreement_type in ['funding', 'website']:
    num = generate_agreement_number(agreement_type)
    print(f"  - {agreement_type.title()}: {num}")

# Test 3: Check database table
print("\n✓ Test 3: Database Table")
import sqlite3
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM agreements_agreement")
count = cursor.fetchone()[0]
print(f"  - Total agreements in DB: {count}")
conn.close()

# Test 4: Verify templates exist
print("\n✓ Test 4: Template Files")
templates = [
    'templates/agreements/agreement_list.html',
    'templates/agreements/agreement_form.html',
    'templates/agreements/agreement_detail.html',
    'templates/agreements/pdf/funding_agreement.html',
    'templates/agreements/pdf/website_agreement.html',
]
for tmpl in templates:
    exists = os.path.exists(tmpl)
    status = "✓" if exists else "✗"
    print(f"  {status} {tmpl}")

# Test 5: Verify imports work
print("\n✓ Test 5: Dependencies")
try:
    from xhtml2pdf import pisa
    print(f"  ✓ xhtml2pdf: installed")
except ImportError:
    print(f"  ✗ xhtml2pdf: NOT installed")

try:
    from io import BytesIO
    print(f"  ✓ BytesIO: available")
except ImportError:
    print(f"  ✗ BytesIO: NOT available")

# Test 6: Check URL routing
print("\n✓ Test 6: URL Configuration")
from django.urls import reverse
try:
    url = reverse('agreements:agreement_list')
    print(f"  ✓ agreement_list: {url}")
    url = reverse('agreements:agreement_create')
    print(f"  ✓ agreement_create: {url}")
except:
    print(f"  ✗ URL routing error")

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
print("\nNow you can:")
print("1. Start server: python manage.py runserver")
print("2. Navigate to: http://localhost:8000/agreements/")
print("3. Create a new agreement")
print("4. Download as PDF")
