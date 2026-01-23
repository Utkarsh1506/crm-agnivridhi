# Generated migration to fix charset for text fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0009_alter_client_sector'),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                # Fix business_description column charset
                "ALTER TABLE clients_client MODIFY business_description LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;",
                # Fix funding_purpose column charset
                "ALTER TABLE clients_client MODIFY funding_purpose LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;",
                # Fix notes column charset
                "ALTER TABLE clients_client MODIFY notes LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;",
                # Fix rejection_reason column charset
                "ALTER TABLE clients_client MODIFY rejection_reason LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;",
            ],
            reverse_sql=[
                # Reverse migration (going back to utf8 - not recommended but provided for completeness)
                "ALTER TABLE clients_client MODIFY business_description LONGTEXT CHARACTER SET utf8 COLLATE utf8_general_ci;",
                "ALTER TABLE clients_client MODIFY funding_purpose LONGTEXT CHARACTER SET utf8 COLLATE utf8_general_ci;",
                "ALTER TABLE clients_client MODIFY notes LONGTEXT CHARACTER SET utf8 COLLATE utf8_general_ci;",
                "ALTER TABLE clients_client MODIFY rejection_reason LONGTEXT CHARACTER SET utf8 COLLATE utf8_general_ci;",
            ],
        ),
    ]
