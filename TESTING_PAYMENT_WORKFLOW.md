# Quick Testing Guide - Payment Recording & Approval

## Prerequisites
- Django server running: `python manage.py runserver`
- At least 2 users: 1 SALES, 1 MANAGER
- At least 1 client assigned to SALES user

---

## Test Scenario 1: Record Payment (Sales Employee)

### Steps:
1. **Login as SALES user**
   - Navigate to: http://127.0.0.1:8000/accounts/login/
   - Use sales credentials

2. **Go to My Clients**
   - Dashboard → My Clients
   - Click on any assigned client

3. **Create a Booking** (if none exists)
   - Click "Create Booking" button
   - Fill form:
     * Service Name: "CGTMSE Loan"
     * Scheme Name: "CGTMSE"
     * Amount: 50000
     * Upfront Payment: 10000
     * Discount: 10
     * Funding Amount: 500000
   - Submit

4. **Record Payment**
   - On client detail page, find the booking
   - Should see green "Record Payment" button
   - Click it
   - Fill payment form:
     * Amount: ₹45,000 (pre-filled from booking final amount)
     * Payment Method: "Bank Transfer"
     * Transaction Reference: "UTR123456789012"
     * Upload Proof: (optional - upload any image)
     * Notes: "First installment received"
   - Click "Record Payment"

5. **Verify Success**
   - Should redirect to client detail page
   - Should see success message: "Payment recorded successfully! Reference: UTR123456789012. Awaiting manager approval."
   - Booking should now show "Payment Pending Approval" badge
   - "Record Payment" button should disappear

---

## Test Scenario 2: Approve Payment (Manager)

### Steps:
1. **Login as MANAGER user**
   - Navigate to: http://127.0.0.1:8000/accounts/login/
   - Use manager credentials

2. **Go to Dashboard**
   - Should see yellow alert at top: "1 payment awaiting your approval!"
   - Should see badge on "Payments" in sidebar
   - Should see "Pending Payment Approvals" section

3. **Review Payment Details**
   - In "Pending Payment Approvals" table, verify:
     * Payment ID
     * Client name
     * Booking ID
     * Amount: ₹45,000
     * Method: Bank Transfer / NEFT / RTGS
     * Reference: UTR123456789012
     * Recorded By: (Sales employee name)
     * Date: (timestamp)

4. **Approve Payment**
   - Click green "Approve" button
   - Should see success message: "Payment approved! Booking #XXX is now PAID. You can now create an application."
   - Payment should disappear from pending list

5. **Verify Booking Status Changed**
   - Go to client detail page
   - Find the booking
   - Status badge should now be green "PAID"
   - Should see blue "Create Application" button
   - "Record Payment" button should be gone

---

## Test Scenario 3: Reject Payment (Manager)

### Steps:
1. **Create another booking and record payment** (repeat Scenario 1)

2. **As Manager, click "Reject" button**
   - In pending payments table, click red "Reject" button
   - Should open rejection confirmation page

3. **Fill Rejection Form**
   - Should see warning alert
   - Should see payment details summary
   - Fill "Rejection Reason":
     * Example: "Invalid transaction reference - UTR not found in bank statement"
   - Click "Confirm Rejection"

4. **Verify Rejection**
   - Should redirect to manager dashboard
   - Should see warning message with rejection reason
   - Payment should disappear from pending list

5. **Verify on Client Page**
   - Go to client detail page
   - Booking should still show status "PENDING"
   - "Record Payment" button should reappear (can record new payment)

---

## Test Scenario 4: Permission Checks

### Test 4A: Sales can't record payment for unassigned client
1. **Login as SALES user A**
2. **Try to access:** `/payments/record/X/` (booking ID of client assigned to SALES user B)
3. **Expected:** Error message "You can only record payments for your assigned clients."

### Test 4B: Sales can't approve payments
1. **Login as SALES user**
2. **Try to access:** `/payments/approve/X/` (any payment ID)
3. **Expected:** 403 Forbidden or redirect to dashboard

### Test 4C: Client role has no access
1. **Login as CLIENT user**
2. **Try to access:** `/payments/record/X/`
3. **Expected:** Access denied

---

## Test Scenario 5: Edge Cases

### Test 5A: Duplicate Payment Prevention
1. Record payment for a booking
2. Try to access `/payments/record/X/` again (same booking ID)
3. **Expected:** Warning message "Payment already recorded for this booking."
4. Should redirect to client detail page

### Test 5B: Required Field Validation
1. Go to record payment page
2. Leave "Transaction Reference" empty
3. Try to submit
4. **Expected:** Browser validation error "Please fill out this field"

### Test 5C: Already Approved Payment
1. Approve a payment
2. Try to access `/payments/approve/X/` again (same payment ID)
3. **Expected:** Warning message "Payment is already Captured."
4. Should redirect to dashboard

---

## Expected Database Changes

### After Recording Payment:
```sql
-- Check payment record
SELECT id, booking_id, client_id, amount, payment_method, reference_id, status, received_by_id
FROM payments_payment
WHERE booking_id = X;

-- Expected: status = 'PENDING', received_by_id = (sales user id)
```

### After Approving Payment:
```sql
-- Check payment status
SELECT status, approved_by_id, approval_date
FROM payments_payment
WHERE id = X;

-- Expected: status = 'CAPTURED', approved_by_id = (manager user id), approval_date = (timestamp)

-- Check booking status
SELECT status, payment_date
FROM bookings_booking
WHERE id = X;

-- Expected: status = 'PAID', payment_date = (timestamp)
```

### After Rejecting Payment:
```sql
-- Check payment status
SELECT status, notes
FROM payments_payment
WHERE id = X;

-- Expected: status = 'FAILED', notes contains rejection reason
```

---

## Visual Checks

### Record Payment Page:
- ✓ Two-column layout (form on left, booking details on right)
- ✓ All form fields visible and properly labeled
- ✓ Amount pre-filled from booking
- ✓ Payment method dropdown has 6 options
- ✓ Transaction reference field marked as required (red asterisk)
- ✓ File upload accepts images and PDFs
- ✓ Blue info alert explains pending status
- ✓ Breadcrumb navigation at top
- ✓ Quick Tips card on right sidebar

### Client Detail Page - Bookings:
- ✓ Bookings displayed in cards with left border color
- ✓ Status badge color-coded (green=PAID, yellow=PENDING, red=CANCELLED)
- ✓ Amount shows with currency symbol
- ✓ Discount percentage visible if applicable
- ✓ Created date formatted nicely
- ✓ Action buttons change based on status
- ✓ "Record Payment" button appears only if status=PENDING and no payment exists
- ✓ "Payment Pending Approval" badge shows if payment recorded but not approved
- ✓ "Create Application" button appears only if status=PAID

### Manager Dashboard:
- ✓ Yellow alert at top if pending payments exist
- ✓ Badge on "Payments" nav item shows pending count
- ✓ "Pending Payment Approvals" section with table
- ✓ All payment details visible in table
- ✓ Approve button is green with checkmark icon
- ✓ Reject button is red with X icon
- ✓ Reference ID in monospace font

### Reject Payment Page:
- ✓ Red/danger theme throughout
- ✓ Warning alert at top
- ✓ Payment details card with all info
- ✓ Rejection reason textarea with placeholder
- ✓ Confirm button is large and red
- ✓ Cancel button to go back

---

## Common Issues & Solutions

### Issue: "Payment already recorded for this booking"
**Solution:** Payment already exists. Check if it's pending approval or approved. Delete old payment from admin if testing.

### Issue: "You can only record payments for your assigned clients"
**Solution:** Client is not assigned to this SALES user. Assign client first or use correct SALES user.

### Issue: Booking not showing on client detail page
**Solution:** 
1. Verify booking exists in database
2. Check `client_detail` view passes `bookings` in context
3. Check template has bookings display section

### Issue: Approve button does nothing
**Solution:** 
1. Check browser console for JavaScript errors
2. Verify CSRF token in form
3. Check manager_dashboard template uses POST form for approve

### Issue: File upload not working
**Solution:**
1. Verify `MEDIA_ROOT` and `MEDIA_URL` in settings.py
2. Check form has `enctype="multipart/form-data"`
3. Ensure media directory has write permissions

---

## Success Criteria

✅ Sales can record payments for assigned clients only  
✅ Payments start as PENDING status  
✅ Manager sees pending payments on dashboard  
✅ Manager can approve → booking status changes to PAID  
✅ Manager can reject → payment marked as FAILED  
✅ "Create Application" button appears after payment approval  
✅ Duplicate payment prevention works  
✅ Required field validation works  
✅ File upload works for payment proof  
✅ All templates responsive and user-friendly  
✅ Permission checks prevent unauthorized access  

---

## Next Test: Application Creation

Once Step 1 is verified working, proceed to test Step 2:
- Click "Create Application" button on PAID booking
- Pre-fill form with booking data
- Create application with DRAFT status
- Initialize timeline tracking

Refer to `PAYMENT_WORKFLOW_GUIDE.md` for Step 2 implementation details.
