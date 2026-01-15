from django.core.management.base import BaseCommand
from clients.models import Client
from payments.models import RevenueEntry


class Command(BaseCommand):
    help = 'Debug revenue entries sync'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n🔍 REVENUE ENTRIES DEBUG:\n'))

        # Total revenue entries
        total_entries = RevenueEntry.objects.count()
        self.stdout.write(f'Total RevenueEntry records: {total_entries}')

        # Show first 5 entries
        self.stdout.write(self.style.SUCCESS('\n📋 SAMPLE ENTRIES:\n'))
        for entry in RevenueEntry.objects.all()[:5]:
            self.stdout.write(
                f'ID: {entry.id} | Client ID: {entry.client.id} | '
                f'Client: {entry.client.company_name} | '
                f'Pitched: ₹{entry.total_pitched_amount} | '
                f'Received: ₹{entry.received_amount} | '
                f'Created: {entry.created_at}'
            )

        # Check if any clients have entries
        self.stdout.write(self.style.SUCCESS('\n✅ CLIENTS WITH REVENUE ENTRIES:\n'))
        clients_with_entries = Client.objects.filter(revenue_entries__isnull=False).distinct()
        self.stdout.write(f'Count: {clients_with_entries.count()}')

        for client in clients_with_entries[:10]:
            entries_count = client.revenue_entries.count()
            latest = client.revenue_entries.latest('created_at')
            self.stdout.write(
                f'  - {client.company_name} (ID {client.id}): '
                f'{entries_count} entries | Latest: ₹{latest.total_pitched_amount}'
            )

        self.stdout.write(self.style.SUCCESS(f'\n📊 TOTAL CLIENTS: {Client.objects.count()}'))
