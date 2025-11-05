"""
Utility functions for accounts app
"""
import csv
from io import StringIO
from django.http import HttpResponse
from datetime import datetime


def export_to_csv(queryset, fields, filename_prefix='export'):
    """
    Generic function to export queryset to CSV
    
    Args:
        queryset: Django queryset to export
        fields: List of field names to include
        filename_prefix: Prefix for the downloaded filename
    
    Returns:
        HttpResponse with CSV content
    """
    response = HttpResponse(content_type='text/csv')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    response['Content-Disposition'] = f'attachment; filename="{filename_prefix}_{timestamp}.csv"'
    
    writer = csv.writer(response)
    
    # Write header row
    headers = []
    for field in fields:
        if isinstance(field, dict):
            headers.append(field.get('label', field.get('name', '')))
        else:
            headers.append(field.replace('_', ' ').title())
    writer.writerow(headers)
    
    # Write data rows
    for obj in queryset:
        row = []
        for field in fields:
            if isinstance(field, dict):
                field_name = field.get('name')
                accessor = field.get('accessor')
                if accessor:
                    # Custom accessor function
                    value = accessor(obj)
                else:
                    # Standard field access
                    value = getattr(obj, field_name, '')
            else:
                value = getattr(obj, field, '')
            
            # Handle special types
            if hasattr(value, 'all'):  # ManyToMany or reverse FK
                value = ', '.join(str(v) for v in value.all())
            elif callable(value):
                value = value()
            
            row.append(str(value))
        writer.writerow(row)
    
    return response


def get_field_value(obj, field_path):
    """
    Get nested field value from object using dot notation
    Example: 'client.company_name' or 'assigned_to.get_full_name'
    """
    parts = field_path.split('.')
    value = obj
    for part in parts:
        if hasattr(value, part):
            value = getattr(value, part)
            if callable(value):
                value = value()
        else:
            return ''
    return value
