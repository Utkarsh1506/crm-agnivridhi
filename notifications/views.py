from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from collections import Counter
from .models import Notification
from .models import SupportRequest
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse


@login_required
def request_callback(request):
	"""Create a support/callback request for the current client."""
	user = request.user
	# Ensure requester is a client
	client = getattr(user, 'client_profile', None)
	if not client:
		messages.error(request, 'Only clients can request callbacks.')
		return render(request, 'errors/403.html', status=403)

	if request.method == 'POST':
		subject = request.POST.get('subject', 'Request Callback').strip()
		message = request.POST.get('message', '').strip()
		booking_id = request.POST.get('booking_id')
		booking = None
		if booking_id:
			from bookings.models import Booking
			booking = Booking.objects.filter(id=booking_id, client=client).first()

		# Choose default assignee: booking.assigned_to or client's assigned_manager/sales
		assigned_to = None
		if booking and booking.assigned_to:
			assigned_to = booking.assigned_to
		elif getattr(client, 'assigned_manager', None):
			assigned_to = client.assigned_manager
		elif getattr(client, 'assigned_sales', None):
			assigned_to = client.assigned_sales

		sr = SupportRequest.objects.create(
			client=client,
			user=user,
			booking=booking,
			subject=subject,
			message=message or 'Please call me regarding my service.',
			contact_email=user.email or getattr(client, 'contact_email', None),
			contact_phone=getattr(client, 'contact_phone', None),
			assigned_to=assigned_to,
		)
		messages.success(request, 'Callback request submitted. Our team will contact you shortly.')
		return redirect('accounts:client_portal')

	return redirect('accounts:client_portal')
@login_required
def notification_list(request):
	"""List notifications with pagination and filters. Admin/Owner/Superuser sees all; others see own."""
	user = request.user
	base_qs = Notification.objects.select_related('recipient', 'sent_by', 'related_booking', 'related_application', 'related_payment').order_by('-created_at')
	if getattr(user, 'role', None) in ['ADMIN', 'OWNER'] or getattr(user, 'is_superuser', False):
		qs = base_qs
	else:
		qs = base_qs.filter(recipient=user)

	# Filters: status, channel, subject/message search, page_size
	status = request.GET.get('status', '').strip()
	channel = request.GET.get('channel', '').strip()
	q = request.GET.get('q', '').strip()
	page_size = request.GET.get('page_size') or '100'
	try:
		page_size = max(1, min(200, int(page_size)))
	except Exception:
		page_size = 100

	if status:
		qs = qs.filter(status=status)
	if channel:
		qs = qs.filter(channel=channel)
	if q:
		qs = qs.filter(Q(subject__icontains=q) | Q(message__icontains=q))

	paginator = Paginator(qs, page_size)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	status_counts = Counter(qs.values_list('status', flat=True))

	return render(request, 'notifications/notification_list.html', {
		'page_obj': page_obj,
		'status_counts_items': list(status_counts.items()),
		'filter_status': status,
		'filter_channel': channel,
		'filter_q': q,
		'page_size': page_size,
	})


@login_required
def activity_feed(request):
	"""
	Activity feed showing all user activities across the CRM.
	Only accessible by Admin and Owner roles.
	Shows what sales employees, clients, and managers are doing.
	"""
	user = request.user
	from activity_logs.models import ActivityLog
	
	# Check access - only Admin/Owner/Superuser
	user_role = getattr(user, 'role', '').upper()
	if not (user_role in ['ADMIN', 'OWNER'] or getattr(user, 'is_superuser', False)):
		messages.error(request, 'You do not have permission to access the activity feed.')
		return render(request, 'errors/403.html', status=403)
	
	# Get all activity logs
	activities_qs = ActivityLog.objects.select_related('user').order_by('-timestamp')
	
	# Filters
	action_filter = request.GET.get('action', '').strip()
	entity_filter = request.GET.get('entity', '').strip()
	user_filter = request.GET.get('user', '').strip()
	role_filter = request.GET.get('role', '').strip()
	search_query = request.GET.get('q', '').strip()
	page_size = request.GET.get('page_size') or '50'
	
	try:
		page_size = max(1, min(200, int(page_size)))
	except Exception:
		page_size = 50
	
	# Apply filters
	if action_filter:
		activities_qs = activities_qs.filter(action=action_filter)
	
	if entity_filter:
		activities_qs = activities_qs.filter(entity_type=entity_filter)
	
	if user_filter:
		activities_qs = activities_qs.filter(user_id=user_filter)
	
	if role_filter:
		from django.contrib.auth import get_user_model
		User = get_user_model()
		role_users = User.objects.filter(role__iexact=role_filter).values_list('id', flat=True)
		activities_qs = activities_qs.filter(user_id__in=role_users)
	
	if search_query:
		activities_qs = activities_qs.filter(
			Q(description__icontains=search_query) |
			Q(user__email__icontains=search_query) |
			Q(user__first_name__icontains=search_query) |
			Q(user__last_name__icontains=search_query)
		)
	
	# Pagination
	paginator = Paginator(activities_qs, page_size)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	
	# Get statistics
	total_activities = activities_qs.count()
	action_counts = Counter(activities_qs.values_list('action', flat=True))
	entity_counts = Counter(activities_qs.values_list('entity_type', flat=True))
	
	# Get unique users for filter dropdown
	from django.contrib.auth import get_user_model
	User = get_user_model()
	active_users = User.objects.filter(
		id__in=activities_qs.values_list('user_id', flat=True).distinct()
	).order_by('first_name', 'last_name', 'email')
	
	# Role counts
	role_activity_counts = {}
	for role_choice in ['SALES', 'MANAGER', 'CLIENT', 'ADMIN', 'OWNER']:
		role_users = User.objects.filter(role__iexact=role_choice).values_list('id', flat=True)
		count = activities_qs.filter(user_id__in=role_users).count()
		if count > 0:
			role_activity_counts[role_choice] = count
	
	context = {
		'page_obj': page_obj,
		'total_activities': total_activities,
		'action_counts': dict(action_counts),
		'entity_counts': dict(entity_counts),
		'role_activity_counts': role_activity_counts,
		'active_users': active_users,
		'filter_action': action_filter,
		'filter_entity': entity_filter,
		'filter_user': user_filter,
		'filter_role': role_filter,
		'search_query': search_query,
		'page_size': page_size,
		'action_types': ActivityLog.ACTION_TYPES,
		'entity_types': ActivityLog.ENTITY_TYPES,
	}
	
	return render(request, 'notifications/activity_feed.html', context)
