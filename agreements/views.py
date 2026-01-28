from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import render_to_string
from django.db.models import Q
import logging

from accounts.views import sales_required, manager_required, admin_required
from .models import Agreement
from .forms import AgreementForm
from clients.models import Client

logger = logging.getLogger(__name__)


def generate_agreement_number(agreement_type):
    """Generate unique agreement number"""
    prefix = 'FA' if agreement_type == 'funding' else 'WA'  # FA = Funding Agreement, WA = Website Agreement
    today = timezone.now().strftime('%Y%m%d')
    
    last = Agreement.objects.filter(
        agreement_number__startswith=f"{prefix}-{today}"
    ).order_by('-agreement_number').first()
    
    if last:
        try:
            last_seq = int(last.agreement_number.split('-')[-1])
            seq = last_seq + 1
        except:
            seq = 1
    else:
        seq = 1
    
    return f"{prefix}-{today}-{seq:03d}"


# ============= ADMIN/MANAGER/OWNER VIEWS =============

def agreement_list(request):
    """List all agreements for admin/manager/owner"""
    # Check if user is admin, manager, or owner
    if not (request.user.is_authenticated and (request.user.role in ['ADMIN', 'MANAGER'] or request.user.is_owner)):
        return HttpResponseForbidden("Only Admins, Managers, and Owners can access agreements.")
    
    # Admins and owners see all agreements, managers see all agreements
    agreements = Agreement.objects.all().select_related(
        'client', 'employee', 'created_by'
    ).order_by('-created_at')
    
    # Filter by agreement type if specified
    agreement_type = request.GET.get('type')
    if agreement_type in ['funding', 'website']:
        agreements = agreements.filter(agreement_type=agreement_type)
    
    # Filter by client if specified
    client_id = request.GET.get('client')
    if client_id:
        try:
            agreements = agreements.filter(client_id=int(client_id))
        except (ValueError, TypeError):
            logger.warning(f"Invalid client_id {client_id} by user {request.user.pk}")
    
    # Get clients for filter dropdown - show all approved clients for admin/manager/owner
    clients = Client.objects.filter(is_approved=True).order_by('company_name')
    
    context = {
        'agreements': agreements,
        'clients': clients,
        'selected_type': agreement_type,
        'selected_client_id': int(client_id) if client_id and client_id.isdigit() else None,
    }
    
    return render(request, 'agreements/agreement_list.html', context)


def agreement_create(request):
    """Create new agreement - Only for admin, manager, and owner"""
    # Check if user is admin, manager, or owner
    if not (request.user.is_authenticated and (request.user.role in ['ADMIN', 'MANAGER'] or request.user.is_owner)):
        return HttpResponseForbidden("Only Admins, Managers, and Owners can create agreements.")
    
    if request.method == 'POST':
        form = AgreementForm(request.POST, user=request.user)
        if form.is_valid():
            agreement = form.save(commit=False)
            
            # Generate agreement number
            agreement.agreement_number = generate_agreement_number(agreement.agreement_type)
            agreement.created_by = request.user
            
            try:
                agreement.save()
                messages.success(
                    request, 
                    f'Agreement {agreement.agreement_number} created successfully!'
                )
                return redirect('agreements:agreement_detail', pk=agreement.pk)
            except Exception as e:
                logger.error(f"Error creating agreement: {str(e)}", exc_info=True)
                messages.error(request, 'Error creating agreement. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AgreementForm(user=request.user)
    
    return render(request, 'agreements/agreement_form.html', {
        'form': form,
        'title': 'Create Agreement'
    })


def agreement_detail(request, pk):
    """View agreement details"""
    # Check if user is admin, manager, or owner
    if not (request.user.is_authenticated and (request.user.role in ['ADMIN', 'MANAGER'] or request.user.is_owner)):
        return HttpResponseForbidden("Only Admins, Managers, and Owners can view agreements.")
    
    agreement = get_object_or_404(Agreement, pk=pk)
    
    return render(request, 'agreements/agreement_detail.html', {
        'agreement': agreement
    })


def agreement_edit(request, pk):
    """Edit existing agreement"""
    # Check if user is admin, manager, or owner
    if not (request.user.is_authenticated and (request.user.role in ['ADMIN', 'MANAGER'] or request.user.is_owner)):
        return HttpResponseForbidden("Only Admins, Managers, and Owners can edit agreements.")
    
    agreement = get_object_or_404(Agreement, pk=pk)
    
    if request.method == 'POST':
        form = AgreementForm(request.POST, instance=agreement, user=request.user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Agreement updated successfully!')
                return redirect('agreements:agreement_detail', pk=agreement.pk)
            except Exception as e:
                logger.error(f"Error updating agreement: {str(e)}", exc_info=True)
                messages.error(request, 'Error updating agreement. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AgreementForm(instance=agreement, user=request.user)
    
    return render(request, 'agreements/agreement_form.html', {
        'form': form,
        'agreement': agreement,
        'title': 'Edit Agreement'
    })


def agreement_delete(request, pk):
    """Delete agreement"""
    # Check if user is admin, manager, or owner
    if not (request.user.is_authenticated and (request.user.role in ['ADMIN', 'MANAGER'] or request.user.is_owner)):
        return HttpResponseForbidden("Only Admins, Managers, and Owners can delete agreements.")
    
    agreement = get_object_or_404(Agreement, pk=pk)
    
    if request.method == 'POST':
        agreement_number = agreement.agreement_number
        try:
            agreement.delete()
            messages.success(request, f'Agreement {agreement_number} deleted successfully!')
            return redirect('agreements:agreement_list')
        except Exception as e:
            logger.error(f"Error deleting agreement: {str(e)}", exc_info=True)
            messages.error(request, 'Error deleting agreement. Please try again.')
    
    return render(request, 'agreements/agreement_confirm_delete.html', {
        'agreement': agreement
    })


def agreement_pdf(request, pk):
    """Generate and download PDF for agreement"""
    # Check if user is admin, manager, or owner
    if not (request.user.is_authenticated and (request.user.role in ['ADMIN', 'MANAGER'] or request.user.is_owner)):
        return HttpResponseForbidden("Only Admins, Managers, and Owners can download agreement PDFs.")
    
    from xhtml2pdf import pisa
    from io import BytesIO
    
    agreement = get_object_or_404(Agreement, pk=pk)
    
    # Select template based on agreement type
    if agreement.agreement_type == 'funding':
        template_name = 'agreements/pdf/funding_agreement.html'
    else:
        template_name = 'agreements/pdf/website_agreement.html'
    
    # Render HTML
    html_string = render_to_string(template_name, {
        'agreement': agreement,
        'today': timezone.now().date()
    })
    
    # Generate PDF
    try:
        result = BytesIO()
        pdf_status = pisa.CreatePDF(
            BytesIO(html_string.encode('utf-8')),
            result,
            encoding='utf-8'
        )
        
        if pdf_status.err:
            logger.error(f"Error generating PDF: {pdf_status.err}")
            messages.error(request, 'Error generating PDF. Please try again.')
            return redirect('agreements:agreement_detail', pk=pk)
        
        # Create response
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{agreement.agreement_number}.pdf"'
        
        return response
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}", exc_info=True)
        messages.error(request, 'Error generating PDF. Please try again.')
        return redirect('agreements:agreement_detail', pk=pk)


# ============= MANAGER VIEWS =============

@manager_required
def manager_agreement_list(request):
    """List all agreements for managers"""
    agreements = Agreement.objects.all().select_related(
        'client', 'employee', 'created_by'
    ).order_by('-created_at')
    
    # Apply filters
    agreement_type = request.GET.get('type')
    if agreement_type in ['funding', 'website']:
        agreements = agreements.filter(agreement_type=agreement_type)
    
    client_id = request.GET.get('client')
    if client_id:
        try:
            agreements = agreements.filter(client_id=int(client_id))
        except (ValueError, TypeError):
            pass
    
    clients = Client.objects.filter(is_approved=True).order_by('company_name')
    
    context = {
        'agreements': agreements,
        'clients': clients,
        'selected_type': agreement_type,
        'selected_client_id': int(client_id) if client_id and client_id.isdigit() else None,
    }
    
    return render(request, 'agreements/manager_agreement_list.html', context)


# ============= ADMIN VIEWS =============

@admin_required
def admin_agreement_list(request):
    """List all agreements for admin"""
    return manager_agreement_list(request)  # Same functionality for now
