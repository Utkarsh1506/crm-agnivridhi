from django.db import migrations, models
import django.db.models.deletion
import decimal

class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_revenueentry'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='description',
            field=models.CharField(blank=True, help_text='Payment description/purpose', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='booking',
            field=models.ForeignKey(blank=True, help_text='Associated booking (optional)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='bookings.booking'),
        ),
    ]
