# 🎯 SALES DASHBOARD - COMPLETE FEATURE TESTING CHECKLIST

## 📋 Testing Date: November 7, 2025
**Tester:** [Your Name]  
**Server:** http://127.0.0.1:8000/  
**Test Account:** `sales1` / [password]

---

## 🔐 STEP 1: LOGIN & ACCESS

### Test Login
- [ ] Navigate to: http://127.0.0.1:8000/login/
- [ ] Enter username: `sales1`
- [ ] Enter password: [your password]
- [ ] Click "Login" button
- [ ] **Expected:** Redirect to `/dashboard/`
- [ ] **Expected:** Auto-redirect to `/dashboard/sales/`
- [ ] **Expected:** Page loads with "Sales Dashboard" title

### Verify Role Display
- [ ] Check navbar shows "Sales" role badge
- [ ] Check username is displayed correctly
- [ ] Check Agnivridhi logo visible

**✅ Pass Criteria:** Successfully logged in and redirected to Sales Dashboard

---

## 📊 STEP 2: DASHBOARD STATISTICS CARDS

### Stats Card #1: My Clients
- [ ] Card displays "My Clients" label
- [ ] Shows number count (e.g., "5" or "0")
- [ ] Number is accurate (matches clients table below)
- [ ] Card styled properly with cyan theme

### Stats Card #2: My Bookings
- [ ] Card displays "My Bookings" label
- [ ] Shows number count
- [ ] Number matches bookings table below
- [ ] Card styled consistently

### Stats Card #3: My Applications
- [ ] Card displays "My Applications" label
- [ ] Shows number count
- [ ] Number is accurate
- [ ] Card styled consistently

**✅ Pass Criteria:** All 3 stats cards display correctly with accurate numbers

---

## 🧭 STEP 3: NAVIGATION SIDEBAR

### Sidebar Links Test
Test each navigation link by clicking and verifying:

#### Link #1: Dashboard
- [ ] Click "Dashboard" link (with speedometer icon)
- [ ] **Expected URL:** `/dashboard/sales/` or `/dashboard/`
- [ ] **Expected:** Page reloads/stays on dashboard
- [ ] **Status:** Should show as "active" (highlighted)

#### Link #2: My Clients
- [ ] Click "My Clients" link (with building icon)
- [ ] **Expected URL:** Check where it redirects (may be `#` or specific route)
- [ ] **Note:** Currently shows `href="#"` - this might need fixing
- [ ] **Expected Behavior:** Should show only assigned clients

#### Link #3: My Bookings
- [ ] Click "My Bookings" link (with calendar icon)
- [ ] **Expected URL:** `/bookings/sales/bookings/`
- [ ] **Expected:** Page loads with list of bookings assigned to sales user
- [ ] **Status:** HTTP 200 OK

#### Link #4: My Applications
- [ ] Click "My Applications" link (with file icon)
- [ ] **Expected URL:** `/applications/sales/applications/`
- [ ] **Expected:** Page loads with applications assigned to sales user
- [ ] **Status:** HTTP 200 OK

**✅ Pass Criteria:** All navigation links work (except #2 if it's `href="#"`)

---

## 👥 STEP 4: MY ASSIGNED CLIENTS TABLE

### Table Structure
- [ ] Table header shows: "My Assigned Clients"
- [ ] Building icon (🏢) displayed
- [ ] Table columns: Client ID | Company | Sector | Turnover | Funding Required | Status

### Data Display (If Clients Exist)
For each client row, verify:
- [ ] Client ID displays correctly
- [ ] Company name shows
- [ ] Sector displays properly (e.g., "Manufacturing")
- [ ] Annual Turnover shows with ₹ symbol and "L" (lakhs)
- [ ] Funding Required shows with ₹ symbol and "L"
- [ ] Status badge displays (e.g., "ACTIVE", "LEAD", "CONVERTED")
- [ ] Badge is colored appropriately (bg-info class)

### Empty State (If No Clients)
- [ ] Shows message: "No clients assigned yet"
- [ ] Message is centered and styled in muted color

### Data Accuracy
- [ ] **CRITICAL:** Verify you ONLY see clients assigned to your sales user
- [ ] **CRITICAL:** Should NOT see clients assigned to other sales users
- [ ] Number of clients matches "My Clients" stat card

**✅ Pass Criteria:** Table displays only assigned clients with accurate data

---

## 📅 STEP 5: MY BOOKINGS TABLE

### Table Structure
- [ ] Table header shows: "My Bookings"
- [ ] Calendar icon displayed
- [ ] Table columns: Booking ID | Client | Service | Amount | Status | Action

### Data Display (If Bookings Exist)
For each booking row, verify:

#### Column: Booking ID
- [ ] Booking ID is a clickable link
- [ ] Click booking ID
- [ ] **Expected:** Redirects to `/bookings/<id>/`
- [ ] **Expected:** Booking detail page loads (HTTP 200)
- [ ] Go back to dashboard

#### Column: Client
- [ ] Client company name displays
- [ ] Name matches the client in your assigned clients

#### Column: Service
- [ ] Service name displays (e.g., "MSME Registration", "GST Registration")
- [ ] Text is readable and properly formatted

#### Column: Amount
- [ ] Amount shows with ₹ symbol
- [ ] Shows `final_amount` if available, otherwise `amount`
- [ ] Number formatted properly (e.g., "₹5000.00")

#### Column: Status
- [ ] Status badge displays (e.g., "CONFIRMED", "PENDING")
- [ ] Badge has `bg-secondary` class (gray background)
- [ ] Status text is readable

#### Column: Action
**This is critical - test both scenarios:**

**Scenario A: Payment NOT completed**
- [ ] Button shows "Record Payment" with cash icon
- [ ] Button is green (`btn-success`)
- [ ] Button is small size (`btn-sm`)
- [ ] Click "Record Payment" button
- [ ] **Expected URL:** `/record-payment/<booking_id>/`
- [ ] **Expected:** Payment recording form page loads
- [ ] Form has fields: Amount, Payment Method, Reference ID, Notes, Proof (file upload)
- [ ] Go back to dashboard (use browser back or navigate)

**Scenario B: Payment completed (CAPTURED status)**
- [ ] Button shows "Create Application" with file-plus icon
- [ ] Button is blue (`btn-primary`)
- [ ] Click "Create Application" button
- [ ] **Expected URL:** `/applications/create-from-booking/<booking_id>/`
- [ ] **Expected:** Application creation form loads
- [ ] Form pre-fills with booking and client data
- [ ] Go back to dashboard

### Empty State (If No Bookings)
- [ ] Shows message: "No bookings yet"
- [ ] Message is centered and muted

### Data Accuracy
- [ ] **CRITICAL:** Only see bookings assigned to you (assigned_to = sales1)
- [ ] **CRITICAL:** Should NOT see other sales users' bookings
- [ ] Number matches "My Bookings" stat card

**✅ Pass Criteria:** Table shows only assigned bookings with working action buttons

---

## 🔍 STEP 6: PERMISSION & SECURITY TESTING

### Access Control Tests

#### Test: Cannot Access Manager Routes
- [ ] Try accessing: http://127.0.0.1:8000/applications/pending/
- [ ] **Expected:** HTTP 403 Forbidden page or redirect
- [ ] **Expected:** Custom 403 error page with shield icon
- [ ] **Expected:** Message indicates lack of permission

#### Test: Cannot Access Admin Routes
- [ ] Try accessing: http://127.0.0.1:8000/applications/admin/applications/
- [ ] **Expected:** HTTP 403 Forbidden or redirect
- [ ] Try accessing: http://127.0.0.1:8000/payments/admin/payments/
- [ ] **Expected:** HTTP 403 Forbidden or redirect

#### Test: Cannot Access Other Sales' Data
- [ ] Check clients table - should not see clients assigned to other sales
- [ ] Check bookings table - should not see bookings assigned to other sales
- [ ] If you know another sales user exists, verify their clients don't show

#### Test: Can Access Own Routes
- [ ] Navigate to: http://127.0.0.1:8000/bookings/sales/bookings/
- [ ] **Expected:** HTTP 200 OK, page loads
- [ ] Navigate to: http://127.0.0.1:8000/applications/sales/applications/
- [ ] **Expected:** HTTP 200 OK, page loads

**✅ Pass Criteria:** Sales user sees only assigned data, blocked from manager/admin routes

---

## 🔄 STEP 7: WORKFLOW TESTING

### Workflow 1: Record Payment for Booking

#### Prerequisites:
- [ ] Have at least one booking in "My Bookings" table without payment

#### Steps:
1. [ ] Click "Record Payment" button on a booking
2. [ ] Payment form page loads
3. [ ] Fill out form:
   - [ ] Amount: (check pre-filled or enter amount)
   - [ ] Payment Method: Select "UPI_QR" or other option
   - [ ] Reference ID: Enter "TEST-REF-12345"
   - [ ] Notes: Enter "Test payment recording"
   - [ ] Proof: Upload a test image/PDF (optional)
4. [ ] Click "Submit" or "Record Payment" button
5. [ ] **Expected:** Redirect back to dashboard or bookings page
6. [ ] **Expected:** Success message appears
7. [ ] **Expected:** Payment status changes to "PENDING" (awaiting manager approval)
8. [ ] Check booking row again:
   - [ ] Action button might change or show different state
9. [ ] **Server Log Check:** Look for `POST /record-payment/<id>/` with HTTP 200 or 302

**✅ Pass Criteria:** Payment recorded successfully and awaits approval

---

### Workflow 2: Create Application from Paid Booking

#### Prerequisites:
- [ ] Have a booking with payment status "CAPTURED"

#### Steps:
1. [ ] Find booking with "Create Application" button
2. [ ] Click "Create Application" button
3. [ ] Application form page loads
4. [ ] Verify pre-filled fields:
   - [ ] Client: Should be auto-selected from booking
   - [ ] Booking: Should reference the booking ID
   - [ ] Amount: Should pre-fill from booking
5. [ ] Fill additional fields:
   - [ ] Scheme: Select a scheme from dropdown
   - [ ] Applied Amount: Verify or adjust amount
   - [ ] Purpose: Enter "Test application purpose"
6. [ ] Click "Submit" or "Create Application" button
7. [ ] **Expected:** Redirect to applications list or detail page
8. [ ] **Expected:** Success message appears
9. [ ] **Expected:** New application appears in "My Applications"
10. [ ] Navigate to "My Applications" sidebar link
11. [ ] **Expected:** New application is listed
12. [ ] **Server Log Check:** Look for `POST /applications/create-from-booking/<id>/` with 200 or 302

**✅ Pass Criteria:** Application created successfully from booking

---

## 📱 STEP 8: RESPONSIVE DESIGN & UI/UX

### Desktop View (Full Width)
- [ ] Dashboard displays in 3-column grid for stats cards
- [ ] Tables have proper spacing
- [ ] Sidebar is visible and fixed
- [ ] No horizontal scrolling
- [ ] All text is readable

### Tablet View (Resize to ~768px width)
- [ ] Stats cards stack properly (maybe 2 columns)
- [ ] Tables remain responsive with horizontal scroll if needed
- [ ] Sidebar might collapse or overlay
- [ ] Navigation still accessible

### Mobile View (Resize to ~375px width)
- [ ] Stats cards stack vertically (1 column)
- [ ] Tables have horizontal scroll
- [ ] Sidebar becomes hamburger menu or overlay
- [ ] All features still accessible

### Visual Consistency
- [ ] Agnivridhi cyan/teal color scheme throughout
- [ ] Bootstrap icons display correctly
- [ ] Cards have consistent styling
- [ ] Buttons use proper Bootstrap classes
- [ ] Table hover effects work
- [ ] No broken images or icons

**✅ Pass Criteria:** Dashboard is responsive and visually consistent

---

## 🐛 STEP 9: ERROR HANDLING

### Test Error Scenarios

#### No Data Scenarios:
- [ ] Dashboard handles 0 clients gracefully
- [ ] Dashboard handles 0 bookings gracefully
- [ ] Dashboard handles 0 applications gracefully
- [ ] Empty state messages are helpful and styled

#### Invalid Actions:
- [ ] Try recording payment for non-existent booking: `/record-payment/99999/`
- [ ] **Expected:** 404 error page or redirect with error message
- [ ] Try creating application from non-existent booking
- [ ] **Expected:** 404 error or error message

#### Form Validation:
- [ ] Go to record payment form
- [ ] Submit without filling required fields
- [ ] **Expected:** Validation errors display
- [ ] **Expected:** Form doesn't submit
- [ ] Fill form properly and submit
- [ ] **Expected:** Successful submission

**✅ Pass Criteria:** All error scenarios handled gracefully

---

## 🚀 STEP 10: PERFORMANCE & LOGGING

### Performance Check
- [ ] Dashboard loads within 2 seconds
- [ ] No visible lag when clicking links
- [ ] Tables render quickly even with multiple rows
- [ ] Images/icons load without delay

### Server Log Verification
**Check terminal for logs:**

Expected log entries:
```
[07/Nov/2025 XX:XX:XX] "GET /dashboard/ HTTP/1.1" 302 0
[07/Nov/2025 XX:XX:XX] "GET /dashboard/sales/ HTTP/1.1" 200 XXXX
[07/Nov/2025 XX:XX:XX] "GET /bookings/sales/bookings/ HTTP/1.1" 200 XXXX
[07/Nov/2025 XX:XX:XX] "GET /applications/sales/applications/ HTTP/1.1" 200 XXXX
```

- [ ] All successful routes return HTTP 200
- [ ] Redirects show HTTP 302
- [ ] No HTTP 500 errors (server errors)
- [ ] No HTTP 403 errors on allowed routes
- [ ] HTTP 403 appears only on restricted routes

### Database Query Efficiency
- [ ] Dashboard doesn't cause excessive database queries
- [ ] Page load doesn't freeze or timeout

**✅ Pass Criteria:** Dashboard performs well with proper logging

---

## 📋 FINAL CHECKLIST SUMMARY

### Core Features:
- [ ] ✅ Login and role-based redirect works
- [ ] ✅ Dashboard displays 3 stat cards with accurate counts
- [ ] ✅ Sidebar navigation has 4 links (1 may be placeholder)
- [ ] ✅ My Clients table shows only assigned clients
- [ ] ✅ My Bookings table shows only assigned bookings
- [ ] ✅ Booking ID links to detail page
- [ ] ✅ "Record Payment" button works for unpaid bookings
- [ ] ✅ "Create Application" button works for paid bookings

### Security:
- [ ] ✅ Sales user cannot access manager/admin routes (403)
- [ ] ✅ Sales user sees only their assigned data
- [ ] ✅ Other sales users' data is hidden

### Workflows:
- [ ] ✅ Can record payment successfully
- [ ] ✅ Can create application from booking
- [ ] ✅ Data persists after workflow actions

### UI/UX:
- [ ] ✅ Responsive design works on all screen sizes
- [ ] ✅ Consistent Agnivridhi branding
- [ ] ✅ All icons display correctly
- [ ] ✅ No broken links or buttons

### Performance:
- [ ] ✅ Dashboard loads quickly (<2 sec)
- [ ] ✅ Server logs show HTTP 200 for all valid routes
- [ ] ✅ No server errors in terminal

---

## 🎯 TEST RESULTS

### Overall Status: ⏳ TESTING IN PROGRESS

| Feature | Status | Notes |
|---------|--------|-------|
| Login & Access | ⏳ | |
| Stats Cards | ⏳ | |
| Sidebar Navigation | ⏳ | "My Clients" link is `href="#"` |
| Clients Table | ⏳ | |
| Bookings Table | ⏳ | |
| Action Buttons | ⏳ | |
| Record Payment | ⏳ | |
| Create Application | ⏳ | |
| Permissions | ⏳ | |
| Responsive Design | ⏳ | |

---

## 🐛 ISSUES FOUND

### Issue #1: My Clients Navigation Link
- **Location:** Sidebar → "My Clients" link
- **Current:** `href="#"` (goes nowhere)
- **Expected:** Should link to clients list filtered by sales user
- **Severity:** Medium
- **Fix Needed:** Update href to proper URL (e.g., `/clients/` with filter)
- **Status:** 🔴 NEEDS FIX

### Issue #2: [Add more issues as found]
- **Location:**
- **Description:**
- **Expected:**
- **Severity:**
- **Status:**

---

## 📝 TESTING NOTES

**Note 1:** The "My Clients" link in sidebar currently has `href="#"` which means it doesn't navigate anywhere. This should be updated to link to a clients list view filtered by the sales user.

**Note 2:** Action buttons in bookings table dynamically change based on payment status:
- No payment OR payment not CAPTURED → "Record Payment" (green)
- Payment CAPTURED → "Create Application" (blue)

**Note 3:** All payment recordings go to PENDING status and require manager/admin approval before being CAPTURED.

---

## 🎬 NEXT STEPS AFTER SALES DASHBOARD

Once Sales Dashboard is fully tested:
1. Test **Manager Dashboard** - Verify manager can approve payments
2. Test **Admin Dashboard** - Full system overview
3. Test **Client Dashboard** - AI recommendations and applications
4. Test **Complete Workflow** - End-to-end from booking to application approval

---

**Testing Start Time:** [Fill in when you start]  
**Testing End Time:** [Fill in when complete]  
**Total Issues Found:** [Count at end]  
**Critical Issues:** [Count at end]  
**Status:** ⏳ IN PROGRESS → ✅ COMPLETE
