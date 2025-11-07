"""
Test Manager and Sales Dashboards with Team Data
"""
from django.test import Client as TestClient
from accounts.models import User

c = TestClient()
c.defaults['HTTP_HOST'] = '127.0.0.1:8000'

print("\n" + "="*80)
print("TESTING MANAGER & SALES DASHBOARDS")
print("="*80)

# Test Manager 1 Login
print("\n[1] Testing Manager1 (Rajesh Kumar)...")
manager1 = User.objects.get(username='manager1')
c.force_login(manager1)

resp = c.get('/dashboard/manager/')
print(f"  Dashboard access: {resp.status_code} {'✓' if resp.status_code == 200 else '✗'}")

content = resp.content.decode('utf-8')
print(f"  Manager name in page: {'✓' if 'Rajesh' in content else '✗'}")

# Check if team data is visible
team = User.objects.filter(role='SALES', manager=manager1)
print(f"  Team size: {team.count()} sales employees")
for sales in team:
    is_visible = sales.get_full_name() in content
    print(f"    - {sales.get_full_name()}: {'✓ visible' if is_visible else '✗ not visible'}")

# Test Sales Employee under Manager 1
print("\n[2] Testing sales2 (Neha Gupta) under Manager1...")
sales2 = User.objects.get(username='sales2')
c.force_login(sales2)

resp = c.get('/dashboard/sales/')
print(f"  Dashboard access: {resp.status_code} {'✓' if resp.status_code == 200 else '✗'}")

content = resp.content.decode('utf-8')
print(f"  Sales name in page: {'✓' if 'Neha' in content else '✗'}")
print(f"  Reports to: {sales2.manager.get_full_name() if sales2.manager else 'None'}")

# Test Manager 2 Team
print("\n[3] Testing Manager2 (Priya Sharma)...")
manager2 = User.objects.get(username='manager2')
c.force_login(manager2)

resp = c.get('/dashboard/manager/')
print(f"  Dashboard access: {resp.status_code} {'✓' if resp.status_code == 200 else '✗'}")

team2 = User.objects.filter(role='SALES', manager=manager2)
print(f"  Team size: {team2.count()} sales employees")
print(f"  Team members:")
for sales in team2:
    print(f"    - {sales.get_full_name()} ({sales.username})")

# Test Sales Employee under Manager 2
print("\n[4] Testing sales5 (Vikram Reddy) under Manager2...")
sales5 = User.objects.get(username='sales5')
c.force_login(sales5)

resp = c.get('/dashboard/sales/')
print(f"  Dashboard access: {resp.status_code} {'✓' if resp.status_code == 200 else '✗'}")
print(f"  Reports to: {sales5.manager.get_full_name() if sales5.manager else 'None'}")

# Test Data Isolation - sales5 shouldn't see manager1's team data
c.force_login(sales5)
resp = c.get('/dashboard/sales/')
content = resp.content.decode('utf-8')

# Check if sales1's client (Test Co Pvt Ltd) is NOT visible to sales5
print("\n[5] Data Isolation Check...")
print(f"  sales5 can see sales1's client 'Test Co Pvt Ltd': {'✗ LEAK!' if 'Test Co Pvt Ltd' in content else '✓ ISOLATED'}")

# Manager cross-access check
print("\n[6] Manager Dashboard Permission Check...")
c.force_login(sales5)
resp = c.get('/dashboard/manager/')
print(f"  sales5 accessing manager dashboard: {resp.status_code} {'✓ BLOCKED' if resp.status_code in [302, 403] else '✗ ALLOWED'}")

print("\n" + "="*80)
print("✅ HIERARCHY TESTING COMPLETE")
print("="*80)
print("\n📊 Structure:")
for i, mgr in enumerate(User.objects.filter(role='MANAGER').order_by('username'), 1):
    team = User.objects.filter(role='SALES', manager=mgr)
    print(f"  {i}. {mgr.get_full_name()} → {team.count()} sales employees")
print("\n")
