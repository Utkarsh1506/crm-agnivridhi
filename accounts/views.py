from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from functools import wraps
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from accounts.email_utils_client_credentials import send_client_credentials_email
from .forms import ProfileForm


def role_required(*roles):
    """
    Decorator to check if user has required role
    Usage: @role_required('ADMIN', 'MANAGER')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            
            # Superusers bypass all role checks
            if getattr(request.user, 'is_superuser', False):
                return view_func(request, *args, **kwargs)
            
            if hasattr(request.user, 'role'):
                # Case-insensitive role comparison
                user_role = request.user.role.upper() if request.user.role else ''
                allowed_roles = [r.upper() for r in roles]
                if user_role in allowed_roles:
                    return view_func(request, *args, **kwargs)
            
            # Return 403 using the dedicated template
            try:
                # Lightweight debug to help identify role mismatches during dev
                print(f"[role_required] 403 for user={getattr(request.user,'username',None)} role={getattr(request.user,'role',None)} allowed={roles}")
            except Exception:
                pass
            from django.shortcuts import render
            return render(request, 'errors/403.html', status=403)
        return wrapper
    return decorator


def admin_required(view_func):
    """Decorator for admin-only views (ADMIN and OWNER roles have admin privileges)"""
    return role_required('ADMIN', 'OWNER')(view_func)


def staff_required(view_func):
    """Decorator for staff (Admin, Manager, Sales) views - OWNER inherits staff privileges"""
    return role_required('ADMIN', 'MANAGER', 'SALES', 'OWNER')(view_func)


def manager_required(view_func):
    """Decorator for manager-only views - OWNER inherits manager privileges"""
    return role_required('ADMIN', 'MANAGER', 'OWNER')(view_func)


def sales_required(view_func):
    """Decorator for sales views - ADMIN, MANAGER, and OWNER can also access"""
    return role_required('SALES', 'ADMIN', 'MANAGER', 'OWNER')(view_func)


def client_required(view_func):
    """Decorator for client-only views"""
    return role_required('CLIENT')(view_func)


def login_view(request):
    """
    Custom login view with role-based redirect
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            
            # Role-based redirect
            # PRIORITY 1: Owner gets Owner Dashboard (not superuser dashboard)
            if getattr(user, 'is_owner', False) or getattr(user, 'role', '').upper() == 'OWNER':
                return redirect('accounts:owner_dashboard')
            
            # PRIORITY 2: Superuser (if not owner) gets superuser dashboard
            if user.is_superuser:
                return redirect('accounts:superuser_dashboard')

            # PRIORITY 3: Role-based routing
            role = getattr(user, 'role', None)
            if role:
                if role == 'CLIENT':
                    return redirect('accounts:client_portal')
                else:
                    # Admin, Manager, Sales go to their respective dashboards
                    return redirect('accounts:dashboard')
            
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    """
    Logout view
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


def custom_403_view(request, exception=None):
    """
    Custom 403 Forbidden error page
    Shows role-specific information and safe navigation options
    """
    return render(request, 'errors/403.html', status=403)


def custom_404_view(request, exception=None):
    """
    Custom 404 Not Found error page
    Shows helpful navigation based on user role
    """
    return render(request, 'errors/404.html', status=404)


def custom_500_view(request):
    """
    Custom 500 Internal Server Error page
    Note: This handler receives no request context in production
    """
    return render(request, 'errors/500.html', status=500)


@login_required
def dashboard_view(request):
    """
    Main dashboard with role-based routing
    """
    user = request.user
    
    # PRIORITY 1: Owner gets Owner Dashboard (not superuser dashboard)
    if getattr(user, 'is_owner', False) or getattr(user, 'role', '').upper() == 'OWNER':
        return redirect('accounts:owner_dashboard')
    
    # PRIORITY 2: Superuser (if not owner) gets dedicated dashboard
    if user.is_superuser:
        return redirect('accounts:superuser_dashboard')

    # PRIORITY 3: Role-based routing
    role = getattr(user, 'role', None)
    if role:
        role_upper = role.upper()
        if role_upper == 'ADMIN':
            return redirect('accounts:admin_dashboard')
        elif role_upper == 'MANAGER':
            return redirect('accounts:manager_dashboard')
        elif role_upper == 'SALES':
            return redirect('accounts:sales_dashboard')
        elif role_upper == 'CLIENT':
            return redirect('accounts:client_portal')
    
    # Fallback generic dashboard (shouldn't generally hit)
    return render(request, 'accounts/dashboard.html', {'user': user})


@admin_required
def admin_dashboard(request):
    """
    Admin dashboard with analytics
    """
    from clients.models import Client
    from bookings.models import Booking
    from applications.models import Application
    from payments.models import Payment
    from edit_requests.models import EditRequest
    from django.db.models import Sum, Count, Q
    from accounts.models import User
    
    # Analytics
    total_clients = Client.objects.count()
    active_clients = Client.objects.filter(status='ACTIVE').count()
    
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='PENDING').count()
    
    total_applications = Application.objects.count()
    pending_applications = Application.objects.filter(status__in=['DRAFT', 'SUBMITTED', 'UNDER_REVIEW']).count()
    
    # Filters
    method_filter = request.GET.get('method')
    salesperson_filter = request.GET.get('salesperson')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    base_success = Payment.objects.filter(status__in=['AUTHORIZED', 'CAPTURED'])
    if method_filter:
        base_success = base_success.filter(payment_method=method_filter)
    if salesperson_filter:
        base_success = base_success.filter(received_by_id=salesperson_filter)
    if date_from:
        from django.utils.dateparse import parse_date
        parsed_from = parse_date(date_from)
        if parsed_from:
            base_success = base_success.filter(payment_date__date__gte=parsed_from)
    if date_to:
        from django.utils.dateparse import parse_date
        parsed_to = parse_date(date_to)
        if parsed_to:
            base_success = base_success.filter(payment_date__date__lte=parsed_to)
    
        total_revenue = base_success.aggregate(Sum('amount'))['amount__sum'] or 0

    # Live client revenue totals (pitched/received/pending with GST)
    client_revenue = Client.objects.aggregate(
        total_pitched=Sum('total_pitched_amount'),
        total_with_gst=Sum('total_with_gst'),
        total_received=Sum('received_amount'),
        total_pending=Sum('pending_amount'),
    )
    client_revenue = {k: v or 0 for k, v in client_revenue.items()}
    
    # Pending revenue (awaiting approval)
    pending_revenue = Payment.objects.filter(status='PENDING').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Failed/disputed revenue
    failed_revenue = Payment.objects.filter(status='FAILED').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # All recent payments (not just pending) for comprehensive view
    all_recent_payments = Payment.objects.select_related('client', 'booking', 'received_by').order_by('-created_at')[:20]
    
    pending_edit_requests = EditRequest.objects.filter(status='PENDING').count()

    # Pending payments (awaiting approval)
    pending_payments = Payment.objects.filter(status='PENDING').order_by('-created_at')[:10]
    pending_payments_count = Payment.objects.filter(status='PENDING').count()
    
    # Recent items
    recent_clients = Client.objects.order_by('-created_at')[:5]
    recent_bookings = Booking.objects.order_by('-booking_date')[:5]
    recent_applications = Application.objects.order_by('-application_date')[:5]
    pending_edits = EditRequest.objects.filter(status='PENDING').order_by('-created_at')[:10]
    
    # Revenue by month (last 6 months)
    from django.utils import timezone
    from datetime import timedelta
    now = timezone.now()
    labels = []
    revenue_series = []
    from payments.models import Payment as _P
    for i in range(5, -1, -1):
        start = (now.replace(day=1) - timedelta(days=30*i)).replace(day=1)
        # Compute end by moving to next month start
        if start.month == 12:
            end = start.replace(year=start.year+1, month=1, day=1)
        else:
            end = start.replace(month=start.month+1, day=1)
        month_qs = base_success.filter(payment_date__gte=start, payment_date__lt=end)
        month_sum = month_qs.aggregate(Sum('amount'))['amount__sum'] or 0
        labels.append(start.strftime('%b %Y'))
        revenue_series.append(float(month_sum))

    # Revenue by method
    method_breakdown_qs = Payment.objects.filter(status__in=['AUTHORIZED','CAPTURED']).values('payment_method').annotate(total=Sum('amount')).order_by('-total')
    method_labels = [row['payment_method'] or 'UNKNOWN' for row in method_breakdown_qs]
    method_values = [float(row['total'] or 0) for row in method_breakdown_qs]

    # Top sales by revenue
    top_sales_qs = Payment.objects.filter(status__in=['AUTHORIZED','CAPTURED'], received_by__isnull=False).values('received_by__username', 'received_by__first_name', 'received_by__last_name').annotate(total=Sum('amount')).order_by('-total')[:5]
    top_sales = [
        {
            'name': (f"{r['received_by__first_name']} {r['received_by__last_name']}").strip() or r['received_by__username'],
            'total': float(r['total'] or 0)
        }
        for r in top_sales_qs
    ]

    # Daily totals last 7 days
    daily_labels = []
    daily_values = []
    for i in range(6, -1, -1):
        day = now.date() - timedelta(days=i)
        day_sum = base_success.filter(payment_date__date=day).aggregate(total=Sum('amount'))['total'] or 0
        daily_labels.append(day.strftime('%b %d'))
        daily_values.append(float(day_sum))

    # Pending vs approved by salesperson
    status_by_sales = Payment.objects.values('received_by__username').annotate(
        pending=Count('id', filter=Q(status='PENDING')),
        approved=Count('id', filter=Q(status__in=['AUTHORIZED','CAPTURED']))
    ).order_by('-approved', '-pending')
    status_sales_labels = [row['received_by__username'] or 'Unassigned' for row in status_by_sales]
    status_sales_pending = [row['pending'] for row in status_by_sales]
    status_sales_approved = [row['approved'] for row in status_by_sales]

    # Sales team for filter dropdown
    sales_team = User.objects.filter(role='SALES').order_by('first_name', 'last_name')

    # Recent activity logs
    from activity_logs.models import ActivityLog
    recent_activities = ActivityLog.objects.select_related('user').order_by('-timestamp')[:15]

    context = {
        'total_clients': total_clients,
        'active_clients': active_clients,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'total_revenue': total_revenue,
        'pending_revenue': pending_revenue,
        'failed_revenue': failed_revenue,
        'client_revenue': client_revenue,
        'all_recent_payments': all_recent_payments,
        'pending_edit_requests': pending_edit_requests,
        'pending_payments': pending_payments,
        'pending_payments_count': pending_payments_count,
        'recent_clients': recent_clients,
        'recent_bookings': recent_bookings,
        'recent_applications': recent_applications,
        'pending_edits': pending_edits,
        'chart_labels': labels,
        'chart_revenue': revenue_series,
        'method_labels': method_labels,
        'method_values': method_values,
        'top_sales': top_sales,
        'daily_labels': daily_labels,
        'daily_values': daily_values,
        'status_sales_labels': status_sales_labels,
        'status_sales_pending': status_sales_pending,
        'status_sales_approved': status_sales_approved,
        'selected_method': method_filter or '',
        'selected_salesperson': salesperson_filter or '',
        'date_from': date_from or '',
        'date_to': date_to or '',
        'sales_team': sales_team,
        'recent_activities': recent_activities,
    }
    
    return render(request, 'dashboards/admin_dashboard.html', context)


@manager_required
def manager_dashboard(request):
    """
    Manager dashboard with team metrics
    """
    from clients.models import Client
    from bookings.models import Booking
    from applications.models import Application
    from payments.models import Payment
    from accounts.models import User
    
    # Team members under this manager
    team_members = User.objects.filter(manager=request.user, role='SALES')
    
    # Clients assigned to team
    team_clients = Client.objects.filter(assigned_manager=request.user)
    
    # Bookings with payment info - include bookings where:
    # 1. Client is assigned to this manager, OR
    # 2. The sales employee who recorded payment reports to this manager
    from django.db.models import Q
    team_bookings = Booking.objects.filter(
        Q(client__assigned_manager=request.user) |
        Q(assigned_to__manager=request.user)
    ).select_related('client', 'service', 'assigned_to').order_by('-booking_date').distinct()
    
    # Pending applications count for sidebar badge
    pending_count = Application.objects.filter(
        client__assigned_manager=request.user,
        status__in=['SUBMITTED', 'UNDER_REVIEW']
    ).count()
    
    # Pending payments count (awaiting manager approval) - check both client assignment and sales team
    pending_payments_count = Payment.objects.filter(
        Q(client__assigned_manager=request.user) |
        Q(received_by__manager=request.user),
        status='PENDING'
    ).distinct().count()
    
    # Get actual pending payments for display
    pending_payments = Payment.objects.filter(
        Q(client__assigned_manager=request.user) |
        Q(received_by__manager=request.user),
        status='PENDING'
    ).select_related('client', 'booking', 'received_by').order_by('-created_at').distinct()[:10]
    
    # Get all payments for team bookings and attach to booking objects
    all_team_payments = Payment.objects.filter(
        Q(client__assigned_manager=request.user) |
        Q(received_by__manager=request.user),
        booking__isnull=False
    ).select_related('booking')
    
    # Create payment lookup and annotate bookings
    booking_payments_dict = {payment.booking_id: payment for payment in all_team_payments}
    for booking in team_bookings:
        booking.payment = booking_payments_dict.get(booking.id)
    
    # Recent team applications (last 10)
    team_applications = Application.objects.filter(
        Q(client__assigned_manager=request.user) |
        Q(assigned_to__manager=request.user)
    ).select_related('client', 'scheme', 'assigned_to').order_by('-created_at').distinct()[:10]
    
    # Pending client approvals count
    pending_clients_count = Client.objects.filter(
        Q(assigned_manager=request.user) | Q(created_by__manager=request.user),
        is_approved=False
    ).count()
    
    context = {
        'team_members': team_members,
        'team_clients': team_clients,
        'team_bookings': team_bookings,
        'team_applications': team_applications,
        'pending_payments': pending_payments,
        'total_team_members': team_members.count(),
        'total_clients': team_clients.count(),
        'total_bookings': team_bookings.count(),
        'pending_count': pending_count,
        'pending_payments_count': pending_payments_count,
        'pending_clients_count': pending_clients_count,
    }
    
    return render(request, 'dashboards/manager_dashboard.html', context)


@manager_required
def pending_approvals(request):
    """
    Unified view for all pending approvals - Applications, Bookings (Payments), and Client Edit Requests
    """
    from clients.models import Client
    from bookings.models import Booking
    from applications.models import Application
    from payments.models import Payment
    from edit_requests.models import EditRequest
    from django.db.models import Q
    
    user = request.user
    
    # 1. Pending Applications (SUBMITTED status) - include entire manager team scope
    pending_applications = Application.objects.filter(
        Q(client__assigned_manager=user) | Q(client__assigned_sales__manager=user),
        status='SUBMITTED'
    ).select_related('client', 'scheme', 'assigned_to').order_by('-created_at').distinct()
    
    # 2. Pending Booking Payments (PENDING status) - include team clients
    pending_payments = Payment.objects.filter(
        (Q(client__assigned_manager=user) | Q(client__assigned_sales__manager=user) | Q(received_by__manager=user)),
        status='PENDING'
    ).select_related('booking', 'client', 'received_by').order_by('-created_at').distinct()
    
    # Get booking details for each payment
    bookings_with_pending_payments = []
    for payment in pending_payments:
        if hasattr(payment, 'booking'):
            bookings_with_pending_payments.append({
                'booking': payment.booking,
                'payment': payment
            })
    
    # 3. Pending Client Edit Requests
    pending_edit_requests = EditRequest.objects.filter(
        status='PENDING',
        entity_type='CLIENT'
    ).select_related('requested_by', 'approved_by').order_by('-created_at')
    
    # Get client details for edit requests
    edit_requests_with_details = []
    for edit_request in pending_edit_requests:
        try:
            client = Client.objects.get(pk=edit_request.entity_id)
            # Only show if client belongs to this manager's team (direct or via sales)
            if client.assigned_manager == user or (getattr(client, 'assigned_sales', None) and client.assigned_sales and client.assigned_sales.manager == user):
                edit_requests_with_details.append({
                    'edit_request': edit_request,
                    'client': client
                })
        except Client.DoesNotExist:
            pass
    
    # 4. Pending New Client Approvals
    pending_clients = Client.objects.filter(
        Q(assigned_manager=user) | Q(created_by__manager=user),
        is_approved=False
    ).select_related('assigned_sales', 'assigned_manager', 'created_by').order_by('-created_at')
    
    context = {
        'pending_applications': pending_applications,
        'pending_applications_count': pending_applications.count(),
        'bookings_with_pending_payments': bookings_with_pending_payments,
        'pending_payments_count': len(bookings_with_pending_payments),
        'edit_requests_with_details': edit_requests_with_details,
        'pending_edit_requests_count': len(edit_requests_with_details),
        'pending_clients': pending_clients,
        'pending_clients_count': pending_clients.count(),
        'total_pending': pending_applications.count() + len(bookings_with_pending_payments) + len(edit_requests_with_details) + pending_clients.count(),
    }
    
    return render(request, 'accounts/pending_approvals.html', context)


@manager_required
def team_members_list(request):
    """
    Full page view of team members under this manager
    """
    from accounts.models import User
    
    # Team members under this manager
    team_members = User.objects.filter(manager=request.user, role='SALES').select_related('manager')
    
    context = {
        'team_members': team_members,
        'total_team_members': team_members.count(),
    }
    
    return render(request, 'accounts/team_members_list.html', context)


@manager_required
def team_diagnostic(request):
    """Diagnostic page to check team relationships"""
    from accounts.models import User
    from clients.models import Client
    from bookings.models import Booking
    from payments.models import Payment
    from django.db.models import Q
    
    # Team members
    team_members = User.objects.filter(manager=request.user, role='SALES')
    
    # Clients assigned to manager
    clients_by_manager = Client.objects.filter(assigned_manager=request.user)
    
    # Clients assigned to team sales
    clients_by_sales = Client.objects.filter(assigned_sales__manager=request.user)
    
    # Bookings
    bookings_by_client_manager = Booking.objects.filter(client__assigned_manager=request.user)
    bookings_by_sales = Booking.objects.filter(assigned_to__manager=request.user)
    
    # Payments
    payments_by_client = Payment.objects.filter(client__assigned_manager=request.user, status='PENDING')
    payments_by_sales = Payment.objects.filter(received_by__manager=request.user, status='PENDING')
    
    context = {
        'team_members': team_members,
        'clients_by_manager': clients_by_manager,
        'clients_by_sales': clients_by_sales,
        'bookings_by_client_manager': bookings_by_client_manager,
        'bookings_by_sales': bookings_by_sales,
        'payments_by_client': payments_by_client,
        'payments_by_sales': payments_by_sales,
    }
    
    return render(request, 'accounts/team_diagnostic.html', context)


@manager_required
def team_clients_list(request):
    """
    Full page view of clients assigned to this manager's team
    """
    from clients.models import Client
    
    # Clients assigned to team
    team_clients = Client.objects.filter(assigned_manager=request.user).select_related('assigned_sales', 'assigned_manager')
    
    context = {
        'team_clients': team_clients,
        'total_clients': team_clients.count(),
    }
    
    return render(request, 'accounts/team_clients_list.html', context)


@sales_required
def sales_dashboard(request):
    """
    Sales dashboard with assigned clients
    """
    from clients.models import Client
    from bookings.models import Booking
    from applications.models import Application
    
    # Assigned clients (only approved ones)
    assigned_clients = Client.objects.filter(assigned_sales=request.user, is_approved=True)
    
    # Bookings for assigned clients
    my_bookings = Booking.objects.filter(client__assigned_sales=request.user).select_related('client', 'service')
    
    # Applications
    my_applications = Application.objects.filter(assigned_to=request.user).select_related('client', 'scheme')
    
    # Pending client approvals created by this sales person
    pending_clients_count = Client.objects.filter(created_by=request.user, is_approved=False).count()
    
    context = {
        'assigned_clients': assigned_clients,
        'my_bookings': my_bookings,
        'my_applications': my_applications,
        'total_clients': assigned_clients.count(),
        'total_bookings': my_bookings.count(),
        'total_applications': my_applications.count(),
        'pending_clients_count': pending_clients_count,
    }
    
    return render(request, 'dashboards/sales_dashboard.html', context)


@sales_required
def record_payment(request, booking_id):
    """Sales can record an offline payment for a booking"""
    from django.shortcuts import get_object_or_404
    from bookings.models import Booking
    from payments.models import Payment
    from decimal import Decimal

    booking = get_object_or_404(Booking, id=booking_id)

    # permission: booking must be assigned to this sales or user is manager/admin
    if getattr(booking, 'assigned_to_id', None) != request.user.id and not (getattr(request.user, 'is_manager', False) or getattr(request.user, 'is_admin', False)):
        messages.error(request, 'You are not allowed to record payment for this booking.')
        return redirect('accounts:sales_dashboard')

    # Prefill defaults
    default_amount = getattr(booking, 'final_amount', None) or getattr(booking, 'amount', None) or Decimal('0.00')

    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        reference_id = request.POST.get('reference_id')
        notes = request.POST.get('notes')
        proof = request.FILES.get('proof')

        # Create or update payment
        payment, created = Payment.objects.get_or_create(booking=booking, defaults={
            'client': booking.client,
            'amount': amount or default_amount,
            'currency': 'INR',
        })
        payment.client = booking.client
        payment.amount = amount or default_amount
        payment.payment_method = payment_method or 'UPI_QR'
        payment.reference_id = reference_id
        payment.received_by = request.user
        payment.notes = notes
        if proof:
            payment.proof = proof
        from django.utils import timezone
        payment.payment_date = timezone.now()
        # Mark as PENDING for manager/admin approval
        payment.status = 'PENDING'
        payment.save()

        # Log activity
        from activity_logs.models import ActivityLog
        ActivityLog.log_action(
            user=request.user,
            action='PAYMENT',
            entity_type='PAYMENT',
            entity_id=payment.pk,
            description=f'Recorded payment for booking {booking.booking_id} - Amount: ₹{amount or default_amount} - Method: {payment_method}',
            request=request
        )

        messages.success(request, 'Payment recorded and sent for approval.')
        # Do not change booking status until approval
        return redirect('accounts:sales_dashboard')

    return render(request, 'payments/record_payment.html', {
        'booking': booking,
        'default_amount': default_amount,
    })


@login_required
def approve_payment(request, payment_id):
    """Manager/Admin can approve recorded payments"""
    if not (getattr(request.user, 'is_manager', False) or getattr(request.user, 'is_admin', False) or request.user.is_superuser):
        messages.error(request, 'Permission denied.')
        return redirect('accounts:dashboard')
    from django.shortcuts import get_object_or_404
    from payments.models import Payment
    from activity_logs.models import ActivityLog
    from .email_utils import send_payment_approval_email
    
    payment = get_object_or_404(Payment, id=payment_id)
    old_status = payment.status
    payment.status = 'CAPTURED'
    payment.save(update_fields=['status'])
    
    # Log activity
    ActivityLog.log_action(
        user=request.user,
        action='APPROVE',
        entity_type='PAYMENT',
        entity_id=payment.id,
        description=f'Approved payment #{payment.id} for {payment.client.company_name} - Amount: ₹{payment.amount}',
        old_value=old_status,
        new_value='CAPTURED',
        request=request
    )
    
    # Send email notification
    try:
        send_payment_approval_email(payment, request.user)
    except Exception as e:
        print(f"Email notification failed: {e}")
    
    try:
        booking = payment.booking
        old_booking_status = booking.status
        booking.status = 'PAID'
        booking.save(update_fields=['status'])
        
        # Log booking status change
        ActivityLog.log_action(
            user=request.user,
            action='STATUS_CHANGE',
            entity_type='BOOKING',
            entity_id=booking.id,
            description=f'Changed booking {booking.booking_id} status to PAID due to payment approval',
            old_value=old_booking_status,
            new_value='PAID',
            request=request
        )
    except Exception:
        pass
    
    messages.success(request, 'Payment approved and notification sent.')
    # Redirect back to where the action was initiated, prefer manager dashboard if manager
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER')
    if getattr(request.user, 'is_manager', False):
        return redirect('accounts:manager_dashboard')
    if next_url:
        try:
            return redirect(next_url)
        except Exception:
            pass
    return redirect('accounts:admin_dashboard')


@login_required
def reject_payment(request, payment_id):
    """Manager/Admin can reject recorded payments"""
    if not (getattr(request.user, 'is_manager', False) or getattr(request.user, 'is_admin', False) or request.user.is_superuser):
        messages.error(request, 'Permission denied.')
        return redirect('accounts:dashboard')
    from django.shortcuts import get_object_or_404
    from payments.models import Payment
    from activity_logs.models import ActivityLog
    from .email_utils import send_payment_rejection_email
    
    payment = get_object_or_404(Payment, id=payment_id)
    old_status = payment.status
    payment.status = 'FAILED'
    payment.save(update_fields=['status'])
    
    # Log activity
    ActivityLog.log_action(
        user=request.user,
        action='REJECT',
        entity_type='PAYMENT',
        entity_id=payment.id,
        description=f'Rejected payment #{payment.id} for {payment.client.company_name} - Amount: ₹{payment.amount}',
        old_value=old_status,
        new_value='FAILED',
        request=request
    )
    
    # Send email notification
    try:
        send_payment_rejection_email(payment, request.user)
    except Exception as e:
        print(f"Email notification failed: {e}")
    
    messages.success(request, 'Payment rejected and notification sent.')
    # Redirect back to where the action was initiated, prefer manager dashboard if manager
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER')
    if getattr(request.user, 'is_manager', False):
        return redirect('accounts:manager_dashboard')
    if next_url:
        try:
            return redirect(next_url)
        except Exception:
            pass
    return redirect('accounts:admin_dashboard')


@client_required
def client_portal(request):
    """
    Client portal with applications and documents
    """
    from applications.models import Application
    from documents.models import Document
    from bookings.models import Booking
    from schemes.models import Scheme
    
    # Get client profile
    try:
        client = request.user.client_profile
    except:
        messages.error(request, 'Client profile not found.')
        return redirect('accounts:dashboard')
    
    # Check profile completion
    required_fields = ['business_type', 'sector', 'company_age', 'address_line1',
                      'city', 'state', 'pincode', 'annual_turnover', 'funding_required']
    completed_fields = sum([1 for field in required_fields if getattr(client, field)])
    completion_percentage = int((completed_fields / len(required_fields)) * 100)
    profile_incomplete = completion_percentage < 100
    
    # If profile is incomplete, redirect to profile completion page
    if profile_incomplete:
        messages.warning(request, 'Please complete your profile to access all features.')
        return redirect('clients:complete_profile')
    
    # Client data
    applications = Application.objects.filter(client=client).order_by('-application_date')
    documents = Document.objects.filter(client=client).order_by('-created_at')
    bookings = Booking.objects.filter(client=client).order_by('-booking_date')
    
    # Recommended schemes (AI)
    all_schemes = Scheme.objects.filter(status='ACTIVE')
    recommended_schemes = []
    for scheme in all_schemes:
        score = scheme.get_recommended_for_client(client)
        if score > 50:  # Only show schemes with >50% match
            is_eligible, reasons = scheme.check_client_eligibility(client)
            recommended_schemes.append({
                'scheme': scheme,
                'score': score,
                'is_eligible': is_eligible,
                'reasons': reasons
            })
    
    # Sort by score descending
    recommended_schemes.sort(key=lambda x: x['score'], reverse=True)
    recommended_schemes = recommended_schemes[:3]  # Top 3
    
    context = {
        'client': client,
        'applications': applications,
        'documents': documents,
        'bookings': bookings,
        'recommended_schemes': recommended_schemes,
        'profile_incomplete': profile_incomplete,
        'completion_percentage': completion_percentage,
    }
    
    return render(request, 'dashboards/client_portal.html', context)


@login_required
def superuser_dashboard(request):
    """
    Dedicated dashboard for superuser (site owner) distinct from Admin role users.
    """
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('accounts:dashboard')

    # Reuse admin analytics plus include system/user metrics
    from clients.models import Client
    from bookings.models import Booking
    from applications.models import Application
    from payments.models import Payment
    from edit_requests.models import EditRequest
    from django.db.models import Sum
    from accounts.models import User

    total_clients = Client.objects.count()
    total_bookings = Booking.objects.count()
    total_applications = Application.objects.count()
    total_revenue = Payment.objects.filter(status__in=['AUTHORIZED', 'CAPTURED']).aggregate(Sum('amount'))['amount__sum'] or 0
    pending_edit_requests = EditRequest.objects.filter(status='PENDING').count()

    # User metrics
    total_users = User.objects.count()
    admins = User.objects.filter(role='ADMIN').count()
    managers = User.objects.filter(role='MANAGER').count()
    sales = User.objects.filter(role='SALES').count()
    clients_count = User.objects.filter(role='CLIENT').count()
    staff_count = User.objects.filter(is_staff=True).count()

    context = {
        'total_clients': total_clients,
        'total_bookings': total_bookings,
        'total_applications': total_applications,
        'total_revenue': total_revenue,
        'pending_edit_requests': pending_edit_requests,
        'total_users': total_users,
        'admins': admins,
        'managers': managers,
        'sales': sales,
        'clients_count': clients_count,
        'staff_count': staff_count,
    }

    return render(request, 'dashboards/superuser_dashboard.html', context)


@admin_required
def owner_dashboard(request):
    """
    Owner Dashboard: accessible only to Admin role users flagged as is_owner.
    Distinct from superuser dashboard; focuses on business KPIs.
    """
    user_role = getattr(request.user, 'role', '')
    if not (getattr(request.user, 'is_owner', False) or user_role.upper() == 'OWNER'):
        messages.error(request, 'Only the company owner can access this dashboard.')
        return redirect('accounts:admin_dashboard')

    from clients.models import Client, ClientCredential
    from bookings.models import Booking
    from applications.models import Application
    from payments.models import Payment
    from django.db.models import Sum, Count, Q
    from django.utils import timezone
    from datetime import timedelta

    total_clients = Client.objects.count()
    active_clients = Client.objects.filter(status='ACTIVE').count()
    total_bookings = Booking.objects.count()
    total_applications = Application.objects.count()
    
    # Get unsent client credentials
    unsent_credentials = ClientCredential.objects.filter(is_sent=False).select_related('client').order_by('-created_at')
    
    # Filter support
    method_filter = request.GET.get('method')
    base_success = Payment.objects.filter(status__in=['AUTHORIZED', 'CAPTURED'])
    if method_filter:
        base_success = base_success.filter(payment_method=method_filter)
    total_revenue = base_success.aggregate(Sum('amount'))['amount__sum'] or 0

    # Live client revenue totals (pitched/received/pending with GST)
    client_revenue = Client.objects.aggregate(
        total_pitched=Sum('total_pitched_amount'),
        total_with_gst=Sum('total_with_gst'),
        total_received=Sum('received_amount'),
        total_pending=Sum('pending_amount'),
    )
    client_revenue = {k: v or 0 for k, v in client_revenue.items()}

    # Last 10 days client revenue (new clients only)
    ten_days_ago = timezone.now() - timedelta(days=10)
    last10_revenue = Client.objects.filter(created_at__gte=ten_days_ago).aggregate(
        total_pitched=Sum('total_pitched_amount'),
        total_with_gst=Sum('total_with_gst'),
        total_received=Sum('received_amount'),
        total_pending=Sum('pending_amount'),
    )
    last10_revenue = {k: v or 0 for k, v in last10_revenue.items()}

    top_sectors = Client.objects.values('sector').annotate(c=Count('id')).order_by('-c')[:5]

    # Revenue by month (last 6 months)
    now = timezone.now()
    labels = []
    revenue_series = []
    for i in range(5, -1, -1):
        start = (now.replace(day=1) - timedelta(days=30*i)).replace(day=1)
        if start.month == 12:
            end = start.replace(year=start.year+1, month=1, day=1)
        else:
            end = start.replace(month=start.month+1, day=1)
        month_qs = base_success.filter(payment_date__gte=start, payment_date__lt=end)
        month_sum = month_qs.aggregate(Sum('amount'))['amount__sum'] or 0
        labels.append(start.strftime('%b %Y'))
        revenue_series.append(float(month_sum))

    # Revenue by method
    method_breakdown_qs = Payment.objects.filter(status__in=['AUTHORIZED','CAPTURED']).values('payment_method').annotate(total=Sum('amount')).order_by('-total')
    method_labels = [row['payment_method'] or 'UNKNOWN' for row in method_breakdown_qs]
    method_values = [float(row['total'] or 0) for row in method_breakdown_qs]

    # Top sales by revenue
    top_sales_qs = Payment.objects.filter(status__in=['AUTHORIZED','CAPTURED'], received_by__isnull=False).values('received_by__username', 'received_by__first_name', 'received_by__last_name').annotate(total=Sum('amount')).order_by('-total')[:5]
    top_sales = [
        {
            'name': (f"{r['received_by__first_name']} {r['received_by__last_name']}").strip() or r['received_by__username'],
            'total': float(r['total'] or 0)
        }
        for r in top_sales_qs
    ]

    # Daily totals last 7 days
    daily_labels = []
    daily_values = []
    for i in range(6, -1, -1):
        day = now.date() - timedelta(days=i)
        day_sum = base_success.filter(payment_date__date=day).aggregate(total=Sum('amount'))['total'] or 0
        daily_labels.append(day.strftime('%b %d'))
        daily_values.append(float(day_sum))

    # Pending vs approved by salesperson
    status_by_sales = Payment.objects.values('received_by__username').annotate(
        pending=Count('id', filter=Q(status='PENDING')),
        approved=Count('id', filter=Q(status__in=['AUTHORIZED','CAPTURED']))
    ).order_by('-approved', '-pending')
    status_sales_labels = [row['received_by__username'] or 'Unassigned' for row in status_by_sales]
    status_sales_pending = [row['pending'] for row in status_by_sales]
    status_sales_approved = [row['approved'] for row in status_by_sales]

    # Pending payments summary for owner view
    pending_payments_count = Payment.objects.filter(status='PENDING').count()
    
    # Revenue breakdown
    pending_revenue = Payment.objects.filter(status='PENDING').aggregate(Sum('amount'))['amount__sum'] or 0
    failed_revenue = Payment.objects.filter(status='FAILED').aggregate(Sum('amount'))['amount__sum'] or 0
    all_recent_payments = Payment.objects.select_related('client', 'booking', 'received_by').order_by('-created_at')[:20]

    context = {
        'total_clients': total_clients,
        'active_clients': active_clients,
        'total_bookings': total_bookings,
        'total_applications': total_applications,
        'total_revenue': total_revenue,
        'client_revenue': client_revenue,
        'last10_revenue': last10_revenue,
        'top_sectors': top_sectors,
        'chart_labels': labels,
        'chart_revenue': revenue_series,
        'method_labels': method_labels,
        'method_values': method_values,
        'top_sales': top_sales,
        'daily_labels': daily_labels,
        'daily_values': daily_values,
        'status_sales_labels': status_sales_labels,
        'status_sales_pending': status_sales_pending,
        'status_sales_approved': status_sales_approved,
        'pending_payments_count': pending_payments_count,
        'pending_revenue': pending_revenue,
        'failed_revenue': failed_revenue,
        'all_recent_payments': all_recent_payments,
        'selected_method': method_filter or '',
        'unsent_credentials': unsent_credentials,
    }

    return render(request, 'dashboards/owner_dashboard.html', context)


@admin_required
def mark_credential_as_sent(request, credential_id):
    """Mark client credential as sent by owner/admin."""
    from clients.models import ClientCredential
    
    credential = get_object_or_404(ClientCredential, id=credential_id)
    
    if request.method == 'POST':
        login_url = getattr(settings, 'CLIENT_LOGIN_URL', None) or request.build_absolute_uri(reverse('accounts:login'))
        email_sent = send_client_credentials_email(credential, login_url=login_url)
        if email_sent:
            credential.mark_as_sent(request.user)
            messages.success(
                request,
                f'Login email sent to {credential.email} for {credential.client.company_name}.',
            )
        else:
            messages.error(
                request,
                f'Could not send email to {credential.email}. Please verify SMTP settings and try again.',
            )
        return redirect('accounts:owner_dashboard')
    
    return redirect('accounts:owner_dashboard')


@admin_required
def users_list(request):
    """Admin/Owner: list all users with role and manager relationships."""
    from accounts.models import User
    from django.core.paginator import Paginator
    from django.db.models import Q

    users_qs = User.objects.select_related('manager').order_by('-date_joined')

    # Filters
    role = request.GET.get('role', '').strip()
    manager_id = request.GET.get('manager', '').strip()
    q = request.GET.get('q', '').strip()
    page_size = request.GET.get('page_size') or '50'
    try:
        page_size = max(1, min(200, int(page_size)))
    except Exception:
        page_size = 50

    if role:
        users_qs = users_qs.filter(role=role)
    if manager_id:
        try:
            users_qs = users_qs.filter(manager_id=int(manager_id))
        except Exception:
            pass
    if q:
        users_qs = users_qs.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(username__icontains=q) | Q(email__icontains=q)
        )

    page_number = request.GET.get('page')
    paginator = Paginator(users_qs, page_size)
    users_page = paginator.get_page(page_number)

    # Simple role counts for header badges (dict of role -> count)
    from collections import Counter
    role_counts = Counter(users_qs.values_list('role', flat=True))

    # Managers list for filter dropdown
    managers = User.objects.filter(role__in=['ADMIN','MANAGER']).order_by('first_name','last_name')

    return render(request, 'accounts/users_list.html', {
        'users_page': users_page,
        'role_counts_items': list(role_counts.items()),
        'paginator': paginator,
        'filter_role': role,
        'filter_manager': manager_id,
        'filter_q': q,
        'page_size': page_size,
        'managers': managers,
    })


@login_required
def profile_view(request):
    """View/update current user's profile"""
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def change_password(request):
    """Allow logged-in users to change password"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Keep user logged in after password change
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


# Export Views
@staff_required
def export_clients(request):
    """Export clients to CSV"""
    from clients.models import Client
    from .utils import export_to_csv
    
    queryset = Client.objects.all().select_related('assigned_manager', 'assigned_sales')
    
    # Apply filters if provided
    status_filter = request.GET.get('status')
    sector_filter = request.GET.get('sector')
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    if sector_filter:
        queryset = queryset.filter(sector=sector_filter)
    
    fields = [
        {'name': 'id', 'label': 'ID'},
        {'name': 'company_name', 'label': 'Company Name'},
        {'name': 'contact_person', 'label': 'Contact Person'},
        {'name': 'email', 'label': 'Email'},
        {'name': 'phone', 'label': 'Phone'},
        {'name': 'get_business_type_display', 'label': 'Business Type'},
        {'name': 'get_sector_display', 'label': 'Sector'},
        {'name': 'funding_required', 'label': 'Funding Required (Lakhs)'},
        {'name': 'get_status_display', 'label': 'Status'},
        {'name': 'assigned_manager', 'label': 'Manager', 'accessor': lambda obj: obj.assigned_manager.get_full_name() if obj.assigned_manager else 'N/A'},
        {'name': 'assigned_sales', 'label': 'Sales', 'accessor': lambda obj: obj.assigned_sales.get_full_name() if obj.assigned_sales else 'N/A'},
        {'name': 'created_at', 'label': 'Created Date', 'accessor': lambda obj: obj.created_at.strftime('%Y-%m-%d %H:%M')},
    ]
    
    return export_to_csv(queryset, fields, 'clients')


@staff_required
def export_bookings(request):
    """Export bookings to CSV"""
    from bookings.models import Booking
    from .utils import export_to_csv
    
    queryset = Booking.objects.all().select_related('client', 'service', 'assigned_to')
    
    # Apply filters
    status_filter = request.GET.get('status')
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    
    fields = [
        {'name': 'booking_id', 'label': 'Booking ID'},
        {'name': 'client', 'label': 'Client', 'accessor': lambda obj: obj.client.company_name},
        {'name': 'service', 'label': 'Service', 'accessor': lambda obj: obj.service.name},
        {'name': 'amount', 'label': 'Amount'},
        {'name': 'discount', 'label': 'Discount'},
        {'name': 'final_amount', 'label': 'Final Amount'},
        {'name': 'get_status_display', 'label': 'Status'},
        {'name': 'assigned_to', 'label': 'Assigned To', 'accessor': lambda obj: obj.assigned_to.get_full_name() if obj.assigned_to else 'N/A'},
        {'name': 'booking_date', 'label': 'Booking Date', 'accessor': lambda obj: obj.booking_date.strftime('%Y-%m-%d')},
        {'name': 'created_at', 'label': 'Created Date', 'accessor': lambda obj: obj.created_at.strftime('%Y-%m-%d %H:%M')},
    ]
    
    return export_to_csv(queryset, fields, 'bookings')


@staff_required
def export_payments(request):
    """Export payments to CSV"""
    from payments.models import Payment
    from .utils import export_to_csv
    
    queryset = Payment.objects.all().select_related('client', 'booking', 'received_by')
    
    # Apply filters
    status_filter = request.GET.get('status')
    method_filter = request.GET.get('method')
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    if method_filter:
        queryset = queryset.filter(payment_method=method_filter)
    
    fields = [
        {'name': 'id', 'label': 'Payment ID'},
        {'name': 'client', 'label': 'Client', 'accessor': lambda obj: obj.client.company_name},
        {'name': 'booking', 'label': 'Booking', 'accessor': lambda obj: obj.booking.booking_id if obj.booking else 'N/A'},
        {'name': 'amount', 'label': 'Amount'},
        {'name': 'currency', 'label': 'Currency'},
        {'name': 'get_payment_method_display', 'label': 'Payment Method'},
        {'name': 'get_status_display', 'label': 'Status'},
        {'name': 'reference_id', 'label': 'Reference ID'},
        {'name': 'received_by', 'label': 'Received By', 'accessor': lambda obj: obj.received_by.get_full_name() if obj.received_by else 'N/A'},
        {'name': 'payment_date', 'label': 'Payment Date', 'accessor': lambda obj: obj.payment_date.strftime('%Y-%m-%d %H:%M') if obj.payment_date else 'N/A'},
        {'name': 'notes', 'label': 'Notes'},
    ]
    
    return export_to_csv(queryset, fields, 'payments')


@admin_required
def export_dashboard_data(request):
    """Export filtered dashboard revenue data to CSV"""
    from payments.models import Payment
    from django.http import HttpResponse
    import csv
    from datetime import datetime
    
    # Get filters from request
    method_filter = request.GET.get('method')
    salesperson_filter = request.GET.get('salesperson')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    # Build queryset
    queryset = Payment.objects.filter(status__in=['AUTHORIZED', 'CAPTURED']).select_related('client', 'booking', 'received_by')
    
    if method_filter:
        queryset = queryset.filter(payment_method=method_filter)
    if salesperson_filter:
        queryset = queryset.filter(received_by_id=salesperson_filter)
    if date_from:
        from django.utils.dateparse import parse_date
        parsed_from = parse_date(date_from)
        if parsed_from:
            queryset = queryset.filter(payment_date__date__gte=parsed_from)
    if date_to:
        from django.utils.dateparse import parse_date
        parsed_to = parse_date(date_to)
        if parsed_to:
            queryset = queryset.filter(payment_date__date__lte=parsed_to)
    
    # Create CSV
    response = HttpResponse(content_type='text/csv')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    response['Content-Disposition'] = f'attachment; filename="dashboard_revenue_{timestamp}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Payment ID', 'Client', 'Booking', 'Amount', 'Method', 'Salesperson', 'Payment Date', 'Status'])
    
    for payment in queryset:
        writer.writerow([
            payment.id,
            payment.client.company_name,
            payment.booking.booking_id if payment.booking else 'N/A',
            payment.amount,
            payment.get_payment_method_display(),
            payment.received_by.get_full_name() if payment.received_by else 'N/A',
            payment.payment_date.strftime('%Y-%m-%d %H:%M') if payment.payment_date else 'N/A',
            payment.get_status_display(),
        ])
    
    return response


@staff_required
def global_search(request):
    """Global search across clients, bookings, and applications"""
    from clients.models import Client
    from bookings.models import Booking
    from applications.models import Application
    from django.db.models import Q
    
    query = request.GET.get('q', '').strip()
    
    if not query:
        return render(request, 'accounts/search_results.html', {
            'query': '',
            'clients': [],
            'bookings': [],
            'applications': [],
        })
    
    # Search clients
    clients = Client.objects.filter(
        Q(company_name__icontains=query) |
        Q(contact_person__icontains=query) |
        Q(contact_email__icontains=query) |
        Q(contact_phone__icontains=query) |
        Q(pan_number__icontains=query) |
        Q(gst_number__icontains=query)
    ).select_related('assigned_manager', 'assigned_sales')[:10]
    
    # Search bookings
    bookings = Booking.objects.filter(
        Q(booking_id__icontains=query) |
        Q(client__company_name__icontains=query) |
        Q(service__name__icontains=query)
    ).select_related('client', 'service', 'assigned_to')[:10]
    
    # Search applications
    applications = Application.objects.filter(
        Q(application_id__icontains=query) |
        Q(client__company_name__icontains=query) |
        Q(scheme__name__icontains=query)
    ).select_related('client', 'scheme', 'assigned_to')[:10]
    
    context = {
        'query': query,
        'clients': clients,
        'bookings': bookings,
        'applications': applications,
        'total_results': clients.count() + bookings.count() + applications.count(),
    }
    
    return render(request, 'accounts/search_results.html', context)


@admin_required
def reports_dashboard(request):
    """Advanced reporting dashboard"""
    from clients.models import Client
    from bookings.models import Booking
    from applications.models import Application
    from payments.models import Payment
    from django.db.models import Sum, Count, Avg, Q
    from django.db.models.functions import TruncMonth, TruncWeek
    from django.utils import timezone
    from datetime import timedelta
    from collections import defaultdict
    
    # Date range filter
    period = request.GET.get('period', '30')  # Default 30 days
    try:
        days = int(period)
    except:
        days = 30
    
    start_date = timezone.now() - timedelta(days=days)
    
    # Revenue Analysis
    revenue_data = Payment.objects.filter(
        status__in=['AUTHORIZED', 'CAPTURED'],
        payment_date__gte=start_date
    ).aggregate(
        total=Sum('amount'),
        count=Count('id'),
        average=Avg('amount')
    )
    
    # Revenue by method
    revenue_by_method = Payment.objects.filter(
        status__in=['AUTHORIZED', 'CAPTURED'],
        payment_date__gte=start_date
    ).values('payment_method').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')
    
    # Monthly revenue trend (last 12 months)
    monthly_revenue = Payment.objects.filter(
        status__in=['AUTHORIZED', 'CAPTURED'],
        payment_date__gte=timezone.now() - timedelta(days=365)
    ).annotate(
        month=TruncMonth('payment_date')
    ).values('month').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('month')
    
    # Sales Performance
    sales_performance = Payment.objects.filter(
        status__in=['AUTHORIZED', 'CAPTURED'],
        payment_date__gte=start_date,
        received_by__isnull=False
    ).values(
        'received_by__username',
        'received_by__first_name',
        'received_by__last_name'
    ).annotate(
        total_revenue=Sum('amount'),
        total_payments=Count('id'),
        avg_payment=Avg('amount')
    ).order_by('-total_revenue')[:10]
    
    # Client Acquisition
    new_clients = Client.objects.filter(
        created_at__gte=start_date
    ).annotate(
        week=TruncWeek('created_at')
    ).values('week').annotate(
        count=Count('id')
    ).order_by('week')
    
    # Client by sector
    clients_by_sector = Client.objects.values('sector').annotate(
        count=Count('id'),
        active_count=Count('id', filter=Q(status='ACTIVE'))
    ).order_by('-count')
    
    # Booking Statistics
    booking_stats = Booking.objects.filter(
        created_at__gte=start_date
    ).aggregate(
        total=Count('id'),
        pending=Count('id', filter=Q(status='PENDING')),
        confirmed=Count('id', filter=Q(status='CONFIRMED')),
        paid=Count('id', filter=Q(status='PAID')),
        completed=Count('id', filter=Q(status='COMPLETED')),
        cancelled=Count('id', filter=Q(status='CANCELLED')),
        total_value=Sum('final_amount')
    )
    
    # Application Statistics
    app_stats = Application.objects.filter(
        created_at__gte=start_date
    ).aggregate(
        total=Count('id'),
        draft=Count('id', filter=Q(status='DRAFT')),
        submitted=Count('id', filter=Q(status='SUBMITTED')),
        under_review=Count('id', filter=Q(status='UNDER_REVIEW')),
        approved=Count('id', filter=Q(status='APPROVED')),
        rejected=Count('id', filter=Q(status='REJECTED')),
        total_amount=Sum('applied_amount')
    )
    
    # Top schemes by applications
    top_schemes = Application.objects.filter(
        created_at__gte=start_date
    ).values(
        'scheme__name'
    ).annotate(
        app_count=Count('id'),
        approved_count=Count('id', filter=Q(status='APPROVED')),
        total_amount=Sum('applied_amount')
    ).order_by('-app_count')[:10]
    
    # Conversion rates
    total_clients = Client.objects.filter(created_at__gte=start_date).count()
    total_bookings = Booking.objects.filter(created_at__gte=start_date).count()
    paid_bookings = Booking.objects.filter(created_at__gte=start_date, status='PAID').count()
    
    client_to_booking_rate = (total_bookings / total_clients * 100) if total_clients > 0 else 0
    booking_to_payment_rate = (paid_bookings / total_bookings * 100) if total_bookings > 0 else 0
    
    # Format data for charts
    monthly_labels = [item['month'].strftime('%b %Y') for item in monthly_revenue]
    monthly_values = [float(item['total'] or 0) for item in monthly_revenue]
    
    weekly_labels = [item['week'].strftime('%b %d') for item in new_clients]
    weekly_values = [item['count'] for item in new_clients]
    
    context = {
        'period_days': days,
        'revenue_data': revenue_data,
        'revenue_by_method': revenue_by_method,
        'sales_performance': sales_performance,
        'booking_stats': booking_stats,
        'app_stats': app_stats,
        'top_schemes': top_schemes,
        'clients_by_sector': clients_by_sector,
        'client_to_booking_rate': round(client_to_booking_rate, 1),
        'booking_to_payment_rate': round(booking_to_payment_rate, 1),
        'monthly_labels': monthly_labels,
        'monthly_values': monthly_values,
        'weekly_labels': weekly_labels,
        'weekly_values': weekly_values,
        'total_clients': total_clients,
        'total_bookings': total_bookings,
        'paid_bookings': paid_bookings,
    }
    
    return render(request, 'accounts/reports_dashboard.html', context)


@staff_required
def route_directory(request):
    """Staff-only page listing key routes per role for quick reference."""
    routes = {
        'superuser': [
            {'path': '/dashboard/superuser/', 'name': 'superuser_dashboard', 'desc': 'Full system visibility and analytics.'},
        ],
        'owner': [
            {'path': '/dashboard/owner/', 'name': 'owner_dashboard', 'desc': 'Company-level metrics and management access.'},
        ],
        'admin': [
            {'path': '/dashboard/admin/', 'name': 'admin_dashboard', 'desc': 'Central dashboard overview.'},
            {'path': '/reports/', 'name': 'reports_dashboard', 'desc': 'Analytics and business metrics.'},
            {'path': '/export/clients/', 'name': 'export_clients', 'desc': 'Export client data.'},
            {'path': '/export/bookings/', 'name': 'export_bookings', 'desc': 'Export bookings.'},
            {'path': '/export/payments/', 'name': 'export_payments', 'desc': 'Export payments.'},
            {'path': '/export/dashboard/', 'name': 'export_dashboard_data', 'desc': 'Export revenue data for dashboard KPIs.'},
        ],
        'manager': [
            {'path': '/dashboard/manager/', 'name': 'manager_dashboard', 'desc': 'Team overview dashboard.'},
            {'path': '/applications/pending/', 'name': 'pending_applications', 'desc': 'Pending application approvals.'},
            {'path': '/applications/team/', 'name': 'team_applications_list', 'desc': 'Team applications list.'},
            {'path': '/team/members/', 'name': 'team_members_list', 'desc': 'Assigned sales employees.'},
            {'path': '/team/clients/', 'name': 'team_clients_list', 'desc': 'Team clients.'},
            {'path': '/bookings/team/', 'name': 'team_bookings_list', 'desc': 'Team bookings overview.'},
            {'path': '/documents/team/', 'name': 'team_documents_list', 'desc': 'Team documents.'},
            {'path': '/payments/team/', 'name': 'team_payments_list', 'desc': 'Team payments.'},
            {'path': '/team/diagnostic/', 'name': 'team_diagnostic', 'desc': 'Team diagnostic.'},
        ],
        'sales': [
            {'path': '/dashboard/sales/', 'name': 'sales_dashboard', 'desc': 'Sales dashboard.'},
            {'path': '/bookings/sales/', 'name': 'sales_bookings_list', 'desc': 'My bookings.'},
            {'path': '/applications/sales/', 'name': 'sales_applications_list', 'desc': 'My applications.'},
        ],
        'client': [
            {'path': '/dashboard/client/', 'name': 'client_portal', 'desc': 'Client portal.'},
            {'path': '/bookings/client/', 'name': 'client_bookings_list', 'desc': 'My bookings.'},
            {'path': '/applications/client/', 'name': 'client_applications_list', 'desc': 'My applications.'},
            {'path': '/documents/client/', 'name': 'client_documents_list', 'desc': 'Documents.'},
            {'path': '/payments/client/', 'name': 'client_payments_list', 'desc': 'Payments.'},
            {'path': '/schemes/', 'name': 'scheme_list', 'desc': 'Browse schemes.'},
        ],
        'applications': [
            {'path': '/applications/admin/<pk>/', 'name': 'admin_application_detail', 'desc': 'Admin application detail (alias).'},
            {'path': '/applications/manager/<pk>/', 'name': 'manager_application_detail', 'desc': 'Manager application detail.'},
            {'path': '/applications/sales/<pk>/', 'name': 'sales_application_detail', 'desc': 'Sales application detail.'},
            {'path': '/applications/client/<pk>/', 'name': 'client_application_detail', 'desc': 'Client application detail.'},
        ],
        'bookings': [
            {'path': '/bookings/<id>/', 'name': 'booking_detail', 'desc': 'Role-scoped booking detail.'},
        ],
        'documents': [
            {'path': '/documents/<pk>/', 'name': 'document_detail', 'desc': 'Document detail.'},
            {'path': '/documents/<pk>/download/', 'name': 'document_download', 'desc': 'Download file.'},
        ],
        'payments': [
            {'path': '/payments/<pk>/', 'name': 'payment_detail', 'desc': 'Payment detail.'},
            {'path': '/payments/<payment_id>/approve/', 'name': 'approve_payment', 'desc': 'Approve payment.'},
            {'path': '/payments/<payment_id>/reject/', 'name': 'reject_payment', 'desc': 'Reject payment.'},
        ],
        'api': [
            {'path': '/api/schema/', 'name': 'schema', 'desc': 'OpenAPI schema JSON.'},
            {'path': '/api/docs/', 'name': 'swagger-ui', 'desc': 'Swagger UI.'},
            {'path': '/api/redoc/', 'name': 'redoc', 'desc': 'Redoc UI.'},
        ],
        'pdf': [
            {'path': '/pdf/payment/<payment_id>/', 'name': 'download_payment_receipt', 'desc': 'Payment receipt PDF.'},
            {'path': '/pdf/booking/<booking_id>/', 'name': 'download_booking_confirmation', 'desc': 'Booking confirmation PDF.'},
            {'path': '/pdf/application/<application_id>/', 'name': 'download_application_form', 'desc': 'Application form PDF.'},
        ],
    }
    return render(request, 'accounts/route_directory.html', {'routes': routes})


# =============================================================================
# PDF Generation Views
# =============================================================================

@login_required
@user_passes_test(lambda u: u.is_staff)
def download_payment_receipt_pdf(request, payment_id):
    """Download payment receipt PDF"""
    from payments.models import Payment
    from .pdf_utils import generate_payment_receipt_pdf
    
    try:
        payment = Payment.objects.select_related('client', 'booking').get(id=payment_id)
        
        # Check permission
        if not request.user.is_staff and payment.client.salesperson != request.user:
            messages.error(request, 'You do not have permission to view this receipt.')
            return redirect('accounts:dashboard')
        
        return generate_payment_receipt_pdf(payment)
    
    except Payment.DoesNotExist:
        messages.error(request, 'Payment not found.')
        return redirect('accounts:admin_dashboard')


@login_required
@user_passes_test(lambda u: u.is_staff)
def download_booking_confirmation_pdf(request, booking_id):
    """Download booking confirmation PDF"""
    from bookings.models import Booking
    from .pdf_utils import generate_booking_confirmation_pdf
    
    try:
        booking = Booking.objects.select_related('client', 'service').get(id=booking_id)
        
        # Check permission
        if not request.user.is_staff and booking.client.salesperson != request.user:
            messages.error(request, 'You do not have permission to view this booking.')
            return redirect('accounts:dashboard')
        
        return generate_booking_confirmation_pdf(booking)
    
    except Booking.DoesNotExist:
        messages.error(request, 'Booking not found.')
        return redirect('accounts:admin_dashboard')


@login_required
@user_passes_test(lambda u: u.is_staff)
def download_application_form_pdf(request, application_id):
    """Download application form PDF"""
    from applications.models import Application
    from .pdf_utils import generate_application_form_pdf
    
    try:
        application = Application.objects.select_related('client', 'scheme').get(id=application_id)
        
        # Check permission
        if not request.user.is_staff and application.client.salesperson != request.user:
            messages.error(request, 'You do not have permission to view this application.')
            return redirect('accounts:dashboard')
        
        return generate_application_form_pdf(application)
    
    except Application.DoesNotExist:
        messages.error(request, 'Application not found.')
        return redirect('accounts:admin_dashboard')
