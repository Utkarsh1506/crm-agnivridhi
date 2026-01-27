# Generated migration to add document_number field and make file optional

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_alter_document_document_type_documentchecklist'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='document_number',
            field=models.CharField(blank=True, help_text='Manual document number/reference', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(blank=True, help_text='Uploaded/generated document file (optional)', null=True, upload_to='documents/%Y/%m/'),
        ),
    ]
