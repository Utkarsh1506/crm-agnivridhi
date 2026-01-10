from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
        ('bookings', '0002_add_service_faqs'),
        ('notifications', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SupportRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('OPEN', 'Open'), ('IN_PROGRESS', 'In Progress'), ('RESOLVED', 'Resolved')], default='OPEN', max_length=20)),
                ('contact_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('contact_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='support_requests_assigned', to=settings.AUTH_USER_MODEL)),
                ('booking', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='support_requests', to='bookings.booking')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='support_requests', to='clients.client')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='support_requests_created', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Support Request',
                'verbose_name_plural': 'Support Requests',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='supportrequest',
            index=models.Index(fields=['client', 'status'], name='support_cli_status_idx'),
        ),
        migrations.AddIndex(
            model_name='supportrequest',
            index=models.Index(fields=['assigned_to', 'status'], name='support_assigned_status_idx'),
        ),
        migrations.AddIndex(
            model_name='supportrequest',
            index=models.Index(fields=['-created_at'], name='support_created_idx'),
        ),
    ]
