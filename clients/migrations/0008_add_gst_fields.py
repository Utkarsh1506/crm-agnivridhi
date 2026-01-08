from django.db import migrations, models
import decimal

class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_merge_0006_client_pending_and_0006_client_revenue_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='gst_percentage',
            field=models.DecimalField(decimal_places=2, default=decimal.Decimal('18.00'), help_text='GST percentage to apply', max_digits=5),
        ),
        migrations.AddField(
            model_name='client',
            name='gst_amount',
            field=models.DecimalField(decimal_places=2, default=decimal.Decimal('0.00'), help_text='GST amount (auto-calculated)', max_digits=12),
        ),
        migrations.AddField(
            model_name='client',
            name='total_with_gst',
            field=models.DecimalField(decimal_places=2, default=decimal.Decimal('0.00'), help_text='Total pitched amount including GST', max_digits=12),
        ),
        migrations.AlterField(
            model_name='client',
            name='total_pitched_amount',
            field=models.DecimalField(decimal_places=2, default=decimal.Decimal('0.00'), help_text='Total pitched amount (₹) discussed with client (excluding GST)', max_digits=12),
        ),
    ]
