from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification


@login_required
def notification_list(request):
	"""List notifications with pagination and filters. Admin/Owner/Superuser sees all; others see own."""
	user = request.user
	from django.core.paginator import Paginator
	from django.db.models import Q
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

	from collections import Counter
	status_counts = Counter(qs.values_list('status', flat=True))

	return render(request, 'notifications/notification_list.html', {
		'page_obj': page_obj,
		'status_counts_items': list(status_counts.items()),
		'filter_status': status,
		'filter_channel': channel,
		'filter_q': q,
		'page_size': page_size,
	})
