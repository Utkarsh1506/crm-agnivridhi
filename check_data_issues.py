import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("\n" + "="*160)
print("CHECKING CLIENTS WITH MISMATCHED STATUS")
print("="*160 + "\n")

print(f"{'ID':<3} {'Client Name':<35} {'Pitched':<12} {'Total+GST':<12} {'Received':<12} {'Pending':<12} {'Status (Method)':<15} {'Issue':<20}")
print("-"*160)

cursor.execute("""
    SELECT id, company_name, total_pitched_amount, gst_percentage, gst_amount, total_with_gst, received_amount, pending_amount 
    FROM clients_client 
    ORDER BY id
""")

rows = cursor.fetchall()

for row in rows:
    pitched = float(row['total_pitched_amount'] or 0)
    total_with_gst = float(row['total_with_gst'] or 0)
    received = float(row['received_amount'] or 0)
    pending = float(row['pending_amount'] or 0)
    
    # Determine status using get_payment_status logic
    if total_with_gst == 0:
        status = "NO_REVENUE"
    elif received == 0:
        status = "UNPAID"
    elif received >= total_with_gst:
        status = "PAID"
    else:
        status = "PARTIAL"
    
    # Check for issues
    issue = ""
    if total_with_gst > 0 and pitched == 0:
        issue = "❌ GST but no pitched"
    elif total_with_gst == 0 and (pitched > 0 or received > 0):
        issue = "❌ Data exists but 0 total"
    elif total_with_gst > 0 and received == 0 and status == "PAID":
        issue = "❌ Shows PAID but ₹0 received"
    
    if issue or total_with_gst > 0:
        print(f"{row['id']:<3} {row['company_name'][:34]:<35} ₹{pitched:<10} ₹{total_with_gst:<10} ₹{received:<10} ₹{pending:<10} {status:<15} {issue:<20}")

print("\n" + "="*160)

# Find specific issue: total_with_gst = 0 but has other data
print("\n🔍 ISSUE 1: Clients with ₹0 total_with_gst but have pitched amount or received amount:")
print("-"*160)

cursor.execute("""
    SELECT id, company_name, total_pitched_amount, total_with_gst, received_amount
    FROM clients_client 
    WHERE total_with_gst = 0 AND (total_pitched_amount > 0 OR received_amount > 0)
    ORDER BY id
""")

broken_clients = cursor.fetchall()
if broken_clients:
    for row in broken_clients:
        print(f"ID {row['id']}: {row['company_name']} - Pitched: ₹{row['total_pitched_amount']}, Received: ₹{row['received_amount']}, Total+GST: ₹{row['total_with_gst']}")
else:
    print("✅ None found - all data is consistent")

print("\n" + "="*160)

conn.close()
