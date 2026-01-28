import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Check for agreements tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'agreements%'")
tables = cursor.fetchall()

print("Agreements Tables:")
for table in tables:
    print(f"  ✓ {table[0]}")

# Get agreement table schema
if tables:
    cursor.execute("PRAGMA table_info(agreements_agreement)")
    columns = cursor.fetchall()
    print(f"\nAgreement Model Fields ({len(columns)} columns):")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")

conn.close()
