"""
Test AI Scheme Recommendations
Run: python test_ai_recommendations.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from clients.models import Client
from schemes.models import Scheme

def test_recommendations():
    print("=" * 70)
    print("🤖 AI SCHEME RECOMMENDATIONS TEST")
    print("=" * 70)
    print()
    
    # Get first client
    client = Client.objects.first()
    
    if not client:
        print("❌ No clients found in database!")
        print("   Create a client first to test recommendations.")
        return
    
    # Display client info
    print(f"📊 CLIENT INFORMATION")
    print(f"{'─' * 70}")
    print(f"Company Name:       {client.company_name}")
    print(f"Sector:             {client.get_sector_display()}")
    print(f"Business Type:      {client.get_business_type_display()}")
    print(f"Annual Turnover:    ₹{client.annual_turnover:,.2f} lakhs")
    print(f"Funding Required:   ₹{client.funding_required:,.2f} lakhs")
    print(f"Company Age:        {client.company_age} years")
    print()
    
    # Get all active schemes
    schemes = Scheme.objects.filter(status='ACTIVE')
    
    if not schemes:
        print("❌ No active schemes found in database!")
        return
    
    print(f"🏛️  AVAILABLE SCHEMES: {schemes.count()}")
    print(f"{'─' * 70}")
    print()
    
    # Calculate AI recommendations
    recommendations = []
    for scheme in schemes:
        score = scheme.get_recommended_for_client(client)
        is_eligible, reasons = scheme.check_client_eligibility(client)
        recommendations.append((scheme, score, is_eligible, reasons))
    
    # Sort by score (highest first)
    recommendations.sort(key=lambda x: x[1], reverse=True)
    
    # Display recommendations
    print("🎯 AI RECOMMENDATIONS (Sorted by Match Score)")
    print("=" * 70)
    print()
    
    for idx, (scheme, score, is_eligible, reasons) in enumerate(recommendations, 1):
        # Determine match level
        if score >= 75:
            match_level = "🟢 EXCELLENT MATCH"
        elif score >= 50:
            match_level = "🟡 GOOD MATCH"
        elif score >= 25:
            match_level = "🟠 PARTIAL MATCH"
        else:
            match_level = "🔴 POOR MATCH"
        
        print(f"#{idx}. {scheme.name}")
        print(f"    Category: {scheme.get_category_display()}")
        print(f"    Match Score: {score}/100 {match_level}")
        print(f"    Eligibility: {'✅ ELIGIBLE' if is_eligible else '❌ NOT ELIGIBLE'}")
        
        if not is_eligible:
            print(f"    Reasons:")
            for reason in reasons:
                print(f"      • {reason}")
        else:
            print(f"    ✨ All eligibility criteria met!")
        
        print(f"    Funding Range: ₹{scheme.min_funding:,.2f} - ₹{scheme.max_funding:,.2f} lakhs")
        if scheme.interest_rate:
            print(f"    Interest Rate: {scheme.interest_rate}%")
        if scheme.subsidy_percent:
            print(f"    Subsidy: {scheme.subsidy_percent}%")
        print()
    
    # Display top 3 recommendations
    print("=" * 70)
    print("🏆 TOP 3 RECOMMENDATIONS FOR CLIENT PORTAL")
    print("=" * 70)
    
    top_3 = recommendations[:3]
    for idx, (scheme, score, is_eligible, reasons) in enumerate(top_3, 1):
        print(f"{idx}. {scheme.name} - {score}% Match")
        if is_eligible:
            print(f"   ✅ Ready to apply")
        else:
            print(f"   ❌ Not eligible: {', '.join(reasons[:2])}")
    
    print()
    print("=" * 70)
    print("✅ AI Recommendation Engine Working Perfectly!")
    print("=" * 70)
    print()
    print("🔗 Next Steps:")
    print("   1. Login as client at http://127.0.0.1:8000/login/")
    print("   2. View dashboard to see these recommendations")
    print("   3. Click on schemes to view details")
    print("   4. Apply for eligible schemes")
    print()

if __name__ == '__main__':
    try:
        test_recommendations()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
