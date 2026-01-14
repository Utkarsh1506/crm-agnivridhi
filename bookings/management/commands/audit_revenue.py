from django.core.management.base import BaseCommand
from clients.models import Client
from django.db.models import Sum


class Command(BaseCommand):
    help = 'Audit client revenue data'

    def handle(self, *args, **options):
        print("\n" + "="*70)
        print("CLIENT REVENUE AUDIT")
        print("="*70)

        # Get all clients
        all_clients = Client.objects.all()
        clients_with_revenue = all_clients.exclude(total_with_gst=0, total_pitched_amount=0, received_amount=0)

        print(f"\nTotal clients: {all_clients.count()}")
        print(f"Clients with revenue: {clients_with_revenue.count()}")

        print("\n" + "="*70)
        print("CLIENTS WITH REVENUE")
        print("="*70)

        if clients_with_revenue.exists():
            for c in clients_with_revenue:
                print(f"\nClient: {c.company_name}")
                print(f"  Total Pitched: ₹{c.total_pitched_amount}")
                print(f"  GST Amount:    ₹{c.gst_amount}")
                print(f"  Total with GST: ₹{c.total_with_gst}")
                print(f"  Received:      ₹{c.received_amount}")
                print(f"  Pending:       ₹{c.pending_amount}")
                print(f"  Bookings:      {c.bookings.count()}")

        # Aggregate
        agg = Client.objects.aggregate(
            total_pitched=Sum('total_pitched_amount'),
            total_with_gst=Sum('total_with_gst'),
            total_received=Sum('received_amount'),
            total_pending=Sum('pending_amount'),
        )

        print("\n" + "="*70)
        print("AGGREGATE TOTALS (All Clients)")
        print("="*70)
        print(f"Total Pitched:  ₹{agg.get('total_pitched') or 0}")
        print(f"Total with GST: ₹{agg.get('total_with_gst') or 0}")
        print(f"Total Received: ₹{agg.get('total_received') or 0}")
        print(f"Total Pending:  ₹{agg.get('total_pending') or 0}")

        print("\n" + "="*70)
        print("ALL CLIENTS (first 25)")
        print("="*70)
        for c in all_clients[:25]:
            if c.total_with_gst > 0 or c.received_amount > 0:
                status = "✓ PAID" if c.received_amount > 0 else "⏳ PENDING"
                print(f"{status} | {c.company_name}: ₹{c.total_with_gst} (Received: ₹{c.received_amount})")
