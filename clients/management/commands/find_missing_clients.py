from django.core.management.base import BaseCommand
from clients.models import Client


class Command(BaseCommand):
    help = 'Check specific missing clients'

    def handle(self, *args, **options):
        missing_names = [
            'Vibhanshu',
            'KRITI',
            'Darsun',
            'Shivansh',
            'Vashnavi',
            'LEDERRA',
            'BRIO',
            'ULTRA VISION',
            'Sarfraz'
        ]

        self.stdout.write(self.style.SUCCESS('\n🔍 SEARCHING FOR MISSING CLIENTS:\n'))

        for name in missing_names:
            clients = Client.objects.filter(company_name__icontains=name)
            
            if clients.exists():
                for client in clients:
                    self.stdout.write(f'\n✅ FOUND: {client.company_name}')
                    self.stdout.write(f'   ID: {client.id}')
                    self.stdout.write(f'   Client ID: {client.client_id}')
                    self.stdout.write(f'   Pitched: ₹{client.total_pitched_amount}')
                    self.stdout.write(f'   GST %: {client.gst_percentage}')
                    self.stdout.write(f'   GST Amount: ₹{client.gst_amount}')
                    self.stdout.write(f'   Total: ₹{client.total_with_gst}')
                    self.stdout.write(f'   Received: ₹{client.received_amount}')
                    self.stdout.write(f'   Pending: ₹{client.pending_amount}')
                    self.stdout.write(f'   Status: {client.get_payment_status()}')
            else:
                self.stdout.write(self.style.ERROR(f'\n❌ NOT FOUND: {name}'))

        self.stdout.write(self.style.SUCCESS(f'\n\n📊 TOTAL CLIENTS IN DATABASE: {Client.objects.count()}'))
