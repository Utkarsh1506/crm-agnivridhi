#!/usr/bin/env python
"""
Run the seed command for Agnivridhi employees
"""
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

# Now run the command
from django.core.management import call_command

if __name__ == '__main__':
    print("=" * 70)
    print("SEEDING AGNIVRIDHI EMPLOYEE DATA")
    print("=" * 70)
    call_command('seed_agnivridhi_employees')
    print("=" * 70)
    print("✓ SEEDING COMPLETE!")
    print("=" * 70)
