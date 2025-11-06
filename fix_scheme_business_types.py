"""
Fix scheme business types to match Client model
Run: python fix_scheme_business_types.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from schemes.models import Scheme

# Mapping from old codes to new codes
BUSINESS_TYPE_MAPPING = {
    'PRIVATE_LIMITED': 'PVT_LTD',  # Change PRIVATE_LIMITED to PVT_LTD
}

def fix_business_types():
    print("=" * 60)
    print("🔧 FIXING SCHEME BUSINESS TYPE CODES")
    print("=" * 60)
    print()
    
    schemes = Scheme.objects.all()
    
    for scheme in schemes:
        original_types = scheme.eligible_business_types.copy() if scheme.eligible_business_types else []
        updated_types = []
        
        for btype in original_types:
            if btype in BUSINESS_TYPE_MAPPING:
                updated_types.append(BUSINESS_TYPE_MAPPING[btype])
                print(f"   {btype} → {BUSINESS_TYPE_MAPPING[btype]}")
            else:
                updated_types.append(btype)
        
        if updated_types != original_types:
            scheme.eligible_business_types = updated_types
            scheme.save()
            print(f"✅ Updated: {scheme.name}")
            print(f"   Old: {original_types}")
            print(f"   New: {updated_types}")
        else:
            print(f"⏭️  No changes needed: {scheme.name}")
        
        print()
    
    print("=" * 60)
    print("✅ DONE! All business type codes fixed.")
    print("=" * 60)
    print()
    print("🔗 Run test again: python test_ai_recommendations.py")
    print()

if __name__ == '__main__':
    try:
        fix_business_types()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
