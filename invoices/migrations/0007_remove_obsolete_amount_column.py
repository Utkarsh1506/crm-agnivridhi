"""Remove obsolete columns from invoices_invoice table.

Automatically detects and removes columns that exist in DB but not in the model.
"""
from django.db import migrations


def remove_obsolete_columns(apps, schema_editor):
    """Remove columns that exist in DB but not in current model."""
    connection = schema_editor.connection
    vendor = connection.vendor
    table = 'invoices_invoice'
    
    if vendor != 'mysql':
        return  # Only needed for MySQL production
    
    # Get model fields (expected columns)
    Invoice = apps.get_model('invoices', 'Invoice')
    model_fields = {f.column for f in Invoice._meta.fields if hasattr(f, 'column')}
    
    with connection.cursor() as cursor:
        # Get all existing columns in database
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = DATABASE() 
            AND table_name = %s
            ORDER BY column_name
        """, [table])
        db_columns = {row[0] for row in cursor.fetchall()}
        
        # Find obsolete columns (in DB but not in model)
        obsolete = db_columns - model_fields
        
        if not obsolete:
            print(f"✓ No obsolete columns found in {table}")
            return
        
        print(f"\n🔧 Found {len(obsolete)} obsolete column(s) in {table}:")
        for col in sorted(obsolete):
            print(f"   - {col}")
        
        # Remove each obsolete column
        for col_name in sorted(obsolete):
            print(f"\n   Dropping '{col_name}'...", end=' ')
            try:
                cursor.execute(f"ALTER TABLE `{table}` DROP COLUMN `{col_name}`;")
                print("✓ Done")
            except Exception as e:
                print(f"✗ Failed: {e}")
        
        print(f"\n✓ Cleanup complete")



def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('invoices', '0006_sync_invoice_columns'),
    ]

    operations = [
        migrations.RunPython(remove_obsolete_columns, noop),
    ]
