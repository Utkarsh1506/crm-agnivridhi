from payments.models import Payment
p=Payment.objects.filter(status='PENDING').first()
if not p:
    print('No PENDING payment found')
else:
    p.status='APPROVED'
    p.save()
    print('Payment', p.id, 'set to APPROVED')
