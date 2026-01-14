from django.core.management.base import BaseCommand
from bookings.models import Booking
from clients.models import Client
from decimal import Decimal


class Command(BaseCommand):
    help = 'Sync received_amount from booking status (PAID = received, PENDING = pending)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be saved'))
        
        print("\n" + "="*70)
        print("SYNC BOOKING PAYMENT STATUS TO RECEIVED AMOUNT")
        print("="*70)
        
        bookings_updated = 0
        clients_updated = 0
        
        # For each booking, if status is PAID but received_amount is 0,  set it
        bookings = Booking.objects.filter(total_with_gst__gt=0)
        print(f"\nProcessing {bookings.count()} bookings...\n")
        
        for booking in bookings:
            old_received = booking.received_amount
            old_pending = booking.pending_amount
            
            # If booking is PAID, mark as received
            if booking.status in ['PAID', 'COMPLETED'] and booking.received_amount == 0:
                booking.received_amount = booking.total_with_gst
                booking.pending_amount = Decimal('0.00')
                
                if not dry_run:
                    booking.save()
                
                bookings_updated += 1
                self.stdout.write(
                    f"  ✓ {booking.booking_id}: {booking.status} - "
                    f"Received: ₹{old_received} → ₹{booking.received_amount}"
                )
        
        print(f"\n{bookings_updated} bookings synced")
        
        # Now recalculate all client received amounts
        print(f"\nRecalculating client received amounts...")
        
        if not dry_run:
            for client in Client.objects.all():
                old_received = client.received_amount
                client.calculate_aggregated_revenue()
                
                Client.objects.filter(pk=client.pk).update(
                    received_amount=client.received_amount,
                    pending_amount=client.pending_amount
                )
                
                if client.received_amount != old_received:
                    clients_updated += 1
                    self.stdout.write(
                        f"  ✓ {client.company_name}: "
                        f"Received: ₹{old_received} → ₹{client.received_amount}"
                    )
        
        print(f"\n{clients_updated} clients updated")
        
        print("\n" + "="*70)
        print("SYNC COMPLETE!")
        print("="*70 + "\n")
