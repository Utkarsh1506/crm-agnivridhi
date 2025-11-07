#!/usr/bin/env python
"""
Setup Company Organizational Structure
3 Managers → Each manages 3 Sales Employees → Each Sales has Clients
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from django.contrib.auth import get_user_model
from clients.models import Client
from bookings.models import Booking, Service
from payments.models import Payment
from applications.models import Application
from schemes.models import Scheme
from django.utils import timezone
from decimal import Decimal
import random

User = get_user_model()

print("\n" + "="*80)
print("COMPANY ORGANIZATIONAL STRUCTURE SETUP")
print("="*80)

# =============================================================================
# STEP 1: Create 3 Managers
# =============================================================================
print("\n[1/6] Creating Managers...")
managers = []
manager_data = [
    {'username': 'manager1', 'first_name': 'Rajesh', 'last_name': 'Kumar', 'email': 'rajesh.kumar@agnivridhiindia.com'},
    {'username': 'manager2', 'first_name': 'Priya', 'last_name': 'Sharma', 'email': 'priya.sharma@agnivridhiindia.com'},
    {'username': 'manager3', 'first_name': 'Amit', 'last_name': 'Patel', 'email': 'amit.patel@agnivridhiindia.com'},
]

for idx, data in enumerate(manager_data, 1):
    user, created = User.objects.get_or_create(
        username=data['username'],
        defaults={
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'role': 'MANAGER',
            'is_staff': True,
            'is_active': True,
        }
    )
    if created:
        user.set_password('test123')
        user.save()
        print(f"  ✓ Created: {data['first_name']} {data['last_name']} ({data['username']})")
    else:
        # Update existing user
        user.role = 'MANAGER'
        user.is_staff = True
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        user.save()
        print(f"  ↻ Updated: {data['first_name']} {data['last_name']} ({data['username']})")
    managers.append(user)

# =============================================================================
# STEP 2: Create 9 Sales Employees (3 per manager)
# =============================================================================
print("\n[2/6] Creating Sales Employees...")
sales_employees = []
sales_data = [
    # Manager 1's Team
    {'username': 'sales1', 'first_name': 'Sales', 'last_name': 'One', 'email': 'sales1@agnivridhiindia.com', 'manager_idx': 0},
    {'username': 'sales2', 'first_name': 'Neha', 'last_name': 'Gupta', 'email': 'neha.gupta@agnivridhiindia.com', 'manager_idx': 0},
    {'username': 'sales3', 'first_name': 'Rohit', 'last_name': 'Singh', 'email': 'rohit.singh@agnivridhiindia.com', 'manager_idx': 0},
    
    # Manager 2's Team
    {'username': 'sales4', 'first_name': 'Anjali', 'last_name': 'Verma', 'email': 'anjali.verma@agnivridhiindia.com', 'manager_idx': 1},
    {'username': 'sales5', 'first_name': 'Vikram', 'last_name': 'Reddy', 'email': 'vikram.reddy@agnivridhiindia.com', 'manager_idx': 1},
    {'username': 'sales6', 'first_name': 'Pooja', 'last_name': 'Nair', 'email': 'pooja.nair@agnivridhiindia.com', 'manager_idx': 1},
    
    # Manager 3's Team
    {'username': 'sales7', 'first_name': 'Karan', 'last_name': 'Malhotra', 'email': 'karan.malhotra@agnivridhiindia.com', 'manager_idx': 2},
    {'username': 'sales8', 'first_name': 'Divya', 'last_name': 'Iyer', 'email': 'divya.iyer@agnivridhiindia.com', 'manager_idx': 2},
    {'username': 'sales9', 'first_name': 'Arjun', 'last_name': 'Kapoor', 'email': 'arjun.kapoor@agnivridhiindia.com', 'manager_idx': 2},
]

for data in sales_data:
    manager = managers[data['manager_idx']]
    user, created = User.objects.get_or_create(
        username=data['username'],
        defaults={
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'role': 'SALES',
            'manager': manager,
            'is_staff': False,
            'is_active': True,
        }
    )
    if created:
        user.set_password('test123')
        user.save()
        print(f"  ✓ {data['first_name']} {data['last_name']} ({data['username']}) → reports to {manager.get_full_name()}")
    else:
        user.role = 'SALES'
        user.manager = manager
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        user.save()
        print(f"  ↻ {data['first_name']} {data['last_name']} ({data['username']}) → reports to {manager.get_full_name()}")
    sales_employees.append(user)

# =============================================================================
# STEP 3: Create Schemes (if not exist)
# =============================================================================
print("\n[3/6] Creating Loan Schemes...")
schemes_data = [
    {'name': 'MSME Business Loan', 'loan_type': 'BUSINESS', 'min_amount': 500000, 'max_amount': 50000000, 'interest_rate': 12.5},
    {'name': 'Working Capital Loan', 'loan_type': 'WORKING_CAPITAL', 'min_amount': 100000, 'max_amount': 10000000, 'interest_rate': 13.0},
    {'name': 'Term Loan', 'loan_type': 'TERM', 'min_amount': 1000000, 'max_amount': 100000000, 'interest_rate': 11.5},
]

schemes = []
for data in schemes_data:
    scheme, created = Scheme.objects.get_or_create(
        name=data['name'],
        defaults={
            'loan_type': data['loan_type'],
            'min_amount': data['min_amount'],
            'max_amount': data['max_amount'],
            'interest_rate': data['interest_rate'],
            'is_active': True,
        }
    )
    if created:
        print(f"  ✓ Created: {data['name']}")
    else:
        print(f"  ↻ Exists: {data['name']}")
    schemes.append(scheme)

# =============================================================================
# STEP 4: Create Clients (2-3 clients per sales employee)
# =============================================================================
print("\n[4/6] Creating Clients...")

company_names = [
    'TechVista Solutions Pvt Ltd', 'GreenLeaf Industries Ltd', 'NexGen Manufacturing Co',
    'BlueSky Enterprises Pvt Ltd', 'Sunrise Textiles Ltd', 'Apex Engineering Works',
    'Crystal Foods Pvt Ltd', 'Metro Logistics Ltd', 'Pioneer Electronics Co',
    'Global Trade Solutions', 'Stellar Pharmaceuticals Ltd', 'Omega Steel Industries',
    'Prime Automation Pvt Ltd', 'Bright Future Exports', 'Unity Plastics Ltd',
    'Vision Chemicals Co', 'Rapid Transport Services', 'Elite Packaging Pvt Ltd',
    'Fusion Tech Solutions', 'Royal Garments Ltd', 'Infinity Builders Pvt Ltd',
    'Zenith Imports Ltd', 'Skyline Consultancy', 'Galaxy Retail Chain',
]

sectors = ['MANUFACTURING', 'TECHNOLOGY', 'RETAIL', 'SERVICES', 'AGRICULTURE']
statuses = ['PROSPECT', 'QUALIFIED', 'ACTIVE']

clients_created = 0
for idx, sales_emp in enumerate(sales_employees):
    # Each sales employee gets 2-3 clients
    num_clients = random.randint(2, 3)
    
    for i in range(num_clients):
        company_name = company_names[clients_created % len(company_names)]
        
        client, created = Client.objects.get_or_create(
            company_name=company_name,
            defaults={
                'contact_person': f'{random.choice(["Rahul", "Sneha", "Arun", "Kavita", "Manish"])} {random.choice(["Shah", "Joshi", "Mehta", "Desai", "Pillai"])}',
                'email': f'contact.{clients_created}@{company_name.lower().replace(" ", "").replace("pvtltd", "").replace("ltd", "").replace("co", "")[:15]}.com',
                'phone': f'+91 {random.randint(7000000000, 9999999999)}',
                'sector': random.choice(sectors),
                'annual_turnover': Decimal(random.choice([50, 100, 200, 500, 1000, 2000])),
                'funding_required': Decimal(random.choice([10, 25, 50, 100, 200, 500])),
                'status': random.choice(statuses),
                'assigned_sales': sales_emp,
            }
        )
        
        if created:
            print(f"  ✓ {company_name} → assigned to {sales_emp.get_full_name()}")
            clients_created += 1
        else:
            # Update assignment
            client.assigned_sales = sales_emp
            client.save()
            print(f"  ↻ {company_name} → reassigned to {sales_emp.get_full_name()}")
            clients_created += 1

# =============================================================================
# STEP 5: Create Bookings for Active Clients
# =============================================================================
print("\n[5/6] Creating Bookings...")

# Get or create a service
service, _ = Service.objects.get_or_create(
    name='Loan Processing',
    defaults={
        'description': 'Complete loan application processing service',
        'price': Decimal('5000.00'),
        'is_active': True,
    }
)

active_clients = Client.objects.filter(status='ACTIVE')
bookings_created = 0

for client in active_clients[:15]:  # Create bookings for up to 15 active clients
    # 1-2 bookings per active client
    num_bookings = random.randint(1, 2)
    
    for i in range(num_bookings):
        scheme = random.choice(schemes)
        
        booking, created = Booking.objects.get_or_create(
            client=client,
            scheme=scheme,
            defaults={
                'assigned_to': client.assigned_sales,
                'status': random.choice(['PENDING', 'CONFIRMED', 'PAID']),
                'total_amount': Decimal(random.choice([5000, 10000, 15000, 20000])),
                'booking_date': timezone.now(),
            }
        )
        
        if created:
            print(f"  ✓ Booking for {client.company_name} - {scheme.name} (₹{booking.total_amount})")
            bookings_created += 1

print(f"\n  Total bookings created: {bookings_created}")

# =============================================================================
# STEP 6: Create Some Payments for PAID Bookings
# =============================================================================
print("\n[6/6] Creating Payments for PAID Bookings...")

paid_bookings = Booking.objects.filter(status='PAID', payment__isnull=True)
payments_created = 0

for booking in paid_bookings[:10]:  # Create payments for up to 10 bookings
    payment, created = Payment.objects.get_or_create(
        booking=booking,
        defaults={
            'client': booking.client,
            'amount': booking.total_amount,
            'payment_method': random.choice(['UPI_QR', 'BANK_TRANSFER', 'CASH']),
            'reference_id': f'REF-{booking.id}-{random.randint(1000, 9999)}',
            'received_by': booking.assigned_to,
            'status': random.choice(['PENDING', 'CAPTURED']),
            'payment_date': timezone.now(),
        }
    )
    
    if created:
        print(f"  ✓ Payment ₹{payment.amount} for {booking.client.company_name}")
        payments_created += 1

print(f"\n  Total payments created: {payments_created}")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "="*80)
print("SETUP COMPLETE - ORGANIZATIONAL STRUCTURE SUMMARY")
print("="*80)

print(f"\n📊 HIERARCHY:")
print(f"   └─ 3 Managers")
print(f"      └─ 9 Sales Employees (3 per manager)")
print(f"         └─ ~{clients_created} Clients (2-3 per sales employee)")
print(f"            └─ {bookings_created} Bookings")
print(f"               └─ {payments_created} Payments")

print(f"\n👥 TEAM BREAKDOWN:")
for i, manager in enumerate(managers, 1):
    team = User.objects.filter(role='SALES', manager=manager)
    team_clients = Client.objects.filter(assigned_sales__in=team)
    print(f"\n  Manager {i}: {manager.get_full_name()} ({manager.username})")
    for sales in team:
        client_count = Client.objects.filter(assigned_sales=sales).count()
        booking_count = Booking.objects.filter(assigned_to=sales).count()
        print(f"    ├─ {sales.get_full_name()} ({sales.username}): {client_count} clients, {booking_count} bookings")

print(f"\n🔑 LOGIN CREDENTIALS:")
print(f"   All users password: test123")
print(f"\n   Managers:")
for manager in managers:
    print(f"     • {manager.username} / test123")
print(f"\n   Sales Employees:")
for sales in sales_employees:
    print(f"     • {sales.username} / test123")

print(f"\n✅ Ready to test multi-tier management and data isolation!")
print("="*80 + "\n")
