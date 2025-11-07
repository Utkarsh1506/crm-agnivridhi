from django.contrib.auth import get_user_model
from django.test import Client
from payments.models import Payment
from bookings.models import Booking

USERNAME='manager1'
PASSWORD='test123'

User=get_user_model()
try:
    u=User.objects.get(username=USERNAME)
    u.set_password(PASSWORD)
    u.save()
except User.DoesNotExist:
    print('manager1 not found')
    raise SystemExit(1)

c=Client()
# Ensure host to avoid DisallowedHost
c.defaults['HTTP_HOST']='127.0.0.1:8000'
if not c.login(username=USERNAME,password=PASSWORD):
    print('manager login failed')
    raise SystemExit(1)

# pick a pending payment
p=Payment.objects.filter(status='PENDING').first()
if not p:
    print('No PENDING payment found')
    raise SystemExit(1)

url=f"/api/payments/{p.id}/approve/"
print('POST to', url)
resp=c.post(url, {})
print('POST status:', resp.status_code)
# refresh payment
p.refresh_from_db()
print('Payment status now:', p.status)
print('done')
