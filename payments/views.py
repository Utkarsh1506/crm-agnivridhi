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
    
    if getattr(user, 'role', None) in ['ADMIN', 'OWNER'] or getattr(user, 'is_superuser', False):
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
        return redirect('payment_list')
    
    context = {
        'payment': payment,
    }
    return render(request, 'payments/payment_detail.html', context)
