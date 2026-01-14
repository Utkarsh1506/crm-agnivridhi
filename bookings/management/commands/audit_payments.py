from django.core.management.base import BaseCommand
from payments.models import Payment
from clients.models import Client


class Command(BaseCommand):
    help = 'Check Payment records'

    def handle(self, *args, **options):
        print("\n" + "="*70)
        print("PAYMENT AUDIT")
        print("="*70)

        total_payments = Payment.objects.count()
        print(f"\nTotal payments: {total_payments}")

        if total_payments > 0:
            print(f"Authorized: {Payment.objects.filter(status='AUTHORIZED').count()}")
            print(f"Pending: {Payment.objects.filter(status='PENDING').count()}")
            print(f"Failed: {Payment.objects.filter(status='FAILED').count()}")

            print("\n" + "="*70)
            print("Recent Payments")
            print("="*70)
            
            for p in Payment.objects.select_related('client', 'booking').order_by('-created_at')[:10]:
                print(f"\n  Payment ID: {p.id}")
                print(f"  Client: {p.client.company_name}")
                print(f"  Amount: ₹{p.amount}")
                print(f"  Status: {p.status}")
                print(f"  Booking: {p.booking.booking_id if p.booking else 'None'}")
        else:
            print("\nNo payments found!")

        print("\n" + "="*70)
        print("Client Received Amounts")
        print("="*70)

        clients = Client.objects.filter(received_amount__gt=0)
        print(f"\nClients with received_amount > 0: {clients.count()}")
        
        for c in clients:
            print(f"  {c.company_name}: ₹{c.received_amount}")
