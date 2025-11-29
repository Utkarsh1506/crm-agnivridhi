# Generated corrective migration to ensure tax columns exist on MySQL
from django.db import migrations

def ensure_tax_columns(apps, schema_editor):
    table = 'invoices_invoice'
    connection = schema_editor.connection
    vendor = connection.vendor

    # Column definitions: (name, sql_type, null_allowed, default_sql)
    cols = [
        ('taxable_amount', 'DECIMAL(12,2)', False, None),
        ('cgst_amount', 'DECIMAL(10,2)', True, "DEFAULT 0.00"),
        ('sgst_amount', 'DECIMAL(10,2)', True, "DEFAULT 0.00"),
        ('igst_amount', 'DECIMAL(10,2)', True, "DEFAULT 0.00"),
        ('total_amount', 'DECIMAL(12,2)', False, None),
    ]

    with connection.cursor() as cursor:
        db_columns = []
        try:
            if vendor == 'mysql':
                cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = %s", [table])
                db_columns = [row[0] for row in cursor.fetchall()]
            elif vendor == 'sqlite':
                cursor.execute("PRAGMA table_info(%s);" % table)
                db_columns = [row[1] for row in cursor.fetchall()]
            else:
                cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = %s", [table])
                db_columns = [row[0] for row in cursor.fetchall()]
        except Exception:
            db_columns = []

        for name, sql_type, allow_null, default_sql in cols:
            if name in db_columns:
                continue
            # Build ALTER TABLE statement
            null_sql = "NULL" if allow_null else "NOT NULL"
            default_clause = f" {default_sql}" if default_sql else ""
            alter = f"ALTER TABLE `{table}` ADD COLUMN `{name}` {sql_type} {null_sql}{default_clause};"
            cursor.execute(alter)


def reverse_code(apps, schema_editor):
    # No-op: do not drop columns on reverse
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('invoices', '0004_invoice_client_address_invoice_client_city_and_more'),
    ]

    operations = [
        migrations.RunPython(ensure_tax_columns, reverse_code),
    ]
