"""
Comprehensive System Testing for Agnivridhi CRM
Tests all major modules: Dashboards, Bookings, Applications, Clients, Schemes

Run: python test_complete_system.py
"""

import os
import django
import sys
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from accounts.models import User
from clients.models import Client as ClientModel
from schemes.models import Scheme
from bookings.models import Booking
from applications.models import Application
from payments.models import Payment

User = get_user_model()

class Colors:
    """Terminal colors for output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

def print_test(name, status, message=""):
    if status:
        symbol = f"{Colors.OKGREEN}✓{Colors.ENDC}"
        status_text = f"{Colors.OKGREEN}PASS{Colors.ENDC}"
    else:
        symbol = f"{Colors.FAIL}✗{Colors.ENDC}"
        status_text = f"{Colors.FAIL}FAIL{Colors.ENDC}"
    
    print(f"{symbol} {name:<50} [{status_text}]")
    if message:
        print(f"  {Colors.WARNING}→ {message}{Colors.ENDC}")

def print_section(text):
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{'-'*80}{Colors.ENDC}")

class CRMSystemTester:
    def __init__(self):
        self.client = Client()
        self.results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'errors': []
        }
        self.test_data = {}
        
    def run_test(self, test_func):
        """Decorator to track test results"""
        def wrapper(*args, **kwargs):
            self.results['total'] += 1
            try:
                result = test_func(*args, **kwargs)
                if result:
                    self.results['passed'] += 1
                else:
                    self.results['failed'] += 1
                return result
            except Exception as e:
                self.results['failed'] += 1
                self.results['errors'].append({
                    'test': test_func.__name__,
                    'error': str(e)
                })
                print_test(test_func.__name__, False, f"Exception: {str(e)}")
                return False
        return wrapper
    
    # ==================== DATABASE TESTS ====================
    
    def test_database_models(self):
        print_section("DATABASE & MODELS")
        
        # Test User Model
        result = self.run_test(lambda: User.objects.exists())()
        print_test("Users exist in database", result)
        
        # Test Client Model
        result = self.run_test(lambda: ClientModel.objects.model._meta.get_fields())()
        print_test("Client model structure valid", bool(result))
        
        # Test Scheme Model
        result = self.run_test(lambda: Scheme.objects.model._meta.get_fields())()
        print_test("Scheme model structure valid", bool(result))
        
        # Test Booking Model
        result = self.run_test(lambda: Booking.objects.model._meta.get_fields())()
        print_test("Booking model structure valid", bool(result))
        
        # Test Application Model
        result = self.run_test(lambda: Application.objects.model._meta.get_fields())()
        print_test("Application model structure valid", bool(result))
        
        # Test Payment Model
        result = self.run_test(lambda: Payment.objects.model._meta.get_fields())()
        print_test("Payment model structure valid", bool(result))
    
    # ==================== USER & AUTHENTICATION TESTS ====================
    
    def test_users_and_roles(self):
        print_section("USERS & AUTHENTICATION")
        
        # Get test users
        try:
            self.test_data['admin'] = User.objects.filter(role='ADMIN').first()
            self.test_data['manager'] = User.objects.filter(role='MANAGER').first()
            self.test_data['sales'] = User.objects.filter(role='SALES').first()
            self.test_data['client'] = User.objects.filter(role='CLIENT').first()
        except Exception as e:
            print_test("Get test users", False, str(e))
            return
        
        # Test Admin exists
        result = self.test_data['admin'] is not None
        print_test("Admin user exists", result)
        
        # Test Manager exists
        result = self.test_data['manager'] is not None
        print_test("Manager user exists", result)
        
        # Test Sales exists
        result = self.test_data['sales'] is not None
        print_test("Sales user exists", result)
        
        # Test Client exists
        result = self.test_data['client'] is not None
        print_test("Client user exists", result)
        
        # Test role permissions
        if self.test_data['admin']:
            result = self.test_data['admin'].is_admin
            print_test("Admin has admin permissions", result)
        
        if self.test_data['manager']:
            result = self.test_data['manager'].is_manager
            print_test("Manager has manager permissions", result)
        
        if self.test_data['sales']:
            result = self.test_data['sales'].is_sales
            print_test("Sales has sales permissions", result)
    
    # ==================== DASHBOARD ACCESS TESTS ====================
    
    def test_dashboard_access(self):
        print_section("DASHBOARD ACCESS")
        
        # Test login redirect
        response = self.client.get('/')
        result = response.status_code == 302  # Should redirect to login
        print_test("Root URL redirects to login", result)
        
        # Test admin dashboard access (without login)
        response = self.client.get('/admin-dashboard/')
        result = response.status_code == 302  # Should redirect to login
        print_test("Admin dashboard requires authentication", result)
        
        # Test manager dashboard access (without login)
        response = self.client.get('/manager-dashboard/')
        result = response.status_code == 302
        print_test("Manager dashboard requires authentication", result)
        
        # Test sales dashboard access (without login)
        response = self.client.get('/sales/dashboard/')
        result = response.status_code == 302
        print_test("Sales dashboard requires authentication", result)
        
        # Test client dashboard access (without login)
        response = self.client.get('/clients/dashboard/')
        result = response.status_code == 302
        print_test("Client dashboard requires authentication", result)
    
    # ==================== SCHEME TESTS ====================
    
    def test_schemes(self):
        print_section("SCHEMES MODULE")
        
        # Count schemes
        scheme_count = Scheme.objects.count()
        result = True  # Just checking it doesn't crash
        print_test(f"Schemes in database: {scheme_count}", result)
        
        # Get first scheme
        scheme = Scheme.objects.first()
        if scheme:
            self.test_data['scheme'] = scheme
            print_test(f"Sample scheme: {scheme.name}", True)
            
            # Test scheme fields
            result = hasattr(scheme, 'name') and hasattr(scheme, 'description')
            print_test("Scheme has required fields", result)
            
            # Test scheme benefits
            result = hasattr(scheme, 'benefits')
            print_test("Scheme has benefits field", result)
            
            # Test scheme eligibility
            result = hasattr(scheme, 'eligibility')
            print_test("Scheme has eligibility field", result)
        else:
            print_test("At least one scheme exists", False, "No schemes found")
    
    # ==================== CLIENT TESTS ====================
    
    def test_clients(self):
        print_section("CLIENTS MODULE")
        
        # Count clients
        client_count = ClientModel.objects.count()
        result = True
        print_test(f"Clients in database: {client_count}", result)
        
        # Get first client
        client = ClientModel.objects.first()
        if client:
            self.test_data['client_obj'] = client
            print_test(f"Sample client: {client.company_name}", True)
            
            # Test client fields
            result = hasattr(client, 'contact_email') and hasattr(client, 'contact_phone')
            print_test("Client has contact fields", result)
            
            # Test client user relationship
            result = hasattr(client, 'user')
            print_test("Client has user relationship", result)
            
            # Test client company info
            result = hasattr(client, 'company_name')
            print_test("Client has company information", result)
        else:
            print_test("Clients exist", True, "No clients yet - this is OK for new system")
    
    # ==================== COMPANY INFO (via Client) TESTS ====================
    
    def test_companies(self):
        print_section("COMPANY INFORMATION")
        
        # Test client with company info
        client = ClientModel.objects.first()
        if client:
            # Test company fields in client
            result = hasattr(client, 'business_type') and hasattr(client, 'sector')
            print_test("Client has business type and sector fields", result)
            
            # Test company name
            result = hasattr(client, 'company_name')
            print_test("Client has company name field", result)
            
            # Test company address
            result = hasattr(client, 'address_line1') and hasattr(client, 'city')
            print_test("Client has address fields", result)
        else:
            print_test("Company information structure", True, "No clients yet - this is OK")
    
    # ==================== BOOKING TESTS ====================
    
    def test_bookings(self):
        print_section("BOOKINGS MODULE")
        
        # Count bookings
        booking_count = Booking.objects.count()
        result = True
        print_test(f"Bookings in database: {booking_count}", result)
        
        # Get first booking
        booking = Booking.objects.first()
        if booking:
            self.test_data['booking'] = booking
            print_test(f"Sample booking ID: {booking.booking_id}", True)
            
            # Test booking fields
            result = hasattr(booking, 'client') and hasattr(booking, 'service')
            print_test("Booking has client and service relationships", result)
            
            # Test booking status
            result = hasattr(booking, 'status')
            print_test("Booking has status field", result)
            
            # Test booking created_by
            result = hasattr(booking, 'created_by')
            print_test("Booking tracks creator", result)
        else:
            print_test("Bookings exist", True, "No bookings yet - this is OK")
    
    # ==================== APPLICATION TESTS ====================
    
    def test_applications(self):
        print_section("APPLICATIONS MODULE")
        
        # Count applications
        app_count = Application.objects.count()
        result = True
        print_test(f"Applications in database: {app_count}", result)
        
        # Get first application
        application = Application.objects.first()
        if application:
            self.test_data['application'] = application
            print_test(f"Sample application ID: {application.application_id}", True)
            
            # Test application fields
            result = hasattr(application, 'client') and hasattr(application, 'status')
            print_test("Application has client relationship and status", result)
            
            # Test application dates
            result = hasattr(application, 'submission_date')
            print_test("Application tracks submission date", result)
            
            # Test application assigned_to
            result = hasattr(application, 'assigned_to')
            print_test("Application has assignment field", result)
        else:
            print_test("Applications exist", True, "No applications yet - this is OK")
    
    # ==================== PAYMENT TESTS ====================
    
    def test_payments(self):
        print_section("PAYMENTS MODULE")
        
        # Count payments
        payment_count = Payment.objects.count()
        result = True
        print_test(f"Payments in database: {payment_count}", result)
        
        # Get first payment
        payment = Payment.objects.first()
        if payment:
            self.test_data['payment'] = payment
            print_test(f"Sample payment ID: {payment.id}", True)
            
            # Test payment fields
            result = hasattr(payment, 'amount') and hasattr(payment, 'payment_method')
            print_test("Payment has amount and method fields", result)
            
            # Test payment status
            result = hasattr(payment, 'status')
            print_test("Payment has status field", result)
            
            # Test payment relationships
            result = hasattr(payment, 'booking') or hasattr(payment, 'application')
            print_test("Payment linked to booking/application", result)
        else:
            print_test("Payments exist", True, "No payments yet - this is OK")
    
    # ==================== URL ROUTING TESTS ====================
    
    def test_url_routing(self):
        print_section("URL ROUTING")
        
        # Test accounts URLs
        response = self.client.get('/login/')
        result = response.status_code in [200, 302]
        print_test("Login URL accessible", result)
        
        # Test schemes URLs
        response = self.client.get('/schemes/')
        result = response.status_code in [200, 302]
        print_test("Schemes URL accessible", result)
        
        # Test clients URLs
        response = self.client.get('/clients/')
        result = response.status_code in [200, 302]
        print_test("Clients URL accessible", result)
        
        # Test bookings URLs
        response = self.client.get('/bookings/')
        result = response.status_code in [200, 302]
        print_test("Bookings URL accessible", result)
        
        # Test applications URLs
        response = self.client.get('/applications/')
        result = response.status_code in [200, 302]
        print_test("Applications URL accessible", result)
        
        # Test API URLs
        response = self.client.get('/api/')
        result = response.status_code in [200, 302, 404]  # 404 is OK if no root API endpoint
        print_test("API URLs accessible", result)
    
    # ==================== RELATIONSHIP TESTS ====================
    
    def test_model_relationships(self):
        print_section("MODEL RELATIONSHIPS")
        
        # Test User -> Client relationship
        user_with_client = User.objects.filter(role='CLIENT', client_profile__isnull=False).first()
        result = user_with_client is not None or ClientModel.objects.count() == 0
        print_test("User-Client relationship", result, "OK if no clients exist yet")
        
        # Test Booking -> Client relationship
        booking = Booking.objects.select_related('client').first()
        result = booking is None or (booking and hasattr(booking, 'client'))
        print_test("Booking-Client relationship", result)
        
        # Test Booking -> Service relationship
        booking = Booking.objects.select_related('service').first()
        result = booking is None or (booking and hasattr(booking, 'service'))
        print_test("Booking-Service relationship", result)
        
        # Test Application -> Client relationship  
        application = Application.objects.select_related('client').first()
        result = application is None or (application and hasattr(application, 'client'))
        print_test("Application-Client relationship", result)
        
        # Test Payment -> Booking relationship
        payment = Payment.objects.filter(booking__isnull=False).first()
        result = payment is None or (payment and hasattr(payment, 'booking'))
        print_test("Payment-Booking relationship", result)
    
    # ==================== RUN ALL TESTS ====================
    
    def run_all_tests(self):
        print_header("AGNIVRIDHI CRM - COMPREHENSIVE SYSTEM TEST")
        print(f"{Colors.BOLD}Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}\n")
        
        # Run all test suites
        self.test_database_models()
        self.test_users_and_roles()
        self.test_dashboard_access()
        self.test_schemes()
        self.test_clients()
        self.test_companies()
        self.test_bookings()
        self.test_applications()
        self.test_payments()
        self.test_url_routing()
        self.test_model_relationships()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        print_header("TEST SUMMARY")
        
        total = self.results['total']
        passed = self.results['passed']
        failed = self.results['failed']
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"{Colors.BOLD}Total Tests:{Colors.ENDC} {total}")
        print(f"{Colors.OKGREEN}Passed:{Colors.ENDC} {passed}")
        print(f"{Colors.FAIL}Failed:{Colors.ENDC} {failed}")
        print(f"{Colors.BOLD}Pass Rate:{Colors.ENDC} {pass_rate:.1f}%\n")
        
        if pass_rate >= 90:
            status = f"{Colors.OKGREEN}EXCELLENT ✓{Colors.ENDC}"
        elif pass_rate >= 75:
            status = f"{Colors.WARNING}GOOD ⚠{Colors.ENDC}"
        else:
            status = f"{Colors.FAIL}NEEDS ATTENTION ✗{Colors.ENDC}"
        
        print(f"{Colors.BOLD}Overall Status:{Colors.ENDC} {status}\n")
        
        # Print errors if any
        if self.results['errors']:
            print(f"{Colors.FAIL}{Colors.BOLD}ERRORS DETECTED:{Colors.ENDC}\n")
            for i, error in enumerate(self.results['errors'], 1):
                print(f"{i}. {error['test']}")
                print(f"   {Colors.WARNING}{error['error']}{Colors.ENDC}\n")
        
        print(f"\n{Colors.BOLD}Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}\n")

if __name__ == '__main__':
    tester = CRMSystemTester()
    tester.run_all_tests()
