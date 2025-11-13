from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import timedelta

from .models import ClientActivity, ServiceOffering, ClientServiceEnrollment
from clients.models import Client
from applications.models import Application
from bookings.models import Booking
from schemes.models import Scheme
from documents.models import Document, DocumentChecklist


@login_required
def client_dashboard(request):
    """
    Enhanced client dashboard with timeline, services, and recommendations
    """
    if not request.user.is_client:
        messages.error(request, "Access denied. This page is for clients only.")
        return redirect('accounts:dashboard')
    
    # Get client profile
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        messages.error(request, "Client profile not found.")
        return redirect('accounts:dashboard')
    
    # Get activities timeline (visible to client)
    activities = ClientActivity.objects.filter(
        client=client,
        is_visible_to_client=True
    ).select_related(
        'created_by', 'application', 'booking', 'document', 'service_offering', 'scheme'
    ).order_by('-created_at')[:20]  # Last 20 activities
    
    # Pending tasks
    pending_tasks = ClientActivity.objects.filter(
        client=client,
        is_visible_to_client=True,
        status__in=['PENDING', 'IN_PROGRESS'],
        activity_type__in=['TASK_ASSIGNED', 'DOCUMENTS_REQUESTED']
    ).order_by('due_date', '-created_at')
    
    # Applications summary
    applications = Application.objects.filter(client=client)
    applications_count = applications.count()
    approved_applications = applications.filter(status='APPROVED').count()
    pending_applications = applications.filter(status__in=['PENDING', 'UNDER_REVIEW']).count()
    
    # Bookings summary
    bookings = Booking.objects.filter(client=client)
    bookings_count = bookings.count()
    active_bookings = bookings.filter(status='CONFIRMED').count()
    
    # Documents summary
    documents = Document.objects.filter(client=client, uploaded_by__role='CLIENT')
    uploaded_documents = documents.count()
    
    # Document checklist progress
    checklist_total = DocumentChecklist.objects.filter(client=client, is_required=True).count()
    checklist_uploaded = DocumentChecklist.objects.filter(
        client=client, 
        is_required=True, 
        is_uploaded=True
    ).count()
    checklist_progress = (checklist_uploaded / checklist_total * 100) if checklist_total > 0 else 0
    
    # Enrolled services
    enrolled_services = ClientServiceEnrollment.objects.filter(
        client=client,
        status__in=['ENROLLED', 'IN_PROGRESS']
    ).select_related('service')
    
    # Recommended services (not enrolled yet)
    recommended_services = ClientServiceEnrollment.objects.filter(
        client=client,
        status='RECOMMENDED'
    ).select_related('service')[:3]  # Top 3
    
    # Available services (featured)
    available_services = ServiceOffering.objects.filter(
        is_active=True,
        is_featured=True
    ).exclude(
        id__in=ClientServiceEnrollment.objects.filter(client=client).values_list('service_id', flat=True)
    )[:4]  # Top 4
    
    # Recommended schemes based on client profile
    recommended_schemes = Scheme.objects.filter(
        is_active=True,
        scheme_status='OPEN'
    )
    
    # Filter by sector if available
    if client.sector:
        recommended_schemes = recommended_schemes.filter(
            Q(sector__icontains=client.sector) | Q(sector='ALL_SECTORS')
        )
    
    # Filter by business type
    if client.business_type:
        recommended_schemes = recommended_schemes.filter(
            Q(business_type__icontains=client.business_type) | Q(business_type='ALL_TYPES')
        )
    
    recommended_schemes = recommended_schemes[:6]  # Top 6
    
    # Recent milestones
    milestones = ClientActivity.objects.filter(
        client=client,
        is_visible_to_client=True,
        activity_type='MILESTONE_ACHIEVED'
    ).order_by('-created_at')[:5]
    
    # Upcoming meetings
    upcoming_meetings = ClientActivity.objects.filter(
        client=client,
        is_visible_to_client=True,
        activity_type='MEETING_SCHEDULED',
        status__in=['PENDING', 'IN_PROGRESS'],
        due_date__gte=timezone.now().date()
    ).order_by('due_date')[:3]
    
    context = {
        'client': client,
        'activities': activities,
        'pending_tasks': pending_tasks,
        'applications_count': applications_count,
        'approved_applications': approved_applications,
        'pending_applications': pending_applications,
        'bookings_count': bookings_count,
        'active_bookings': active_bookings,
        'uploaded_documents': uploaded_documents,
        'checklist_total': checklist_total,
        'checklist_uploaded': checklist_uploaded,
        'checklist_progress': round(checklist_progress, 1),
        'enrolled_services': enrolled_services,
        'recommended_services': recommended_services,
        'available_services': available_services,
        'recommended_schemes': recommended_schemes,
        'milestones': milestones,
        'upcoming_meetings': upcoming_meetings,
    }
    
    return render(request, 'tracking/client_dashboard.html', context)


@login_required
def client_timeline(request):
    """
    Full timeline view for client
    """
    if not request.user.is_client:
        messages.error(request, "Access denied.")
        return redirect('accounts:dashboard')
    
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        messages.error(request, "Client profile not found.")
        return redirect('accounts:dashboard')
    
    # Get all visible activities
    activities = ClientActivity.objects.filter(
        client=client,
        is_visible_to_client=True
    ).select_related(
        'created_by', 'application', 'booking', 'document', 'service_offering', 'scheme'
    ).order_by('-created_at')
    
    # Filter by type if requested
    activity_type = request.GET.get('type')
    if activity_type:
        activities = activities.filter(activity_type=activity_type)
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        activities = activities.filter(status=status)
    
    context = {
        'client': client,
        'activities': activities,
        'activity_type_filter': activity_type,
        'status_filter': status,
    }
    
    return render(request, 'tracking/client_timeline.html', context)


@login_required
def client_services(request):
    """
    View all available and enrolled services
    """
    if not request.user.is_client:
        messages.error(request, "Access denied.")
        return redirect('accounts:dashboard')
    
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        messages.error(request, "Client profile not found.")
        return redirect('accounts:dashboard')
    
    # Enrolled services
    enrolled_services = ClientServiceEnrollment.objects.filter(
        client=client
    ).select_related('service', 'recommended_by').order_by('-created_at')
    
    # Available services
    available_services = ServiceOffering.objects.filter(
        is_active=True
    ).exclude(
        id__in=enrolled_services.values_list('service_id', flat=True)
    ).order_by('display_order', 'name')
    
    context = {
        'client': client,
        'enrolled_services': enrolled_services,
        'available_services': available_services,
    }
    
    return render(request, 'tracking/client_services.html', context)


@login_required
def service_detail(request, service_id):
    """
    Service detail page
    """
    service = get_object_or_404(ServiceOffering, id=service_id, is_active=True)
    
    # Check if client is enrolled
    enrollment = None
    if request.user.is_client:
        try:
            client = Client.objects.get(user=request.user)
            enrollment = ClientServiceEnrollment.objects.filter(
                client=client,
                service=service
            ).first()
        except Client.DoesNotExist:
            pass
    
    context = {
        'service': service,
        'enrollment': enrollment,
    }
    
    return render(request, 'tracking/service_detail.html', context)


# ==================== SALES VIEWS ====================

@login_required
def sales_client_activities(request, client_id):
    """
    View and manage activities for a specific client (Sales only)
    """
    if not request.user.is_sales and not request.user.is_manager and not request.user.is_admin:
        messages.error(request, "Access denied.")
        return redirect('accounts:dashboard')
    
    # Get client - must be assigned to this sales or created by them
    client = get_object_or_404(
        Client,
        pk=client_id
    )
    
    # Check if this sales can access this client
    if request.user.is_sales:
        if client.assigned_sales != request.user and client.created_by != request.user:
            messages.error(request, "Access denied. This client is not assigned to you.")
            return redirect('clients:sales_clients_list')
    
    # Get all activities for this client
    activities = ClientActivity.objects.filter(
        client=client
    ).select_related(
        'created_by', 'application', 'booking', 'document', 'service_offering', 'scheme'
    ).order_by('-created_at')
    
    # Get related data
    applications = Application.objects.filter(client=client)
    bookings = Booking.objects.filter(client=client)
    documents = Document.objects.filter(client=client)
    
    context = {
        'client': client,
        'activities': activities,
        'applications': applications,
        'bookings': bookings,
        'documents': documents,
    }
    
    return render(request, 'tracking/sales_client_activities.html', context)


@login_required
def sales_add_activity(request, client_id):
    """
    Add new activity/update for a client (Sales only)
    """
    if not request.user.is_sales and not request.user.is_manager and not request.user.is_admin:
        messages.error(request, "Access denied.")
        return redirect('accounts:dashboard')
    
    client = get_object_or_404(Client, pk=client_id)
    
    # Check access
    if request.user.is_sales:
        if client.assigned_sales != request.user and client.created_by != request.user:
            messages.error(request, "Access denied.")
            return redirect('clients:sales_clients_list')
    
    if request.method == 'POST':
        activity_type = request.POST.get('activity_type')
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status', 'PENDING')
        priority = request.POST.get('priority', 'MEDIUM')
        is_visible = request.POST.get('is_visible_to_client', 'on') == 'on'
        due_date = request.POST.get('due_date') or None
        
        # Optional relationships
        application_id = request.POST.get('application')
        booking_id = request.POST.get('booking')
        document_id = request.POST.get('document')
        service_id = request.POST.get('service_offering')
        scheme_id = request.POST.get('scheme')
        
        # Create activity
        activity = ClientActivity.objects.create(
            client=client,
            activity_type=activity_type,
            title=title,
            description=description,
            status=status,
            priority=priority,
            is_visible_to_client=is_visible,
            due_date=due_date,
            created_by=request.user,
            application_id=application_id if application_id else None,
            booking_id=booking_id if booking_id else None,
            document_id=document_id if document_id else None,
            service_offering_id=service_id if service_id else None,
            scheme_id=scheme_id if scheme_id else None,
        )
        
        messages.success(request, f"Activity '{title}' added successfully!")
        return redirect('tracking:sales_client_activities', client_id=client.id)
    
    # GET request - show form
    applications = Application.objects.filter(client=client)
    bookings = Booking.objects.filter(client=client)
    documents = Document.objects.filter(client=client)
    services = ServiceOffering.objects.filter(is_active=True)
    schemes = Scheme.objects.filter(is_active=True)
    
    context = {
        'client': client,
        'applications': applications,
        'bookings': bookings,
        'documents': documents,
        'services': services,
        'schemes': schemes,
        'activity_types': ClientActivity.ActivityType.choices,
        'statuses': ClientActivity.Status.choices,
        'priorities': ClientActivity.Priority.choices,
    }
    
    return render(request, 'tracking/sales_add_activity.html', context)


@login_required
def sales_edit_activity(request, activity_id):
    """
    Edit existing activity (Sales only)
    """
    if not request.user.is_sales and not request.user.is_manager and not request.user.is_admin:
        messages.error(request, "Access denied.")
        return redirect('accounts:dashboard')
    
    activity = get_object_or_404(ClientActivity, pk=activity_id)
    client = activity.client
    
    # Check access
    if request.user.is_sales:
        if client.assigned_sales != request.user and client.created_by != request.user:
            messages.error(request, "Access denied.")
            return redirect('clients:sales_clients_list')
    
    if request.method == 'POST':
        activity.activity_type = request.POST.get('activity_type')
        activity.title = request.POST.get('title')
        activity.description = request.POST.get('description')
        activity.status = request.POST.get('status')
        activity.priority = request.POST.get('priority')
        activity.is_visible_to_client = request.POST.get('is_visible_to_client', 'off') == 'on'
        activity.due_date = request.POST.get('due_date') or None
        
        # Mark as completed if status is COMPLETED
        if activity.status == 'COMPLETED' and not activity.completed_at:
            activity.completed_at = timezone.now()
        
        activity.save()
        
        messages.success(request, "Activity updated successfully!")
        return redirect('tracking:sales_client_activities', client_id=client.id)
    
    # GET request
    context = {
        'activity': activity,
        'client': client,
        'activity_types': ClientActivity.ActivityType.choices,
        'statuses': ClientActivity.Status.choices,
        'priorities': ClientActivity.Priority.choices,
    }
    
    return render(request, 'tracking/sales_edit_activity.html', context)


@login_required
def sales_delete_activity(request, activity_id):
    """
    Delete activity (Sales/Manager/Admin only)
    """
    if not request.user.is_sales and not request.user.is_manager and not request.user.is_admin:
        messages.error(request, "Access denied.")
        return redirect('accounts:dashboard')
    
    activity = get_object_or_404(ClientActivity, pk=activity_id)
    client = activity.client
    
    # Check access
    if request.user.is_sales:
        if client.assigned_sales != request.user and client.created_by != request.user:
            messages.error(request, "Access denied.")
            return redirect('clients:sales_clients_list')
    
    if request.method == 'POST':
        activity.delete()
        messages.success(request, "Activity deleted successfully!")
        return redirect('tracking:sales_client_activities', client_id=client.id)
    
    context = {
        'activity': activity,
        'client': client,
    }
    
    return render(request, 'tracking/sales_delete_activity_confirm.html', context)
