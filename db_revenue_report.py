import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("\n" + "="*120)
print("ALL CLIENTS REVENUE DATA FROM DATABASE")
print("="*120 + "\n")

print(f"{'ID':<3} {'Client Name':<40} {'Pitched':<12} {'GST%':<7} {'GST Amt':<12} {'Total+GST':<12} {'Received':<12} {'Pending':<12}")
print("-"*120)

cursor.execute("""
    SELECT id, company_name, total_pitched_amount, gst_percentage, gst_amount, total_with_gst, received_amount, pending_amount 
    FROM clients_client 
    ORDER BY id
""")

rows = cursor.fetchall()

for row in rows:
    print(f"{row['id']:<3} {row['company_name'][:39]:<40} ₹{float(row['total_pitched_amount'] or 0):<10} {float(row['gst_percentage'] or 0):<6.1f}% ₹{float(row['gst_amount'] or 0):<10} ₹{float(row['total_with_gst'] or 0):<10} ₹{float(row['received_amount'] or 0):<10} ₹{float(row['pending_amount'] or 0):<10}")

print("-"*120)

# Calculate totals
cursor.execute("""
    SELECT 
        COUNT(*) as count,
        SUM(total_pitched_amount) as total_pitched,
        SUM(gst_amount) as total_gst,
        SUM(total_with_gst) as total_with_gst,
        SUM(received_amount) as total_received,
        SUM(pending_amount) as total_pending
    FROM clients_client
""")

totals = cursor.fetchone()

print(f"{'TOTAL':<3} {'':<40} ₹{float(totals['total_pitched'] or 0):<10} {'AVG':<6}  ₹{float(totals['total_gst'] or 0):<10} ₹{float(totals['total_with_gst'] or 0):<10} ₹{float(totals['total_received'] or 0):<10} ₹{float(totals['total_pending'] or 0):<10}")
print("="*120)

print(f"\n📊 SUMMARY:")
print(f"   Total Clients: {totals['count']}")
print(f"   Total Pitched Amount: ₹{float(totals['total_pitched'] or 0)}")
print(f"   Total GST: ₹{float(totals['total_gst'] or 0)}")
print(f"   Total with GST: ₹{float(totals['total_with_gst'] or 0)}")
print(f"   Total Received: ₹{float(totals['total_received'] or 0)}")
print(f"   Total Pending: ₹{float(totals['total_pending'] or 0)}")

# Clients breakdown
cursor.execute("""
    SELECT 
        COUNT(CASE WHEN total_pitched_amount > 0 THEN 1 END) as with_revenue,
        COUNT(CASE WHEN total_pitched_amount = 0 THEN 1 END) as without_revenue
    FROM clients_client
""")

breakdown = cursor.fetchone()

print(f"\n👥 CLIENT BREAKDOWN:")
print(f"   Clients with Revenue: {breakdown['with_revenue']}")
print(f"   Clients without Revenue: {breakdown['without_revenue']}")

print()

conn.close()
