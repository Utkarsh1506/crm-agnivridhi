from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Invoice
from .forms import InvoiceForm
from .utils import generate_invoice_number, amount_to_words


@login_required
def sales_invoice_list(request):
    """
    Sales user ke liye: uske banaye huye saare invoices/proformas.
    """
    invoices = Invoice.objects.filter(created_by=request.user).select_related("client")
    return render(request, "invoices/sales_invoice_list.html", {"invoices": invoices})


@login_required
def sales_invoice_create(request):
    """
    Manual invoice/proforma create form.
    """
    if request.method == "POST":
        form = InvoiceForm(request.POST, user=request.user)
        if form.is_valid():
            inv: Invoice = form.save(commit=False)

            inv.created_by = request.user
            inv.invoice_number = generate_invoice_number(inv.invoice_type)

            qty = form.cleaned_data['quantity']
            rate = form.cleaned_data['rate']
            gst_rate = form.cleaned_data['gst_rate']

            amount = qty * rate
            igst_amount = amount * gst_rate / Decimal('100')

            inv.amount = amount
            inv.igst_amount = igst_amount
            inv.total_amount = amount + igst_amount

            if not inv.due_date:
                inv.due_date = inv.issue_date + timezone.timedelta(days=7)

            inv.status = 'final'
            inv.save()

            # PDF ki jagah abhi HTML invoice page show karenge
            return redirect("invoices:sales_invoice_pdf", pk=inv.pk)
    else:
        form = InvoiceForm(user=request.user)

    return render(request, "invoices/sales_invoice_form.html", {"form": form})


@login_required
def sales_invoice_pdf(request, pk):
    """
    Abhi yeh sirf HTML invoice page return karega (Proforma format me).
    Baad me PDF lib add karke same template ko PDF me convert kar sakte ho.
    """
    invoice = get_object_or_404(Invoice, pk=pk, created_by=request.user)

    amount_words = amount_to_words(invoice.total_amount)
    tax_words = amount_to_words(invoice.igst_amount)

    context = {
        "invoice": invoice,

        # Client details
        "client_gstin": invoice.client.gst_number or "",
        "client_pan": invoice.client.pan_number or "",
        "client_address_line1": invoice.client.address_line1 or "",
        "client_address_line2": invoice.client.address_line2 or "",
        "client_city": invoice.client.city or "",
        "client_state": invoice.client.state or "",
        "client_pincode": invoice.client.pincode or "",
        "client_email": invoice.client.contact_email,
        "client_phone": invoice.client.contact_phone,

        # Supply info
        "place_of_supply": invoice.place_of_supply or invoice.client.state or "Maharashtra",
        "place_of_supply_code": invoice.place_of_supply_code or "27",

        "igst_rate": invoice.gst_rate,
        "amount_in_words": amount_words,
        "tax_amount_in_words": tax_words,
    }

    # Sirf HTML render kar rahe hain
    html_string = render_to_string("invoices/proforma_invoice_pdf.html", context)
    return HttpResponse(html_string)
