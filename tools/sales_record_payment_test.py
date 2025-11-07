from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from bookings.models import Booking
from payments.models import Payment

USERNAME='sales1'
PASSWORD='test123'

User=get_user_model()
try:
    u=User.objects.get(username=USERNAME)
except User.DoesNotExist:
    print('sales1 not found')
    raise SystemExit(1)

c=Client()
# Ensure host to avoid DisallowedHost
c.defaults['HTTP_HOST']='127.0.0.1:8000'
if not c.login(username=USERNAME,password=PASSWORD):
    print('login failed')
    raise SystemExit(1)

b=Booking.objects.filter(assigned_to__username=USERNAME).first()
if not b:
    print('no booking for user')
    raise SystemExit(1)

rp=reverse('accounts:record_payment', args=[b.id])
print('POSTing to', rp)
resp=c.post(rp, {'amount':'5000','payment_method':'UPI','reference_id':'TEST-POST-1','notes':'automated test'})
print('POST status:', resp.status_code)

payments=Payment.objects.filter(booking=b)
print('Payments for booking:', payments.count())
for p in payments:
    print('- id', p.id, 'amount', p.amount, 'status', p.status, 'received_by', getattr(p,'received_by',None))

print('done')
