from django.core.management.base import BaseCommand
from django.utils import timezone
from clients.models import Client
from accounts.models import User
from decimal import Decimal


class Command(BaseCommand):
    help = 'Test if revenue data saves properly'

    def handle(self, *args, **options):
        try:
            # Create test user if doesn't exist
            timestamp = str(timezone.now().timestamp()).replace('.', '')
            test_email = f'test.revenue.{timestamp}@agnivridhi.com'
            test_username = f'test_revenue_{timestamp}'
            
            user = User.objects.create(
                email=test_email,
                username=test_username,
                first_name='Test',
                last_name='Revenue',
                role='CLIENT'
            )
            
            # Get an admin user for created_by
            admin_user = User.objects.filter(role='OWNER').first()
            if not admin_user:
                admin_user = user

            # Create test client with revenue data
            test_client = Client.objects.create(
                user=user,
                company_name=f'Test Revenue Client {timestamp}',
                business_type='PVT_LTD',
                sector='IT_SOFTWARE',
                created_by=admin_user,
                total_pitched_amount=Decimal('10000.00'),
                gst_percentage=Decimal('18.00'),
                received_amount=Decimal('5000.00')
            )

            # Refresh from DB to see calculated values
            test_client.refresh_from_db()

            self.stdout.write(self.style.SUCCESS('\n✅ TEST CLIENT CREATED\n'))
            self.stdout.write(f'ID: {test_client.id}')
            self.stdout.write(f'Company: {test_client.company_name}')
            self.stdout.write(f'Pitched Amount: ₹{test_client.total_pitched_amount}')
            self.stdout.write(f'GST %: {test_client.gst_percentage}%')
            self.stdout.write(f'GST Amount: ₹{test_client.gst_amount}')
            self.stdout.write(f'Total with GST: ₹{test_client.total_with_gst}')
            self.stdout.write(f'Received Amount: ₹{test_client.received_amount}')
            self.stdout.write(f'Pending Amount: ₹{test_client.pending_amount}')
            self.stdout.write(f'Status: {test_client.get_payment_status()}\n')

            # Check database directly
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT id, company_name, total_pitched_amount, gst_percentage, gst_amount, total_with_gst, received_amount, pending_amount FROM clients_client WHERE id = %s',
                    [test_client.id]
                )
                row = cursor.fetchone()
                if row:
                    self.stdout.write(self.style.SUCCESS('✅ DATABASE VERIFICATION:'))
                    self.stdout.write(f'ID: {row[0]}')
                    self.stdout.write(f'Company: {row[1]}')
                    self.stdout.write(f'Pitched: {row[2]}')
                    self.stdout.write(f'GST %: {row[3]}')
                    self.stdout.write(f'GST Amount: {row[4]}')
                    self.stdout.write(f'Total with GST: {row[5]}')
                    self.stdout.write(f'Received: {row[6]}')
                    self.stdout.write(f'Pending: {row[7]}\n')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ ERROR: {str(e)}\n'))
            import traceback
            traceback.print_exc()
