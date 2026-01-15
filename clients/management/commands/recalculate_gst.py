from django.core.management.base import BaseCommand
from clients.models import Client
from decimal import Decimal


class Command(BaseCommand):
    help = 'Recalculate and update GST fields for all clients'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n📊 RECALCULATING GST FOR ALL CLIENTS:\n'))

        updated_count = 0

        for client in Client.objects.all():
            old_gst_amount = client.gst_amount
            old_total_with_gst = client.total_with_gst

            # Set default GST percentage if not set
            if not client.gst_percentage or client.gst_percentage == 0:
                client.gst_percentage = Decimal('18.00')

            # Calculate GST amount
            if client.total_pitched_amount > 0:
                client.gst_amount = client.total_pitched_amount * (client.gst_percentage / Decimal('100'))
                client.total_with_gst = client.total_pitched_amount + client.gst_amount
            else:
                client.gst_amount = Decimal('0.00')
                client.total_with_gst = Decimal('0.00')

            # Recalculate pending
            if client.total_with_gst > 0:
                client.pending_amount = client.total_with_gst - client.received_amount
            else:
                client.pending_amount = Decimal('0.00')

            # Save if changed
            if old_gst_amount != client.gst_amount or old_total_with_gst != client.total_with_gst:
                client.save(update_fields=['gst_percentage', 'gst_amount', 'total_with_gst', 'pending_amount'])
                self.stdout.write(
                    f'✅ {client.company_name}: '
                    f'GST ₹{old_gst_amount} → ₹{client.gst_amount}, '
                    f'Total ₹{old_total_with_gst} → ₹{client.total_with_gst}'
                )
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(f'\n✅ COMPLETE: {updated_count} clients updated\n'))
