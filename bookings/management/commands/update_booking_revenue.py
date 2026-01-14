"""
Management command to update revenue tracking for existing bookings.
This will populate the new revenue fields based on existing amount fields.
"""
from django.core.management.base import BaseCommand
from bookings.models import Booking
from clients.models import Client
from decimal import Decimal


class Command(BaseCommand):
    help = 'Update revenue fields for all existing bookings and recalculate client totals'

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
        
        # Update all bookings
        bookings = Booking.objects.all()
        updated_count = 0
        
        self.stdout.write(f'Processing {bookings.count()} bookings...')
        
        for booking in bookings:
            # If pitched_amount is not set, use final_amount as base
            if booking.pitched_amount == 0 and booking.final_amount > 0:
                booking.pitched_amount = booking.final_amount
                
                # Calculate GST (default 18%)
                booking.gst_percentage = Decimal('18.00')
                booking.gst_amount = (booking.pitched_amount * booking.gst_percentage) / Decimal('100.00')
                booking.total_with_gst = booking.pitched_amount + booking.gst_amount
                
                # Set received/pending based on status
                if booking.status in ['PAID', 'COMPLETED']:
                    booking.received_amount = booking.total_with_gst
                    booking.pending_amount = Decimal('0.00')
                else:
                    booking.received_amount = Decimal('0.00')
                    booking.pending_amount = booking.total_with_gst
                
                if not dry_run:
                    booking.save()
                    
                updated_count += 1
                self.stdout.write(
                    f'  Updated {booking.booking_id}: ₹{booking.total_with_gst} '
                    f'(Received: ₹{booking.received_amount}, Pending: ₹{booking.pending_amount})'
                )
        
        self.stdout.write(self.style.SUCCESS(f'Updated {updated_count} bookings'))
        
        # Recalculate client totals
        if not dry_run:
            self.stdout.write('\\nRecalculating client revenue totals...')
            clients = Client.objects.all()
            
            for client in clients:
                old_total = client.total_with_gst
                client.calculate_aggregated_revenue()
                
                # Use update() to avoid triggering save() method
                Client.objects.filter(pk=client.pk).update(
                    total_pitched_amount=client.total_pitched_amount,
                    gst_amount=client.gst_amount,
                    gst_percentage=client.gst_percentage,
                    total_with_gst=client.total_with_gst,
                    received_amount=client.received_amount,
                    pending_amount=client.pending_amount
                )
                
                if client.total_with_gst != old_total:
                    self.stdout.write(
                        f'  {client.company_name}: ₹{old_total} → ₹{client.total_with_gst}'
                    )
            
            self.stdout.write(self.style.SUCCESS('Client totals updated!'))
        else:
            self.stdout.write(self.style.WARNING('Skipping client total update (dry run)'))
        
        self.stdout.write(self.style.SUCCESS('\\nRevenue tracking setup complete!'))
