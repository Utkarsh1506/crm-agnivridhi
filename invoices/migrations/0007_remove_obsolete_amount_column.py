"""Remove obsolete 'amount' column from invoices_invoice table.

This column is not in the current model and is causing IntegrityError.
"""
from django.db import migrations


def remove_amount_column(apps, schema_editor):
    """Remove old 'amount' column if it exists."""
    connection = schema_editor.connection
    vendor = connection.vendor
    table = 'invoices_invoice'
    
    if vendor != 'mysql':
        return  # Only needed for MySQL production
    
    with connection.cursor() as cursor:
        # Check if column exists
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = DATABASE() 
            AND table_name = %s 
            AND column_name = 'amount'
        """, [table])
        
        if cursor.fetchone():
            print(f"Removing obsolete 'amount' column from {table}...")
            try:
                cursor.execute(f"ALTER TABLE `{table}` DROP COLUMN `amount`;")
                print("  Column removed successfully")
            except Exception as e:
                print(f"  Warning: Could not remove column: {e}")


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('invoices', '0006_sync_invoice_columns'),
    ]

    operations = [
        migrations.RunPython(remove_amount_column, noop),
    ]
