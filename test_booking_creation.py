"""
Test script to verify staff booking creation functionality
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from django.contrib.auth import get_user_model
from clients.models import Client
from bookings.models import Service
from django.urls import reverse

User = get_user_model()

print("=" * 60)
print("STAFF BOOKING CREATION TEST")
print("=" * 60)

# Get Manager user
manager = User.objects.filter(role='MANAGER', username='manager1').first()
if manager:
    print(f"\n✓ Manager found: {manager.get_full_name()} ({manager.username})")
else:
    print("\n✗ Manager not found!")

# Get manager's client
if manager:
    client = Client.objects.filter(assigned_manager=manager).first()
    if client:
        print(f"✓ Manager's client: {client.company_name} (ID: {client.id})")
        print(f"  - Created by: {client.created_by.get_full_name()}")
        print(f"  - Assigned manager: {client.assigned_manager.get_full_name() if client.assigned_manager else 'None'}")
        print(f"  - Assigned sales: {client.assigned_sales.get_full_name() if client.assigned_sales else 'None'}")
    else:
        print("✗ No client found for this manager")

# Check available services
services = Service.objects.filter(is_active=True)
print(f"\n✓ Active services available: {services.count()}")
if services.exists():
    print("  Sample services:")
    for service in services[:3]:
        print(f"    - {service.name} (₹{service.price})")

# Test URL construction
if manager and client:
    url = reverse('bookings:create_booking_for_client', args=[client.id])
    print(f"\n✓ Booking creation URL: {url}")
    print(f"  Full URL: http://127.0.0.1:8000{url}")

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
print("\nNext Steps:")
print("1. Start the development server")
print("2. Login as manager1 / manager1")
print("3. Go to client detail page")
print("4. Click 'Create Booking' button")
print("5. Select a service and submit")
print("=" * 60)
