# Generated migration for client approval flow

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='is_approved',
            field=models.BooleanField(default=True, help_text='Whether client is approved by manager'),
        ),
        migrations.AddField(
            model_name='client',
            name='approved_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='approved_clients',
                to=settings.AUTH_USER_MODEL,
                help_text='Manager who approved this client'
            ),
        ),
        migrations.AddField(
            model_name='client',
            name='approved_at',
            field=models.DateTimeField(
                blank=True,
                null=True,
                help_text='Date when client was approved'
            ),
        ),
        migrations.AddField(
            model_name='client',
            name='rejection_reason',
            field=models.TextField(
                blank=True,
                null=True,
                help_text='Reason for rejection if not approved'
            ),
        ),
    ]
