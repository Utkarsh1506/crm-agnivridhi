from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application
from schemes.models import Scheme
from clients.models import Client
from django.utils import timezone
from accounts.views import manager_required, staff_required, client_required, sales_required

@login_required
def application_list(request):
    """Deprecated generic endpoint: redirect to role-specific page for privacy."""
    user = request.user
    if getattr(user, 'is_client', False):
        return redirect('client_applications_list')
    elif getattr(user, 'role', None) == 'SALES':
        return redirect('sales_applications_list')
    elif getattr(user, 'role', None) in ['MANAGER', 'ADMIN']:
        return redirect('team_applications_list')
    return redirect('dashboard')


@client_required
def client_applications_list(request):
    client = request.user.client_profile
    applications = Application.objects.filter(client=client).order_by('-created_at')
    return render(request, 'applications/application_list.html', {'applications': applications})


@sales_required
def sales_applications_list(request):
    applications = Application.objects.filter(assigned_to=request.user).order_by('-created_at')
    return render(request, 'applications/application_list.html', {'applications': applications})


@staff_required
def create_application_from_booking(request, booking_id: int):
    """Staff creates an application from a paid/approved booking."""
    from bookings.models import Booking
    from payments.models import Payment

    booking = get_object_or_404(Booking, id=booking_id)

    # Validate: must have payment captured (manager approved)
    payment = getattr(booking, 'payment', None)
    if not payment or payment.status != 'CAPTURED':
        messages.error(request, 'Payment must be approved before creating an application.')
        return redirect('sales_dashboard')

    # Pick a scheme id from internal notes if available
    scheme = None
    if booking.internal_notes and 'SCHEME_ID=' in booking.internal_notes:
        try:
            scheme_id = int(booking.internal_notes.split('SCHEME_ID=')[-1].split()[0])
            scheme = Scheme.objects.filter(id=scheme_id).first()
        except Exception:
            scheme = None

    client = booking.client

    if request.method == 'POST':
        applied_amount = request.POST.get('applied_amount')
        purpose = request.POST.get('purpose', '')

        if not scheme:
            messages.error(request, 'Scheme missing. Please select a scheme.')
            return redirect('create_application_from_booking', booking_id=booking.id)

        try:
            # Create application referencing booking and assign to current sales
            application = Application.objects.create(
                client=client,
                scheme=scheme,
                applied_amount=applied_amount,
                purpose=purpose,
                status='SUBMITTED',
                created_by=request.user,
                assigned_to=getattr(booking, 'assigned_to', None)
            )

            # Notify manager for approval
            if getattr(client, 'assigned_manager', None):
                _notify_manager_for_approval(application, client.assigned_manager)

            messages.success(request, f'Application created from booking {booking.booking_id}.')
            return redirect('application_detail', pk=application.pk)
        except Exception as e:
            messages.error(request, f'Error creating application: {str(e)}')

    return render(request, 'applications/create_application_from_booking.html', {
        'booking': booking,
        'client': booking.client,
        'scheme': scheme,
    })

@manager_required
def team_applications_list(request):
    """Manager view: All applications for team clients"""
    user = request.user
    
    # Get all clients assigned to this manager's team
    team_clients = Client.objects.filter(assigned_manager=user).select_related('assigned_sales', 'assigned_manager')
    
    # Get applications for these clients
    applications = Application.objects.filter(client__in=team_clients).select_related('client', 'client__assigned_sales', 'scheme', 'assigned_to').order_by('-created_at')
    
    # Statistics
    from django.db.models import Sum, Count, Q
    stats = applications.aggregate(
        total_amount=Sum('applied_amount'),
        submitted_count=Count('id', filter=Q(status='SUBMITTED')),
        under_review_count=Count('id', filter=Q(status='UNDER_REVIEW')),
        approved_count=Count('id', filter=Q(status='APPROVED')),
        rejected_count=Count('id', filter=Q(status='REJECTED')),
    )
    
    # Group by client
    applications_by_client = {}
    for app in applications:
        client_name = app.client.company_name
        if client_name not in applications_by_client:
            applications_by_client[client_name] = {
                'client': app.client,
                'applications': []
            }
        applications_by_client[client_name]['applications'].append(app)
    
    context = {
        'applications': applications,
        'applications_by_client': applications_by_client,
        'total_applications': applications.count(),
        'total_clients': team_clients.count(),
        'stats': stats,
    }
    return render(request, 'applications/team_applications_list.html', context)


@login_required
def application_detail(request, pk):
    """Deprecated generic endpoint: redirect to role-specific detail page."""
    user = request.user
    if getattr(user, 'is_client', False):
        return redirect('client_application_detail', pk=pk)
    elif getattr(user, 'role', None) == 'SALES':
        return redirect('sales_application_detail', pk=pk)
    elif getattr(user, 'role', None) == 'MANAGER':
        return redirect('manager_application_detail', pk=pk)
    elif getattr(user, 'role', None) == 'ADMIN':
        return redirect('owner_application_detail', pk=pk)
    return redirect('dashboard')


@client_required
def client_application_detail(request, pk):
    """Client view: View their own application details"""
    application = get_object_or_404(Application, pk=pk)
    
    # Check permissions - client can only view their own applications
    if application.client.user != request.user:
        messages.error(request, "You don't have permission to view this application.")
        return redirect('client_applications_list')
    
    context = {
        'application': application,
        'user_role': 'client',
    }
    return render(request, 'applications/application_detail.html', context)


@sales_required
def sales_application_detail(request, pk):
    """Sales view: View applications assigned to them"""
    application = get_object_or_404(Application, pk=pk)
    
    # Check permissions - sales can view applications assigned to them
    if application.assigned_to != request.user:
        messages.error(request, "You don't have permission to view this application.")
        return redirect('sales_applications_list')
    
    context = {
        'application': application,
        'user_role': 'sales',
    }
    return render(request, 'applications/application_detail.html', context)


@manager_required
def manager_application_detail(request, pk):
    """Manager view: View team applications with approval controls"""
    application = get_object_or_404(Application, pk=pk)
    
    # Check permissions - manager can view applications from their team clients
    if application.client.assigned_manager != request.user:
        messages.error(request, "You don't have permission to view this application.")
        return redirect('team_applications_list')
    
    context = {
        'application': application,
        'user_role': 'manager',
        'can_approve': True,  # Manager has approval rights
    }
    return render(request, 'applications/application_detail.html', context)


@staff_required
def owner_application_detail(request, pk):
    """Owner/Admin view: View any application with full controls"""
    application = get_object_or_404(Application, pk=pk)
    
    # Admin can view all applications
    context = {
        'application': application,
        'user_role': 'admin',
        'can_approve': True,  # Admin has full approval rights
    }
    return render(request, 'applications/application_detail.html', context)

@login_required
def create_application(request, scheme_id):
    """Deprecated: Always redirect to booking-first flow."""
    scheme = get_object_or_404(Scheme, pk=scheme_id)
    messages.warning(request, 'Applications are created after documentation booking and payment approval.')
    return redirect('create_documentation_booking', scheme_id=scheme.pk)


def _notify_sales_employee(application, sales_user):
    """Create notification for sales employee about new application"""
    from notifications.models import Notification
    
    try:
        Notification.objects.create(
            recipient=sales_user,
            channel='EMAIL',
            notification_type='CUSTOM',
            subject=f'New Application Submitted by {application.client.company_name}',
            message=f'''
A new scheme application has been submitted by your client.

Client: {application.client.company_name}
Scheme: {application.scheme.name}
Amount: ₹{application.applied_amount} lakhs
Application ID: {application.application_id}

Please track the application status and coordinate with the manager for approval.
            '''.strip(),
            email_to=sales_user.email,
            status='QUEUED',
            related_application=application,
            sent_by=application.client.user
        )
    except Exception as e:
        print(f"Error creating sales notification: {str(e)}")


def _notify_manager_for_approval(application, manager_user):
    """Create notification for manager to approve application"""
    from notifications.models import Notification
    
    try:
        Notification.objects.create(
            recipient=manager_user,
            channel='EMAIL',
            notification_type='CUSTOM',
            subject=f'Application Approval Required: {application.application_id}',
            message=f'''
A new scheme application requires your approval.

Client: {application.client.company_name}
Scheme: {application.scheme.name}
Applied Amount: ₹{application.applied_amount} lakhs
Application ID: {application.application_id}
Purpose: {application.purpose}

Please review and approve/reject this application in the system.
            '''.strip(),
            email_to=manager_user.email,
            status='QUEUED',
            related_application=application,
            sent_by=application.client.user
        )
    except Exception as e:
        print(f"Error creating manager notification: {str(e)}")


@login_required
def approve_application(request, pk):
    """Manager/Admin approves an application and notifies sales and client"""
    application = get_object_or_404(Application, pk=pk)

    # Permission check
    user = request.user
    if not (user.is_admin or user.is_manager):
        messages.error(request, "You don't have permission to approve applications.")
        return redirect('application_detail', pk=pk)

    if request.method == 'POST':
        approved_amount = request.POST.get('approved_amount')
        try:
            # Update application
            if approved_amount:
                application.approved_amount = approved_amount
            application.status = Application.Status.APPROVED
            application.approval_date = timezone.now().date()
            application.save()

            # Notify sales and client
            sales_user = application.client.assigned_sales
            if sales_user:
                _notify_sales_on_approval(application, sales_user)
            _notify_client_on_approval(application)

            messages.success(request, f"Application {application.application_id} approved.")
        except Exception as e:
            messages.error(request, f"Error approving application: {str(e)}")

    return redirect('application_detail', pk=pk)


@login_required
def reject_application(request, pk):
    """Manager/Admin rejects an application and notifies sales and client"""
    application = get_object_or_404(Application, pk=pk)

    # Permission check
    user = request.user
    if not (user.is_admin or user.is_manager):
        messages.error(request, "You don't have permission to reject applications.")
        return redirect('application_detail', pk=pk)

    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', '').strip()
        try:
            application.status = Application.Status.REJECTED
            application.rejection_reason = reason or 'Not specified'
            application.rejection_date = timezone.now().date()
            application.save()

            # Notify sales and client
            sales_user = application.client.assigned_sales
            if sales_user:
                _notify_sales_on_rejection(application, sales_user)
            _notify_client_on_rejection(application)

            messages.success(request, f"Application {application.application_id} rejected.")
        except Exception as e:
            messages.error(request, f"Error rejecting application: {str(e)}")

    return redirect('application_detail', pk=pk)


def _notify_sales_on_approval(application, sales_user):
    from notifications.models import Notification
    try:
        Notification.objects.create(
            recipient=sales_user,
            channel='EMAIL',
            notification_type='APPLICATION_APPROVED',
            subject=f'Application Approved: {application.application_id}',
            message=f'''
Great news! Your client's application has been approved.

Client: {application.client.company_name}
Scheme: {application.scheme.name}
Approved Amount: ₹{application.approved_amount or application.applied_amount} lakhs
Application ID: {application.application_id}
            '''.strip(),
            email_to=sales_user.email,
            status='QUEUED',
            related_application=application,
            sent_by=None
        )
    except Exception as e:
        print(f"Error creating sales approval notification: {str(e)}")


def _notify_client_on_approval(application):
    from notifications.models import Notification
    try:
        Notification.objects.create(
            recipient=application.client.user,
            channel='EMAIL',
            notification_type='APPLICATION_APPROVED',
            subject=f'Your Application is Approved: {application.application_id}',
            message=f'''
Congratulations! Your application has been approved.

Scheme: {application.scheme.name}
Approved Amount: ₹{application.approved_amount or application.applied_amount} lakhs
Application ID: {application.application_id}
            '''.strip(),
            email_to=application.client.contact_email,
            status='QUEUED',
            related_application=application,
            sent_by=None
        )
    except Exception as e:
        print(f"Error creating client approval notification: {str(e)}")


def _notify_sales_on_rejection(application, sales_user):
    from notifications.models import Notification
    try:
        Notification.objects.create(
            recipient=sales_user,
            channel='EMAIL',
            notification_type='APPLICATION_REJECTED',
            subject=f'Application Rejected: {application.application_id}',
            message=f'''
The application has been rejected.

Client: {application.client.company_name}
Scheme: {application.scheme.name}
Reason: {application.rejection_reason}
Application ID: {application.application_id}
            '''.strip(),
            email_to=sales_user.email,
            status='QUEUED',
            related_application=application,
            sent_by=None
        )
    except Exception as e:
        print(f"Error creating sales rejection notification: {str(e)}")


def _notify_client_on_rejection(application):
    from notifications.models import Notification
    try:
        Notification.objects.create(
            recipient=application.client.user,
            channel='EMAIL',
            notification_type='APPLICATION_REJECTED',
            subject=f'Your Application Decision: {application.application_id}',
            message=f'''
We're sorry to inform you that your application has been rejected.

Scheme: {application.scheme.name}
Reason: {application.rejection_reason}
Application ID: {application.application_id}
            '''.strip(),
            email_to=application.client.contact_email,
            status='QUEUED',
            related_application=application,
            sent_by=None
        )
    except Exception as e:
        print(f"Error creating client rejection notification: {str(e)}")


@login_required
def pending_applications(request):
    """Manager-only view for applications awaiting approval"""
    user = request.user
    
    if not (user.is_admin or user.is_manager):
        messages.error(request, "You don't have permission to view this page.")
        return redirect('dashboard')
    
    # Get applications requiring approval
    pending_apps = Application.objects.filter(
        status__in=['SUBMITTED', 'UNDER_REVIEW']
    ).select_related('client', 'scheme', 'assigned_to').order_by('-created_at')
    
    context = {
        'applications': pending_apps,
        'title': 'Applications Awaiting Approval',
    }
    return render(request, 'applications/pending_applications.html', context)
