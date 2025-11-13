#!/usr/bin/env python
"""
Create comprehensive test data for all roles
Tests real-time connectivity and system functionality
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from accounts.models import User
from clients.models import Client
from schemes.models import Scheme
from bookings.models import Booking
from applications.models import Application
from payments.models import Payment
from documents.models import Document, DocumentChecklist
from tracking.models import ClientActivity, ServiceOffering, ClientServiceEnrollment

def create_comprehensive_test_data():
    """Create test data for all roles"""
    
    print("=" * 80)
    print("🚀 CREATING COMPREHENSIVE TEST DATA FOR ALL ROLES")
    print("=" * 80)
    
    # ==================== USERS ====================
    print("\n👥 STEP 1: Creating/Verifying Users...")
    
    # Admin
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@agnivridhiindia.com',
            'role': 'ADMIN',
            'first_name': 'System',
            'last_name': 'Admin'
        }
    )
    if created:
        admin.set_password('Admin@123')
        admin.save()
        print("  ✅ Created Admin user")
    else:
        print("  ✓ Admin user exists")
    
    # Manager
    manager, created = User.objects.get_or_create(
        username='manager1',
        defaults={
            'email': 'manager1@agnivridhiindia.com',
            'role': 'MANAGER',
            'first_name': 'Rajesh',
            'last_name': 'Kumar'
        }
    )
    if created:
        manager.set_password('Manager@123')
        manager.save()
        print("  ✅ Created Manager user")
    else:
        print("  ✓ Manager user exists")
    
    # Sales Users (3)
    sales_users = []
    for i in range(1, 4):
        sales, created = User.objects.get_or_create(
            username=f'sales{i}',
            defaults={
                'email': f'sales{i}@agnivridhiindia.com',
                'role': 'SALES',
                'first_name': ['Amit', 'Priya', 'Rahul'][i-1],
                'last_name': ['Shah', 'Patel', 'Verma'][i-1]
            }
        )
        if created:
            sales.set_password('Sales@123')
            sales.save()
            print(f"  ✅ Created Sales user: {sales.first_name}")
        else:
            print(f"  ✓ Sales user exists: {sales.first_name}")
        sales_users.append(sales)
    
    # Client Users (3)
    client_users = []
    for i in range(1, 4):
        client_user, created = User.objects.get_or_create(
            username=f'client{i}',
            defaults={
                'email': f'client{i}@testcompany.com',
                'role': 'CLIENT',
                'first_name': ['Suresh', 'Meena', 'Vikram'][i-1],
                'last_name': ['Gupta', 'Reddy', 'Singh'][i-1]
            }
        )
        if created:
            client_user.set_password('Client@123')
            client_user.save()
            print(f"  ✅ Created Client user: {client_user.first_name}")
        else:
            print(f"  ✓ Client user exists: {client_user.first_name}")
        client_users.append(client_user)
    
    # ==================== CLIENTS ====================
    print("\n🏢 STEP 2: Creating Client Profiles...")
    
    clients = []
    client_data = [
        {
            'company_name': 'TechVenture Solutions Pvt Ltd',
            'business_type': 'PVT_LTD',
            'sector': 'IT_SOFTWARE',
            'company_age': 3,
            'annual_turnover': 75.00,
            'funding_required': 50.00,
            'city': 'Bangalore',
            'state': 'Karnataka'
        },
        {
            'company_name': 'Green Agro Industries',
            'business_type': 'PARTNERSHIP',
            'sector': 'AGRICULTURE',
            'company_age': 5,
            'annual_turnover': 120.00,
            'funding_required': 80.00,
            'city': 'Pune',
            'state': 'Maharashtra'
        },
        {
            'company_name': 'MediCare Health Services',
            'business_type': 'PVT_LTD',
            'sector': 'HEALTHCARE',
            'company_age': 2,
            'annual_turnover': 45.00,
            'funding_required': 30.00,
            'city': 'Delhi',
            'state': 'Delhi'
        }
    ]
    
    for i, data in enumerate(client_data):
        client, created = Client.objects.get_or_create(
            user=client_users[i],
            defaults={
                **data,
                'registration_number': f'U12345KA202{i}PTC12345{i}',
                'gst_number': f'29AABCU123{i}D1Z{i}',
                'pan_number': f'AABCU123{i}D',
                'contact_person': f"{client_users[i].first_name} {client_users[i].last_name}",
                'contact_email': client_users[i].email,
                'contact_phone': f'987654321{i}',
                'address_line1': f'{100 + i*10}, Test Street',
                'pincode': f'56000{i}',
                'assigned_sales': sales_users[i % len(sales_users)],
                'created_by': sales_users[i % len(sales_users)],
                'status': 'ACTIVE'
            }
        )
        if created:
            print(f"  ✅ Created: {client.company_name} (assigned to {client.assigned_sales.first_name})")
        else:
            print(f"  ✓ Exists: {client.company_name}")
        clients.append(client)
    
    # ==================== SERVICES ====================
    print("\n💼 STEP 3: Creating Service Offerings...")
    
    services_data = [
        {
            'service_type': 'WEB_DEVELOPMENT',
            'name': 'Professional Website Development',
            'short_description': 'Custom business website with responsive design',
            'description': 'Complete website development with admin panel, SEO, and hosting support',
            'pricing_type': 'PROJECT',
            'base_price': 25000,
            'icon': 'bi-globe',
            'is_featured': True,
            'display_order': 1
        },
        {
            'service_type': 'DIGITAL_MARKETING',
            'name': 'Digital Marketing Package',
            'short_description': 'Social media and online marketing',
            'description': 'Complete digital presence including social media, SEO, and ad campaigns',
            'pricing_type': 'HOURLY',
            'base_price': 1500,
            'icon': 'bi-megaphone',
            'is_featured': True,
            'display_order': 2
        },
        {
            'service_type': 'CERTIFICATION',
            'name': 'Business Certifications',
            'short_description': 'MSME, GST, ISO certifications',
            'description': 'Help with all business certifications and registrations',
            'pricing_type': 'CUSTOM',
            'icon': 'bi-award',
            'is_featured': True,
            'display_order': 3
        }
    ]
    
    services = []
    for service_data in services_data:
        service, created = ServiceOffering.objects.get_or_create(
            name=service_data['name'],
            defaults=service_data
        )
        if created:
            print(f"  ✅ Created: {service.name}")
        else:
            print(f"  ✓ Exists: {service.name}")
        services.append(service)
    
    # ==================== SCHEMES ====================
    print("\n⭐ STEP 4: Creating Schemes...")
    
    schemes_data = [
        {
            'name': 'PMEGP',
            'full_name': 'Prime Minister Employment Generation Programme',
            'scheme_code': 'PMEGP2025',
            'category': 'SUBSIDY',
            'status': 'ACTIVE',
            'description': 'Credit linked subsidy program for generating employment through micro enterprises',
            'benefits': 'Subsidy of 15-35% on project cost, Easy loan access',
            'eligible_sectors': ['MANUFACTURING', 'SERVICE', 'RETAIL'],
            'eligible_business_types': ['PVT_LTD', 'PARTNERSHIP', 'PROPRIETORSHIP'],
            'min_funding': 1.00,
            'max_funding': 25.00,
            'interest_rate': 8.5,
            'subsidy_percent': 25.00
        },
        {
            'name': 'Startup India',
            'full_name': 'Startup India Seed Fund Scheme',
            'scheme_code': 'STARTUP2025',
            'category': 'GRANT',
            'status': 'ACTIVE',
            'description': 'Financial assistance to startups for proof of concept, prototype development',
            'benefits': 'Up to ₹50L seed funding, Tax exemptions, Easy compliance',
            'eligible_sectors': ['IT_SOFTWARE', 'MANUFACTURING', 'HEALTHCARE'],
            'eligible_business_types': ['STARTUP', 'PVT_LTD'],
            'min_funding': 5.00,
            'max_funding': 50.00,
            'interest_rate': 0.0
        },
        {
            'name': 'Agriculture Loan',
            'full_name': 'Kisan Credit Card Scheme',
            'scheme_code': 'KCC2025',
            'category': 'LOAN',
            'status': 'ACTIVE',
            'description': 'Credit facility for farmers to meet crop production expenses',
            'benefits': 'Low interest rates, Flexible repayment, Crop insurance',
            'eligible_sectors': ['AGRICULTURE'],
            'eligible_business_types': ['PROPRIETORSHIP', 'PARTNERSHIP'],
            'min_funding': 2.00,
            'max_funding': 30.00,
            'interest_rate': 7.0
        }
    ]
    
    schemes = []
    for scheme_data in schemes_data:
        scheme, created = Scheme.objects.get_or_create(
            scheme_code=scheme_data['scheme_code'],
            defaults=scheme_data
        )
        if created:
            print(f"  ✅ Created: {scheme.name}")
        else:
            print(f"  ✓ Exists: {scheme.name}")
        schemes.append(scheme)
    
    # ==================== BOOKINGS ====================
    print("\n📅 STEP 5: Skipping Bookings (Service-based, not Scheme-based)...")
    print("  ℹ️  Bookings require Service model, not Scheme model")
    
    # ==================== APPLICATIONS ====================
    print("\n📝 STEP 6: Skipping Applications (Require Bookings)...")
    print("  ℹ️  Applications will be created manually through UI")
    
    # ==================== DOCUMENTS & CHECKLIST ====================
    print("\n📄 STEP 7: Creating Document Checklists...")
    
    required_docs = [
        'COMPANY_REG', 'GST_CERT', 'PAN_CARD', 'BANK_STATEMENT', 'ITR', 'BALANCE_SHEET'
    ]
    
    for client in clients:
        for doc_type in required_docs:
            checklist, created = DocumentChecklist.objects.get_or_create(
                client=client,
                document_type=doc_type,
                defaults={
                    'is_required': True,
                    'notes': 'Required for loan application',
                    'created_by': client.assigned_sales
                }
            )
            if created:
                print(f"  ✅ Checklist item: {client.company_name} - {doc_type}")
    
    # ==================== CLIENT ACTIVITIES ====================
    print("\n🔔 STEP 8: Creating Client Activities...")
    
    activity_types = [
        ('APPLICATION_SUBMITTED', 'Application Submitted', 'Your application has been submitted successfully', 'COMPLETED'),
        ('APPLICATION_UNDER_REVIEW', 'Under Review', 'Your application is being reviewed by our team', 'IN_PROGRESS'),
        ('DOCUMENTS_REQUESTED', 'Documents Required', 'Please upload GST Certificate and Bank Statements', 'PENDING'),
        ('MEETING_SCHEDULED', 'Meeting Scheduled', 'A meeting has been scheduled to discuss your application', 'PENDING'),
        ('SERVICE_RECOMMENDED', 'Website Development Recommended', 'We recommend our professional website service', 'PENDING'),
    ]
    
    for client in clients:
        for activity_type, title, desc, status in activity_types:
            activity, created = ClientActivity.objects.get_or_create(
                client=client,
                activity_type=activity_type,
                defaults={
                    'title': title,
                    'description': desc,
                    'status': status,
                    'priority': 'MEDIUM',
                    'is_visible_to_client': True,
                    'created_by': client.assigned_sales,
                    'service_offering': services[0] if 'SERVICE' in activity_type else None
                }
            )
            if created:
                print(f"  ✅ Activity: {client.company_name} - {title}")
    
    # ==================== SERVICE ENROLLMENTS ====================
    print("\n🎯 STEP 9: Creating Service Enrollments...")
    
    for i, client in enumerate(clients):
        enrollment, created = ClientServiceEnrollment.objects.get_or_create(
            client=client,
            service=services[i % len(services)],
            defaults={
                'status': ['RECOMMENDED', 'INTERESTED', 'ENROLLED'][i],
                'recommended_by': client.assigned_sales,
                'agreed_price': services[i % len(services)].base_price if services[i % len(services)].base_price else None,
                'notes': f'Recommended during consultation'
            }
        )
        if created:
            print(f"  ✅ Enrolled: {client.company_name} → {enrollment.service.name}")
        else:
            print(f"  ✓ Enrollment exists: {client.company_name}")
    
    # ==================== SUMMARY ====================
    print("\n" + "=" * 80)
    print("✅ TEST DATA CREATION COMPLETE!")
    print("=" * 80)
    
    print(f"\n📊 SUMMARY:")
    print(f"  Users: {User.objects.count()} total")
    print(f"    - Admin: {User.objects.filter(role='ADMIN').count()}")
    print(f"    - Managers: {User.objects.filter(role='MANAGER').count()}")
    print(f"    - Sales: {User.objects.filter(role='SALES').count()}")
    print(f"    - Clients: {User.objects.filter(role='CLIENT').count()}")
    print(f"\n  Clients: {Client.objects.count()}")
    print(f"  Schemes: {Scheme.objects.count()}")
    print(f"  Services: {ServiceOffering.objects.count()}")
    print(f"  Activities: {ClientActivity.objects.count()}")
    print(f"  Service Enrollments: {ClientServiceEnrollment.objects.count()}")
    print(f"  Document Checklist Items: {DocumentChecklist.objects.count()}")
    
    print(f"\n🔑 LOGIN CREDENTIALS:")
    print(f"  Admin:    admin@agnivridhiindia.com / Admin@123")
    print(f"  Manager:  manager1@agnivridhiindia.com / Manager@123")
    print(f"  Sales 1:  sales1@agnivridhiindia.com / Sales@123")
    print(f"  Sales 2:  sales2@agnivridhiindia.com / Sales@123")
    print(f"  Sales 3:  sales3@agnivridhiindia.com / Sales@123")
    print(f"  Client 1: client1@testcompany.com / Client@123")
    print(f"  Client 2: client2@testcompany.com / Client@123")
    print(f"  Client 3: client3@testcompany.com / Client@123")
    
    print(f"\n🌐 TEST URLs:")
    print(f"  Client Dashboard: /tracking/dashboard/")
    print(f"  Sales Dashboard: /accounts/sales_dashboard/")
    print(f"  Manager Dashboard: /accounts/manager_dashboard/")
    print(f"  Admin: /admin/")
    
    print("\n✅ All test data created successfully!")
    print("🚀 System is ready for real-time connectivity testing!\n")

if __name__ == '__main__':
    create_comprehensive_test_data()
