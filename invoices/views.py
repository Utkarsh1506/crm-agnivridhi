from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseServerError
import logging
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta

from accounts.views import sales_required, manager_required, admin_required
from .models import Invoice
from .forms import InvoiceForm

logger = logging.getLogger(__name__)
from clients.models import Client


def generate_invoice_number(invoice_type):
    """Generate unique invoice number"""
    prefix = 'PI' if invoice_type == 'proforma' else 'INV'
    today = timezone.now().strftime('%Y%m%d')
    
    last = Invoice.objects.filter(invoice_number__startswith=f"{prefix}-{today}").order_by('-invoice_number').first()
    if last:
        try:
            last_seq = int(last.invoice_number.split('-')[-1])
            seq = last_seq + 1
        except:
            seq = 1
    else:
        seq = 1
    
    return f"{prefix}-{today}-{seq:03d}"


def calculate_invoice_amounts(form_data):
    """Calculate taxable, GST, and total amounts"""
    qty = form_data['quantity']
    rate = form_data['rate']
    gst_rate = form_data['gst_rate']
    place = form_data['place_of_supply'].strip().lower()
    
    taxable = qty * rate
    company_state = 'maharashtra'  # Your company state
    
    if place == company_state:
        # Intra-state: CGST + SGST
        half_gst = gst_rate / Decimal('2')
        cgst = taxable * half_gst / Decimal('100')
        sgst = taxable * half_gst / Decimal('100')
        igst = Decimal('0.00')
    else:
        # Inter-state: IGST
        igst = taxable * gst_rate / Decimal('100')
        cgst = Decimal('0.00')
        sgst = Decimal('0.00')
    
    total = taxable + cgst + sgst + igst
    
    return {
        'taxable_amount': taxable,
        'cgst_amount': cgst,
        'sgst_amount': sgst,
        'igst_amount': igst,
        'total_amount': total,
    }


# ============= SALES VIEWS =============

@sales_required
def sales_invoice_list(request):
    """Sales invoice list with client filter and logging"""
    from django.db import models as django_models
    from django.db import connection
    from django.db.utils import OperationalError, ProgrammingError
    
    # Check if tax columns exist before querying
    try:
        with connection.cursor() as cursor:
            if connection.vendor == 'mysql':
                cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'invoices_invoice' AND column_name = 'taxable_amount'")
                has_tax_cols = cursor.fetchone() is not None
            else:
                has_tax_cols = True  # Assume SQLite has columns
    except Exception:
        has_tax_cols = False
    
    if not has_tax_cols:
        # Graceful message if migration not run yet
        return render(request, 'invoices/sales_list.html', {
            'invoices': [],
            'clients': [],
            'selected_client_id': None,
            'migration_pending': True,
        })
    
    try:
        clients = Client.objects.filter(
            django_models.Q(assigned_sales=request.user) | django_models.Q(created_by=request.user),
            is_approved=True
        ).order_by('company_name')
        invoices = Invoice.objects.filter(created_by=request.user)
        client_id = request.GET.get('client')
        if client_id:
            try:
                invoices = invoices.filter(client_id=int(client_id))
            except (ValueError, TypeError):
                logger.warning("Sales invalid client_id '%s' user=%s", client_id, request.user.pk)
        invoices = invoices.select_related('client').order_by('-created_at')
        selected_client = int(client_id) if client_id and client_id.isdigit() else None
        return render(request, 'invoices/sales_list.html', {
            'invoices': invoices,
            'clients': clients,
            'selected_client_id': selected_client,
        })
    except (OperationalError, ProgrammingError) as e:
        # Database schema issue - show migration pending
        logger.error("Sales invoice DB error: %s user=%s", str(e), getattr(request.user, 'pk', 'anon'))
        return render(request, 'invoices/sales_list.html', {
            'invoices': [],
            'clients': [],
            'selected_client_id': None,
            'migration_pending': True,
        })
    except Exception:
        logger.exception("Sales invoice list error user=%s", getattr(request.user, 'pk', 'anon'))
        return HttpResponseServerError("Temporary error loading invoices. Please retry.")


@sales_required
def sales_invoice_create(request):
    """Create invoice"""
    from django.db import connection
    from django.db.utils import OperationalError, ProgrammingError
    
    # Check if table schema is ready
    try:
        with connection.cursor() as cursor:
            if connection.vendor == 'mysql':
                cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'invoices_invoice' AND column_name = 'taxable_amount'")
                has_tax_cols = cursor.fetchone() is not None
            else:
                has_tax_cols = True
    except Exception:
        has_tax_cols = False
    
    if not has_tax_cols:
        messages.warning(request, 'Invoice feature requires database migration. Please contact administrator.')
        return redirect('invoices:sales_invoice_list')
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                invoice = form.save(commit=False)
                invoice.created_by = request.user
                invoice.invoice_number = generate_invoice_number(invoice.invoice_type)
                
                # Calculate amounts
                amounts = calculate_invoice_amounts(form.cleaned_data)
                for key, value in amounts.items():
                    setattr(invoice, key, value)
                
                # Set due date if not provided
                if not invoice.due_date:
                    invoice.due_date = invoice.issue_date + timedelta(days=15)
                
                invoice.save()
                messages.success(request, f'Invoice {invoice.invoice_number} created successfully!')
                return redirect('invoices:sales_invoice_pdf', pk=invoice.pk)
            except (OperationalError, ProgrammingError) as e:
                logger.error("Sales invoice creation DB error: %s, user=%s", str(e), request.user.pk)
                messages.error(request, 'Database error. Please contact administrator to run migrations.')
                return redirect('invoices:sales_invoice_list')
            except Exception as e:
                logger.exception("Sales invoice creation failed: user=%s", request.user.pk)
                messages.error(request, f'Error creating invoice: {str(e)}')
                return redirect('invoices:sales_invoice_list')
        else:
            logger.warning("Sales invoice form invalid: %s, user=%s", form.errors, request.user.pk)
    else:
        form = InvoiceForm(user=request.user)
    
    return render(request, 'invoices/sales_form.html', {'form': form})


@sales_required
def sales_invoice_pdf(request, pk):
    """View/Download invoice PDF"""
    invoice = get_object_or_404(Invoice, pk=pk, created_by=request.user)
    
    # Check if download requested
    if request.GET.get('download') == '1':
        from django.http import HttpResponse
        from .pdf_utils import generate_invoice_pdf
        
        # Generate PDF using ReportLab
        pdf_buffer = generate_invoice_pdf(invoice)
        
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{invoice.invoice_number}.pdf"'
        return response
    
    return render(request, 'invoices/invoice_pdf.html', {'invoice': invoice})


# ============= MANAGER VIEWS =============

@manager_required
def manager_invoice_list(request):
    """Manager invoice list with logging"""
    from django.db import models as django_models
    from django.db import connection
    from django.db.utils import OperationalError, ProgrammingError
    
    # Check if tax columns exist before querying
    try:
        with connection.cursor() as cursor:
            if connection.vendor == 'mysql':
                cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'invoices_invoice' AND column_name = 'taxable_amount'")
                has_tax_cols = cursor.fetchone() is not None
            else:
                has_tax_cols = True
    except Exception:
        has_tax_cols = False
    
    if not has_tax_cols:
        return render(request, 'invoices/manager_list.html', {
            'invoices': [],
            'clients': [],
            'selected_client_id': None,
            'migration_pending': True,
        })
    
    try:
        clients = Client.objects.filter(
            django_models.Q(assigned_sales__manager=request.user) |
            django_models.Q(assigned_manager=request.user) |
            django_models.Q(created_by=request.user),
            is_approved=True
        ).distinct().order_by('company_name')
        team_sales_rel = getattr(request.user, 'team_members', None)
        team_sales = team_sales_rel.all() if team_sales_rel else []
        invoices = Invoice.objects.filter(
            django_models.Q(created_by=request.user) |
            django_models.Q(created_by__in=team_sales)
        )
        client_id = request.GET.get('client')
        if client_id:
            try:
                invoices = invoices.filter(client_id=int(client_id))
            except (ValueError, TypeError):
                logger.warning("Manager invalid client_id '%s' user=%s", client_id, request.user.pk)
        invoices = invoices.select_related('client', 'created_by').order_by('-created_at')
        selected_client = int(client_id) if client_id and client_id.isdigit() else None
        return render(request, 'invoices/manager_list.html', {
            'invoices': invoices,
            'clients': clients,
            'selected_client_id': selected_client,
        })
    except (OperationalError, ProgrammingError) as e:
        logger.error("Manager invoice DB error: %s user=%s", str(e), getattr(request.user, 'pk', 'anon'))
        return render(request, 'invoices/manager_list.html', {
            'invoices': [],
            'clients': [],
            'selected_client_id': None,
            'migration_pending': True,
        })
    except Exception:
        logger.exception("Manager invoice list error user=%s", getattr(request.user, 'pk', 'anon'))
        return HttpResponseServerError("Temporary error loading invoices. Please retry.")


@manager_required
def manager_invoice_create(request):
    """Manager create invoice"""
    from django.db import connection
    from django.db.utils import OperationalError, ProgrammingError
    
    # Check if table schema is ready
    try:
        with connection.cursor() as cursor:
            if connection.vendor == 'mysql':
                cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'invoices_invoice' AND column_name = 'taxable_amount'")
                has_tax_cols = cursor.fetchone() is not None
            else:
                has_tax_cols = True
    except Exception:
        has_tax_cols = False
    
    if not has_tax_cols:
        messages.warning(request, 'Invoice feature requires database migration. Please contact administrator.')
        return redirect('invoices:manager_invoice_list')
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                invoice = form.save(commit=False)
                invoice.created_by = request.user
                invoice.invoice_number = generate_invoice_number(invoice.invoice_type)
                
                amounts = calculate_invoice_amounts(form.cleaned_data)
                for key, value in amounts.items():
                    setattr(invoice, key, value)
                
                if not invoice.due_date:
                    invoice.due_date = invoice.issue_date + timedelta(days=15)
                
                invoice.save()
                messages.success(request, f'Invoice {invoice.invoice_number} created!')
                return redirect('invoices:manager_invoice_pdf', pk=invoice.pk)
            except (OperationalError, ProgrammingError) as e:
                logger.error("Manager invoice creation DB error: %s, user=%s", str(e), request.user.pk)
                messages.error(request, 'Database error. Please contact administrator to run migrations.')
                return redirect('invoices:manager_invoice_list')
            except Exception as e:
                logger.exception("Manager invoice creation failed: user=%s", request.user.pk)
                messages.error(request, f'Error creating invoice: {str(e)}')
                return redirect('invoices:manager_invoice_list')
        else:
            logger.warning("Manager invoice form invalid: %s, user=%s", form.errors, request.user.pk)
    else:
        form = InvoiceForm(user=request.user)
    
    return render(request, 'invoices/manager_form.html', {'form': form})


@manager_required
def manager_invoice_pdf(request, pk):
    """Manager view invoice PDF"""
    from django.db import models as django_models
    team_sales = request.user.team_members.all()
    invoice = get_object_or_404(
        Invoice,
        django_models.Q(created_by=request.user) | django_models.Q(created_by__in=team_sales),
        pk=pk
    )
    
    if request.GET.get('download') == '1':
        from django.http import HttpResponse
        from .pdf_utils import generate_invoice_pdf
        
        pdf_buffer = generate_invoice_pdf(invoice)
        
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{invoice.invoice_number}.pdf"'
        return response
    
    return render(request, 'invoices/invoice_pdf.html', {'invoice': invoice})
def admin_invoice_list(request):
    """Admin/Owner invoice list with logging"""
    from django.db import connection
    from django.db.utils import OperationalError, ProgrammingError
    
    # Check if tax columns exist before querying
    try:
        with connection.cursor() as cursor:
            if connection.vendor == 'mysql':
                cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'invoices_invoice' AND column_name = 'taxable_amount'")
                has_tax_cols = cursor.fetchone() is not None
            else:
                has_tax_cols = True
    except Exception:
        has_tax_cols = False
    
    if not has_tax_cols:
        return render(request, 'invoices/admin_list.html', {
            'invoices': [],
            'clients': [],
            'selected_client_id': None,
            'migration_pending': True,
        })
    
    try:
        clients = Client.objects.filter(is_approved=True).order_by('company_name')
        invoices = Invoice.objects.all()
        client_id = request.GET.get('client')
        if client_id:
            try:
                invoices = invoices.filter(client_id=int(client_id))
            except (ValueError, TypeError):
                logger.warning("Admin invalid client_id '%s' user=%s", client_id, request.user.pk)
        invoices = invoices.select_related('client', 'created_by').order_by('-created_at')
        selected_client = int(client_id) if client_id and client_id.isdigit() else None
        return render(request, 'invoices/admin_list.html', {
            'invoices': invoices,
            'clients': clients,
            'selected_client_id': selected_client,
        })
    except (OperationalError, ProgrammingError) as e:
        logger.error("Admin invoice DB error: %s user=%s", str(e), getattr(request.user, 'pk', 'anon'))
        return render(request, 'invoices/admin_list.html', {
            'invoices': [],
            'clients': [],
            'selected_client_id': None,
            'migration_pending': True,
        })
    except Exception:
        logger.exception("Admin invoice list error user=%s", getattr(request.user, 'pk', 'anon'))
        return HttpResponseServerError("Temporary error loading invoices. Please retry.")


@admin_required
def admin_invoice_create(request):
    """Admin/Owner create invoice"""
    from django.db import connection
    from django.db.utils import OperationalError, ProgrammingError
    
    # Check if table schema is ready
    try:
        with connection.cursor() as cursor:
            if connection.vendor == 'mysql':
                cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'invoices_invoice' AND column_name = 'taxable_amount'")
                has_tax_cols = cursor.fetchone() is not None
            else:
                has_tax_cols = True
    except Exception:
        has_tax_cols = False
    
    if not has_tax_cols:
        messages.warning(request, 'Invoice feature requires database migration. Please contact administrator.')
        return redirect('invoices:admin_invoice_list')
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                invoice = form.save(commit=False)
                invoice.created_by = request.user
                invoice.invoice_number = generate_invoice_number(invoice.invoice_type)
                
                amounts = calculate_invoice_amounts(form.cleaned_data)
                for key, value in amounts.items():
                    setattr(invoice, key, value)
                
                if not invoice.due_date:
                    invoice.due_date = invoice.issue_date + timedelta(days=15)
                
                invoice.save()
                messages.success(request, f'Invoice {invoice.invoice_number} created!')
                return redirect('invoices:admin_invoice_pdf', pk=invoice.pk)
            except (OperationalError, ProgrammingError) as e:
                logger.error("Admin invoice creation DB error: %s, user=%s", str(e), request.user.pk)
                messages.error(request, 'Database error. Please contact administrator to run migrations.')
                return redirect('invoices:admin_invoice_list')
            except Exception as e:
                logger.exception("Admin invoice creation failed: user=%s", request.user.pk)
                messages.error(request, f'Error creating invoice: {str(e)}')
                return redirect('invoices:admin_invoice_list')
        else:
            logger.warning("Admin invoice form invalid: %s, user=%s", form.errors, request.user.pk)
    else:
        form = InvoiceForm(user=request.user)
    
    return render(request, 'invoices/admin_form.html', {'form': form})


@admin_required
def admin_invoice_pdf(request, pk):
    """Admin/Owner view invoice PDF"""
    invoice = get_object_or_404(Invoice, pk=pk)
    
    if request.GET.get('download') == '1':
        from django.http import HttpResponse
        from django.template.loader import render_to_string
        from xhtml2pdf import pisa
        from io import BytesIO
        
        html_content = render_to_string('invoices/invoice_pdf_print.html', {'invoice': invoice, 'request': request})
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_content.encode('UTF-8')), result)
        
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename=\"{invoice.invoice_number}.pdf\"'
            return response
        else:
            return HttpResponse('Error generating PDF', status=500)
    
    return render(request, 'invoices/invoice_pdf.html', {'invoice': invoice})
