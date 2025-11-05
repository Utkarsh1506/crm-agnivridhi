"""
Quick Test Script for Agnivridhi CRM
Run this to verify all features are working
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
application = get_wsgi_application()

from django.conf import settings
from clients.models import Client
from bookings.models import Booking, Service
from payments.models import Payment
from applications.models import Application
from accounts.models import User


def test_email_config():
    """Test email configuration"""
    print("\n🔍 Testing Email Configuration...")
    
    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
        print("  ⚠️  Email not configured. Add credentials to .env")
        return False
    
    try:
        from django.core.mail import send_mail
        send_mail(
            'Agnivridhi CRM Test Email',
            'This is a test email from your CRM system.',
            settings.DEFAULT_FROM_EMAIL,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        print("  ✅ Email configuration OK - Check your inbox!")
        return True
    except Exception as e:
        print(f"  ❌ Email error: {e}")
        return False


def test_twilio_config():
    """Test Twilio WhatsApp configuration"""
    print("\n🔍 Testing Twilio WhatsApp Configuration...")
    
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        print("  ⚠️  Twilio not configured. Add credentials to .env")
        return False
    
    try:
        from accounts.whatsapp_utils import get_twilio_client
        client = get_twilio_client()
        if client:
            print("  ✅ Twilio configuration OK")
            print(f"     Account SID: {settings.TWILIO_ACCOUNT_SID[:10]}...")
            print(f"     WhatsApp From: {settings.TWILIO_WHATSAPP_FROM}")
            return True
        else:
            print("  ❌ Failed to initialize Twilio client")
            return False
    except Exception as e:
        print(f"  ❌ Twilio error: {e}")
        return False


def test_pdf_generation():
    """Test PDF generation"""
    print("\n🔍 Testing PDF Generation...")
    
    try:
        from reportlab.pdfgen import canvas
        from io import BytesIO
        
        # Test simple PDF with ReportLab
        buffer = BytesIO()
        c = canvas.Canvas(buffer)
        c.drawString(100, 750, "Test PDF")
        c.drawString(100, 735, "PDF generation working!")
        c.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        print(f"  ✅ ReportLab PDF generated ({len(pdf_bytes)} bytes)")
        
        # Test our PDF utils
        from accounts.pdf_utils import generate_payment_receipt_pdf
        print(f"  ✅ PDF utils imported successfully")
        
        return True
    except Exception as e:
        print(f"  ❌ PDF generation error: {e}")
        return False


def test_database():
    """Test database connectivity"""
    print("\n🔍 Testing Database...")
    
    try:
        client_count = Client.objects.count()
        booking_count = Booking.objects.count()
        payment_count = Payment.objects.count()
        app_count = Application.objects.count()
        user_count = User.objects.count()
        
        print(f"  ✅ Database connected!")
        print(f"     Clients: {client_count}")
        print(f"     Bookings: {booking_count}")
        print(f"     Payments: {payment_count}")
        print(f"     Applications: {app_count}")
        print(f"     Users: {user_count}")
        return True
    except Exception as e:
        print(f"  ❌ Database error: {e}")
        return False


def test_api_configuration():
    """Test REST API configuration"""
    print("\n🔍 Testing REST API Configuration...")
    
    try:
        # Check DRF installed
        import rest_framework
        print(f"  ✅ Django REST Framework: {rest_framework.__version__}")
        
        # Check drf-spectacular
        import drf_spectacular
        print(f"  ✅ drf-spectacular installed")
        
        # Check serializers exist
        from clients.serializers import ClientSerializer
        from bookings.serializers import BookingSerializer
        from payments.serializers import PaymentSerializer
        from applications.serializers import ApplicationSerializer
        print(f"  ✅ All serializers imported successfully")
        
        # Check viewsets exist
        from clients.viewsets import ClientViewSet
        from bookings.viewsets import BookingViewSet
        from payments.viewsets import PaymentViewSet
        from applications.viewsets import ApplicationViewSet
        print(f"  ✅ All viewsets imported successfully")
        
        return True
    except Exception as e:
        print(f"  ❌ API configuration error: {e}")
        return False


def test_environment_variables():
    """Test environment variables"""
    print("\n🔍 Testing Environment Variables...")
    
    required_vars = {
        'SECRET_KEY': settings.SECRET_KEY,
        'DEBUG': settings.DEBUG,
        'EMAIL_HOST': settings.EMAIL_HOST,
        'EMAIL_HOST_USER': settings.EMAIL_HOST_USER,
    }
    
    optional_vars = {
        'TWILIO_ACCOUNT_SID': getattr(settings, 'TWILIO_ACCOUNT_SID', None),
        'TWILIO_AUTH_TOKEN': getattr(settings, 'TWILIO_AUTH_TOKEN', None),
    }
    
    all_ok = True
    
    for var, value in required_vars.items():
        if value and value != '':
            print(f"  ✅ {var}: Configured")
        else:
            print(f"  ❌ {var}: Missing")
            all_ok = False
    
    for var, value in optional_vars.items():
        if value and value != '':
            print(f"  ✅ {var}: Configured")
        else:
            print(f"  ⚠️  {var}: Not configured (optional)")
    
    return all_ok


def show_access_urls():
    """Show important URLs"""
    print("\n🌐 Access URLs:")
    print("  📊 Admin Dashboard:  http://localhost:8000/dashboard/")
    print("  🔧 Django Admin:     http://localhost:8000/admin/")
    print("  🚀 Swagger UI:       http://localhost:8000/api/docs/")
    print("  📖 ReDoc:            http://localhost:8000/api/redoc/")
    print("  🔌 API Root:         http://localhost:8000/api/")
    print("  📄 PDF Test:         http://localhost:8000/pdf/payment/1/")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🧪 AGNIVRIDHI CRM - SYSTEM TEST")
    print("=" * 60)
    
    results = {
        'Environment Variables': test_environment_variables(),
        'Database': test_database(),
        'API Configuration': test_api_configuration(),
        'Email': test_email_config(),
        'Twilio WhatsApp': test_twilio_config(),
        'PDF Generation': test_pdf_generation(),
    }
    
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}  {test_name}")
    
    passed_count = sum(results.values())
    total_count = len(results)
    
    print("\n" + "=" * 60)
    print(f"📊 Results: {passed_count}/{total_count} tests passed")
    print("=" * 60)
    
    show_access_urls()
    
    if passed_count == total_count:
        print("\n✅ All tests passed! System is ready to use.")
        print("\n💡 Next steps:")
        print("   1. Start server: python manage.py runserver")
        print("   2. Open Swagger UI: http://localhost:8000/api/docs/")
        print("   3. Test API endpoints")
        print("   4. Send test WhatsApp messages")
        print("   5. Generate test PDFs")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        print("   Review SETUP_AND_TESTING_GUIDE.md for configuration help.")


if __name__ == '__main__':
    try:
        run_all_tests()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
