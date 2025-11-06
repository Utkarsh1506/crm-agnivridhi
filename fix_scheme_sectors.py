"""
Fix scheme sector codes to match Client model
Run: python fix_scheme_sectors.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from schemes.models import Scheme

# Mapping from old codes to new codes
SECTOR_MAPPING = {
    'SERVICES': 'SERVICE',  # Change SERVICES to SERVICE
    'TRADING': 'RETAIL',    # Change TRADING to RETAIL  
    'TECHNOLOGY': 'IT_SOFTWARE',  # Change TECHNOLOGY to IT_SOFTWARE
}

def fix_sectors():
    print("=" * 60)
    print("🔧 FIXING SCHEME SECTOR CODES")
    print("=" * 60)
    print()
    
    schemes = Scheme.objects.all()
    
    for scheme in schemes:
        original_sectors = scheme.eligible_sectors.copy() if scheme.eligible_sectors else []
        updated_sectors = []
        
        for sector in original_sectors:
            if sector in SECTOR_MAPPING:
                updated_sectors.append(SECTOR_MAPPING[sector])
                print(f"   {sector} → {SECTOR_MAPPING[sector]}")
            else:
                updated_sectors.append(sector)
        
        if updated_sectors != original_sectors:
            scheme.eligible_sectors = updated_sectors
            scheme.save()
            print(f"✅ Updated: {scheme.name}")
            print(f"   Old: {original_sectors}")
            print(f"   New: {updated_sectors}")
        else:
            print(f"⏭️  No changes needed: {scheme.name}")
        
        print()
    
    print("=" * 60)
    print("✅ DONE! All sector codes fixed.")
    print("=" * 60)
    print()
    print("🔗 Run test again: python test_ai_recommendations.py")
    print()

if __name__ == '__main__':
    try:
        fix_sectors()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
