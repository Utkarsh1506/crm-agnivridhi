#!/usr/bin/env python
"""
Import Data to MySQL
Run this on Hostinger server after setting up MySQL database
"""

import os
import sys
import django
from pathlib import Path

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from django.core.management import call_command

print("=" * 60)
print("Import Data to MySQL")
print("=" * 60)
print()

# Ensure database is ready
print("🔍 Checking database connection...")
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print("✅ Database connection successful!")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    print("Please check your .env database settings.")
    sys.exit(1)

print()
print("🔄 Running migrations...")
call_command('migrate', '--noinput')

print()
print("📥 Importing data from fixtures...")
print()

backup_dir = BASE_DIR / 'backup_data'
if not backup_dir.exists():
    print(f"❌ Backup directory not found: {backup_dir}")
    print("Please upload the backup_data folder from your local machine.")
    sys.exit(1)

# Import in order of dependencies
IMPORT_ORDER = [
    'accounts_data.json',
    'schemes_data.json',
    'clients_data.json',
    'bookings_data.json',
    'applications_data.json',
    'payments_data.json',
    'documents_data.json',
    'edit_requests_data.json',
    'notifications_data.json',
    'activity_logs_data.json',
]

for fixture_file in IMPORT_ORDER:
    fixture_path = backup_dir / fixture_file
    
    if not fixture_path.exists():
        print(f"⚠️  Skipping {fixture_file} (not found)")
        continue
    
    print(f"Importing {fixture_file}...", end=" ")
    try:
        call_command('loaddata', str(fixture_path))
        print("✅")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print(f"   You may need to import this manually or skip it.")

print()
print("=" * 60)
print("Import Complete!")
print("=" * 60)
print()
print("🎉 Your data has been migrated to MySQL!")
print()
print("Next steps:")
print("1. Test the application: Visit your domain")
print("2. Login with your existing credentials")
print("3. Verify all data is present")
print("4. Create a database backup via Hostinger panel")
print()
