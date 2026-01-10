from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.add_field(
            model_name='service',
            name='faqs',
            field=models.JSONField(default=list, help_text='FAQ entries for this service'),
        ),
    ]
