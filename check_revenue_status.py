import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("\n" + "="*140)
print("CLIENT REVENUE STATUS - DETAILED BREAKDOWN")
print("="*140 + "\n")

print(f"{'ID':<3} {'Client Name':<35} {'Pitched':<12} {'Total+GST':<12} {'Received':<12} {'Pending':<12} {'Status':<15} {'% Received':<10}")
print("-"*140)

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
    
    # Determine status
    if total_with_gst == 0:
        status = "NO REVENUE"
        pct_received = 0
    elif received == 0:
        status = "UNPAID"
        pct_received = 0
    elif received >= total_with_gst:
        status = "PAID"
        pct_received = 100
    else:
        status = "PARTIAL PAID"
        pct_received = (received / total_with_gst * 100) if total_with_gst > 0 else 0
    
    print(f"{row['id']:<3} {row['company_name'][:34]:<35} ₹{pitched:<10} ₹{total_with_gst:<10} ₹{received:<10} ₹{pending:<10} {status:<15} {pct_received:<9.1f}%")

print("-"*140)

# Summary stats
cursor.execute("""
    SELECT 
        COUNT(*) as total,
        COUNT(CASE WHEN total_with_gst > 0 AND received_amount >= total_with_gst THEN 1 END) as paid,
        COUNT(CASE WHEN total_with_gst > 0 AND received_amount > 0 AND received_amount < total_with_gst THEN 1 END) as partial,
        COUNT(CASE WHEN total_with_gst > 0 AND received_amount = 0 THEN 1 END) as unpaid,
        COUNT(CASE WHEN total_with_gst = 0 THEN 1 END) as no_revenue
    FROM clients_client
""")

stats = cursor.fetchone()

print(f"\n📊 STATUS BREAKDOWN:")
print(f"   Total Clients: {stats['total']}")
print(f"   ✅ PAID: {stats['paid']}")
print(f"   🟡 PARTIAL PAID: {stats['partial']}")
print(f"   ❌ UNPAID: {stats['unpaid']}")
print(f"   ⚪ NO REVENUE: {stats['no_revenue']}")

print("\n" + "="*140)

conn.close()
