"""
Fix clients with broken revenue data:
- If total_with_gst = 0 but total_pitched_amount > 0, recalculate total_with_gst
- Recalculate pending_amount = total_with_gst - received_amount
"""
from django.core.management.base import BaseCommand
from clients.models import Client
from decimal import Decimal


class Command(BaseCommand):
    help = 'Fix clients with broken total_with_gst calculations'

    def handle(self, *args, **kwargs):
        self.stdout.write('\n=== Fixing Broken Revenue Data ===\n')
        
        clients = Client.objects.all()
        fixed_count = 0
        
        for client in clients:
            # Check if total_with_gst is broken
            if client.total_with_gst == 0 and (client.total_pitched_amount > 0 or client.received_amount > 0):
                self.stdout.write(f'\n❌ BROKEN: {client.id}. {client.company_name}')
                self.stdout.write(f'   Before: Pitched={client.total_pitched_amount}, GST={client.gst_amount}, Total+GST={client.total_with_gst}, Received={client.received_amount}')
                
                # Recalculate
                pitched = client.total_pitched_amount or Decimal('0.00')
                gst_pct = client.gst_percentage or Decimal('18.00')
                
                # Recalculate GST
                gst_amount = (pitched * gst_pct / Decimal('100')).quantize(Decimal('0.01'))
                total_with_gst = pitched + gst_amount
                
                # Fix received if it's > new total
                received = client.received_amount or Decimal('0.00')
                if received > total_with_gst:
                    total_with_gst = received
                    gst_amount = Decimal('0.00')
                
                # Calculate pending
                pending = total_with_gst - received
                if pending < 0:
                    pending = Decimal('0.00')
                
                # Update
                client.gst_amount = gst_amount
                client.total_with_gst = total_with_gst
                client.pending_amount = pending
                client.save()
                
                self.stdout.write(f'   After: Pitched={client.total_pitched_amount}, GST={client.gst_amount}, Total+GST={client.total_with_gst}, Received={client.received_amount}')
                fixed_count += 1
        
        if fixed_count == 0:
            self.stdout.write(self.style.SUCCESS('\n✅ No broken clients found - all data is consistent!'))
        else:
            self.stdout.write(self.style.SUCCESS(f'\n✅ Fixed {fixed_count} clients'))
