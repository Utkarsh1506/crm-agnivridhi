#!/usr/bin/env python
"""List all actual columns in production invoices_invoice table."""
import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from django.db import connection

print("=== PRODUCTION TABLE SCHEMA ===\n")

vendor = connection.vendor
print(f"Database: {vendor}\n")

with connection.cursor() as cursor:
    if vendor == 'mysql':
        cursor.execute("""
            SELECT column_name, column_type, is_nullable, column_default, extra
            FROM information_schema.columns 
            WHERE table_schema = DATABASE() 
            AND table_name = 'invoices_invoice'
            ORDER BY ordinal_position
        """)
        cols = cursor.fetchall()
        print(f"Total columns: {len(cols)}\n")
        print(f"{'Column Name':<30} {'Type':<20} {'Nullable':<10} {'Default':<15} {'Extra'}")
        print("-" * 95)
        for name, dtype, nullable, default, extra in cols:
            default_str = str(default)[:14] if default else 'NULL'
            print(f"{name:<30} {dtype:<20} {nullable:<10} {default_str:<15} {extra}")
    elif vendor == 'sqlite':
        cursor.execute("PRAGMA table_info(invoices_invoice);")
        cols = cursor.fetchall()
        print(f"Total columns: {len(cols)}\n")
        for col in cols:
            print(col)

print("\n=== MODEL FIELDS (Expected) ===\n")
from invoices.models import Invoice

model_fields = [f.attname for f in Invoice._meta.fields]
print(f"Total model fields: {len(model_fields)}\n")
for idx, field in enumerate(model_fields, 1):
    print(f"{idx:2}. {field}")

print("\n=== COMPARISON ===\n")
if vendor == 'mysql':
    db_cols = {c[0] for c in cols}
    model_cols = set(model_fields)
    
    extra_in_db = db_cols - model_cols
    missing_in_db = model_cols - db_cols
    
    if extra_in_db:
        print("Extra columns in DATABASE (not in model):")
        for col in sorted(extra_in_db):
            print(f"  - {col}")
    
    if missing_in_db:
        print("\nMissing columns in DATABASE (defined in model):")
        for col in sorted(missing_in_db):
            print(f"  - {col}")
    
    if not extra_in_db and not missing_in_db:
        print("Schema matches perfectly!")
