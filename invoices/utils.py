import datetime
from decimal import Decimal
from .models import Invoice

# Try to import num2words, but don't crash if not installed
try:
    from num2words import num2words as _num2words
    HAS_NUM2WORDS = True
except ImportError:
    HAS_NUM2WORDS = False

    def _num2words(amount, lang=None):
        # Fallback: just return the number as string
        return str(amount)


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
    Convert numeric amount to words (Indian style) if num2words available.
    Otherwise just return the rounded amount as string.
    """
    if amount is None:
        return ""

    rupees = int(Decimal(amount).quantize(Decimal('1')))

    if HAS_NUM2WORDS:
        words = _num2words(rupees, lang='en_IN')
    else:
        words = str(rupees)

    return words.upper()
