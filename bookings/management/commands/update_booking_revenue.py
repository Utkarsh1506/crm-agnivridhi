"""
Management command to update revenue tracking for existing bookings and clients.
Supports both legacy clients (revenue in Client fields) and new multi-booking clients.
"""
from django.core.management.base import BaseCommand
from bookings.models import Booking
from clients.models import Client
from decimal import Decimal


class Command(BaseCommand):
    help = 'Update revenue fields for bookings and recalculate/preserve client totals'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )
        parser.add_argument(
            '--preserve-legacy',
            action='store_true',
            help='Keep existing client-level revenue (for legacy clients without bookings)',
            default=True
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        preserve_legacy = options.get('preserve_legacy', True)
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be saved'))
        
        self.stdout.write('\\n' + self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS('REVENUE SYSTEM MIGRATION'))
        self.stdout.write(self.style.SUCCESS('='*60))
        
        # ===== STEP 1: Update Bookings with Revenue Data =====
        self.stdout.write('\\n' + self.style.SUCCESS('[1/3] UPDATING BOOKING REVENUE FIELDS'))
        self.stdout.write('-' * 60)
        
        bookings = Booking.objects.all()
        updated_bookings = 0
        
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
                    
                updated_bookings += 1
                self.stdout.write(
                    self.style.SUCCESS(f'  ✓ {booking.booking_id}: ₹{booking.total_with_gst} '
                    f'({booking.status})')
                )
        
        self.stdout.write(f'{self.style.SUCCESS(str(updated_bookings))} bookings updated')
        
        # ===== STEP 2: Preserve/Aggregate Client Revenue =====
        self.stdout.write('\\n' + self.style.SUCCESS('[2/3] PROCESSING CLIENT REVENUE'))
        self.stdout.write('-' * 60)
        
        clients_with_legacy_revenue = 0
        clients_with_bookings = 0
        
        if not dry_run:
            for client in Client.objects.all():
                # Check if client has bookings with revenue data
                has_booking_revenue = client.bookings.filter(pitched_amount__gt=0).exists()
                has_client_revenue = client.total_pitched_amount > 0
                
                if has_booking_revenue:
                    # Use booking aggregation
                    client.calculate_aggregated_revenue()
                    Client.objects.filter(pk=client.pk).update(
                        total_pitched_amount=client.total_pitched_amount,
                        gst_amount=client.gst_amount,
                        gst_percentage=client.gst_percentage,
                        total_with_gst=client.total_with_gst,
                        received_amount=client.received_amount,
                        pending_amount=client.pending_amount
                    )
                    clients_with_bookings += 1
                    self.stdout.write(
                        f'  ✓ {client.company_name} (from bookings): ₹{client.total_with_gst}'
                    )
                elif has_client_revenue and preserve_legacy:
                    # Keep existing client-level revenue (legacy)
                    # Ensure all fields are properly calculated
                    gst_pct = Decimal(client.gst_percentage or 18)
                    total = Decimal(client.total_pitched_amount or 0)
                    received = Decimal(client.received_amount or 0)
                    
                    if total > 0:
                        gst_amt = (total * gst_pct / Decimal('100')).quantize(Decimal('0.01'))
                        total_with_gst = total + gst_amt
                        pending = max(Decimal('0.00'), total_with_gst - received)
                        
                        Client.objects.filter(pk=client.pk).update(
                            gst_amount=gst_amt,
                            total_with_gst=total_with_gst,
                            pending_amount=pending
                        )
                        clients_with_legacy_revenue += 1
                        self.stdout.write(
                            f'  ✓ {client.company_name} (legacy): ₹{total_with_gst}'
                        )
            
            self.stdout.write(f'\\n{self.style.SUCCESS(str(clients_with_bookings))} clients using booking aggregation')
            self.stdout.write(f'{self.style.SUCCESS(str(clients_with_legacy_revenue))} clients using legacy data')
        else:
            self.stdout.write(self.style.WARNING('Skipping client update (dry run)'))
        
        # ===== STEP 3: Verification =====
        self.stdout.write('\\n' + self.style.SUCCESS('[3/3] VERIFICATION'))
        self.stdout.write('-' * 60)
        
        total_booking_revenue = Booking.objects.filter(pitched_amount__gt=0).count()
        self.stdout.write(f'  Bookings with revenue: {total_booking_revenue}')
        
        clients_with_revenue = Client.objects.filter(total_with_gst__gt=0).count()
        self.stdout.write(f'  Clients with revenue: {clients_with_revenue}')
        
        self.stdout.write('\\n' + self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS('MIGRATION COMPLETE!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write('\\n' + self.style.WARNING(
            'Note: The system now supports both legacy (client-level) and '
            '\\nnew (booking-level) revenue tracking. When bookings are added with revenue,'
            '\\ntotals automatically aggregate at the client level.'
        ))

