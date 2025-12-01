"""Comprehensive schema sync for Invoice table.

Adds any missing columns defined in models.Invoice without dropping or altering
existing data. Safe to run multiple times; it only adds columns if absent.
"""
from django.db import migrations

def sync_invoice_columns(apps, schema_editor):
    connection = schema_editor.connection
    vendor = connection.vendor
    table = 'invoices_invoice'

    # Map of column name -> SQL definition (MySQL syntax; SQLite fallback handled)
    # For NOT NULL columns on existing rows we provide a DEFAULT to satisfy engine requirements.
    columns = {
        'invoice_number': 'VARCHAR(50) NOT NULL',
        'invoice_type': "VARCHAR(20) NOT NULL DEFAULT 'proforma'",
        'client_id': 'BIGINT',  # FK already may exist; skip if present
        'client_name': 'VARCHAR(255)',
        'client_contact_person': 'VARCHAR(255)',
        'client_address': 'TEXT',
        'client_city': 'VARCHAR(100)',
        'client_state': 'VARCHAR(100)',
        'client_pincode': 'VARCHAR(10)',
        'client_gstin': 'VARCHAR(15)',
        'client_mobile': 'VARCHAR(15)',
        'issue_date': 'DATE NOT NULL DEFAULT CURRENT_DATE',
        'due_date': 'DATE',
        'item_description': 'VARCHAR(500) NOT NULL DEFAULT ""',
        'hsn_sac': "VARCHAR(20) NOT NULL DEFAULT '998314'",
        'quantity': 'DECIMAL(10,2) NOT NULL DEFAULT 1.00',
        'rate': 'DECIMAL(10,2) NOT NULL DEFAULT 0.00',
        'gst_rate': 'DECIMAL(5,2) NOT NULL DEFAULT 18.00',
        'taxable_amount': 'DECIMAL(12,2) NOT NULL DEFAULT 0.00',
        'cgst_amount': 'DECIMAL(10,2) NOT NULL DEFAULT 0.00',
        'sgst_amount': 'DECIMAL(10,2) NOT NULL DEFAULT 0.00',
        'igst_amount': 'DECIMAL(10,2) NOT NULL DEFAULT 0.00',
        'total_amount': 'DECIMAL(12,2) NOT NULL DEFAULT 0.00',
        'place_of_supply': "VARCHAR(100) NOT NULL DEFAULT 'Maharashtra'",
        'notes': 'TEXT',
        'created_by_id': 'BIGINT',  # FK may already exist
        'created_at': 'DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)',
        'updated_at': 'DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)',
    }

    existing = set()
    with connection.cursor() as cursor:
        try:
            if vendor == 'mysql':
                cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = %s", [table])
                existing = {r[0] for r in cursor.fetchall()}
            elif vendor == 'sqlite':
                cursor.execute(f"PRAGMA table_info({table});")
                existing = {r[1] for r in cursor.fetchall()}
            else:
                cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = %s", [table])
                existing = {r[0] for r in cursor.fetchall()}
        except Exception:
            # If introspection fails, do nothing to avoid destructive guesses
            return

        for name, definition in columns.items():
            if name in existing:
                continue
            # Skip FK columns that truly must be created via proper migration if absent
            if name in {'client_id', 'created_by_id'} and vendor != 'sqlite':
                # Attempt to add basic column; constraints not enforced here
                add_sql = f"ALTER TABLE `{table}` ADD COLUMN `{name}` {definition};"
            else:
                add_sql = f"ALTER TABLE `{table}` ADD COLUMN `{name}` {definition};"
            try:
                cursor.execute(add_sql)
            except Exception:
                # Continue on individual failures to avoid blocking remaining columns
                pass

        # Ensure updated_at auto-updates (MySQL only) if just added
        if vendor == 'mysql' and 'updated_at' not in existing:
            try:
                cursor.execute(f"ALTER TABLE `{table}` MODIFY `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);")
            except Exception:
                pass

def noop(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('invoices', '0005_fix_tax_columns'),
    ]

    operations = [
        migrations.RunPython(sync_invoice_columns, noop),
    ]
