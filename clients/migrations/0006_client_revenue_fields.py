from django.db import migrations, models
import decimal

class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0005_alter_client_address_line1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='total_pitched_amount',
            field=models.DecimalField(default=decimal.Decimal('0.00'), help_text='Total pitched amount (₹) discussed with client', max_digits=12, decimal_places=2),
        ),
        migrations.AddField(
            model_name='client',
            name='received_amount',
            field=models.DecimalField(default=decimal.Decimal('0.00'), help_text='Total amount (₹) received so far from client', max_digits=12, decimal_places=2),
        ),
        migrations.AddField(
            model_name='client',
            name='pending_amount',
            field=models.DecimalField(default=decimal.Decimal('0.00'), help_text='Pending amount (₹) expected from client', max_digits=12, decimal_places=2),
        ),
    ]
