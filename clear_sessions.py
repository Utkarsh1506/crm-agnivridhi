"""
Clear all sessions to fix CSRF issues after role changes
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from django.contrib.sessions.models import Session

# Delete all sessions
count = Session.objects.all().count()
Session.objects.all().delete()

print(f"✓ Cleared {count} session(s)")
print("Please log in again at http://127.0.0.1:8000/login/")
