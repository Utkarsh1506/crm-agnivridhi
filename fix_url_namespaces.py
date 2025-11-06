"""
Script to update all hard-coded URL names to namespaced versions in Python files.
Run: python fix_url_namespaces.py
"""
import re
import os

# Map of old URL names to new namespaced versions
URL_MAPPING = {
    # Auth/dashboard
    "('login')": "('accounts:login')",
    "('logout')": "('accounts:logout')",
    "('dashboard')": "('accounts:dashboard')",
    "('client_portal')": "('accounts:client_portal')",
    "('manager_dashboard')": "('accounts:manager_dashboard')",
    "('admin_dashboard')": "('accounts:admin_dashboard')",
    "('sales_dashboard')": "('accounts:sales_dashboard')",
    "('owner_dashboard')": "('accounts:owner_dashboard')",
    "('superuser_dashboard')": "('accounts:superuser_dashboard')",
    
    # Accounts routes
    "('profile')": "('accounts:profile')",
    "('team_members_list')": "('accounts:team_members_list')",
    "('team_clients_list')": "('accounts:team_clients_list')",
    "('team_diagnostic')": "('accounts:team_diagnostic')",
    "('record_payment'": "('accounts:record_payment'",
    "('approve_payment'": "('accounts:approve_payment'",
    "('reject_payment'": "('accounts:reject_payment'",
    
    # Applications
    "('application_list')": "('applications:application_list')",
    "('client_applications_list')": "('applications:client_applications_list')",
    "('sales_applications_list')": "('applications:sales_applications_list')",
    "('team_applications_list')": "('applications:team_applications_list')",
    "('pending_applications')": "('applications:pending_applications')",
    "('application_detail'": "('applications:application_detail'",
    "('client_application_detail'": "('applications:client_application_detail'",
    "('sales_application_detail'": "('applications:sales_application_detail'",
    "('manager_application_detail'": "('applications:manager_application_detail'",
    "('owner_application_detail'": "('applications:owner_application_detail'",
    "('approve_application'": "('applications:approve_application'",
    "('reject_application'": "('applications:reject_application'",
    "('create_application_from_booking'": "('applications:create_application_from_booking'",
    
    # Bookings
    "('booking_list')": "('bookings:booking_list')",
    "('client_bookings_list')": "('bookings:client_bookings_list')",
    "('sales_bookings_list')": "('bookings:sales_bookings_list')",
    "('team_bookings_list')": "('bookings:team_bookings_list')",
    "('booking_detail'": "('bookings:booking_detail'",
    "('create_documentation_booking'": "('bookings:create_documentation_booking'",
    
    # Documents
    "('document_list')": "('documents:document_list')",
    "('client_documents_list')": "('documents:client_documents_list')",
    "('sales_documents_list')": "('documents:sales_documents_list')",
    "('team_documents_list')": "('documents:team_documents_list')",
    "('document_detail'": "('documents:document_detail'",
    "('document_download'": "('documents:document_download'",
    
    # Payments
    "('payment_list')": "('payments:payment_list')",
    "('client_payments_list')": "('payments:client_payments_list')",
    "('sales_payments_list')": "('payments:sales_payments_list')",
    "('team_payments_list')": "('payments:team_payments_list')",
    "('payment_detail'": "('payments:payment_detail'",
    
    # Schemes
    "('scheme_list')": "('schemes:scheme_list')",
    "('scheme_detail'": "('schemes:scheme_detail'",
    "('check_eligibility')": "('schemes:check_eligibility')",
    "('create_application'": "('applications:create_application'",
}


def fix_file(filepath):
    """Update URL references in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        replacements = 0
        
        for old_pattern, new_pattern in URL_MAPPING.items():
            if old_pattern in content:
                count = content.count(old_pattern)
                content = content.replace(old_pattern, new_pattern)
                replacements += count
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated {filepath}: {replacements} replacements")
            return replacements
        return 0
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
        return 0


def main():
    """Fix all Python files in accounts app"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    accounts_dir = os.path.join(base_dir, 'accounts')
    
    total_replacements = 0
    files_updated = 0
    
    for filename in os.listdir(accounts_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            filepath = os.path.join(accounts_dir, filename)
            count = fix_file(filepath)
            if count > 0:
                total_replacements += count
                files_updated += 1
    
    print(f"\n✅ Complete: {files_updated} files updated, {total_replacements} total replacements")


if __name__ == '__main__':
    main()
