import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from bookings.models import Service
from schemes.models import Scheme
from django.db.models import Count

print("=" * 70)
print("SERVICES AND SCHEMES SUMMARY")
print("=" * 70)

print(f"\nTotal Active Services: {Service.objects.filter(is_active=True).count()}")
print(f"Total Active Schemes: {Scheme.objects.filter(status='ACTIVE').count()}")

print("\n" + "=" * 70)
print("SERVICES BY CATEGORY")
print("=" * 70)

for cat_code, cat_name in Service.Category.choices:
    count = Service.objects.filter(is_active=True, category=cat_code).count()
    if count > 0:
        print(f"\n{cat_name}:")
        for service in Service.objects.filter(is_active=True, category=cat_code).order_by('name'):
            print(f"  • {service.name} - ₹{service.price}")

print("\n" + "=" * 70)
print("SCHEMES BY CATEGORY")
print("=" * 70)

for cat_code, cat_name in Scheme.Category.choices:
    schemes = Scheme.objects.filter(status='ACTIVE', category=cat_code).order_by('name')
    if schemes.exists():
        print(f"\n{cat_name}:")
        for scheme in schemes:
            funding_range = ""
            if scheme.min_funding and scheme.max_funding:
                funding_range = f" (₹{scheme.min_funding}-{scheme.max_funding} Lakh)"
            print(f"  • {scheme.name}{funding_range}")

print("\n" + "=" * 70)
print("SETUP COMPLETE!")
print("=" * 70)
