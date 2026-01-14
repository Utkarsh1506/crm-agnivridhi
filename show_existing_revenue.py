"""
Display all clients' current revenue data from database
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from clients.models import Client
from decimal import Decimal

print("\n" + "="*100)
print("ALL CLIENTS REVENUE DATA FROM DATABASE")
print("="*100 + "\n")

print(f"{'ID':<3} {'Client Name':<35} {'Pitched':<12} {'GST%':<6} {'GST Amt':<12} {'Total+GST':<12} {'Received':<12} {'Pending':<12}")
print("-"*100)

total_pitched = Decimal('0.00')
total_gst = Decimal('0.00')
total_with_gst = Decimal('0.00')
total_received = Decimal('0.00')
total_pending = Decimal('0.00')

clients = Client.objects.all().order_by('id')

for client in clients:
    print(f"{client.id:<3} {client.company_name[:34]:<35} ₹{client.total_pitched_amount:<10} {client.gst_percentage:<5.1f}% ₹{client.gst_amount:<10} ₹{client.total_with_gst:<10} ₹{client.received_amount:<10} ₹{client.pending_amount:<10}")
    
    total_pitched += client.total_pitched_amount or Decimal('0.00')
    total_gst += client.gst_amount or Decimal('0.00')
    total_with_gst += client.total_with_gst or Decimal('0.00')
    total_received += client.received_amount or Decimal('0.00')
    total_pending += client.pending_amount or Decimal('0.00')

print("-"*100)
print(f"{'TOTAL':<3} {'':<35} ₹{total_pitched:<10} {'AVG:' if clients.count() > 0 else '':<5} ₹{total_gst:<10} ₹{total_with_gst:<10} ₹{total_received:<10} ₹{total_pending:<10}")
print("="*100)

print(f"\n📊 SUMMARY:")
print(f"   Total Clients: {clients.count()}")
print(f"   Total Pitched Amount: ₹{total_pitched}")
print(f"   Total GST: ₹{total_gst}")
print(f"   Total with GST: ₹{total_with_gst}")
print(f"   Total Received: ₹{total_received}")
print(f"   Total Pending: ₹{total_pending}")

# Clients with revenue
clients_with_revenue = clients.filter(total_pitched_amount__gt=0).count()
clients_no_revenue = clients.filter(total_pitched_amount=0).count()

print(f"\n👥 CLIENT BREAKDOWN:")
print(f"   Clients with Revenue: {clients_with_revenue}")
print(f"   Clients without Revenue: {clients_no_revenue}")

print()
