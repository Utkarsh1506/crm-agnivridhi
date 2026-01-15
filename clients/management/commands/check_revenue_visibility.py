from django.core.management.base import BaseCommand
from clients.models import Client
from django.db.models import Q


class Command(BaseCommand):
    help = 'Check which clients have revenue data and which are visible'

    def handle(self, *args, **options):
        # All clients with revenue data
        clients_with_revenue = Client.objects.filter(
            Q(total_pitched_amount__gt=0) | 
            Q(received_amount__gt=0)
        ).order_by('-created_at')

        self.stdout.write(self.style.SUCCESS(f'\n✅ CLIENTS WITH REVENUE DATA: {clients_with_revenue.count()}\n'))

        for client in clients_with_revenue:
            status = client.get_payment_status()
            self.stdout.write(
                f'ID: {client.id:3d} | {client.company_name[:40]:40s} | '
                f'Pitched: ₹{client.total_pitched_amount:10,.2f} | '
                f'Total: ₹{client.total_with_gst:10,.2f} | '
                f'Received: ₹{client.received_amount:10,.2f} | '
                f'Status: {status}'
            )

        # Check if any have None or null fields
        self.stdout.write(self.style.WARNING('\n⚠️  CHECKING FOR NULL/NONE FIELDS:\n'))
        
        null_checks = Client.objects.filter(
            Q(total_pitched_amount__isnull=True) |
            Q(total_with_gst__isnull=True) |
            Q(received_amount__isnull=True) |
            Q(pending_amount__isnull=True)
        )
        
        if null_checks.exists():
            self.stdout.write(f'Found {null_checks.count()} clients with NULL fields')
            for c in null_checks[:5]:
                self.stdout.write(f'  - {c.id}: {c.company_name}')
        else:
            self.stdout.write('✅ No NULL fields found')

        # Total count
        self.stdout.write(self.style.SUCCESS(f'\n📊 TOTAL CLIENTS: {Client.objects.count()}'))
