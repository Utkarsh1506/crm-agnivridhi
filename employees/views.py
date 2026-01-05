"""
Employee Views - Backend logic for Employee Identity & Verification System.

Views include:
- Admin/HR: Create, manage, deactivate employees, download ID cards
- Public: Verification page (no login required) with rate limiting
- Audit: Verification logs for security monitoring
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.html import escape
from django.core.paginator import Paginator
from django.db.models import Q
import logging

from accounts.views import role_required
from .models import Employee, EmployeeVerificationLog
from .pdf_generator import EmployeeIDCardPDF
from .utils import get_client_ip

logger = logging.getLogger(__name__)


# ============================================================================
# ADMIN/HR VIEWS - Employee Management (Login Required)
# ============================================================================

@login_required(login_url='accounts:login')
@role_required('SUPERUSER', 'OWNER', 'ADMIN')
def employee_list_view(request):
    """
    List all employees with search and filter.
    Admin/HR only.
    
    Query params:
    - search: Search by name, employee_id, department
    - status: Filter by Active/Inactive
    - page: Pagination
    """
    # Get base queryset
    employees = Employee.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        employees = employees.filter(
            Q(full_name__icontains=search_query) |
            Q(employee_id__icontains=search_query) |
            Q(designation__icontains=search_query) |
            Q(department__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter in ['ACTIVE', 'INACTIVE']:
        employees = employees.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(employees, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'employees': page_obj.object_list,
        'search_query': search_query,
        'status_filter': status_filter,
        'total_count': paginator.count,
    }
    
    return render(request, 'employees/employee_list.html', context)


@login_required(login_url='accounts:login')
@role_required('SUPERUSER', 'OWNER', 'ADMIN')
def employee_create_view(request):
    """
    Create a new employee.
    Admin/HR only.
    """
    if request.method == 'POST':
        try:
            # Create employee from form data
            employee = Employee(
                full_name=request.POST.get('full_name', '').strip(),
                designation=request.POST.get('designation', '').strip(),
                department=request.POST.get('department', '').strip(),
                date_of_joining=request.POST.get('date_of_joining'),
                employee_photo=request.FILES.get('employee_photo'),
                status=request.POST.get('status', 'ACTIVE'),
                created_by=request.user,
            )
            
            # Validate required fields
            if not all([employee.full_name, employee.designation, employee.department, employee.employee_photo]):
                messages.error(request, 'All fields (Name, Designation, Department, Photo) are required.')
                return render(request, 'employees/employee_form.html')
            
            # Save (signals will auto-generate ID, token, QR)
            employee.save()
            
            messages.success(
                request,
                f'Employee {employee.employee_id} ({employee.full_name}) created successfully!'
            )
            return redirect('employees:employee_detail', pk=employee.pk)
        
        except Exception as e:
            logger.error(f"Error creating employee: {str(e)}")
            messages.error(request, f'Error creating employee: {str(e)}')
    
    return render(request, 'employees/employee_form.html')


@login_required(login_url='accounts:login')
@role_required('SUPERUSER', 'OWNER', 'ADMIN')
def employee_detail_view(request, pk):
    """
    View employee details with option to deactivate/reactivate.
    Admin/HR only.
    """
    employee = get_object_or_404(Employee, pk=pk)
    
    context = {
        'employee': employee,
        'barcode_url': employee.barcode.url if employee.barcode else None,
    }
    
    return render(request, 'employees/employee_detail.html', context)


@login_required(login_url='accounts:login')
@role_required('SUPERUSER', 'OWNER', 'ADMIN')
@require_http_methods(['POST'])
def employee_status_toggle_view(request, pk):
    """
    Toggle employee status (Active <-> Inactive).
    Admin/HR only.
    """
    employee = get_object_or_404(Employee, pk=pk)
    
    try:
        if employee.status == 'ACTIVE':
            employee.deactivate()
            messages.success(request, f'Employee {employee.employee_id} deactivated.')
        else:
            employee.reactivate()
            messages.success(request, f'Employee {employee.employee_id} reactivated.')
    
    except Exception as e:
        logger.error(f"Error toggling employee status: {str(e)}")
        messages.error(request, f'Error: {str(e)}')
    
    return redirect('employees:employee_detail', pk=employee.pk)


@login_required(login_url='accounts:login')
@role_required('SUPERUSER', 'OWNER', 'ADMIN')
def employee_download_id_card_view(request, pk):
    """
    Download employee ID card as PDF.
    Admin/HR only.
    """
    employee = get_object_or_404(Employee, pk=pk)
    
    try:
        # Generate PDF
        pdf_file = EmployeeIDCardPDF.generate_id_card_pdf(employee)
        
        # Return as file download
        response = FileResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{employee.employee_id}_ID_Card.pdf"'
        
        logger.info(f"ID card downloaded for employee {employee.employee_id}")
        return response
    
    except Exception as e:
        logger.error(f"Error generating ID card: {str(e)}")
        messages.error(request, f'Error generating ID card: {str(e)}')
        return redirect('employees:employee_detail', pk=employee.pk)


# ============================================================================
# PUBLIC VERIFICATION VIEW - No Login Required (Rate Limited)
# ============================================================================

RATE_LIMIT_KEY = 'employee_verify_'
RATE_LIMIT_REQUESTS = 10  # Max requests per IP
RATE_LIMIT_WINDOW = 3600  # Time window in seconds (1 hour)


def apply_rate_limit(ip_address):
    """
    Check and enforce rate limiting on verification endpoint.
    
    Args:
        ip_address (str): Client IP address
        
    Returns:
        tuple: (is_allowed, remaining_requests, reset_time)
    """
    cache_key = f"{RATE_LIMIT_KEY}{ip_address}"
    
    # Get current count
    request_count = cache.get(cache_key, 0)
    
    if request_count >= RATE_LIMIT_REQUESTS:
        return False, 0, RATE_LIMIT_WINDOW
    
    # Increment count
    cache.set(cache_key, request_count + 1, RATE_LIMIT_WINDOW)
    
    return True, RATE_LIMIT_REQUESTS - (request_count + 1), RATE_LIMIT_WINDOW


@require_http_methods(['GET'])
def employee_verify_public_view(request, employee_id):
    """
    PUBLIC VERIFICATION PAGE - No login required.
    
    Displays employee information after scanning QR code.
    Shows warning if employee is inactive.
    
    Rate limited to prevent abuse.
    
    Security:
    - No personal data in QR code (only verification URL)
    - Read-only display
    - Rate limiting
    - IP logging for audit trail
    """
    try:
        # Get client IP for rate limiting and logging
        client_ip = get_client_ip(request)
        
        # Apply rate limiting
        is_allowed, remaining, reset_time = apply_rate_limit(client_ip)
        if not is_allowed:
            logger.warning(f"Rate limit exceeded for IP {client_ip}")
            return render(
                request,
                'employees/verification_rate_limited.html',
                {'reset_time': reset_time},
                status=429
            )
        
        # Fetch employee by employee_id
        employee = get_object_or_404(Employee, employee_id=employee_id)
        
        # Log verification attempt
        EmployeeVerificationLog.objects.create(
            employee=employee,
            ip_address=client_ip,
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
        )
        
        # Prepare context
        context = {
            'employee': employee,
            'is_active': employee.is_active_employee(),
            'verification_status': 'ACTIVE' if employee.is_active_employee() else 'INACTIVE',
        }
        
        return render(request, 'employees/verification_page.html', context)
    
    except Employee.DoesNotExist:
        logger.warning(f"Verification attempt for non-existent employee: {employee_id}")
        return render(request, 'employees/verification_not_found.html', status=404)
    
    except Exception as e:
        logger.error(f"Error in verification view: {str(e)}")
        return render(request, 'employees/verification_error.html', status=500)


# ============================================================================
# AUDIT & LOGGING VIEWS
# ============================================================================

@login_required(login_url='accounts:login')
@role_required('SUPERUSER', 'OWNER', 'ADMIN')
def employee_verification_logs_view(request, pk):
    """
    View verification logs for a specific employee.
    Shows audit trail of who accessed the verification page.
    Admin/HR only.
    """
    employee = get_object_or_404(Employee, pk=pk)
    
    # Get logs ordered by most recent
    logs = EmployeeVerificationLog.objects.filter(
        employee=employee
    ).order_by('-timestamp')
    
    # Pagination
    paginator = Paginator(logs, 50)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'employee': employee,
        'page_obj': page_obj,
        'logs': page_obj.object_list,
        'total_verifications': paginator.count,
    }
    
    return render(request, 'employees/verification_logs.html', context)
