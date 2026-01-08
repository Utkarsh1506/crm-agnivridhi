from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('clients', '0006_client_pending_amount_client_received_amount_and_more'),
        ('clients', '0006_client_revenue_fields'),
    ]

    operations = [
        # No-op merge migration; both branches add the same fields
    ]
