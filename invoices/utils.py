import datetime
from decimal import Decimal
from num2words import num2words
from .models import Invoice


def generate_invoice_number(invoice_type='proforma'):
    prefix = "AGNI-PROF" if invoice_type == 'proforma' else "AGNI-INV"
    year = datetime.date.today().year
    count = Invoice.objects.filter(
        invoice_type=invoice_type,
        issue_date__year=year
    ).count() + 1
    return f"{prefix}/{year}/{str(count).zfill(4)}"


def amount_to_words(amount: Decimal) -> str:
    """
    Convert numeric amount to words (Indian style).
    """
    # simple version: round to rupees
    rupees = int(amount.quantize(Decimal('1')))
    words = num2words(rupees, lang='en_IN')
    return words.upper()
