from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
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
        return redirect('applications:client_applications_list')
    elif getattr(user, 'role', None) == 'SALES':
        return redirect('applications:sales_applications_list')
    elif getattr(user, 'role', None) in ['MANAGER', 'ADMIN']:
        return redirect('applications:team_applications_list')
    return redirect('accounts:dashboard')


@client_required
def client_applications_list(request):
    client = request.user.client_profile
    applications = Application.objects.filter(client=client).order_by('-created_at')
    return render(request, 'applications/application_list.html', {'applications': applications})


@sales_required
def sales_applications_list(request):
    applications = Application.objects.filter(assigned_to=request.user).order_by('-created_at')
    
    # Calculate status counts
    submitted_count = applications.filter(status='SUBMITTED').count()
    approved_count = applications.filter(status='APPROVED').count()
    rejected_count = applications.filter(status='REJECTED').count()
    
    context = {
        'applications': applications,
        'submitted_count': submitted_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
    }
    return render(request, 'applications/sales_application_list.html', context)


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
        return redirect('accounts:sales_dashboard')

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
            return redirect('applications:create_application_from_booking', booking_id=booking.id)

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
            return redirect('applications:application_detail', pk=application.pk)
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
    # Include both: clients directly assigned to manager AND clients assigned to sales employees under this manager
    from django.db.models import Q
    user_role = getattr(user, 'role', '').upper()
    if user_role in ['ADMIN', 'OWNER'] or getattr(user, 'is_superuser', False):
        # Global visibility
        applications = Application.objects.all().select_related('client', 'client__assigned_sales', 'scheme', 'assigned_to').order_by('-created_at')
        team_clients = Client.objects.all().select_related('assigned_sales', 'assigned_manager')
    else:
        team_clients = Client.objects.filter(
            Q(assigned_manager=user) | Q(assigned_sales__manager=user)
        ).select_related('assigned_sales', 'assigned_manager').distinct()
        
        # Team applications only
        applications = Application.objects.filter(client__in=team_clients).select_related('client', 'client__assigned_sales', 'scheme', 'assigned_to').order_by('-created_at')
    
    # Statistics
    from django.db.models import Sum, Count
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
        return redirect('applications:client_application_detail', pk=pk)
    elif getattr(user, 'role', None) == 'SALES':
        return redirect('applications:sales_application_detail', pk=pk)
    elif getattr(user, 'role', None) == 'MANAGER':
        return redirect('applications:manager_application_detail', pk=pk)
    elif getattr(user, 'role', None) == 'ADMIN':
        return redirect('applications:owner_application_detail', pk=pk)
    return redirect('accounts:dashboard')


@client_required
def client_application_detail(request, pk):
    """Client view: View their own application details"""
    application = get_object_or_404(Application, pk=pk)
    
    # Check permissions - client can only view their own applications
    if application.client.user != request.user:
        messages.error(request, "You don't have permission to view this application.")
        return redirect('applications:client_applications_list')
    
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
        return redirect('applications:sales_applications_list')
    
    # Handle submit action
    if request.method == 'POST' and 'submit_application' in request.POST:
        if application.status == 'DRAFT':
            application.status = 'SUBMITTED'
            application.submission_date = timezone.now().date()
            application.save()
            
            # Add to timeline
            timeline = application.timeline or []
            timeline.append({
                'status': 'SUBMITTED',
                'date': str(timezone.now()),
                'by': request.user.get_full_name() or request.user.username,
                'note': 'Application submitted for manager approval'
            })
            application.timeline = timeline
            application.save()
            
            messages.success(request, f'Application {application.application_id} has been submitted for manager approval.')
            return redirect('applications:sales_application_detail', pk=pk)
        else:
            messages.warning(request, 'Only draft applications can be submitted.')
    
    context = {
        'application': application,
        'user_role': 'sales',
        'can_submit': application.status == 'DRAFT',  # Can submit only draft applications
    }
    return render(request, 'applications/application_detail.html', context)


@manager_required
def manager_application_detail(request, pk):
    """Manager/Admin/Owner view: View team applications with approval controls"""
    application = get_object_or_404(Application, pk=pk)
    
    # Check permissions - Admin/Owner can view all, Manager can view their team only
    user_role = getattr(request.user, 'role', '').upper()
    if user_role not in ['ADMIN', 'OWNER'] and not request.user.is_superuser:
        # Manager check - only their team
        if application.client.assigned_manager != request.user and application.client.assigned_sales.manager != request.user:
            messages.error(request, "You don't have permission to view this application.")
            return redirect('applications:team_applications_list')
    
    context = {
        'application': application,
        'user_role': 'manager' if user_role == 'MANAGER' else 'admin',
        'can_approve': True,  # Manager/Admin/Owner has approval rights
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
    return redirect('bookings:create_documentation_booking', scheme_id=scheme.pk)


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
    """Manager/Admin approves an application"""
    application = get_object_or_404(Application, pk=pk)

    # Permission check
    user = request.user
    user_role = getattr(user, 'role', '').upper()
    if user_role not in ['MANAGER', 'ADMIN', 'OWNER']:
        messages.error(request, "You don't have permission to approve applications.")
        return redirect('applications:application_detail', pk=pk)
    
    # Manager can only approve applications from their team
    if user_role == 'MANAGER':
        if application.client.assigned_manager != user and application.client.assigned_sales.manager != user:
            messages.error(request, "You can only approve applications from your team.")
            return redirect('applications:team_applications_list')
    
    if request.method == 'POST':
        if application.status != 'SUBMITTED':
            messages.warning(request, 'Only submitted applications can be approved.')
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('applications:manager_application_detail', pk=pk)
        
        # Get approved amount from form (optional)
        approved_amount = request.POST.get('approved_amount')
        if approved_amount:
            try:
                application.approved_amount = float(approved_amount)
            except ValueError:
                messages.error(request, 'Invalid approved amount.')
                next_url = request.POST.get('next') or request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('applications:approve_application', pk=pk)
        else:
            # If no approved amount specified, use applied amount
            application.approved_amount = application.applied_amount
        
        # Update application status
        application.status = 'APPROVED'
        application.approval_date = timezone.now().date()
        application.save()
        
        # Add to timeline
        timeline = application.timeline or []
        timeline.append({
            'status': 'APPROVED',
            'date': str(timezone.now()),
            'by': user.get_full_name() or user.username,
            'note': f'Application approved by {user.get_role_display()}. Approved amount: ₹{application.approved_amount} lakhs'
        })
        application.timeline = timeline
        application.save()
        
        messages.success(request, f'Application {application.application_id} has been approved for ₹{application.approved_amount} lakhs!')

        # JSON/AJAX response support
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'ok': True,
                'status': 'APPROVED',
                'approved_amount': float(application.approved_amount),
                'application_id': application.application_id,
            })
        
        # TODO: Send notification to sales and client
        
        next_url = request.POST.get('next') or request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('applications:manager_application_detail', pk=pk)
    
    # GET request - show confirmation form
    context = {
        'application': application,
        'user_role': 'manager' if user.role == 'MANAGER' else 'admin',
        'next': request.GET.get('next', ''),
    }
    return render(request, 'applications/approve_application.html', context)


@login_required
def reject_application(request, pk):
    """Manager/Admin rejects an application"""
    application = get_object_or_404(Application, pk=pk)

    # Permission check
    user = request.user
    if user.role not in ['MANAGER', 'ADMIN', 'OWNER']:
        messages.error(request, "You don't have permission to reject applications.")
        return redirect('applications:application_detail', pk=pk)
    
    # Manager can only reject applications from their team
    if user.role == 'MANAGER':
        if application.client.assigned_manager != user:
            messages.error(request, "You can only reject applications from your team.")
            return redirect('applications:team_applications_list')

    if request.method == 'POST':
        if application.status != 'SUBMITTED':
            messages.warning(request, 'Only submitted applications can be rejected.')
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('applications:manager_application_detail', pk=pk)
        
        reason = request.POST.get('rejection_reason', '').strip()
        if not reason:
            messages.error(request, 'Please provide a reason for rejection.')
            return redirect('applications:manager_application_detail', pk=pk)
        
        # Update application status
        application.status = 'REJECTED'
        application.rejection_reason = reason
        application.rejection_date = timezone.now().date()
        application.save()
        
        # Add to timeline
        timeline = application.timeline or []
        timeline.append({
            'status': 'REJECTED',
            'date': str(timezone.now()),
            'by': user.get_full_name() or user.username,
            'note': f'Application rejected by {user.get_role_display()}: {reason}'
        })
        application.timeline = timeline
        application.save()
        
        messages.warning(request, f'Application {application.application_id} has been rejected.')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'ok': True,
                'status': 'REJECTED',
                'reason': application.rejection_reason,
                'application_id': application.application_id,
            })
        
        # TODO: Send notification to sales and client
        
        next_url = request.POST.get('next') or request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('applications:manager_application_detail', pk=pk)
    
    # GET request - show confirmation (reuse approve template style or create lightweight inline form)
    return render(request, 'applications/reject_application.html', {'application': application, 'next': request.GET.get('next', '')})


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
    
    if user.role not in ['MANAGER', 'ADMIN', 'OWNER']:
        messages.error(request, "You don't have permission to view this page.")
        return redirect('accounts:dashboard')
    
    # Get applications requiring approval
    if user.role == 'MANAGER':
        # Manager sees only their team's submitted applications
        pending_apps = Application.objects.filter(
            status='SUBMITTED',
            client__assigned_manager=user
        ).select_related('client', 'scheme', 'assigned_to').order_by('-created_at')
    else:
        # Admin/Owner sees all submitted applications
        pending_apps = Application.objects.filter(
            status='SUBMITTED'
        ).select_related('client', 'scheme', 'assigned_to').order_by('-created_at')
    
    context = {
        'applications': pending_apps,
        'title': 'Applications Awaiting Approval',
        'user_role': user.role.lower() if user.role else 'staff',
    }
    return render(request, 'applications/pending_applications.html', context)
