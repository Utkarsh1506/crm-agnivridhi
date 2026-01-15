from django.core.management.base import BaseCommand
from clients.models import Client
from payments.models import Payment
from bookings.models import Booking
from django.db.models import Sum


class Command(BaseCommand):
    help = 'Check if missing revenue is in payments/bookings tables'

    def handle(self, *args, **options):
        client_ids = [32, 31, 30, 29, 28, 26, 25, 24, 22]  # Missing revenue clients
        
        self.stdout.write(self.style.SUCCESS('\n🔍 CHECKING PAYMENTS & BOOKINGS:\n'))

        for client_id in client_ids:
            try:
                client = Client.objects.get(id=client_id)
                
                # Check Payments
                payments = Payment.objects.filter(client=client)
                payment_total = payments.aggregate(total=Sum('amount'))['total'] or 0
                
                # Check Bookings
                bookings = Booking.objects.filter(client=client)
                booking_count = bookings.count()
                
                if payment_total > 0 or booking_count > 0:
                    self.stdout.write(f'\n📋 {client.company_name} (ID: {client_id})')
                    self.stdout.write(f'   Bookings: {booking_count}')
                    self.stdout.write(f'   Payments Total: ₹{payment_total:,.2f}')
                    
                    if bookings.exists():
                        for booking in bookings:
                            self.stdout.write(f'   - Booking ID {booking.id}: {booking.service.name if booking.service else "No service"}')
                    
                    if payments.exists():
                        for payment in payments[:3]:  # Show first 3
                            self.stdout.write(f'   - Payment: ₹{payment.amount} ({payment.status})')
                
            except Client.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Client {client_id} not found'))

        self.stdout.write(self.style.SUCCESS('\n✅ CHECK COMPLETE'))
