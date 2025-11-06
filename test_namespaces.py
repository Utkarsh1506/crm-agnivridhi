"""
Quick smoke test to verify namespaced URL reversing works correctly.
Run: python manage.py test test_namespaces --settings=agnivridhi_crm.settings
"""
from django.test import TestCase
from django.urls import reverse


class NamespacedURLResolverTest(TestCase):
    """Test suite for namespaced URL resolution."""

    def test_accounts_urls(self):
        """Test accounts app namespaced URLs."""
        self.assertIsNotNone(reverse('accounts:login'))
        self.assertIsNotNone(reverse('accounts:dashboard'))
        self.assertIsNotNone(reverse('accounts:client_portal'))
        self.assertIsNotNone(reverse('accounts:manager_dashboard'))
        self.assertIsNotNone(reverse('accounts:sales_dashboard'))
        print("✓ accounts: namespace resolves")

    def test_applications_urls(self):
        """Test applications app namespaced URLs."""
        self.assertIsNotNone(reverse('applications:application_list'))
        self.assertIsNotNone(reverse('applications:client_applications_list'))
        self.assertIsNotNone(reverse('applications:sales_applications_list'))
        self.assertIsNotNone(reverse('applications:team_applications_list'))
        self.assertIsNotNone(reverse('applications:pending_applications'))
        # Detail routes need kwargs
        self.assertIsNotNone(reverse('applications:manager_application_detail', kwargs={'pk': 1}))
        self.assertIsNotNone(reverse('applications:approve_application', kwargs={'pk': 1}))
        print("✓ applications: namespace resolves")

    def test_bookings_urls(self):
        """Test bookings app namespaced URLs."""
        self.assertIsNotNone(reverse('bookings:booking_list'))
        self.assertIsNotNone(reverse('bookings:client_bookings_list'))
        self.assertIsNotNone(reverse('bookings:sales_bookings_list'))
        self.assertIsNotNone(reverse('bookings:team_bookings_list'))
        self.assertIsNotNone(reverse('bookings:booking_detail', kwargs={'id': 1}))
        self.assertIsNotNone(reverse('bookings:create_documentation_booking', kwargs={'scheme_id': 1}))
        print("✓ bookings: namespace resolves")

    def test_documents_urls(self):
        """Test documents app namespaced URLs."""
        self.assertIsNotNone(reverse('documents:document_list'))
        self.assertIsNotNone(reverse('documents:client_documents_list'))
        self.assertIsNotNone(reverse('documents:sales_documents_list'))
        self.assertIsNotNone(reverse('documents:team_documents_list'))
        self.assertIsNotNone(reverse('documents:document_detail', kwargs={'pk': 1}))
        self.assertIsNotNone(reverse('documents:document_download', kwargs={'pk': 1}))
        print("✓ documents: namespace resolves")

    def test_payments_urls(self):
        """Test payments app namespaced URLs."""
        self.assertIsNotNone(reverse('payments:payment_list'))
        self.assertIsNotNone(reverse('payments:client_payments_list'))
        self.assertIsNotNone(reverse('payments:sales_payments_list'))
        self.assertIsNotNone(reverse('payments:team_payments_list'))
        self.assertIsNotNone(reverse('payments:payment_detail', kwargs={'pk': 1}))
        print("✓ payments: namespace resolves")

    def test_schemes_urls(self):
        """Test schemes app namespaced URLs."""
        self.assertIsNotNone(reverse('schemes:scheme_list'))
        self.assertIsNotNone(reverse('schemes:scheme_detail', kwargs={'pk': 1}))
        self.assertIsNotNone(reverse('schemes:check_eligibility'))
        print("✓ schemes: namespace resolves")

    def test_api_urls(self):
        """Test api app namespaced URLs (DRF router)."""
        # DRF router URLs are automatically namespaced
        self.assertIsNotNone(reverse('api:client-list'))
        self.assertIsNotNone(reverse('api:booking-list'))
        self.assertIsNotNone(reverse('api:payment-list'))
        self.assertIsNotNone(reverse('api:application-list'))
        print("✓ api: namespace resolves")


if __name__ == '__main__':
    import django
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
    django.setup()
    
    from django.test.utils import get_runner
    TestRunner = get_runner(django.conf.settings)
    runner = TestRunner(verbosity=2, interactive=False)
    failures = runner.run_tests(['test_namespaces'])
    if not failures:
        print("\n✅ All namespaced URLs resolve successfully!")
