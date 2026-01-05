"""
Initial migration for Employees app.
Creates Employee, EmployeeIDSequence, and EmployeeVerificationLog models.
"""
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0004_alter_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, help_text='Unique identifier for internal tracking')),
                ('employee_id', models.CharField(db_index=True, editable=False, help_text='Auto-generated unique employee ID (e.g., AGN-EMP-001)', max_length=20, unique=True)),
                ('full_name', models.CharField(db_index=True, help_text='Full legal name of the employee', max_length=200)),
                ('designation', models.CharField(help_text='Job title/designation', max_length=100)),
                ('department', models.CharField(db_index=True, help_text='Department name (e.g., Sales, HR, Engineering)', max_length=100)),
                ('employee_photo', models.ImageField(help_text='Employee portrait photo (JPG, PNG recommended)', upload_to='employees/photos/%Y/%m/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])])),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], db_index=True, default='ACTIVE', help_text='Employment status', max_length=10)),
                ('date_of_joining', models.DateField(default=django.utils.timezone.now, help_text='Employee joining date')),
                ('date_of_exit', models.DateField(blank=True, help_text='Employee exit/termination date (if applicable)', null=True)),
                ('qr_code', models.ImageField(blank=True, editable=False, help_text='Auto-generated QR code for verification', null=True, upload_to='employees/qrcodes/%Y/%m/')),
                ('verification_token', models.CharField(db_index=True, editable=False, help_text='Unique token for verification endpoint', max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Record creation timestamp')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Record last update timestamp')),
                ('created_by', models.ForeignKey(blank=True, help_text='User who created this employee record', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees_created', to='accounts.user')),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
                'db_table': 'employee',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='EmployeeIDSequence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_sequence_number', models.IntegerField(default=0, help_text='Last assigned sequence number for employee IDs')),
                ('prefix', models.CharField(default='AGN-EMP-', editable=False, help_text='Prefix for employee IDs', max_length=20)),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Last update timestamp')),
            ],
            options={
                'verbose_name': 'Employee ID Sequence',
                'verbose_name_plural': 'Employee ID Sequences',
                'db_table': 'employee_id_sequence',
            },
        ),
        migrations.CreateModel(
            name='EmployeeVerificationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True, help_text='Verification attempt timestamp')),
                ('ip_address', models.GenericIPAddressField(blank=True, help_text='IP address of verification attempt', null=True)),
                ('user_agent', models.TextField(blank=True, help_text='Browser user agent')),
                ('employee', models.ForeignKey(help_text='Employee being verified', on_delete=django.db.models.deletion.CASCADE, related_name='verification_logs', to='employees.employee')),
            ],
            options={
                'verbose_name': 'Employee Verification Log',
                'verbose_name_plural': 'Employee Verification Logs',
                'db_table': 'employee_verification_log',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddIndex(
            model_name='employee',
            index=models.Index(fields=['employee_id'], name='employee_employee_id_idx'),
        ),
        migrations.AddIndex(
            model_name='employee',
            index=models.Index(fields=['status'], name='employee_status_idx'),
        ),
        migrations.AddIndex(
            model_name='employee',
            index=models.Index(fields=['department'], name='employee_department_idx'),
        ),
        migrations.AddIndex(
            model_name='employee',
            index=models.Index(fields=['created_at'], name='employee_created_at_idx'),
        ),
        migrations.AddIndex(
            model_name='employeeverificationlog',
            index=models.Index(fields=['employee', 'timestamp'], name='employee_employee_timestamp_idx'),
        ),
    ]
