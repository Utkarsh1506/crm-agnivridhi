#!/usr/bin/env python
"""Diagnose invoice creation issue - check schema and attempt creation."""
import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from django.db import connection
from invoices.models import Invoice
from clients.models import Client
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, timedelta

User = get_user_model()

print("=== INVOICE CREATION DIAGNOSTIC ===\n")

# 1. Check schema
print("1. Checking database schema...")
vendor = connection.vendor
print(f"   Database: {vendor}")

with connection.cursor() as cursor:
    if vendor == 'mysql':
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'invoices_invoice' ORDER BY ordinal_position")
        cols = [r[0] for r in cursor.fetchall()]
    elif vendor == 'sqlite':
        cursor.execute("PRAGMA table_info(invoices_invoice);")
        cols = [r[1] for r in cursor.fetchall()]
    else:
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'invoices_invoice' ORDER BY ordinal_position")
        cols = [r[0] for r in cursor.fetchall()]

print(f"   Columns in invoices_invoice: {len(cols)}")

required_cols = ['invoice_number', 'invoice_type', 'client_id', 'issue_date', 
                 'item_description', 'hsn_sac', 'quantity', 'rate', 'gst_rate',
                 'taxable_amount', 'cgst_amount', 'sgst_amount', 'igst_amount', 
                 'total_amount', 'place_of_supply', 'created_by_id', 
                 'created_at', 'updated_at']

missing = [c for c in required_cols if c not in cols]
if missing:
    print(f"   MISSING COLUMNS: {missing}")
    print("   ACTION: Run 'python manage.py migrate invoices' on production")
else:
    print("   Schema OK - all required columns present")

# 2. Test invoice creation
print("\n2. Testing invoice creation...")
try:
    user = User.objects.filter(role='SALES').first() or User.objects.first()
    if not user:
        print("   ERROR: No users found")
        sys.exit(1)
    
    print(f"   Using user: {user.email} (role: {user.role})")
    
    client = Client.objects.filter(is_approved=True).first()
    if client:
        print(f"   Using client: {client.company_name}")
    else:
        print("   No approved clients - will use manual client details")
    
    # Test data
    test_invoice = {
        'invoice_number': 'TEST-DIAG-001',
        'invoice_type': 'tax' if client else 'proforma',
        'client': client,
        'client_name': 'Test Client' if not client else '',
        'client_address': 'Test Address' if not client else '',
        'client_city': 'Mumbai' if not client else '',
        'client_state': 'Maharashtra' if not client else '',
        'client_pincode': '400001' if not client else '',
        'client_mobile': '9876543210' if not client else '',
        'issue_date': date.today(),
        'due_date': date.today() + timedelta(days=15),
        'item_description': 'Diagnostic Test Service',
        'hsn_sac': '998314',
        'quantity': Decimal('1.00'),
        'rate': Decimal('1000.00'),
        'gst_rate': Decimal('18.00'),
        'taxable_amount': Decimal('1000.00'),
        'cgst_amount': Decimal('90.00'),
        'sgst_amount': Decimal('90.00'),
        'igst_amount': Decimal('0.00'),
        'total_amount': Decimal('1180.00'),
        'place_of_supply': 'Maharashtra',
        'notes': 'Diagnostic test invoice',
        'created_by': user,
    }
    
    print("   Creating test invoice...")
    inv = Invoice.objects.create(**test_invoice)
    print(f"   SUCCESS: Invoice created with ID {inv.id}")
    print(f"   Invoice Number: {inv.invoice_number}")
    print(f"   Total: Rs.{inv.total_amount}")
    print(f"   Created at: {inv.created_at}")
    print(f"   Updated at: {inv.updated_at}")
    
    # Clean up
    print("\n   Cleaning up test invoice...")
    inv.delete()
    print("   Test invoice deleted")
    
except Exception as e:
    print(f"   FAILED: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    print("\n   If you see OperationalError about missing column,")
    print("   run: python manage.py migrate invoices")

print("\n=== DIAGNOSTIC COMPLETE ===")
