from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Client
from .forms import ClientCreationForm, ClientApprovalForm


@login_required
def create_client(request):
    """Create a new client (Sales/Manager/Admin)"""
    # Check permissions
    if request.user.role not in ['SALES', 'MANAGER', 'ADMIN', 'OWNER']:
        messages.error(request, 'You do not have permission to create clients.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = ClientCreationForm(request.POST, created_by=request.user)
        if form.is_valid():
            client = form.save()
            
            # Send notification based on role
            if request.user.role == 'SALES':
                messages.success(
                    request, 
                    f'Client "{client.company_name}" created successfully! Waiting for manager approval.'
                )
                # TODO: Send notification to manager
                return redirect('clients:pending_approval_clients')
            else:
                messages.success(
                    request, 
                    f'Client "{client.company_name}" created and approved successfully!'
                )
                # TODO: Send welcome email to client
                return redirect('clients:client_detail', pk=client.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ClientCreationForm(created_by=request.user)
    
    return render(request, 'clients/create_client.html', {
        'form': form,
        'page_title': 'Create New Client'
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
        if client.assigned_manager != request.user and client.created_by.manager != request.user:
            messages.error(request, 'You can only approve clients in your team.')
            return redirect('clients:pending_approval_clients')
    
    if request.method == 'POST':
        form = ClientApprovalForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['action']
            
            if action == 'approve':
                client.approve(request.user)
                messages.success(request, f'Client "{client.company_name}" has been approved!')
                # TODO: Send notification to sales person
                # TODO: Send welcome email to client
            else:
                reason = form.cleaned_data['rejection_reason']
                client.reject(request.user, reason)
                messages.warning(request, f'Client "{client.company_name}" has been rejected.')
                # TODO: Send notification to sales person with reason
            
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
        if client.assigned_manager != request.user and client.assigned_sales.manager != request.user:
            messages.error(request, 'You can only view clients in your team.')
            return redirect('accounts:dashboard')
    
    return render(request, 'clients/client_detail.html', {
        'client': client,
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
    
    # Get all clients in the manager's team
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

