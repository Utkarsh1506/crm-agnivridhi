"""
Tests for Employee Identity & Verification System
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from io import BytesIO
from PIL import Image

from employees.models import Employee, EmployeeIDSequence, EmployeeVerificationLog
from employees.id_generator import EmployeeIDGenerator
from employees.qr_generator import QRCodeGenerator

User = get_user_model()


class EmployeeIDGeneratorTest(TestCase):
    """Test Employee ID generation"""
    
    def setUp(self):
        # Clear any existing sequences
        EmployeeIDSequence.objects.all().delete()
    
    def test_first_employee_id(self):
        """Test first employee ID is AGN-EMP-001"""
        emp_id = EmployeeIDGenerator.generate_employee_id()
        self.assertEqual(emp_id, 'AGN-EMP-001')
    
    def test_sequential_employee_ids(self):
        """Test sequential ID generation"""
        ids = [EmployeeIDGenerator.generate_employee_id() for _ in range(5)]
        expected = ['AGN-EMP-001', 'AGN-EMP-002', 'AGN-EMP-003', 'AGN-EMP-004', 'AGN-EMP-005']
        self.assertEqual(ids, expected)
    
    def test_verification_token_uniqueness(self):
        """Test verification tokens are unique"""
        tokens = [EmployeeIDGenerator.generate_verification_token() for _ in range(10)]
        self.assertEqual(len(tokens), len(set(tokens)))  # All unique


class EmployeeModelTest(TestCase):
    """Test Employee model"""
    
    def setUp(self):
        EmployeeIDSequence.objects.all().delete()
        self.user = User.objects.create_user(
            username='testadmin',
            email='admin@test.com',
            password='testpass123'
        )
        
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='red')
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        self.test_image = SimpleUploadedFile('test.png', img_io.getvalue(), content_type='image/png')
    
    def test_employee_creation(self):
        """Test creating an employee"""
        employee = Employee.objects.create(
            full_name='John Doe',
            designation='Manager',
            department='Sales',
            employee_photo=self.test_image,
            created_by=self.user,
        )
        
        # Verify auto-generated fields
        self.assertEqual(employee.employee_id, 'AGN-EMP-001')
        self.assertIsNotNone(employee.verification_token)
        self.assertEqual(employee.status, 'ACTIVE')
    
    def test_employee_deactivation(self):
        """Test employee deactivation"""
        employee = Employee.objects.create(
            full_name='Jane Smith',
            designation='Developer',
            department='Engineering',
            employee_photo=self.test_image,
            created_by=self.user,
        )
        
        self.assertTrue(employee.is_active_employee())
        employee.deactivate()
        self.assertFalse(employee.is_active_employee())
        self.assertIsNotNone(employee.date_of_exit)
    
    def test_employee_reactivation(self):
        """Test employee reactivation"""
        employee = Employee.objects.create(
            full_name='Bob Johnson',
            designation='Analyst',
            department='Finance',
            employee_photo=self.test_image,
            created_by=self.user,
        )
        
        employee.deactivate()
        self.assertFalse(employee.is_active_employee())
        
        employee.reactivate()
        self.assertTrue(employee.is_active_employee())
        self.assertIsNone(employee.date_of_exit)
    
    def test_verification_url_generation(self):
        """Test verification URL generation"""
        employee = Employee.objects.create(
            full_name='Alice Brown',
            designation='Manager',
            department='HR',
            employee_photo=self.test_image,
            created_by=self.user,
        )
        
        url = employee.get_verification_url()
        self.assertIn(employee.employee_id, url)
        self.assertTrue(url.startswith('https://'))


class QRCodeGeneratorTest(TestCase):
    """Test QR code generation"""
    
    def test_qr_code_generation(self):
        """Test QR code is generated"""
        test_url = 'https://agnivridhi.com/employee/verify/AGN-EMP-001/'
        qr_file = QRCodeGenerator.generate_qr_code(test_url)
        
        self.assertIsNotNone(qr_file)
        self.assertTrue(qr_file.name.endswith('.png'))
        self.assertTrue(len(qr_file.read()) > 0)


class EmployeeVerificationViewTest(TestCase):
    """Test public verification views"""
    
    def setUp(self):
        EmployeeIDSequence.objects.all().delete()
        self.client = Client()
        self.user = User.objects.create_user(
            username='testadmin',
            email='admin@test.com',
            password='testpass123'
        )
        
        # Create test image
        img = Image.new('RGB', (100, 100), color='red')
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        self.test_image = SimpleUploadedFile('test.png', img_io.getvalue(), content_type='image/png')
        
        # Create test employees
        self.active_employee = Employee.objects.create(
            full_name='Active Employee',
            designation='Manager',
            department='Sales',
            status='ACTIVE',
            employee_photo=self.test_image,
            created_by=self.user,
        )
        
        self.inactive_employee = Employee.objects.create(
            full_name='Inactive Employee',
            designation='Developer',
            department='Engineering',
            status='INACTIVE',
            employee_photo=self.test_image,
            created_by=self.user,
        )
    
    def test_public_verification_page_active_employee(self):
        """Test public verification page for active employee"""
        response = self.client.get(
            reverse('employees:employee_verify_public', kwargs={'employee_id': self.active_employee.employee_id})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('ACTIVE', response.content.decode())
        self.assertIn(self.active_employee.full_name, response.content.decode())
    
    def test_public_verification_page_inactive_employee(self):
        """Test public verification page for inactive employee shows warning"""
        response = self.client.get(
            reverse('employees:employee_verify_public', kwargs={'employee_id': self.inactive_employee.employee_id})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('INACTIVE', response.content.decode())
        self.assertIn('no longer associated', response.content.decode().lower())
    
    def test_verification_page_not_found(self):
        """Test verification page with non-existent employee"""
        response = self.client.get(
            reverse('employees:employee_verify_public', kwargs={'employee_id': 'AGN-EMP-999'})
        )
        
        self.assertEqual(response.status_code, 404)
    
    def test_verification_logging(self):
        """Test that verification attempts are logged"""
        self.client.get(
            reverse('employees:employee_verify_public', kwargs={'employee_id': self.active_employee.employee_id})
        )
        
        # Check log was created
        logs = EmployeeVerificationLog.objects.filter(employee=self.active_employee)
        self.assertEqual(logs.count(), 1)
        
        log = logs.first()
        self.assertIsNotNone(log.timestamp)


class AdminAccessControlTest(TestCase):
    """Test role-based access control for admin views"""
    
    def setUp(self):
        EmployeeIDSequence.objects.all().delete()
        self.client = Client()
        
        # Create test users
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            role='ADMIN'
        )
        
        self.sales_user = User.objects.create_user(
            username='sales',
            email='sales@test.com',
            password='testpass123',
            role='SALES'
        )
        
        # Create test image
        img = Image.new('RGB', (100, 100), color='red')
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        self.test_image = SimpleUploadedFile('test.png', img_io.getvalue(), content_type='image/png')
        
        # Create test employee
        self.employee = Employee.objects.create(
            full_name='Test Employee',
            designation='Manager',
            department='Sales',
            employee_photo=self.test_image,
            created_by=self.admin_user,
        )
    
    def test_admin_can_access_employee_list(self):
        """Test admin can access employee list"""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('employees:employee_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_non_admin_cannot_access_employee_list(self):
        """Test non-admin cannot access employee list"""
        self.client.login(username='sales', password='testpass123')
        response = self.client.get(reverse('employees:employee_list'))
        self.assertEqual(response.status_code, 403)
    
    def test_unauthenticated_redirected_to_login(self):
        """Test unauthenticated user is redirected to login"""
        response = self.client.get(reverse('employees:employee_list'))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertIn('login', response.url)
