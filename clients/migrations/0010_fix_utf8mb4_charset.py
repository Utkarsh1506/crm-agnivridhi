# Generated migration to fix charset for text fields
from django.db import migrations


def apply_mysql_charset_fix(apps, schema_editor):
    """Only apply charset fixes on MySQL databases"""
    if schema_editor.connection.vendor == 'mysql':
        with schema_editor.connection.cursor() as cursor:
            cursor.execute("ALTER TABLE clients_client MODIFY business_description LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            cursor.execute("ALTER TABLE clients_client MODIFY funding_purpose LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            cursor.execute("ALTER TABLE clients_client MODIFY notes LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            cursor.execute("ALTER TABLE clients_client MODIFY rejection_reason LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0008_add_gst_fields'),
    ]

    operations = [
        migrations.RunPython(apply_mysql_charset_fix, migrations.RunPython.noop),
    ]
