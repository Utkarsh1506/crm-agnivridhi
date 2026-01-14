from django.core.management.base import BaseCommand
from clients.models import Client
from payments.models import Payment
from django.db.models import Sum, Q


class Command(BaseCommand):
    help = 'Sync client.received_amount from captured payments'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be saved\n'))
        
        print("="*70)
        print("SYNC CLIENT RECEIVED AMOUNT FROM PAYMENTS")
        print("="*70 + "\n")
        
        updated_count = 0
        
        # Get all clients
        clients = Client.objects.all()
        print(f"Processing {clients.count()} clients...\n")
        
        for client in clients:
            # Get total received from CAPTURED payments
            received_from_payments = Payment.objects.filter(
                client=client,
                status__in=['CAPTURED', 'AUTHORIZED']
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            old_received = client.received_amount
            
            # If received_amount is 0 but payments exist, update it
            if client.received_amount == 0 and received_from_payments > 0:
                client.received_amount = received_from_payments
                
                # Also update pending
                client.pending_amount = max(0, client.total_with_gst - received_from_payments)
                
                if not dry_run:
                    Client.objects.filter(pk=client.pk).update(
                        received_amount=client.received_amount,
                        pending_amount=client.pending_amount
                    )
                
                updated_count += 1
                self.stdout.write(
                    f"✓ {client.company_name}\n"
                    f"  Received: ₹{old_received} → ₹{client.received_amount}\n"
                    f"  Pending: ₹{client.total_with_gst - old_received} → ₹{client.pending_amount}\n"
                )
        
        print()
        print("="*70)
        print(f"UPDATED {updated_count} CLIENTS")
        print("="*70 + "\n")
