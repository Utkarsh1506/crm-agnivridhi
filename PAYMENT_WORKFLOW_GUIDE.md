# Payment-Application Workflow - Quick Implementation Guide

## Current Status:
- ✅ Booking creation working
- ✅ Payment model has all fields (approval, status, etc.)
- ✅ Application model has status tracking and timeline
- ⏳ Need to connect them with workflow

## Implementation Steps:

### STEP 1: Record Payment Button (SIMPLE)
**Location**: Booking detail page or Client detail page

**Add to `templates/clients/client_detail.html`** (in bookings section):
```html
{% if booking.status == 'PENDING' and not booking.payment %}
    <a href="{% url 'payments:record_payment' booking.id %}" class="btn btn-sm btn-success">
        <i class="bi bi-cash"></i> Record Payment
    </a>
{% endif %}
```

### STEP 2: Record Payment View
**File**: `payments/views.py`

```python
@login_required
def record_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        # Create payment record
        payment = Payment.objects.create(
            booking=booking,
            client=booking.client,
            amount=request.POST.get('amount'),
            payment_method=request.POST.get('payment_method'),
            reference_id=request.POST.get('reference_id'),
            notes=request.POST.get('notes'),
            received_by=request.user,
            status='PENDING'  # Awaiting approval
        )
        messages.success(request, 'Payment recorded! Awaiting manager approval.')
        return redirect('clients:client_detail', pk=booking.client.id)
    
    return render(request, 'payments/record_payment.html', {'booking': booking})
```

### STEP 3: Payment Approval (Manager Dashboard)
**Already exists in manager_dashboard.html - just ensure approve button calls:**

```python
@manager_required
def approve_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    payment.approve(request.user)  # Method already exists in model!
    messages.success(request, f'Payment approved! Booking #{payment.booking.booking_id} is now PAID.')
    return redirect('accounts:manager_dashboard')
```

### STEP 4: Create Application Button
**Add to client_detail.html** (after payment approved):
```html
{% if booking.status == 'PAID' and not booking.applications.exists %}
    <a href="{% url 'applications:create_application' %}?booking={{ booking.id }}" 
       class="btn btn-sm btn-primary">
        <i class="bi bi-file-plus"></i> Create Application
    </a>
{% endif %}
```

### STEP 5: Application Status Updates
**File**: `applications/views.py`

```python
@login_required
def update_application_status(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        
        # Update status
        application.status = new_status
        
        # Add to timeline
        timeline_entry = {
            'status': new_status,
            'date': str(timezone.now()),
            'updated_by': request.user.get_full_name(),
            'notes': notes
        }
        application.timeline.append(timeline_entry)
        application.save()
        
        messages.success(request, 'Application status updated!')
        return redirect('applications:application_detail', pk=application_id)
    
    return render(request, 'applications/update_status.html', {'application': application})
```

### STEP 6: Client Dashboard Progress View
**File**: `templates/clients/client_portal.html`

```html
<!-- Applications Section -->
<div class="card">
    <div class="card-header">
        <h5>My Applications</h5>
    </div>
    <div class="card-body">
        {% for app in client.applications.all %}
        <div class="mb-3">
            <h6>{{ app.scheme.name }}</h6>
            <div class="d-flex justify-content-between mb-1">
                <span>Status: <strong>{{ app.get_status_display }}</strong></span>
                <span>{{ app.timeline|length }} updates</span>
            </div>
            
            <!-- Progress bar based on status -->
            {% if app.status == 'DRAFT' %}
                <div class="progress">
                    <div class="progress-bar" style="width: 10%">10%</div>
                </div>
            {% elif app.status == 'SUBMITTED' %}
                <div class="progress">
                    <div class="progress-bar bg-info" style="width: 30%">30%</div>
                </div>
            {% elif app.status == 'UNDER_REVIEW' %}
                <div class="progress">
                    <div class="progress-bar bg-warning" style="width: 60%">60%</div>
                </div>
            {% elif app.status == 'APPROVED' %}
                <div class="progress">
                    <div class="progress-bar bg-success" style="width: 100%">100% - Approved!</div>
                </div>
            {% endif %}
            
            <!-- Timeline -->
            <button class="btn btn-sm btn-link" data-bs-toggle="collapse" data-bs-target="#timeline-{{app.id}}">
                View Timeline
            </button>
            <div class="collapse" id="timeline-{{app.id}}">
                {% for entry in app.timeline %}
                <div class="small">
                    <strong>{{ entry.date|date:"M d, Y H:i" }}</strong> - {{ entry.status }} 
                    {% if entry.notes %}<br>{{ entry.notes }}{% endif %}
                </div>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    </div>
</div>
```

## Quick URLs to Add:

```python
# payments/urls.py
path('record/<int:booking_id>/', views.record_payment, name='record_payment'),
path('approve/<int:payment_id>/', views.approve_payment, name='approve_payment'),

# applications/urls.py
path('update-status/<int:application_id>/', views.update_application_status, name='update_status'),
```

## Testing Workflow:

1. Create Booking → ✅
2. Click "Record Payment" → Enter details → Save as PENDING
3. Manager sees in pending payments → Click Approve
4. Booking status = PAID
5. Click "Create Application" → Fill form → Save as DRAFT
6. Update status to SUBMITTED → UNDER_REVIEW → APPROVED
7. Client sees progress on their dashboard

---

**Kya kare ab?**
1. Ek-ek step implement kare?
2. Ya pura ek saath kar du?
3. Ya simple version pehle - complex features baad me?

Bata do kya approach chahiye!
