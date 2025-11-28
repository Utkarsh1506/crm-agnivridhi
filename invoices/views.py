from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone

from weasyprint import HTML

from .models import Invoice
from .forms import InvoiceForm
from .utils import generate_invoice_number
from users.decorators import sales_required  # adjust path if different

# TODO: replace with proper num-to-words lib later
def number_to_words_dummy(amount):
    return str(amount)

@sales_required
def sales_invoice_list(request):
    invoices = Invoice.objects.filter(created_by=request.user).select_related('client')
    return render(request, "invoices/sales_invoice_list.html", {"invoices": invoices})


@sales_required
def sales_invoice_create(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST, user=request.user)
        if form.is_valid():
            inv: Invoice = form.save(commit=False)

            inv.created_by = request.user
            inv.invoice_number = generate_invoice_number(inv.invoice_type)

            # Amount & tax calculations
            qty = form.cleaned_data['quantity']
            rate = form.cleaned_data['rate']
            gst_rate = form.cleaned_data['gst_rate']

            amount = qty * rate   # taxable
            igst_amount = amount * gst_rate / Decimal('100')

            inv.amount = amount
            inv.igst_amount = igst_amount
            inv.total_amount = amount + igst_amount

            if not inv.due_date:
                inv.due_date = inv.issue_date + timezone.timedelta(days=7)

            inv.status = 'final'
            inv.save()

            return redirect("invoices:sales_invoice_pdf", pk=inv.pk)
    else:
        form = InvoiceForm(user=request.user)

    return render(request, "invoices/sales_invoice_form.html", {"form": form})


@sales_required
def sales_invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, created_by=request.user)

    context = {
        "invoice": invoice,
        "place_of_supply": invoice.place_of_supply or "Maharashtra",
        "place_of_supply_code": invoice.place_of_supply_code or "27",
        "igst_rate": invoice.gst_rate,
        "amount_in_words": number_to_words_dummy(invoice.total_amount),
        "tax_amount_in_words": number_to_words_dummy(invoice.igst_amount),
    }

    html_string = render_to_string("invoices/proforma_invoice_pdf.html", context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename=\"{invoice.invoice_number}.pdf\""

    HTML(string=html_string).write_pdf(response)
    return response
