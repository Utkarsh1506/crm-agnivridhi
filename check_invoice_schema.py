#!/usr/bin/env python
"""Invoice schema verification script (supports SQLite/MySQL).
Run on production to confirm all required columns exist.
Usage: python check_invoice_schema.py
"""
import os, sys, django
from pprint import pprint

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')

django.setup()

from django.db import connection
from invoices.models import Invoice

REQUIRED_COLUMNS = [
    'invoice_number','invoice_type','client_id','client_name','client_contact_person','client_address',
    'client_city','client_state','client_pincode','client_gstin','client_mobile','issue_date','due_date',
    'item_description','hsn_sac','quantity','rate','gst_rate','taxable_amount','cgst_amount','sgst_amount',
    'igst_amount','total_amount','place_of_supply','notes','created_by_id','created_at','updated_at'
]

def get_columns():
    vendor = connection.vendor
    cols = []
    with connection.cursor() as cursor:
        if vendor == 'mysql':
            cursor.execute("SELECT column_name,data_type FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name='invoices_invoice'")
            cols = cursor.fetchall()
        elif vendor == 'sqlite':
            cursor.execute("PRAGMA table_info(invoices_invoice);")
            cols = [(r[1], r[2]) for r in cursor.fetchall()]
        else:
            cursor.execute("SELECT column_name,data_type FROM information_schema.columns WHERE table_name='invoices_invoice'")
            cols = cursor.fetchall()
    return cols

print("Database vendor:", connection.vendor)
columns = get_columns()
existing = {c[0] for c in columns}

print("\nExisting columns (name:type):")
for name, dtype in columns:
    print(f"- {name}: {dtype}")

print("\nMissing required columns:")
missing = [c for c in REQUIRED_COLUMNS if c not in existing]
if missing:
    for m in missing:
        print("✗", m)
else:
    print("None (all present) ✓")

print("\nModel fields (python_name -> db_column):")
for field in Invoice._meta.fields:  # concrete forward fields only
    print(f"* {field.name} -> {field.attname}")

print("\nSummary:")
print(f"Total concrete fields: {len(Invoice._meta.fields)}")
print(f"Missing columns count: {len(missing)}")
if missing:
    print("Action: Run migrations (python manage.py migrate invoices) or apply sync migration 0006.")
else:
    print("Schema OK ✓")
