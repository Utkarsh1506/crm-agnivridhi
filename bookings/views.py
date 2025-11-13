from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal

from .models import Booking, Service
from schemes.models import Scheme
from accounts.views import manager_required, client_required, sales_required


@login_required
def booking_list(request):
	"""Deprecated generic endpoint: redirect to role-specific page for privacy."""
	user = request.user
	if getattr(user, 'is_client', False):
		return redirect('bookings:client_bookings_list')
	elif getattr(user, 'role', None) == 'SALES':
		return redirect('bookings:sales_bookings_list')
	elif getattr(user, 'role', None) in ['MANAGER', 'ADMIN']:
		return redirect('bookings:team_bookings_list')
	return redirect('dashboard')


@client_required
def client_bookings_list(request):
	"""Client-only: list own bookings"""
	client = request.user.client_profile
	bookings = Booking.objects.filter(client=client).order_by('-booking_date')
	return render(request, 'bookings/booking_list.html', {'bookings': bookings})


@sales_required
def sales_bookings_list(request):
	"""Sales-only: list bookings for clients assigned to this sales user"""
	bookings = Booking.objects.filter(
		client__assigned_sales=request.user
	).select_related('client', 'service', 'assigned_to').order_by('-booking_date')
	
	context = {
		'bookings': bookings,
		'total_bookings': bookings.count(),
		'page_title': 'Total Bookings'
	}
	return render(request, 'bookings/sales_booking_list.html', context)


@login_required
def create_scheme_documentation_booking(request, scheme_id: int):
	"""
	Client action: request a documentation/application service booking for a scheme.
	Creates a Booking for the configured Service and assigns to the client's sales if available.
	"""
	if not getattr(request.user, 'is_client', False):
		messages.error(request, 'Only clients can request documentation service.')
		return redirect('schemes:scheme_list')

	scheme = get_object_or_404(Scheme, pk=scheme_id)
	client = request.user.client_profile

	# Find or create the documentation service
	service_name = 'Scheme Application Documentation'
	service, _created = Service.objects.get_or_create(
		name=service_name,
		defaults={
			'category': 'FUNDING',
			'description': 'Documentation and application services for government schemes',
			'short_description': 'End-to-end documentation and application filing',
			'price': Decimal('5000.00'),
			'duration_days': 30,
			'is_active': True,
			'features': ['Application form preparation', 'Document checklist', 'Filing assistance'],
			'deliverables': ['Prepared application', 'Submission support'],
		}
	)

	# Calculate default amounts
	amount = service.price

	# Create booking
	booking = Booking.objects.create(
		client=client,
		service=service,
		status='PENDING',
		priority='MEDIUM',
		amount=amount,
		final_amount=amount,  # will also be set in save()
		requirements=f'Documentation request for scheme: {scheme.name} (ID: {scheme.id})',
		assigned_to=getattr(client, 'assigned_sales', None),
		created_by=request.user,
		internal_notes=f'SCHEME_ID={scheme.id}'
	)

	messages.success(
		request,
		f'Booking created (ID: {booking.booking_id}). Our team will contact you. Please complete payment to proceed.'
	)

	# Redirect client to their bookings list
	return redirect('booking_list')


@login_required
def create_booking_for_client(request, client_id):
	"""
	Staff (Manager/Admin/Sales) can create a booking for a client.
	"""
	from clients.models import Client
	from django.db.models import Q
	
	# Check permissions - only staff can create bookings for clients
	if request.user.role not in ['SALES', 'MANAGER', 'ADMIN', 'OWNER']:
		messages.error(request, 'You do not have permission to create bookings.')
		return redirect('accounts:dashboard')
	
	# Get client and verify access
	client = get_object_or_404(Client, id=client_id)
	
	# Permission check: can only create booking for clients you have access to
	if request.user.role == 'SALES':
		if client.assigned_sales != request.user:
			messages.error(request, 'You can only create bookings for your assigned clients.')
			return redirect('clients:sales_clients_list')
	elif request.user.role == 'MANAGER':
		# Manager can create for clients assigned to them OR their team's clients
		if not (client.assigned_manager == request.user or 
		        (client.assigned_sales and client.assigned_sales.manager == request.user)):
			messages.error(request, 'You can only create bookings for your team clients.')
			return redirect('clients:manager_clients_list')
	# Admin/Owner can create for any client
	
	if request.method == 'POST':
		service_id = request.POST.get('service_id')
		scheme_id = request.POST.get('scheme_id')
		amount = request.POST.get('amount')
		upfront_amount = request.POST.get('upfront_amount', '0')
		discount = request.POST.get('discount', '0')
		funding_amount = request.POST.get('funding_amount', '0')
		requirements = request.POST.get('requirements', '')
		priority = request.POST.get('priority', 'MEDIUM')
		
		if not service_id or not amount:
			messages.error(request, 'Please select a service and enter the amount.')
		else:
			try:
				from decimal import Decimal
				service = get_object_or_404(Service, id=service_id)
				
				# Convert amounts
				amount_decimal = Decimal(amount)
				discount_decimal = Decimal(discount)
				upfront_decimal = Decimal(upfront_amount)
				funding_decimal = Decimal(funding_amount) if funding_amount else Decimal('0')
				
				# Determine who to assign the booking to
				assigned_to = client.assigned_sales if client.assigned_sales else request.user
				
				# Build internal notes with all details
				notes_parts = [f'Created by {request.user.get_full_name()}']
				if scheme_id:
					from schemes.models import Scheme
					scheme = Scheme.objects.filter(id=scheme_id).first()
					if scheme:
						notes_parts.append(f'Scheme: {scheme.name} ({scheme.get_category_display()})')
						notes_parts.append(f'Funding Amount: ₹{funding_decimal:,.2f}')
				if upfront_decimal > 0:
					notes_parts.append(f'Upfront Payment: ₹{upfront_decimal:,.2f}')
				
				internal_notes = ' | '.join(notes_parts)
				
				# Create booking
				booking = Booking.objects.create(
					client=client,
					service=service,
					status='PENDING',
					priority=priority,
					amount=amount_decimal,
					discount_percent=discount_decimal,
					final_amount=amount_decimal - (amount_decimal * discount_decimal / 100),
					requirements=requirements or f'Booking for {service.name}',
					assigned_to=assigned_to,
					created_by=request.user,
					internal_notes=internal_notes
				)
				
				messages.success(
					request,
					f'Booking created successfully (ID: {booking.booking_id}) for {client.company_name}. Final Amount: ₹{booking.final_amount:,.2f}'
				)
				return redirect('clients:client_detail', pk=client.id)
			except Exception as e:
				messages.error(request, f'Error creating booking: {str(e)}')
	
	# GET request - show form
	from schemes.models import Scheme
	active_services = Service.objects.filter(is_active=True).order_by('category', 'name')
	active_schemes = Scheme.objects.filter(status='ACTIVE').order_by('category', 'name')
	
	context = {
		'client': client,
		'services': active_services,
		'schemes': active_schemes,
		'page_title': f'Create Booking for {client.company_name}'
	}
	return render(request, 'bookings/create_booking_for_client.html', context)


@manager_required
def team_bookings_list(request):
	"""Manager/Admin view: Bookings for team; Admin/Owner sees all."""
	from django.db.models import Q
	user_role = getattr(request.user, 'role', '').upper()
	if user_role in ['ADMIN', 'OWNER'] or getattr(request.user, 'is_superuser', False):
		bookings = (
			Booking.objects
			.all()
			.select_related('client', 'service', 'assigned_to', 'payment')
			.order_by('-booking_date')
			.distinct()
		)
	else:
		# Team bookings: client assigned to manager OR booking assigned to manager's team sales
		bookings = (
			Booking.objects
			.filter(Q(client__assigned_manager=request.user) | Q(assigned_to__manager=request.user))
			.select_related('client', 'service', 'assigned_to', 'payment')
			.order_by('-booking_date')
			.distinct()
		)

	# Basic stats
	from django.db.models import Count, Sum, Q as _Q
	stats = bookings.aggregate(
		total=Count('id'),
		pending=Count('id', filter=_Q(status='PENDING')),
		paid=Count('id', filter=_Q(status='PAID')),
		completed=Count('id', filter=_Q(status='COMPLETED')),
		cancelled=Count('id', filter=_Q(status='CANCELLED')),
		total_value=Sum('final_amount'),
	)

	# Optional grouping by client
	bookings_by_client = {}
	for b in bookings:
		key = b.client.company_name
		if key not in bookings_by_client:
			bookings_by_client[key] = { 'client': b.client, 'items': [] }
		bookings_by_client[key]['items'].append(b)

	return render(request, 'bookings/team_bookings_list.html', {
		'bookings': bookings,
		'bookings_by_client': bookings_by_client,
		'stats': stats,
	})


@login_required
def booking_detail(request, id: int):
	"""Role-scoped booking detail view.

	Access rules:
	- Client: only their own bookings
	- Sales: bookings for their assigned clients OR assigned to them
	- Manager: bookings for clients assigned to them OR assigned_to under their team
	- Admin/Superuser: allowed
	"""
	booking = get_object_or_404(
		Booking.objects.select_related('client', 'service', 'assigned_to', 'payment'),
		id=id
	)

	user = request.user
	allowed = False

	try:
		if getattr(user, 'is_superuser', False) or getattr(user, 'is_admin', False):
			allowed = True
		elif getattr(user, 'is_client', False):
			allowed = getattr(booking.client, 'user_id', None) == user.id
		elif getattr(user, 'role', None) == 'SALES':
			# Sales can view bookings for their assigned clients OR bookings assigned to them
			allowed = (
				getattr(booking.client, 'assigned_sales_id', None) == user.id or
				getattr(booking, 'assigned_to_id', None) == user.id
			)
		elif getattr(user, 'role', None) == 'MANAGER':
			# Manager via client assignment or team sales assignment
			allowed = (
				getattr(booking.client, 'assigned_manager_id', None) == user.id or
				getattr(getattr(booking, 'assigned_to', None), 'manager_id', None) == user.id
			)
	except Exception:
		allowed = False

	if not allowed:
		messages.error(request, 'You do not have permission to view this booking.')
		return redirect('dashboard')

	context = {
		'booking': booking,
	}
	return render(request, 'bookings/booking_detail.html', context)
