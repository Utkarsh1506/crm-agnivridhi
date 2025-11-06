import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from accounts.models import User
from payments.models import Payment

print("=" * 60)
print("MANAGER-SALES RELATIONSHIP CHECK")
print("=" * 60)

managers = User.objects.filter(role='MANAGER')
sales_users = User.objects.filter(role='SALES')

print(f"\n📊 MANAGERS ({managers.count()}):")
print("-" * 60)
for m in managers:
    print(f"  • {m.username:15} - {m.get_full_name()}")
    team = User.objects.filter(manager=m, role='SALES')
    print(f"    Team size: {team.count()} sales employees")
    for s in team:
        print(f"      → {s.username} ({s.get_full_name()})")

print(f"\n👤 SALES EMPLOYEES ({sales_users.count()}):")
print("-" * 60)
for s in sales_users:
    mgr = s.manager.username if s.manager else "⚠️  NO MANAGER ASSIGNED"
    print(f"  • {s.username:15} - Manager: {mgr}")

print(f"\n💳 PENDING PAYMENTS:")
print("-" * 60)
pending_payments = Payment.objects.filter(status='PENDING').select_related('received_by', 'client')
if pending_payments.exists():
    for p in pending_payments:
        recorded_by = p.received_by.username if p.received_by else "Unknown"
        mgr = p.received_by.manager.username if p.received_by and p.received_by.manager else "NO MANAGER"
        print(f"  • Payment #{p.id} - ₹{p.amount}")
        print(f"    Client: {p.client.company_name}")
        print(f"    Recorded by: {recorded_by} (Manager: {mgr})")
        print()
else:
    print("  No pending payments")

print("\n" + "=" * 60)
print("FIX COMMAND (if needed):")
print("=" * 60)
print("python manage.py shell")
print(">>> from accounts.models import User")
print(">>> sales1 = User.objects.get(username='sales1')  # adjust username")
print(">>> manager1 = User.objects.get(username='manager1')  # adjust username")
print(">>> sales1.manager = manager1")
print(">>> sales1.save()")
print(">>> print('✅ Fixed!')")
