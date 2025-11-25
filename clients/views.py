from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator

from accounts.email_utils_client_credentials import send_client_credentials_email
from .models import Client
from .forms import (
    ClientCreationForm,
    ClientApprovalForm,
    QuickClientCreationForm,
    ClientProfileCompletionForm,
)


@login_required
def create_client(request):
    """
    Quick client creation - Only requires: company name, contact person, email, phone.
    Client fills remaining details after login.
    """
    # Check permissions
    if request.user.role not in ['SALES', 'MANAGER', 'ADMIN', 'OWNER']:
        messages.error(request, 'You do not have permission to create clients.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = QuickClientCreationForm(request.POST, created_by=request.user)
        if form.is_valid():
            client = form.save()
            
            # Send notification based on role
            if request.user.role == 'SALES':
                messages.success(
                    request, 
                    f'Client "{client.company_name}" created successfully! '
                    f'Waiting for your manager approval. '
                    f'Login credentials will be generated after approval.'
                )
                # TODO: Send notification to manager
                return redirect('clients:sales_clients_list')
            elif request.user.role == 'MANAGER':
                messages.success(
                    request, 
                    f'Client "{client.company_name}" created and approved successfully! '
                    f'Login credentials have been generated. Check Owner Dashboard to share with client.'
                )
                # TODO: Send welcome email to client
                return redirect('accounts:dashboard')  # Manager dashboard
            else:  # ADMIN or OWNER
                messages.success(
                    request, 
                    f'Client "{client.company_name}" created and approved successfully! '
                    f'Check Owner Dashboard for login credentials to share with client.'
                )
                # TODO: Send welcome email to client
                return redirect('accounts:owner_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = QuickClientCreationForm(created_by=request.user)
    
    return render(request, 'clients/create_client.html', {
        'form': form,
        'page_title': 'Create New Client',
        'is_quick_form': True
    })


@login_required
def pending_approval_clients(request):
    """View pending client approvals (Sales/Manager)"""
    if request.user.role == 'SALES':
        # Sales can see their own pending clients
        clients = Client.objects.filter(
            created_by=request.user,
            is_approved=False
        ).select_related('user', 'created_by', 'assigned_manager').order_by('-created_at')
    elif request.user.role in ['MANAGER', 'ADMIN', 'OWNER']:
        # Managers see all pending clients in their team
        clients = Client.objects.filter(
            Q(assigned_manager=request.user) | Q(created_by__manager=request.user),
            is_approved=False
        ).select_related('user', 'created_by', 'assigned_manager').order_by('-created_at')
    else:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('accounts:dashboard')
    
    return render(request, 'clients/pending_approval_clients.html', {
        'clients': clients,
        'page_title': 'Pending Client Approvals'
    })


@login_required
def approve_client(request, pk):
    """Approve or reject a client (Manager/Admin)"""
    client = get_object_or_404(Client, pk=pk)
    
    # Check permissions
    if request.user.role not in ['MANAGER', 'ADMIN', 'OWNER']:
        messages.error(request, 'You do not have permission to approve clients.')
        return redirect('accounts:dashboard')
    
    # Manager can only approve clients in their team
    if request.user.role == 'MANAGER':
        creator_manager = getattr(client.created_by, 'manager', None)
        if client.assigned_manager != request.user and creator_manager != request.user:
            messages.error(request, 'You can only approve clients in your team.')
            return redirect('clients:pending_approval_clients')
    
    if request.method == 'POST':
        form = ClientApprovalForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['action']
            
            if action == 'approve':
                client.approve(request.user)
                # Send credentials email if credentials exist and not sent
                credentials = getattr(client, 'credentials', None)
                if credentials and not credentials.is_sent:
                    from django.contrib.sites.shortcuts import get_current_site

                    login_url = getattr(settings, 'CLIENT_LOGIN_URL', None)
                    if not login_url:
                        site = get_current_site(request)
                        login_url = f"https://{site.domain}/accounts/login/"
                    if send_client_credentials_email(credentials, login_url=login_url):
                        credentials.mark_as_sent(request.user)
                        messages.success(request, f'Client "{client.company_name}" has been approved and credentials emailed!')
                    else:
                        messages.success(request, f'Client "{client.company_name}" has been approved, but email could not be sent.')
                else:
                    messages.success(request, f'Client "{client.company_name}" has been approved!')
                status = 'APPROVED'
                extra = {}
            else:
                reason = form.cleaned_data['rejection_reason']
                client.reject(request.user, reason)
                messages.warning(request, f'Client "{client.company_name}" has been rejected.')
                status = 'REJECTED'
                extra = {'rejection_reason': reason}

            # AJAX support
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'ok': True,
                    'status': status,
                    'client_id': client.client_id,
                    **extra
                })

            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('clients:pending_approval_clients')
    else:
        form = ClientApprovalForm()
    
    return render(request, 'clients/approve_client.html', {
        'client': client,
        'form': form,
        'page_title': f'Approve Client - {client.company_name}'
    })


@login_required
def client_detail(request, pk):
    """View client details"""
    client = get_object_or_404(Client, pk=pk)
    
    # Check permissions
    if request.user.role == 'CLIENT':
        if client.user != request.user:
            messages.error(request, 'You can only view your own profile.')
            return redirect('accounts:dashboard')
    elif request.user.role == 'SALES':
        if client.assigned_sales != request.user:
            messages.error(request, 'You can only view clients assigned to you.')
            return redirect('accounts:dashboard')
    elif request.user.role == 'MANAGER':
        sales_manager = getattr(client.assigned_sales, 'manager', None)
        if client.assigned_manager != request.user and sales_manager != request.user:
            messages.error(request, 'You can only view clients in your team.')
            return redirect('accounts:dashboard')
    
    # Get bookings for this client
    from bookings.models import Booking
    bookings = Booking.objects.filter(client=client).select_related('service').order_by('-created_at')
    
    return render(request, 'clients/client_detail.html', {
        'client': client,
        'bookings': bookings,
        'page_title': f'Client - {client.company_name}'
    })


@login_required
def sales_clients_list(request):
    """List clients for sales person"""
    if request.user.role != 'SALES':
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    clients = Client.objects.filter(
        assigned_sales=request.user
    ).select_related('user', 'assigned_manager').order_by('-created_at')
    
    approved_clients = clients.filter(is_approved=True)
    pending_clients = clients.filter(is_approved=False)
    
    return render(request, 'clients/sales_clients_list.html', {
        'approved_clients': approved_clients,
        'pending_clients': pending_clients,
        'page_title': 'My Clients'
    })


@login_required
def manager_clients_list(request):
    """List clients for manager"""
    if request.user.role not in ['MANAGER', 'ADMIN', 'OWNER']:
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    # If Admin/Owner: show ALL clients (global visibility)
    if request.user.role in ['ADMIN', 'OWNER']:
        clients = Client.objects.all().select_related('user', 'assigned_sales', 'assigned_manager').order_by('-created_at')
    else:
        # Manager scope: clients directly assigned to manager OR via team sales
        clients = Client.objects.filter(
            Q(assigned_manager=request.user) | Q(assigned_sales__manager=request.user)
        ).select_related('user', 'assigned_sales', 'assigned_manager').order_by('-created_at')
    
    approved_clients = clients.filter(is_approved=True)
    pending_clients = clients.filter(is_approved=False)
    
    return render(request, 'clients/manager_clients_list.html', {
        'approved_clients': approved_clients,
        'pending_clients': pending_clients,
        'page_title': 'Team Clients'
    })


@login_required
def admin_clients_list(request):
    """Global client listing for Admin/Owner/Superuser with direct edit access.

    Features:
    - Full visibility of all clients
    - Filtering by search (company/contact), status, sales, manager
    - Pagination with adjustable page size
    - Direct edit link using edit_requests:edit_client_direct
    """
    # Case-insensitive role check
    user_role = getattr(request.user, 'role', '').upper()
    if user_role not in ['ADMIN', 'OWNER'] and not request.user.is_superuser:
        from django.contrib import messages
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')

    qs = Client.objects.select_related('user', 'assigned_sales', 'assigned_manager').all().order_by('-created_at')

    # Filters
    search = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    sales_id = request.GET.get('sales', '').strip()
    manager_id = request.GET.get('manager', '').strip()
    business_type = request.GET.get('business_type', '').strip()
    sector = request.GET.get('sector', '').strip()
    city = request.GET.get('city', '').strip()
    state = request.GET.get('state', '').strip()
    approved = request.GET.get('approved', '').strip()
    created_from = request.GET.get('created_from', '').strip()
    created_to = request.GET.get('created_to', '').strip()
    turnover_min = request.GET.get('turnover_min', '').strip()
    turnover_max = request.GET.get('turnover_max', '').strip()
    funding_min = request.GET.get('funding_min', '').strip()
    funding_max = request.GET.get('funding_max', '').strip()

    if search:
        qs = qs.filter(
            Q(company_name__icontains=search) |
            Q(contact_person__icontains=search) |
            Q(contact_email__icontains=search) |
            Q(client_id__icontains=search)
        )
    if status:
        qs = qs.filter(status=status)
    if sales_id:
        qs = qs.filter(assigned_sales_id=sales_id)
    if manager_id:
        qs = qs.filter(assigned_manager_id=manager_id)
    if business_type:
        qs = qs.filter(business_type=business_type)
    if sector:
        qs = qs.filter(sector=sector)
    if city:
        qs = qs.filter(city__icontains=city)
    if state:
        qs = qs.filter(state__icontains=state)
    if approved in ['yes', 'no']:
        qs = qs.filter(is_approved=(approved == 'yes'))
    if created_from:
        qs = qs.filter(created_at__date__gte=created_from)
    if created_to:
        qs = qs.filter(created_at__date__lte=created_to)
    if turnover_min:
        qs = qs.filter(annual_turnover__gte=turnover_min)
    if turnover_max:
        qs = qs.filter(annual_turnover__lte=turnover_max)
    if funding_min:
        qs = qs.filter(funding_required__gte=funding_min)
    if funding_max:
        qs = qs.filter(funding_required__lte=funding_max)

    # Pagination
    try:
        page_size = int(request.GET.get('page_size', 25))
    except ValueError:
        page_size = 25
    if page_size not in [25, 50, 100, 150, 200]:
        page_size = 25

    paginator = Paginator(qs, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Distinct lists for filter dropdowns
    sales_team = qs.exclude(assigned_sales=None).values('assigned_sales_id', 'assigned_sales__first_name', 'assigned_sales__last_name', 'assigned_sales__username').distinct()
    manager_team = qs.exclude(assigned_manager=None).values('assigned_manager_id', 'assigned_manager__first_name', 'assigned_manager__last_name', 'assigned_manager__username').distinct()

    return render(request, 'clients/admin_clients_list.html', {
        'page_obj': page_obj,
        'total_clients': qs.count(),
        'search': search,
        'status_filter': status,
        'sales_filter': sales_id,
        'manager_filter': manager_id,
        'business_type_filter': business_type,
        'sector_filter': sector,
        'city_filter': city,
        'state_filter': state,
        'approved_filter': approved,
        'created_from': created_from,
        'created_to': created_to,
        'turnover_min': turnover_min,
        'turnover_max': turnover_max,
        'funding_min': funding_min,
        'funding_max': funding_max,
        'page_size': page_size,
        'sales_team': sales_team,
        'manager_team': manager_team,
        'business_type_choices': Client.BusinessType.choices,
        'sector_choices': Client.Sector.choices,
        'page_title': 'All Clients'
    })


@login_required
def complete_client_profile(request):
    """
    Allow clients to complete their profile after initial creation.
    Only accessible to CLIENT role users.
    """
    if request.user.role != 'CLIENT':
        messages.error(request, 'This page is only accessible to client users.')
        return redirect('accounts:dashboard')
    
    try:
        client = request.user.client_profile
    except Client.DoesNotExist:
        messages.error(request, 'No client profile found for your account.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = ClientProfileCompletionForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(
                request,
                'Your profile has been updated successfully! '
                'Our team will review and get back to you soon.'
            )
            return redirect('accounts:client_portal')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ClientProfileCompletionForm(instance=client)
    
    # Calculate profile completion percentage
    required_fields = ['business_type', 'sector', 'company_age', 'address_line1',
                      'city', 'state', 'pincode', 'annual_turnover', 'funding_required']
    completed_fields = sum([1 for field in required_fields if getattr(client, field)])
    completion_percentage = int((completed_fields / len(required_fields)) * 100)
    
    return render(request, 'clients/complete_profile.html', {
        'form': form,
        'client': client,
        'completion_percentage': completion_percentage,
        'page_title': 'Complete Your Profile'
    })

