import datetime
from .models import Invoice

def generate_invoice_number(invoice_type='proforma'):
    prefix = "AGNI-PROF" if invoice_type == 'proforma' else "AGNI-INV"
    year = datetime.date.today().year
    count = Invoice.objects.filter(
        invoice_type=invoice_type,
        issue_date__year=year
    ).count() + 1
    return f"{prefix}/{year}/{str(count).zfill(4)}"
