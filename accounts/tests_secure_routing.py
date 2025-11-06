"""
Secure Routing Test Suite for Agnivridhi CRM
Tests role-based access control, middleware enforcement, and 403 handling.

Run: python manage.py test accounts.tests_secure_routing
"""
from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User
from accounts.constants import (
    ROLE_SUPERUSER, ROLE_OWNER, ROLE_ADMIN,
    ROLE_MANAGER, ROLE_SALES, ROLE_CLIENT
)


class SecureRoutingTestCase(TestCase):
    """Test suite for role-based access control and middleware"""
    
    def setUp(self):
        """Create test users with different roles"""
        self.client_obj = Client()
        
        # Create users for each role
        self.superuser = User.objects.create_user(
            username='superuser',
            password='test123',
            role='SUPERUSER',
            is_superuser=True,
            is_staff=True
        )
        
        self.owner = User.objects.create_user(
            username='owner',
            password='test123',
            role='OWNER',
            is_owner=True,
            is_staff=True
        )
        
        self.admin = User.objects.create_user(
            username='admin',
            password='test123',
            role='ADMIN',
            is_staff=True
        )
        
        self.manager = User.objects.create_user(
            username='manager',
            password='test123',
            role='MANAGER',
            is_staff=True
        )
        
        self.sales = User.objects.create_user(
            username='sales',
            password='test123',
            role='SALES',
            is_staff=True
        )
        
        self.client_user = User.objects.create_user(
            username='client',
            password='test123',
            role='CLIENT'
        )
    
    def test_client_cannot_access_manager_routes(self):
        """Clients should be blocked from manager-only routes"""
        self.client_obj.login(username='client', password='test123')
        
        response = self.client_obj.get(reverse('accounts:manager_dashboard'))
        
        # Should get 403 Forbidden
        self.assertEqual(response.status_code, 403)
    
    def test_sales_cannot_access_manager_routes(self):
        """Sales users should be blocked from manager-only routes"""
        self.client_obj.login(username='sales', password='test123')
        
        response = self.client_obj.get(reverse('accounts:team_members_list'))
        
        # Should get 403 Forbidden (team views are manager+)
        self.assertEqual(response.status_code, 403)
    
    def test_manager_can_access_own_routes(self):
        """Managers should access manager routes successfully"""
        self.client_obj.login(username='manager', password='test123')
        
        response = self.client_obj.get(reverse('accounts:manager_dashboard'))
        
        # Should succeed
        self.assertEqual(response.status_code, 200)
    
    def test_superuser_bypasses_all_restrictions(self):
        """Superusers should access any route"""
        self.client_obj.login(username='superuser', password='test123')
        
        # Try accessing routes from different roles
        routes = [
            reverse('accounts:manager_dashboard'),
            reverse('accounts:sales_dashboard'),
            reverse('accounts:client_portal'),
        ]
        
        for route in routes:
            response = self.client_obj.get(route)
            # Superuser should access all (200) or redirect (302)
            self.assertIn(response.status_code, [200, 302])
    
    def test_unauthenticated_redirects_to_login(self):
        """Unauthenticated users should be redirected to login"""
        response = self.client_obj.get(reverse('accounts:manager_dashboard'))
        
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('accounts:login')))
    
    def test_role_hierarchy_admin_access(self):
        """Admins should access manager and below routes"""
        self.client_obj.login(username='admin', password='test123')
        
        # Admin should access manager routes
        response = self.client_obj.get(reverse('accounts:manager_dashboard'))
        self.assertIn(response.status_code, [200, 302])  # Success or redirect to own dashboard
    
    def test_403_template_renders(self):
        """Custom 403 template should render with user info"""
        self.client_obj.login(username='client', password='test123')
        
        response = self.client_obj.get(reverse('accounts:manager_dashboard'))
        
        self.assertEqual(response.status_code, 403)
        # Should use custom template
        self.assertIn(b'Access Denied', response.content)
        self.assertIn(b'403', response.content)
    
    def test_normalized_role_property(self):
        """User.normalized_role should return lowercase role"""
        self.assertEqual(self.admin.normalized_role, 'admin')
        self.assertEqual(self.manager.normalized_role, 'manager')
        self.assertEqual(self.sales.normalized_role, 'sales')
        self.assertEqual(self.client_user.normalized_role, 'client')
    
    def test_namespace_access_mapping(self):
        """Verify ROLE_NAMESPACE_MAP is correctly configured"""
        from accounts.constants import ROLE_NAMESPACE_MAP
        
        # Managers should have access to bookings namespace
        self.assertIn('bookings', ROLE_NAMESPACE_MAP[ROLE_MANAGER])
        
        # Clients should NOT have access to team views
        self.assertNotIn('team', ROLE_NAMESPACE_MAP.get(ROLE_CLIENT, []))
        
        # Everyone should have accounts namespace
        for role in [ROLE_ADMIN, ROLE_MANAGER, ROLE_SALES, ROLE_CLIENT]:
            self.assertIn('accounts', ROLE_NAMESPACE_MAP[role])


class RoleChangeSignalTestCase(TestCase):
    """Test role change signal behavior"""
    
    def setUp(self):
        """Create a test user"""
        self.user = User.objects.create_user(
            username='testuser',
            password='test123',
            role='SALES'
        )
        # Set last_login to simulate active session
        from django.utils import timezone
        self.user.last_login = timezone.now()
        self.user.save()
    
    def test_role_change_clears_last_login(self):
        """Changing role should clear last_login to force re-authentication"""
        # Change role
        self.user.role = 'MANAGER'
        self.user.save()
        
        # Refresh from DB
        self.user.refresh_from_db()
        
        # last_login should be cleared
        self.assertIsNone(self.user.last_login)
    
    def test_same_role_keeps_last_login(self):
        """Saving without role change should preserve last_login"""
        original_login = self.user.last_login
        
        # Save without changing role
        self.user.phone = '+1234567890'
        self.user.save()
        
        # Refresh
        self.user.refresh_from_db()
        
        # last_login should remain
        self.assertEqual(self.user.last_login, original_login)


if __name__ == '__main__':
    import django
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
    django.setup()
    
    from django.test.utils import get_runner
    TestRunner = get_runner(django.conf.settings)
    runner = TestRunner(verbosity=2, interactive=False)
    failures = runner.run_tests(['accounts.tests_secure_routing'])
    if not failures:
        print("\n✅ All secure routing tests passed!")
