"""
Script to fix all admin.py files by removing gettext_lazy translation wrappers
that cause AttributeError in Python 3.14
"""
import os
import re

def fix_admin_file(filepath):
    """Remove _() translation wrappers from admin.py files"""
    print(f"\n📝 Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove the import line for gettext_lazy
        content = re.sub(r'from django\.utils\.translation import gettext_lazy as _\n', '', content)
        
        # Replace _('Text') with 'Text' in fieldsets
        # This regex finds _('...') patterns
        content = re.sub(r"_\('([^']+)'\)", r"'\1'", content)
        content = re.sub(r'_\("([^"]+)"\)', r'"\1"', content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed: {filepath}")
            return True
        else:
            print(f"⏭️  No changes needed: {filepath}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("FIXING ALL ADMIN.PY FILES - REMOVING TRANSLATION WRAPPERS")
    print("="*70)
    
    # List of all admin.py files
    admin_files = [
        'accounts/admin.py',
        'applications/admin.py',
        'clients/admin.py',
        'schemes/admin.py',
        'bookings/admin.py',
        'payments/admin.py',
        'documents/admin.py',
        'edit_requests/admin.py',
        'notifications/admin.py',
        'activity_logs/admin.py',
    ]
    
    fixed_count = 0
    for admin_file in admin_files:
        if os.path.exists(admin_file):
            if fix_admin_file(admin_file):
                fixed_count += 1
        else:
            print(f"⚠️  File not found: {admin_file}")
    
    print("\n" + "="*70)
    print(f"✅ Successfully fixed {fixed_count} admin files")
    print("="*70)
    print("\n🔄 Next steps:")
    print("   1. Django should auto-reload")
    print("   2. Refresh the Django admin page")
    print("   3. All admin links should now work!")
    print()

if __name__ == '__main__':
    main()
