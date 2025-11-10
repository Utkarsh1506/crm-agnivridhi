#!/usr/bin/env python
"""
Data Migration Script: SQLite to MySQL
Exports data from local SQLite database and prepares for MySQL import
"""

import os
import sys
import django
import json
from pathlib import Path

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from django.core.management import call_command
from django.contrib.contenttypes.models import ContentType

print("=" * 60)
print("SQLite to MySQL Data Migration")
print("=" * 60)
print()

# Create backup directory
backup_dir = BASE_DIR / 'backup_data'
backup_dir.mkdir(exist_ok=True)

print(f"📁 Backup directory: {backup_dir}")
print()

# List of apps to export (in order of dependencies)
APPS_TO_EXPORT = [
    'accounts',
    'schemes',
    'clients',
    'bookings',
    'applications',
    'payments',
    'documents',
    'edit_requests',
    'notifications',
    'activity_logs',
]

print("🔄 Exporting data from SQLite...")
print()

for app in APPS_TO_EXPORT:
    output_file = backup_dir / f'{app}_data.json'
    print(f"Exporting {app}...", end=" ")
    
    try:
        with open(output_file, 'w') as f:
            call_command('dumpdata', app, 
                        format='json', 
                        indent=2,
                        stdout=f,
                        natural_foreign=True,
                        natural_primary=True)
        print(f"✅ Saved to {output_file.name}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

print()
print("=" * 60)
print("Export Complete!")
print("=" * 60)
print()
print("📦 Exported files are in:", backup_dir)
print()
print("Next steps:")
print("1. Upload backup_data/ folder to your Hostinger server")
print("2. Run migrations on MySQL: python manage.py migrate")
print("3. Load data: python manage.py loaddata backup_data/*.json")
print()
print("Alternative method:")
print("  Run: python import_to_mysql.py (see import_to_mysql.py)")
print()
