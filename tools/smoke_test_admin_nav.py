"""Quick smoke test for admin dashboard nav links.

Run via: python manage.py shell -c "exec(open('tools/smoke_test_admin_nav.py').read())"
Prints status codes for each nav path while logged in as admin.
"""
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

User = get_user_model()

USERNAME = 'admin'
PASSWORD = 'test123'

try:
    u = User.objects.get(username=USERNAME)
    # ensure password is known
    u.set_password(PASSWORD)
    u.save()
except User.DoesNotExist:
    print('Admin user not found.')
    raise SystemExit(1)

c = Client()
c.defaults['HTTP_HOST'] = '127.0.0.1:8000'
if not c.login(username=USERNAME, password=PASSWORD):
    print('Login failed')
    raise SystemExit(1)

paths = {
    'Clients': reverse('clients:manager_clients_list'),
    'Bookings': reverse('bookings:team_bookings_list'),
    'Applications': reverse('applications:team_applications_list'),
    'Schemes': reverse('schemes:scheme_list'),
    'Payments': reverse('payments:team_payments_list'),
    'Edit Requests': reverse('edit_requests:manager_edit_requests'),
    'Documents': reverse('documents:team_documents_list'),
    'Users': reverse('accounts:users_list'),
    'Notifications': reverse('notifications:notification_list'),
}

results = []
for label, url in paths.items():
    resp = c.get(url)
    results.append((label, url, resp.status_code))

print('--- Admin Nav Smoke Test ---')
for label, url, code in results:
    print(f"{label:15} {code}  {url}")

failures = [r for r in results if r[2] != 200]
if failures:
    print('\nFailures:')
    for f in failures:
        print(f" - {f[0]} ({f[1]}) -> {f[2]}")
    raise SystemExit(2)
else:
    print('\nAll nav links returned 200.')