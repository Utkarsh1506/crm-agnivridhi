from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import EditRequest
from clients.models import Client


@login_required
def request_client_edit(request, client_id):
    """Sales employee requests to edit client details"""
    client = get_object_or_404(Client, pk=client_id)
    
    # Check permissions - only sales assigned to this client
    if request.user.role != 'SALES' or client.assigned_sales != request.user:
        messages.error(request, 'You do not have permission to request edits for this client.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        field_name = request.POST.get('field_name')
        requested_value = request.POST.get('requested_value')
        reason = request.POST.get('reason')
        
        if not all([field_name, requested_value, reason]):
            messages.error(request, 'All fields are required.')
            return redirect('edit_requests:request_client_edit', client_id=client_id)
        
        # Get current value
        current_value = str(getattr(client, field_name, ''))
        
        # Create edit request
        edit_request = EditRequest.objects.create(
            entity_type='CLIENT',
            entity_id=client.id,
            field_name=field_name,
            current_value=current_value,
            requested_value=requested_value,
            reason=reason,
            requested_by=request.user,
            status='PENDING'
        )
        
        messages.success(request, f'Edit request submitted successfully! Your manager will review it.')
        # TODO: Send notification to manager
        
        return redirect('clients:client_detail', pk=client_id)
    
    # Get editable fields
    editable_fields = [
        ('company_name', 'Company Name'),
        ('business_type', 'Business Type'),
        ('sector', 'Sector'),
        ('company_age', 'Company Age'),
        ('registration_number', 'Registration Number'),
        ('gst_number', 'GST Number'),
        ('pan_number', 'PAN Number'),
        ('address_line1', 'Address Line 1'),
        ('address_line2', 'Address Line 2'),
        ('city', 'City'),
        ('state', 'State'),
        ('pincode', 'Pincode'),
        ('annual_turnover', 'Annual Turnover'),
        ('funding_required', 'Funding Required'),
        ('existing_loans', 'Existing Loans'),
        ('contact_person', 'Contact Person'),
        ('contact_email', 'Contact Email'),
        ('contact_phone', 'Contact Phone'),
        ('alternate_phone', 'Alternate Phone'),
        ('business_description', 'Business Description'),
        ('funding_purpose', 'Funding Purpose'),
    ]
    
    # Get pending edit requests for this client
    pending_requests = EditRequest.objects.filter(
        entity_type='CLIENT',
        entity_id=client_id,
        status='PENDING',
        requested_by=request.user
    ).order_by('-created_at')
    
    return render(request, 'edit_requests/request_client_edit.html', {
        'client': client,
        'editable_fields': editable_fields,
        'pending_requests': pending_requests,
    })


@login_required
def manager_edit_requests(request):
    """Manager views all pending edit requests from their team"""
    if request.user.role not in ['MANAGER', 'ADMIN', 'OWNER']:
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    # Get pending edit requests from team members
    if request.user.role == 'MANAGER':
        pending_requests = EditRequest.objects.filter(
            status='PENDING',
            requested_by__manager=request.user
        ).select_related('requested_by').order_by('-created_at')
    else:
        # Admin/Owner sees all
        pending_requests = EditRequest.objects.filter(
            status='PENDING'
        ).select_related('requested_by').order_by('-created_at')
    
    # Get client details for each request
    requests_with_details = []
    for edit_request in pending_requests:
        if edit_request.entity_type == 'CLIENT':
            try:
                client = Client.objects.get(pk=edit_request.entity_id)
                requests_with_details.append({
                    'edit_request': edit_request,
                    'client': client
                })
            except Client.DoesNotExist:
                pass
    
    return render(request, 'edit_requests/manager_edit_requests.html', {
        'requests_with_details': requests_with_details,
        'pending_count': len(requests_with_details),
    })


@login_required
def approve_edit_request(request, request_id):
    """Manager approves an edit request and applies the changes"""
    edit_request = get_object_or_404(EditRequest, pk=request_id)
    
    # Check permissions
    if request.user.role not in ['MANAGER', 'ADMIN', 'OWNER']:
        messages.error(request, 'You do not have permission to approve edit requests.')
        return redirect('accounts:dashboard')
    
    # Manager can only approve requests from their team
    if request.user.role == 'MANAGER':
        if edit_request.requested_by.manager != request.user:
            messages.error(request, 'You can only approve requests from your team.')
            return redirect('edit_requests:manager_edit_requests')
    
    if edit_request.status != 'PENDING':
        messages.warning(request, 'This request has already been processed.')
        return redirect('edit_requests:manager_edit_requests')
    
    if request.method == 'POST':
        notes = request.POST.get('notes', '')
        
        # Approve the request
        edit_request.status = 'APPROVED'
        edit_request.approved_by = request.user
        edit_request.approval_notes = notes
        edit_request.approval_date = timezone.now()
        edit_request.save()
        
        # Apply the changes to the client
        try:
            if edit_request.entity_type == 'CLIENT':
                client = Client.objects.get(pk=edit_request.entity_id)
                setattr(client, edit_request.field_name, edit_request.requested_value)
                client.save()
                
                edit_request.status = 'APPLIED'
                edit_request.save()
                
                messages.success(request, f'Edit request approved and changes applied to {client.company_name}!')
                # TODO: Send notification to sales employee
            else:
                messages.success(request, 'Edit request approved!')
        except Exception as e:
            messages.error(request, f'Error applying changes: {str(e)}')
        
        return redirect('edit_requests:manager_edit_requests')
    
    # GET - show confirmation
    client = None
    if edit_request.entity_type == 'CLIENT':
        try:
            client = Client.objects.get(pk=edit_request.entity_id)
        except Client.DoesNotExist:
            pass
    
    return render(request, 'edit_requests/approve_edit_request.html', {
        'edit_request': edit_request,
        'client': client,
    })


@login_required
def reject_edit_request(request, request_id):
    """Manager rejects an edit request"""
    edit_request = get_object_or_404(EditRequest, pk=request_id)
    
    # Check permissions
    if request.user.role not in ['MANAGER', 'ADMIN', 'OWNER']:
        messages.error(request, 'You do not have permission to reject edit requests.')
        return redirect('accounts:dashboard')
    
    # Manager can only reject requests from their team
    if request.user.role == 'MANAGER':
        if edit_request.requested_by.manager != request.user:
            messages.error(request, 'You can only reject requests from your team.')
            return redirect('edit_requests:manager_edit_requests')
    
    if edit_request.status != 'PENDING':
        messages.warning(request, 'This request has already been processed.')
        return redirect('edit_requests:manager_edit_requests')
    
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        
        if not reason:
            messages.error(request, 'Please provide a reason for rejection.')
            return redirect('edit_requests:reject_edit_request', request_id=request_id)
        
        # Reject the request
        edit_request.status = 'REJECTED'
        edit_request.approved_by = request.user
        edit_request.approval_notes = reason
        edit_request.approval_date = timezone.now()
        edit_request.save()
        
        messages.warning(request, 'Edit request has been rejected.')
        # TODO: Send notification to sales employee
        
        return redirect('edit_requests:manager_edit_requests')
    
    # GET - show confirmation
    client = None
    if edit_request.entity_type == 'CLIENT':
        try:
            client = Client.objects.get(pk=edit_request.entity_id)
        except Client.DoesNotExist:
            pass
    
    return render(request, 'edit_requests/reject_edit_request.html', {
        'edit_request': edit_request,
        'client': client,
    })


@login_required
def edit_client_direct(request, client_id):
    """Manager/Admin/Owner/Superuser directly edits client details without approval"""
    client = get_object_or_404(Client, pk=client_id)

    # Only manager, admin, owner, or superuser can directly edit
    if not (request.user.is_manager or request.user.is_admin or request.user.is_owner or request.user.is_superuser):
        messages.error(request, 'You do not have permission to edit clients directly.')
        return redirect('clients:client_detail', pk=client_id)

    # Team restriction only for managers
    if request.user.role == 'MANAGER':
        sales_manager = getattr(client.assigned_sales, 'manager', None)
        if client.assigned_manager != request.user and sales_manager != request.user:
            messages.error(request, 'You can only edit clients in your team.')
            return redirect('accounts:dashboard')
    # Admin/Owner/Superuser: no restriction

    if request.method == 'POST':
        # Update client fields
        updateable_fields = [
            'company_name', 'business_type', 'sector', 'company_age',
            'registration_number', 'gst_number', 'pan_number',
            'address_line1', 'address_line2', 'city', 'state', 'pincode',
            'annual_turnover', 'funding_required', 'existing_loans',
            'contact_person', 'contact_email', 'contact_phone', 'alternate_phone',
            'business_description', 'funding_purpose'
        ]

        updated = False
        for field in updateable_fields:
            if field in request.POST:
                value = request.POST.get(field)
                if value is not None:
                    setattr(client, field, value)
                    updated = True

        if updated:
            client.save()
            messages.success(request, f'Client "{client.company_name}" updated successfully!')

        return redirect('clients:client_detail', pk=client_id)

    return render(request, 'edit_requests/edit_client_direct.html', {
        'client': client,
    })

