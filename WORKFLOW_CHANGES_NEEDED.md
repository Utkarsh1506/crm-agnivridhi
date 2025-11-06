# Application Workflow Changes Required

## Current Workflow (INCORRECT)
```
Client → Browses Schemes → Clicks "Apply" → 
Application Created Directly → Shows in Applications Section
```

## New Workflow (CORRECT)
```
1. Client → Browses Schemes → Requests BOOKING (for documentation service)
   ↓
2. Booking Created → Shows in BOOKINGS section (NOT applications yet)
   ↓
3. Sales Employee → Views booking in their dashboard
   ↓
4. Sales → Records PAYMENT (application/documentation charge)
   ↓
5. Manager → Approves Payment
   ↓
6. Sales → Creates APPLICATION manually (fills all details)
   ↓
7. Application → NOW shows in Client's Applications section
```

## Key Changes Needed

### 1. Scheme Detail Page
- **Remove:** Direct "Apply Now" button that creates application
- **Add:** "Request Documentation Service" button that creates a BOOKING
- Booking should be for a service like "Scheme Application Documentation"

### 2. Client Dashboard - Applications Section
- **Current:** Shows all applications directly created
- **New:** Shows only applications that went through: Booking → Payment → Manager Approval flow
- Before payment approval, client sees booking in "Bookings" section

### 3. Client Dashboard - Bookings Section  
- Must show bookings for documentation services
- Status should show: PENDING PAYMENT, PAID, IN PROGRESS, COMPLETED
- Client can track: "I requested documentation for CGTMSE scheme - Status: Awaiting Payment"

### 4. Sales Dashboard
- Show bookings assigned to them
- For each booking with payment approved:
  - Button: "Create Application" 
  - Opens form to fill application details manually
  - On submit → Creates Application record

### 5. Payment Flow
- Booking created → Status: PENDING
- Sales records payment → Payment status: PENDING (needs manager approval)
- Manager approves payment → Booking status: PAID
- Sales can now create application

### 6. Database Changes
**Application Model needs:**
- `booking` field (ForeignKey to Booking) - to link application to the original booking
- This ensures application is only created after booking → payment → approval flow

**Booking Model:**
- Add `scheme` field (ForeignKey to Scheme) - to track which scheme the documentation is for
- Add `application_created` boolean - to track if application was created from this booking

## Implementation Steps

### Step 1: Update Scheme Detail Page
File: `templates/schemes/scheme_detail.html`
- Change "Apply Now" button to "Request Documentation Service"
- Link to booking creation view with scheme context

### Step 2: Create Booking View for Scheme Documentation
File: `bookings/views.py`
- Add `create_scheme_documentation_booking(request, scheme_id)` view
- Creates booking for "Scheme Application Documentation" service
- Links booking to the scheme

### Step 3: Update Application Creation
File: `applications/views.py`
- Change `create_application` to require `booking_id` parameter
- Check if booking payment is approved before allowing application creation
- Link application to booking

### Step 4: Update Client Dashboard
- Bookings section: Show all bookings with status
- Applications section: Show only applications (not direct scheme requests)

### Step 5: Update Sales Dashboard
- Show bookings with "Create Application" button for paid bookings
- Button only appears after payment is manager-approved

## Services Needed in Database
Must create service: **"Scheme Application Documentation"**
- Category: FUNDING
- Price: ₹5000 (or appropriate amount)
- Description: "Documentation and application services for government schemes"

## Summary
This workflow ensures:
✅ Clients must pay documentation charges before application is processed
✅ Manager has control over payment approvals
✅ Sales team manually fills application details (quality control)
✅ Clear tracking: Booking → Payment → Approval → Application
✅ Client sees booking in "Bookings" until application is created
