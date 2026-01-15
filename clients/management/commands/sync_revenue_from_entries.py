from django.core.management.base import BaseCommand
from clients.models import Client
from payments.models import RevenueEntry
from decimal import Decimal


class Command(BaseCommand):
    help = 'Sync RevenueEntry data to Client model fields'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n🔄 SYNCING REVENUE DATA FROM REVENUEENTRY TO CLIENT:\n'))

        # Get latest revenue entry for each client
        clients_updated = 0
        
        for client in Client.objects.all():
            try:
                latest_entry = client.revenue_entries.latest('created_at')
            except RevenueEntry.DoesNotExist:
                # Skip clients without revenue entries
                continue
            
            if latest_entry:
                old_pitched = client.total_pitched_amount
                old_received = client.received_amount
                
                # Update client with latest revenue entry data
                client.total_pitched_amount = latest_entry.total_pitched_amount
                client.received_amount = latest_entry.received_amount
                client.pending_amount = latest_entry.pending_amount
                
                # Recalculate GST if pitched amount exists
                if client.total_pitched_amount > 0 and not client.gst_percentage:
                    client.gst_percentage = Decimal('18.00')
                
                # Save without triggering signals
                client.save(update_fields=['total_pitched_amount', 'received_amount', 'pending_amount', 'gst_percentage'])
                
                if old_pitched != client.total_pitched_amount or old_received != client.received_amount:
                    self.stdout.write(
                        f'✅ {client.company_name}: '
                        f'Pitched ₹{old_pitched} → ₹{client.total_pitched_amount}, '
                        f'Received ₹{old_received} → ₹{client.received_amount}'
                    )
                    clients_updated += 1

        self.stdout.write(self.style.SUCCESS(f'\n✅ SYNC COMPLETE: {clients_updated} clients updated\n'))
