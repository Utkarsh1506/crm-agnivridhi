import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','agnivridhi_crm.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

User = get_user_model()

USERNAME = 'sales1'
PASSWORD = 'test123'

try:
    u = User.objects.get(username=USERNAME)
    u.set_password(PASSWORD)
    u.save()
    print(f"Set password for {USERNAME}")
except User.DoesNotExist:
    print(f"User {USERNAME} does not exist")
    raise SystemExit(1)

c = Client()
# Ensure test client uses local host to avoid DisallowedHost
c.defaults['HTTP_HOST'] = '127.0.0.1:8000'
logged_in = c.login(username=USERNAME, password=PASSWORD)
print('LOGIN_OK:', logged_in)

endpoints = [
    ('/dashboard/',),
    ('/dashboard/sales/',),
]

for ep in endpoints:
    url = ep[0]
    resp = c.get(url)
    print(f"GET {url} -> {resp.status_code}")

# Named URL checks
named_urls = [
    ('bookings:sales_bookings_list', []),
    ('applications:sales_applications_list', []),
]

for name, args in named_urls:
    try:
        path = reverse(name, args=args)
        resp = c.get(path)
        print(f"GET {path} (named {name}) -> {resp.status_code}")
    except Exception as e:
        print(f"Error resolving or getting named url {name}: {e}")

# Get a sample booking assigned to this user
from bookings.models import Booking
b = Booking.objects.filter(assigned_to__username=USERNAME).first()
if not b:
    print('No booking found assigned to', USERNAME)
else:
    print('Sample booking id:', b.id, 'booking_id:', getattr(b,'booking_id',None))
    # resolve record_payment URL using reverse
    try:
        rp = reverse('accounts:record_payment', args=[b.id])
        r = c.get(rp)
        print(f"GET {rp} -> {r.status_code}")
    except Exception as e:
        print('Error resolving or requesting record_payment URL:', e)

print('Smoke checks complete')
