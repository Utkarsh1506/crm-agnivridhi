#!/usr/bin/env python
"""
Create test services and client activities
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from tracking.models import ServiceOffering, ClientActivity, ClientServiceEnrollment
from clients.models import Client
from accounts.models import User
from applications.models import Application

def create_test_data():
    """Create test services and activities"""
    
    print("📦 Creating Service Offerings...\n")
    
    services_data = [
        {
            'service_type': 'WEB_DEVELOPMENT',
            'name': 'Professional Website Development',
            'short_description': 'Custom business website with responsive design and SEO optimization',
            'description': 'Get a professional, mobile-responsive website for your business. Includes custom design, SEO optimization, contact forms, and social media integration.',
            'pricing_type': 'PROJECT',
            'base_price': 25000,
            'icon': 'bi-globe',
            'is_featured': True,
            'display_order': 1,
            'key_features': ['Responsive Design', 'SEO Optimized', 'Contact Forms', 'Social Media Integration', 'Admin Panel']
        },
        {
            'service_type': 'DIGITAL_MARKETING',
            'name': 'Digital Marketing & Social Media',
            'short_description': 'Complete digital marketing solution including social media management',
            'description': 'Boost your online presence with our comprehensive digital marketing services. We handle social media, content creation, ad campaigns, and analytics.',
            'pricing_type': 'HOURLY',
            'base_price': 1500,
            'icon': 'bi-megaphone',
            'is_featured': True,
            'display_order': 2,
            'key_features': ['Social Media Management', 'Content Creation', 'Ad Campaigns', 'Analytics & Reporting', 'SEO Strategy']
        },
        {
            'service_type': 'CERTIFICATION',
            'name': 'Business Certifications & Licenses',
            'short_description': 'Help with MSME, GST, ISO certifications and business licenses',
            'description': 'We assist you in obtaining all necessary business certifications including MSME registration, GST, ISO certifications, and other industry-specific licenses.',
            'pricing_type': 'CUSTOM',
            'icon': 'bi-award',
            'is_featured': True,
            'display_order': 3,
            'key_features': ['MSME Registration', 'GST Registration', 'ISO Certification', 'Trade License', 'Industry Permits']
        },
        {
            'service_type': 'CONSULTING',
            'name': 'Business Growth Consulting',
            'short_description': 'Expert guidance for scaling your business',
            'description': 'Get expert advice on business strategy, operations, finance, and growth planning from our experienced consultants.',
            'pricing_type': 'HOURLY',
            'base_price': 2000,
            'icon': 'bi-graph-up-arrow',
            'is_featured': False,
            'display_order': 4,
            'key_features': ['Business Strategy', 'Financial Planning', 'Operations Optimization', 'Market Research', 'Growth Planning']
        },
        {
            'service_type': 'ACCOUNTING',
            'name': 'Accounting & Taxation Services',
            'short_description': 'Complete accounting, bookkeeping and tax filing services',
            'description': 'Professional accounting and taxation services including bookkeeping, GST filing, ITR filing, and financial statement preparation.',
            'pricing_type': 'FIXED',
            'base_price': 5000,
            'icon': 'bi-calculator',
            'is_featured': False,
            'display_order': 5,
            'key_features': ['Bookkeeping', 'GST Filing', 'ITR Filing', 'Financial Statements', 'Audit Support']
        },
    ]
    
    created_services = []
    for service_data in services_data:
        service, created = ServiceOffering.objects.get_or_create(
            name=service_data['name'],
            defaults=service_data
        )
        if created:
            print(f"  ✅ Created: {service.name}")
            created_services.append(service)
        else:
            print(f"  ⏭️  Already exists: {service.name}")
            created_services.append(service)
    
    print(f"\n📊 Total Services: {ServiceOffering.objects.count()}\n")
    
    # Create activities for client
    print("📋 Creating Sample Activities...\n")
    
    try:
        # Get client
        client = Client.objects.first()
        if not client:
            print("❌ No client found. Please create a client first.")
            return
        
        # Get sales user
        sales_user = User.objects.filter(role='SALES').first()
        if not sales_user:
            print("❌ No SALES user found.")
            return
        
        # Get application if exists
        application = Application.objects.filter(client=client).first()
        
        activities_data = [
            {
                'activity_type': 'APPLICATION_SUBMITTED',
                'title': 'Application Submitted Successfully',
                'description': f'Your application for {application.scheme.name if application else "scheme"} has been submitted successfully. Our team will review it shortly.',
                'status': 'COMPLETED',
                'priority': 'MEDIUM',
                'is_visible_to_client': True,
                'application': application,
            },
            {
                'activity_type': 'APPLICATION_UNDER_REVIEW',
                'title': 'Application Under Review',
                'description': 'Your application is currently being reviewed by our team. We will notify you once the review is complete.',
                'status': 'IN_PROGRESS',
                'priority': 'HIGH',
                'is_visible_to_client': True,
                'application': application,
            },
            {
                'activity_type': 'DOCUMENTS_REQUESTED',
                'title': 'Additional Documents Required',
                'description': 'Please upload the following documents: GST Certificate, Bank Statements (last 6 months), and ITR for last 2 years.',
                'status': 'PENDING',
                'priority': 'URGENT',
                'is_visible_to_client': True,
            },
            {
                'activity_type': 'SERVICE_RECOMMENDED',
                'title': 'Website Development Recommended',
                'description': 'Having a professional website can significantly boost your business credibility and online presence. We recommend our Website Development service.',
                'status': 'PENDING',
                'priority': 'LOW',
                'is_visible_to_client': True,
                'service_offering': created_services[0] if created_services else None,
            },
            {
                'activity_type': 'MEETING_SCHEDULED',
                'title': 'Meeting Scheduled - Application Discussion',
                'description': 'A meeting has been scheduled to discuss your application and next steps. Please check your email for meeting details.',
                'status': 'PENDING',
                'priority': 'HIGH',
                'is_visible_to_client': True,
            },
        ]
        
        for activity_data in activities_data:
            activity, created = ClientActivity.objects.get_or_create(
                client=client,
                title=activity_data['title'],
                defaults={
                    **activity_data,
                    'created_by': sales_user,
                }
            )
            if created:
                print(f"  ✅ {activity.get_activity_type_display()}: {activity.title}")
            else:
                print(f"  ⏭️  Already exists: {activity.title}")
        
        print(f"\n📊 Total Activities for {client.company_name}: {ClientActivity.objects.filter(client=client).count()}\n")
        
        # Enroll client in a service (recommended)
        if created_services:
            enrollment, created = ClientServiceEnrollment.objects.get_or_create(
                client=client,
                service=created_services[0],
                defaults={
                    'status': 'RECOMMENDED',
                    'recommended_by': sales_user,
                    'notes': 'Recommended during initial consultation'
                }
            )
            if created:
                print(f"  ✅ Service Recommended: {enrollment.service.name}")
            else:
                print(f"  ⏭️  Service already recommended: {enrollment.service.name}")
        
        print(f"\n✅ Test data created successfully!")
        print(f"\n🌐 View Client Dashboard at: http://127.0.0.1:8000/tracking/dashboard/")
        print(f"   Login as Client user to see the timeline\n")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    create_test_data()
