# 🔄 WORKFLOW TESTING GUIDE - AGNIVRIDHI CRM

**Test all user roles and complete business flows**

---

## 📋 PRE-TEST CHECKLIST

- ✅ Server running: `python manage.py runserver`
- ✅ Admin created: Username: admin
- ✅ Swagger UI accessible: http://localhost:8000/api/docs/
- ✅ Database has sample data (1 client, 1 booking, 1 payment)

---

## 🧪 WORKFLOW TEST SCENARIOS

### Scenario 1: Client Onboarding (SALES → MANAGER → ADMIN)

**Actors:** Sales Employee, Manager, Admin, Client

**Steps:**

1. **Sales Employee Creates Client Request**
   ```
   Role: Sales Employee
   Action: Create EditRequest for new client
   URL: /edit-requests/create/
   
   Data:
   - Entity Type: CLIENT
   - Requested Action: Create new client
   - Reason: "New prospect from marketing campaign"
   ```

2. **Manager Reviews Request**
   ```
   Role: Manager
   Action: View pending edit requests
   URL: /edit-requests/
   Decision: Approve or Reject
   ```

3. **If Approved, Manager Creates Client**
   ```
   Role: Manager
   Action: Create client account
   URL: /clients/create/
   
   Required Fields:
   - Company Name: "ABC Pvt Ltd"
   - Business Type: Pvt Ltd Company
   - Sector: Manufacturing
   - Annual Turnover: 50 lakhs
   - Funding Required: 20 lakhs
   - Company Age: 3 years
   - Assigned Sales: [Select sales employee]
   - Contact Details
   - Address
   ```

4. **System Auto-Generates Credentials**
   ```
   System Action:
   - Creates User account
   - Creates Client profile
   - Generates Client ID: CLI-20251105-XXXX
   - Links user to client
   ```

5. **Manager Sends Credentials via WhatsApp**
   ```
   System Action (Auto):
   - Calls send_custom_whatsapp()
   - Sends username and password
   - Sends login URL
   ```

**Expected Result:**
- ✅ EditRequest created (Status: PENDING)
- ✅ Manager sees request in dashboard
- ✅ Client account created
- ✅ Client ID auto-generated
- ✅ User account linked
- ✅ WhatsApp notification sent
- ✅ Client can login

**Test via API:**
```bash
# 1. Create edit request (Sales)
POST /api/edit-requests/
{
  "entity_type": "CLIENT",
  "requested_action": "create",
  "reason": "New prospect"
}

# 2. Create client (Manager)
POST /api/clients/
{
  "company_name": "ABC Pvt Ltd",
  "business_type": "PVT_LTD",
  "sector": "MANUFACTURING",
  "annual_turnover": "50.00",
  "funding_required": "20.00",
  ...
}
```

---

### Scenario 2: Service Booking (CLIENT → SALES → PAYMENT)

**Actors:** Client, Sales Employee, System

**Steps:**

1. **Client Browses Services**
   ```
   Role: Client
   Action: View available services
   URL: /services/
   ```

2. **Client Requests Service Booking**
   ```
   Role: Client
   Action: Select service (e.g., "DPR Preparation")
   URL: /bookings/request/
   
   Data:
   - Service: DPR Preparation
   - Requirements: "Need DPR for manufacturing unit expansion"
   ```

3. **Sales Employee Creates Booking**
   ```
   Role: Sales Employee
   Action: Create booking for client
   URL: /bookings/create/
   
   Data:
   - Client: ABC Pvt Ltd
   - Service: DPR Preparation
   - Amount: ₹25,000
   - Discount: 10%
   - Final Amount: ₹22,500
   - Priority: High
   ```

4. **System Creates Payment Entry**
   ```
   System Action:
   - Creates Booking (Status: PENDING)
   - Auto-generates Booking ID: BKG-20251105-XXXX
   - Creates Payment (Status: PENDING)
   - Calculates final amount after discount
   ```

5. **Client Makes Payment**
   ```
   Role: Client
   Option A: Online via Razorpay
   Option B: Manual (UPI/Bank Transfer)
   
   If Manual:
   - Upload payment proof
   - Enter UTR/Reference number
   - Submit for approval
   ```

6. **Sales Employee Approves Manual Payment**
   ```
   Role: Sales Employee
   Action: Approve payment
   URL: /payments/{id}/approve/
   
   System Action:
   - Updates Payment status: CAPTURED
   - Updates Booking status: PAID
   - Sends email confirmation
   - Sends WhatsApp notification
   - Generates PDF receipt
   ```

**Expected Result:**
- ✅ Booking created with auto ID
- ✅ Payment entry created
- ✅ Discount applied correctly
- ✅ Payment approved (if manual)
- ✅ Booking status updated
- ✅ PDF receipt generated
- ✅ Email sent
- ✅ WhatsApp sent
- ✅ Client can download receipt

**Test via API:**
```bash
# 1. List services
GET /api/services/

# 2. Create booking
POST /api/bookings/
{
  "client": 1,
  "service": 1,
  "amount": "25000.00",
  "discount_percent": "10.00",
  "requirements": "Need DPR for expansion"
}

# 3. Create payment
POST /api/payments/
{
  "booking": 1,
  "amount": "22500.00",
  "payment_method": "UPI_QR",
  "reference_id": "UTR123456789"
}

# 4. Approve payment
POST /api/payments/1/approve/
{
  "notes": "Payment verified"
}
```

---

### Scenario 3: Scheme Application (CLIENT → ELIGIBILITY → APPLICATION)

**Actors:** Client, System, Manager, Admin

**Steps:**

1. **Client Checks Eligible Schemes**
   ```
   Role: Client
   Action: View scheme eligibility
   URL: /schemes/check-eligibility/
   
   System Action:
   - Runs check_client_eligibility() for all active schemes
   - Calculates AI recommendation scores
   - Shows eligible schemes (sorted by score)
   - Shows ineligible schemes with reasons
   ```

2. **Client Views Scheme Details**
   ```
   Role: Client
   Action: Click on eligible scheme
   URL: /schemes/{id}/
   
   Shows:
   - Scheme description
   - Benefits
   - Eligibility criteria
   - Required documents
   - Funding range
   - Application process
   ```

3. **Client Applies for Scheme**
   ```
   Role: Client
   Action: Submit application
   URL: /applications/create/
   
   Data:
   - Scheme: CGTMSE
   - Applied Amount: ₹15 lakhs
   - Purpose: "Working capital for business expansion"
   ```

4. **System Creates Application**
   ```
   System Action:
   - Creates Application (Status: DRAFT)
   - Auto-generates Application ID: APP-20251105-XXXX
   - Initializes timeline with first entry
   - Assigns to sales employee (auto)
   ```

5. **Sales Employee Reviews & Submits**
   ```
   Role: Sales Employee
   Action: Review application details
   URL: /applications/{id}/
   Action: Update status to SUBMITTED
   
   System Action:
   - Updates status
   - Adds timeline entry
   - Sets submission_date
   - Sends WhatsApp notification to client
   - Sends email notification
   ```

6. **Manager Updates Status**
   ```
   Role: Manager
   Action: Update application status as it progresses
   
   Status Flow:
   DRAFT → SUBMITTED → UNDER_REVIEW → APPROVED/REJECTED
   
   Each update:
   - Adds timeline entry
   - Sends notification
   - Logs activity
   ```

**Expected Result:**
- ✅ Eligibility checked automatically
- ✅ AI scores calculated
- ✅ Application created with auto ID
- ✅ Timeline tracking started
- ✅ Status updates tracked
- ✅ Notifications sent on each status change
- ✅ Client sees live progress
- ✅ Manager can add remarks

**Test via API:**
```bash
# 1. Check eligibility
GET /api/schemes/?client_id=1

# 2. Get scheme details
GET /api/schemes/1/

# 3. Create application
POST /api/applications/
{
  "client": 1,
  "scheme": 1,
  "applied_amount": "15.00",
  "purpose": "Working capital for expansion"
}

# 4. Update status
POST /api/applications/1/update_status/
{
  "status": "SUBMITTED",
  "notes": "All documents verified"
}
```

---

### Scenario 4: Edit Request Workflow (SALES → ADMIN)

**Actors:** Sales Employee, Admin

**Steps:**

1. **Sales Employee Needs to Edit Client Data**
   ```
   Role: Sales Employee
   Scenario: Client's phone number changed
   Current Value: +91-9876543210
   New Value: +91-9876543211
   
   Action: Sales cannot directly edit (no permission)
   Solution: Create EditRequest
   ```

2. **Sales Creates Edit Request**
   ```
   Role: Sales Employee
   Action: Request edit
   URL: /edit-requests/create/
   
   Data:
   - Entity Type: CLIENT
   - Entity ID: 1
   - Field Name: contact_phone
   - Current Value: +91-9876543210
   - Requested Value: +91-9876543211
   - Reason: "Client informed phone number change"
   ```

3. **System Logs Edit Request**
   ```
   System Action:
   - Creates EditRequest (Status: PENDING)
   - Notifies Admin via email
   - Stores current and requested values
   - Links to requesting user
   ```

4. **Admin Reviews Request**
   ```
   Role: Admin
   Action: View pending edit requests
   URL: /edit-requests/pending/
   
   Shows:
   - Who requested
   - What field to change
   - Current vs Requested value
   - Reason
   - Approve/Reject buttons
   ```

5. **Admin Approves**
   ```
   Role: Admin
   Action: Click "Approve"
   
   System Action:
   - Updates status to APPROVED
   - Sets approved_by = admin
   - Sets approval_date
   - Calls apply_changes()
   - Actually updates client.contact_phone
   - Updates status to APPLIED
   - Notifies sales employee
   - Logs activity
   ```

**Expected Result:**
- ✅ Sales cannot directly edit
- ✅ EditRequest created
- ✅ Admin notified
- ✅ Admin can see change preview
- ✅ On approval, changes auto-applied
- ✅ Sales employee notified
- ✅ Activity logged
- ✅ Data integrity maintained

**Test via API:**
```bash
# 1. Try direct edit (Sales) - Should fail
PUT /api/clients/1/
{
  "contact_phone": "+91-9876543211"
}
# Response: 403 Forbidden

# 2. Create edit request
POST /api/edit-requests/
{
  "entity_type": "CLIENT",
  "entity_id": 1,
  "field_name": "contact_phone",
  "current_value": "+91-9876543210",
  "requested_value": "+91-9876543211",
  "reason": "Client informed phone number change"
}

# 3. Admin approves
POST /api/edit-requests/1/approve/
{
  "notes": "Change verified with client"
}

# 4. Verify change applied
GET /api/clients/1/
# Should show new phone number
```

---

### Scenario 5: Document Generation & Download (SYSTEM → CLIENT)

**Actors:** System, Client, Sales Employee

**Steps:**

1. **System Auto-Generates Documents**
   ```
   Trigger: Booking status changes to PAID
   
   System Action:
   - Calls generate_booking_confirmation_pdf()
   - Creates PDF with ReportLab
   - Creates Document record
   - Saves file to media/documents/
   - Status: GENERATED
   ```

2. **Sales Employee Manually Generates DPR**
   ```
   Role: Sales Employee
   Action: Generate DPR for client
   URL: /documents/generate-dpr/{client_id}/
   
   System Action:
   - Calls generate_dpr_report_pdf()
   - Pulls data from client, bookings, payments, applications
   - Generates comprehensive report
   - Creates Document record
   ```

3. **Client Views Available Documents**
   ```
   Role: Client
   Action: Go to "My Documents"
   URL: /documents/my-documents/
   
   Shows:
   - List of all documents
   - Document types
   - Generation dates
   - File sizes
   - Download buttons
   ```

4. **Client Downloads Document**
   ```
   Role: Client
   Action: Click "Download" on DPR
   
   System Action:
   - Calls document.record_download(user)
   - Increments download_count
   - Updates last_downloaded_by
   - Updates last_downloaded_at
   - Updates status to DOWNLOADED
   - Serves PDF file
   ```

**Expected Result:**
- ✅ Documents auto-generated on triggers
- ✅ Manual generation available
- ✅ PDFs professionally formatted
- ✅ Download tracking works
- ✅ Client can access their documents
- ✅ File sizes calculated
- ✅ Multiple downloads allowed

**Test via API:**
```bash
# 1. List client documents
GET /api/documents/?client=1

# 2. Generate payment receipt
GET /pdf/payment/1/

# 3. Generate booking confirmation
GET /pdf/booking/1/

# 4. Generate application form
GET /pdf/application/1/
```

---

## 🎯 ROLE-BASED PERMISSION TESTING

### Test Matrix

| Action | Admin | Manager | Sales | Client |
|--------|-------|---------|-------|--------|
| Create Client | ✅ | ✅ | ❌* | ❌ |
| Edit Client | ✅ | ❌* | ❌* | ❌ |
| View All Clients | ✅ | ✅ | ❌ | ❌ |
| View Own Clients | ✅ | ✅ | ✅ | ✅ |
| Create Booking | ✅ | ✅ | ✅ | ❌ |
| Edit Booking | ✅ | ❌* | ❌* | ❌ |
| Create Application | ✅ | ✅ | ✅ | ✅ |
| Edit Application | ✅ | ❌* | ❌* | ❌ |
| Approve EditRequest | ✅ | ❌ | ❌ | ❌ |
| Create EditRequest | ✅ | ✅ | ✅ | ❌ |
| Approve Payment | ✅ | ✅ | ✅ | ❌ |
| View Analytics | ✅ | ✅ | 🔵 | ❌ |
| Manage Schemes | ✅ | ❌ | ❌ | ❌ |
| Manage Services | ✅ | ❌ | ❌ | ❌ |
| Download Documents | ✅ | ✅ | ✅ | ✅ |
| Generate DPR | ✅ | ✅ | ✅ | ❌ |

**Legend:**
- ✅ = Full access
- ❌ = No access
- ❌* = No direct access (must use EditRequest)
- 🔵 = Limited access (own data only)

---

## 🧪 API TESTING CHECKLIST

### Authentication
- [ ] Login with each role
- [ ] Session persists across requests
- [ ] Logout works
- [ ] Unauthorized access blocked

### Clients API
- [ ] GET `/api/clients/` - List (role-filtered)
- [ ] POST `/api/clients/` - Create (staff only)
- [ ] GET `/api/clients/{id}/` - Detail
- [ ] PUT `/api/clients/{id}/` - Update (admin only)
- [ ] DELETE `/api/clients/{id}/` - Delete (admin only)
- [ ] GET `/api/clients/{id}/bookings/` - Client bookings
- [ ] GET `/api/clients/{id}/payments/` - Client payments
- [ ] GET `/api/clients/{id}/applications/` - Client applications

### Bookings API
- [ ] GET `/api/bookings/` - List (role-filtered)
- [ ] POST `/api/bookings/` - Create (staff only)
- [ ] GET `/api/bookings/{id}/` - Detail
- [ ] PUT `/api/bookings/{id}/` - Update
- [ ] POST `/api/bookings/{id}/update_status/` - Status change

### Payments API
- [ ] GET `/api/payments/` - List
- [ ] POST `/api/payments/` - Create (staff only)
- [ ] GET `/api/payments/{id}/` - Detail
- [ ] POST `/api/payments/{id}/approve/` - Approve (staff only)
- [ ] POST `/api/payments/{id}/reject/` - Reject (staff only)

### Applications API
- [ ] GET `/api/applications/` - List (role-filtered)
- [ ] POST `/api/applications/` - Create
- [ ] GET `/api/applications/{id}/` - Detail
- [ ] PUT `/api/applications/{id}/` - Update
- [ ] POST `/api/applications/{id}/update_status/` - Status change
- [ ] POST `/api/applications/{id}/assign/` - Assign to staff

### PDF Downloads
- [ ] GET `/pdf/payment/{id}/` - Payment receipt
- [ ] GET `/pdf/booking/{id}/` - Booking confirmation
- [ ] GET `/pdf/application/{id}/` - Application form

---

## 📊 DATA VALIDATION TESTING

### Client Data
- [ ] Company name required
- [ ] Turnover must be positive
- [ ] Funding required must be positive
- [ ] Phone number format validated
- [ ] Email format validated
- [ ] PAN format validated (if provided)
- [ ] GST format validated (if provided)
- [ ] Duplicate prevention (same company name + sector)

### Booking Data
- [ ] Service selection required
- [ ] Amount must match service price
- [ ] Discount percentage 0-100
- [ ] Final amount = amount - (amount * discount/100)
- [ ] Expected completion date in future
- [ ] Cannot delete booking with payment

### Application Data
- [ ] Applied amount within scheme limits
- [ ] Cannot apply to same scheme twice (if active)
- [ ] Eligibility check on creation
- [ ] Status transitions valid (can't go backwards)

### Payment Data
- [ ] Amount matches booking final_amount
- [ ] Reference ID unique for manual payments
- [ ] Cannot delete successful payment
- [ ] Refund amount <= original amount

---

## 🎯 SUCCESS CRITERIA

### All Tests Pass If:

1. **Role Separation Works**
   - ✅ Each role sees only allowed data
   - ✅ Each role can perform only allowed actions
   - ✅ Permission denials are graceful

2. **Workflows Complete Successfully**
   - ✅ Client onboarding end-to-end
   - ✅ Booking and payment cycle
   - ✅ Application tracking
   - ✅ Edit request approval
   - ✅ Document generation

3. **Notifications Work**
   - ✅ Emails sent (console or SMTP)
   - ✅ WhatsApp sent (with credentials)
   - ✅ PDF receipts generated
   - ✅ Activity logs created

4. **Data Integrity Maintained**
   - ✅ No orphan records
   - ✅ Foreign keys enforced
   - ✅ Calculations accurate
   - ✅ Status transitions logical

5. **User Experience is Smooth**
   - ✅ Forms validate properly
   - ✅ Error messages are clear
   - ✅ Success messages appear
   - ✅ Navigation is intuitive

---

## 🐛 COMMON ISSUES & FIXES

### Issue: "Permission Denied"
**Fix:** Check if user has correct role assigned

### Issue: "PDF not generating"
**Fix:** Check if ReportLab is installed: `pip list | grep reportlab`

### Issue: "WhatsApp not sending"
**Fix:** Check TWILIO_* variables in .env file

### Issue: "Email not showing up"
**Fix:** Check terminal output (console backend) or email settings

### Issue: "Client ID not auto-generating"
**Fix:** Don't provide client_id when creating client (let model generate)

---

## 📝 TEST REPORT TEMPLATE

```
TEST DATE: [Date]
TESTED BY: [Name]
SYSTEM VERSION: 1.0.0

SCENARIO: [Scenario Name]
ACTORS: [Roles involved]

STEPS COMPLETED:
✅ Step 1: [Description]
✅ Step 2: [Description]
❌ Step 3: [Description] - FAILED

FAILURE DETAILS:
- Expected: [What should happen]
- Actual: [What happened]
- Error Message: [If any]
- Screenshots: [Attach]

RESOLUTION:
[How it was fixed]

OVERALL STATUS: PASS/FAIL
```

---

**Happy Testing! 🚀**

*Run through each scenario and verify all features work as expected.*
