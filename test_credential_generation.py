"""
Test script to verify automatic credential generation when a client is created
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from django.contrib.auth import get_user_model
from clients.models import Client, ClientCredential

User = get_user_model()

def test_credential_generation():
    print("\n" + "="*60)
    print("Testing Client Credential Auto-Generation")
    print("="*60)
    
    # Clean up any existing test data
    print("\n0. Cleaning up existing test data...")
    User.objects.filter(username='testclient123').delete()
    print("✓ Cleaned up existing test data")
    
    # Get a sales user to assign the client to
    sales_user = User.objects.filter(role='SALES').first()
    if not sales_user:
        print("❌ No sales user found. Creating one...")
        sales_user = User.objects.create_user(
            username='test_sales',
            email='test_sales@test.com',
            password='Test@123',
            role='SALES',
            first_name='Test',
            last_name='Sales'
        )
    
    print(f"✓ Using sales user: {sales_user.username}")
    
    # Create a test client user first
    print("\n1. Creating client user account...")
    client_user = User.objects.create_user(
        username='testclient123',
        email='testclient123@test.com',
        password='TempPassword123',  # This will be overwritten by signal
        role='CLIENT',
        first_name='Test',
        last_name='Client'
    )
    print(f"✓ Created user: {client_user.username}")
    
    # Create the client profile
    print("\n2. Creating client profile...")
    try:
        client = Client.objects.create(
            user=client_user,
            company_name='Test Company Auto Credentials',
            business_type='STARTUP',
            sector='TECHNOLOGY',
            company_age=2,  # Added required field
            contact_person='Test Person',
            contact_email='testclient123@test.com',
            contact_phone='9876543210',
            address_line1='Test Address',
            city='Test City',
            state='Test State',
            pincode='123456',
            annual_turnover=1000000,
            funding_required=500000,
            assigned_sales=sales_user,
            created_by=sales_user
        )
        print(f"✓ Created client: {client.company_name} (ID: {client.client_id})")
    except Exception as e:
        print(f"❌ Error creating client: {str(e)}")
        return
    
    # Check if credentials were generated
    print("\n3. Checking if credentials were auto-generated...")
    try:
        credential = ClientCredential.objects.get(client=client)
        print("✓ Credentials were auto-generated!")
        print(f"\n{'='*60}")
        print("GENERATED CREDENTIALS:")
        print(f"{'='*60}")
        print(f"  Company:  {client.company_name}")
        print(f"  Username: {credential.username}")
        print(f"  Email:    {credential.email}")
        print(f"  Password: {credential.plain_password}")
        print(f"  Created:  {credential.created_at}")
        print(f"  Is Sent:  {credential.is_sent}")
        print(f"{'='*60}\n")
        
        # Check if the user's password was updated
        print("4. Verifying password was set on user account...")
        if client.user.check_password(credential.plain_password):
            print("✓ Password was successfully set on user account!")
        else:
            print("❌ Password mismatch - signal may not have updated user password")
        
    except ClientCredential.DoesNotExist:
        print("❌ No credentials found! Signal may not have fired.")
        return
    
    print("\n" + "="*60)
    print("TEST COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nNext steps:")
    print("1. Login as owner/admin")
    print("2. Go to Owner Dashboard")
    print("3. You should see the credentials in the 'New Client Login Credentials' section")
    print("4. Copy and share the credentials with the client")
    print("5. Click 'Mark as Sent' when done")
    print("="*60 + "\n")

if __name__ == '__main__':
    test_credential_generation()
