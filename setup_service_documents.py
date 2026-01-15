"""
Script to set up service document requirements for common services
Run this after setting up services in the admin panel
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from bookings.models import Service, ServiceDocumentRequirement

# Define document requirements for each service type
SERVICE_DOCUMENTS = {
    'Funding Services': [
        {
            'document_type': 'COMPANY_REG',
            'is_mandatory': True,
            'description': 'Company registration certificate is required to verify your business registration status',
            'display_order': 1
        },
        {
            'document_type': 'GST_CERT',
            'is_mandatory': True,
            'description': 'GST registration certificate is required for tax compliance verification',
            'display_order': 2
        },
        {
            'document_type': 'PAN_CARD',
            'is_mandatory': True,
            'description': 'PAN card of the company is required for identification and tax purposes',
            'display_order': 3
        },
        {
            'document_type': 'BANK_STATEMENT',
            'is_mandatory': True,
            'description': '6 months of bank statements are required to assess your financial health',
            'display_order': 4
        },
        {
            'document_type': 'ITR',
            'is_mandatory': True,
            'description': 'Last 2 years of Income Tax Returns are required to verify your financial records',
            'display_order': 5
        },
        {
            'document_type': 'BALANCE_SHEET',
            'is_mandatory': True,
            'description': 'Latest Balance Sheet and P&L statement are required for financial analysis',
            'display_order': 6
        },
        {
            'document_type': 'MSME_CERT',
            'is_mandatory': False,
            'description': 'MSME/Udyam Registration certificate if applicable (optional)',
            'display_order': 7
        },
    ],
    'Incorporation Services': [
        {
            'document_type': 'PAN_CARD',
            'is_mandatory': True,
            'description': 'PAN card of the director/proprietor',
            'display_order': 1
        },
        {
            'document_type': 'COMPANY_REG',
            'is_mandatory': True,
            'description': 'Proof of registered office address',
            'display_order': 2
        },
        {
            'document_type': 'BOARD_RESOLUTION',
            'is_mandatory': False,
            'description': 'Board resolution if applicable (optional)',
            'display_order': 3
        },
    ],
    'Certification Services': [
        {
            'document_type': 'COMPANY_REG',
            'is_mandatory': True,
            'description': 'Company registration certificate',
            'display_order': 1
        },
        {
            'document_type': 'GST_CERT',
            'is_mandatory': True,
            'description': 'GST registration certificate',
            'display_order': 2
        },
        {
            'document_type': 'BALANCE_SHEET',
            'is_mandatory': True,
            'description': 'Latest Balance Sheet and P&L statement',
            'display_order': 3
        },
    ],
    'Growth Services': [
        {
            'document_type': 'BALANCE_SHEET',
            'is_mandatory': True,
            'description': 'Last 2-3 years of financial statements',
            'display_order': 1
        },
        {
            'document_type': 'ITR',
            'is_mandatory': True,
            'description': 'Income Tax Returns for last 2 years',
            'display_order': 2
        },
        {
            'document_type': 'BANK_STATEMENT',
            'is_mandatory': False,
            'description': '6 months of bank statements (optional)',
            'display_order': 3
        },
    ],
}

def setup_service_documents():
    """Set up document requirements for services"""
    
    for category, documents in SERVICE_DOCUMENTS.items():
        # Find services in this category
        services = Service.objects.filter(category=category)
        
        if not services.exists():
            print(f"⚠️  No services found in category: {category}")
            continue
        
        for service in services:
            print(f"\n📋 Setting up documents for: {service.name}")
            
            for doc_config in documents:
                doc_req, created = ServiceDocumentRequirement.objects.get_or_create(
                    service=service,
                    document_type=doc_config['document_type'],
                    defaults={
                        'is_mandatory': doc_config['is_mandatory'],
                        'description': doc_config['description'],
                        'display_order': doc_config['display_order'],
                    }
                )
                
                if created:
                    print(f"  ✅ Added: {doc_req.get_document_type_display()}")
                else:
                    print(f"  ℹ️  Already exists: {doc_req.get_document_type_display()}")
    
    print("\n✅ Service document setup complete!")

if __name__ == '__main__':
    setup_service_documents()
