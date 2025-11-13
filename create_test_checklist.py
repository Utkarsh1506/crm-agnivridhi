#!/usr/bin/env python
"""
Create test checklist data for a client
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from accounts.models import User
from clients.models import Client
from documents.models import DocumentChecklist, Document

def create_test_checklist():
    """Create test checklist for a client"""
    
    # Get a sales user
    try:
        sales_user = User.objects.filter(role='SALES').first()
        if not sales_user:
            print("❌ No SALES user found. Please create one first.")
            return
        
        print(f"✅ Found sales user: {sales_user.email}")
        
        # Get a client assigned to this sales user
        client = Client.objects.filter(assigned_sales=sales_user).first()
        if not client:
            print("❌ No client assigned to this sales user.")
            return
        
        print(f"✅ Found client: {client.company_name}")
        
        # Create checklist items
        required_documents = [
            ('COMPANY_REG', 'Company Registration Certificate', True),
            ('GST_CERT', 'GST Registration Certificate', True),
            ('PAN_CARD', 'PAN Card', True),
            ('MSME_CERT', 'MSME/Udyam Registration', True),
            ('BANK_STATEMENT', 'Bank Statements (6 months)', True),
            ('ITR', 'Income Tax Returns (Last 2 years)', True),
            ('BALANCE_SHEET', 'Balance Sheet & P&L', True),
            ('INCORPORATION_CERT', 'Certificate of Incorporation', False),
            ('MOA_AOA', 'MOA & AOA', False),
            ('BOARD_RESOLUTION', 'Board Resolution', False),
        ]
        
        print(f"\n📋 Creating checklist for {client.company_name}...")
        created_count = 0
        
        for doc_type, display_name, is_required in required_documents:
            checklist_item, created = DocumentChecklist.objects.get_or_create(
                client=client,
                document_type=doc_type,
                defaults={
                    'is_required': is_required,
                    'notes': f'Required for scheme application' if is_required else 'Optional document',
                    'created_by': sales_user
                }
            )
            
            if created:
                created_count += 1
                status = "✅ Required" if is_required else "⚪ Optional"
                print(f"  {status} - {display_name}")
            else:
                print(f"  ⏭️  Already exists - {display_name}")
        
        print(f"\n✅ Created {created_count} new checklist items!")
        print(f"📊 Total checklist items: {DocumentChecklist.objects.filter(client=client).count()}")
        
        # Calculate completion
        total_required = DocumentChecklist.objects.filter(client=client, is_required=True).count()
        uploaded_required = DocumentChecklist.objects.filter(
            client=client, 
            is_required=True, 
            is_uploaded=True
        ).count()
        progress = (uploaded_required / total_required * 100) if total_required > 0 else 0
        
        print(f"\n📈 Completion Status:")
        print(f"   Total Required: {total_required}")
        print(f"   Uploaded: {uploaded_required}")
        print(f"   Progress: {progress:.1f}%")
        
        print(f"\n🌐 View at: http://127.0.0.1:8000/documents/sales/")
        print(f"   Login as: {sales_user.email} / Sales@123")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    create_test_checklist()
