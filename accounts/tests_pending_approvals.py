from django.test import TestCase, Client as DjangoClient
from django.urls import reverse
from django.utils import timezone
from accounts.models import User
from clients.models import Client as BizClient
from schemes.models import Scheme
from applications.models import Application
from bookings.models import Booking
from payments.models import Payment
from decimal import Decimal


class PendingApprovalsFlowTests(TestCase):
    def setUp(self):
        # Users
        self.manager = User.objects.create_user(username='mgr', password='pass', role='MANAGER')
        self.sales = User.objects.create_user(username='sales', password='pass', role='SALES', manager=self.manager)
        self.client_user = User.objects.create_user(username='cuser', password='pass', role='CLIENT')

        # Business client (unapproved)
        self.biz_client = BizClient.objects.create(
            user=self.client_user,
            company_name='Acme Corp',
            business_type='PVT_LTD',
            sector='SERVICE',
            company_age=5,
            annual_turnover=100,
            funding_required=50,
            existing_loans=0,
            contact_person='John Doe',
            contact_email='john@example.com',
            contact_phone='9999999999',
            address_line1='Addr1',
            city='City',
            state='State',
            pincode='123456',
            assigned_sales=self.sales,
            assigned_manager=self.manager,
            is_approved=False,
        )

        # Scheme
        # Minimal Scheme per actual model fields
        self.scheme = Scheme.objects.create(
            name='Test Scheme',
            full_name='Test Funding Scheme',
            scheme_code='TST001',
            category='LOAN',
            status='ACTIVE',
            description='A test scheme',
            benefits='Benefit list',
            eligible_sectors=['SERVICE'],
            eligible_business_types=['PVT_LTD'],
        )

        # Application SUBMITTED
        self.application = Application.objects.create(
            client=self.biz_client,
            scheme=self.scheme,
            status='SUBMITTED',
            applied_amount=25,
            purpose='Growth funding',
            assigned_to=self.sales,
            submission_date=timezone.now().date(),
            created_by=self.sales,
        )

        # Booking + Payment PENDING
        # Need a Service for Booking foreign key
        from bookings.models import Service
        self.service = Service.objects.create(
            name='Consulting',
            category='CONSULTING',
            description='Desc',
            short_description='Short',
            price=Decimal('5000.00'),
            duration_days=30,
        )

        self.booking = Booking.objects.create(
            client=self.biz_client,
            service=self.service,
            amount=Decimal('5000.00'),
            final_amount=Decimal('5000.00'),
            status='PENDING',
        )

        self.payment = Payment.objects.create(
            booking=self.booking,
            client=self.biz_client,
            amount=5000,
            status='PENDING',
            payment_method='OTHER',
            received_by=self.sales,
        )

        self.web = DjangoClient()
        self.web.login(username='mgr', password='pass')

    def test_pending_approvals_page_lists_all_items(self):
        url = reverse('accounts:pending_approvals')
        resp = self.web.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.application.application_id, resp.content.decode())
        self.assertIn(str(self.payment.id), resp.content.decode())
        self.assertIn(self.biz_client.company_name, resp.content.decode())

    def test_inline_application_approval_redirects_back(self):
        approve_url = reverse('applications:approve_application', args=[self.application.pk])
        resp = self.web.post(approve_url, {'approved_amount': '30', 'next': reverse('accounts:pending_approvals')})
        self.application.refresh_from_db()
        self.assertEqual(self.application.status, 'APPROVED')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers.get('Location'), reverse('accounts:pending_approvals'))

    def test_application_approval_ajax(self):
        approve_url = reverse('applications:approve_application', args=[self.application.pk])
        resp = self.web.post(approve_url, {'approved_amount': '40'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.application.refresh_from_db()
        self.assertEqual(self.application.status, 'APPROVED')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['status'], 'APPROVED')
