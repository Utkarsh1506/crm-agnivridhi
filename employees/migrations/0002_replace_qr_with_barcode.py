"""
Migration: Replace QR code field with barcode field.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),  # Adjust based on your latest migration
    ]

    operations = [
        # Remove QR code field
        migrations.RemoveField(
            model_name='employee',
            name='qr_code',
        ),
        
        # Add barcode field
        migrations.AddField(
            model_name='employee',
            name='barcode',
            field=models.ImageField(
                blank=True,
                editable=False,
                help_text='Auto-generated barcode for employee identification',
                null=True,
                upload_to='employees/barcodes/%Y/%m/'
            ),
        ),
    ]
