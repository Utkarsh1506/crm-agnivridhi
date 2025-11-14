from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Payment
from accounts.views import manager_required, client_required, sales_required

@login_required
def payment_list(request):
    """Deprecated generic endpoint: redirect to role-specific page for privacy."""
    user = request.user
    if getattr(user, 'is_client', False):
        return redirect('payments:client_payments_list')
    elif getattr(user, 'role', None) == 'SALES':
        return redirect('payments:sales_payments_list')
    elif getattr(user, 'role', None) in ['MANAGER', 'ADMIN']:
        return redirect('payments:team_payments_list')
    return redirect('dashboard')


@client_required
def client_payments_list(request):
    client = request.user.client_profile
    payments = Payment.objects.filter(client=client).order_by('-created_at')
    return render(request, 'payments/payment_list.html', {'payments': payments})


@sales_required
def sales_payments_list(request):
    # Payments related to bookings for clients assigned to this sales
    from django.db.models import Q
    payments = Payment.objects.filter(
        Q(received_by=request.user) | Q(client__assigned_sales=request.user)
    ).select_related('client', 'booking', 'booking__service', 'received_by').order_by('-created_at')
    
    context = {
        'payments': payments,
        'page_title': 'My Payments'
    }
    return render(request, 'payments/sales_payments_list.html', context)


@manager_required
def team_payments_list(request):
    """Manager/Admin view: Payments for team clients; Admin/Owner sees all."""
    user = request.user
    
    # Get all clients assigned to this manager's team
    # Include both: clients directly assigned to manager AND clients assigned to sales employees under this manager
    from clients.models import Client
    from django.db.models import Q
    
    user_role = getattr(user, 'role', '').upper()
    if user_role in ['ADMIN', 'OWNER'] or getattr(user, 'is_superuser', False):
        payments = Payment.objects.all().select_related('client', 'client__assigned_sales', 'booking', 'received_by').order_by('-created_at')
        # For totals by client, include all clients
        team_clients = Client.objects.all().select_related('assigned_sales', 'assigned_manager')
    else:
        team_clients = Client.objects.filter(
            Q(assigned_manager=user) | Q(assigned_sales__manager=user)
        ).select_related('assigned_sales', 'assigned_manager').distinct()
        
        # Get payments for these clients
        payments = Payment.objects.filter(client__in=team_clients).select_related('client', 'client__assigned_sales', 'booking', 'received_by').order_by('-created_at')
    
    # Statistics
    from django.db.models import Sum, Count
    stats = payments.aggregate(
        total_amount=Sum('amount'),
        pending_count=Count('id', filter=Q(status='PENDING')),
        captured_count=Count('id', filter=Q(status='CAPTURED')),
        failed_count=Count('id', filter=Q(status='FAILED')),
    )
    
    # Group by client
    payments_by_client = {}
    for payment in payments:
        client_name = payment.client.company_name
        if client_name not in payments_by_client:
            payments_by_client[client_name] = {
                'client': payment.client,
                'payments': []
            }
        payments_by_client[client_name]['payments'].append(payment)
    
    context = {
        'payments': payments,
        'payments_by_client': payments_by_client,
        'total_payments': payments.count(),
        'total_clients': team_clients.count(),
        'stats': stats,
    }
    return render(request, 'payments/team_payments_list.html', context)


@login_required
def payment_detail(request, pk):
    """View payment details"""
    payment = get_object_or_404(Payment, pk=pk)
    
    # Check permissions
    user = request.user
    if user.is_client and payment.client.user != user:
        messages.error(request, "You don't have permission to view this payment.")
        return redirect('payments:client_payments_list')
    
    # Determine back URL based on role
    user_role = getattr(user, 'role', '').upper()
    if user_role in ['ADMIN', 'OWNER', 'MANAGER'] or user.is_superuser:
        back_url = 'payments:team_payments_list'
    elif user_role == 'SALES':
        back_url = 'payments:sales_payments_list'
    elif user_role == 'CLIENT':
        back_url = 'payments:client_payments_list'
    else:
        back_url = 'payments:team_payments_list'
    
    context = {
        'payment': payment,
        'back_url': back_url,
    }
    return render(request, 'payments/payment_detail.html', context)


@login_required
def record_payment(request, booking_id):
    """Record payment for a booking"""
    from bookings.models import Booking
    from django.utils import timezone
    
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if payment already exists
    if hasattr(booking, 'payment'):
        messages.warning(request, 'Payment already recorded for this booking.')
        return redirect('clients:client_detail', pk=booking.client.id)
    
    # Permission check
    user = request.user
    if user.role == 'SALES' and booking.client.assigned_sales != user:
        messages.error(request, 'You can only record payments for your assigned clients.')
        return redirect('clients:sales_clients_list')
    elif user.role == 'MANAGER':
        if not (booking.client.assigned_manager == user or 
                (booking.client.assigned_sales and booking.client.assigned_sales.manager == user)):
            messages.error(request, 'You can only record payments for your team clients.')
            return redirect('clients:manager_clients_list')
    
    if request.method == 'POST':
        try:
            from decimal import Decimal
            
            amount = Decimal(request.POST.get('amount'))
            payment_method = request.POST.get('payment_method')
            reference_id = request.POST.get('reference_id', '').strip()
            notes = request.POST.get('notes', '').strip()
            proof = request.FILES.get('proof')
            
            if not reference_id:
                messages.error(request, 'Transaction reference is required.')
                return redirect('payments:record_payment', booking_id=booking_id)
            
            # Create payment record
            payment = Payment.objects.create(
                booking=booking,
                client=booking.client,
                amount=amount,
                payment_method=payment_method,
                reference_id=reference_id,
                notes=notes,
                proof=proof,
                received_by=user,
                status='PENDING'  # Awaiting approval
            )
            
            messages.success(
                request, 
                f'Payment recorded successfully! Reference: {reference_id}. Awaiting manager approval.'
            )
            return redirect('clients:client_detail', pk=booking.client.id)
            
        except Exception as e:
            messages.error(request, f'Error recording payment: {str(e)}')
            return redirect('payments:record_payment', booking_id=booking_id)
    
    context = {
        'booking': booking,
        'page_title': f'Record Payment - {booking.booking_id}'
    }
    return render(request, 'payments/record_payment.html', context)


@manager_required
def approve_payment(request, payment_id):
    """Manager/Admin approves a payment"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    if payment.status != 'PENDING':
        messages.warning(request, f'Payment is already {payment.get_status_display()}.')
        return redirect('accounts:manager_dashboard')
    
    # Approve the payment (uses model method)
    payment.approve(request.user)
    
    messages.success(
        request, 
        f'Payment approved! Booking #{payment.booking.booking_id} is now PAID. You can now create an application.'
    )
    return redirect('accounts:manager_dashboard')


@manager_required
def reject_payment(request, payment_id):
    """Manager/Admin rejects a payment"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    if payment.status != 'PENDING':
        messages.warning(request, f'Payment is already {payment.get_status_display()}.')
        return redirect('accounts:manager_dashboard')
    
    if request.method == 'POST':
        reason = request.POST.get('reason', 'Payment verification failed')
        payment.reject(request.user, reason)
        
        messages.warning(request, f'Payment rejected. Reason: {reason}')
        return redirect('accounts:manager_dashboard')
    
    context = {
        'payment': payment
    }
    return render(request, 'payments/reject_payment.html', context)
