# 🧪 TESTING SESSION - November 6, 2025

## 📋 AVAILABLE TEST ACCOUNTS

| Role | Username | Email | Use For |
|------|----------|-------|---------|
| **ADMIN** | admin | admin@agnivridhiindia.com | Full system access, approvals |
| **ADMIN** | owner | akash@agnivridhiindia.com | Alternative admin |
| **MANAGER** | manager1 | utkarshchoudhary1573@gmail.com | Team management, approvals |
| **SALES** | sales1 | sales1@agnivridhiindia.com | Client management, payments |
| **CLIENT** | client1 | client1@agnivridhiindia.com | AI recommendations, applications |

**Note:** Use password you set during setup (or reset via Django admin)

---

## ✅ TEST 1: CLIENT DASHBOARD & AI RECOMMENDATIONS

### Steps:
1. ✅ Open http://127.0.0.1:8000/login/ (DONE)
2. Login with: `client1` / [password]
3. Should redirect to Client Portal
4. **Check AI Recommendations Section:**
   - Should see **CGTMSE** with **100% Match** ✅ ELIGIBLE
   - Should see **SIDBI** with **75% Match** ✅ ELIGIBLE
   - Should see match percentages for other schemes
   - Eligibility status (green check or reasons)

### Expected Results:
- ✅ CGTMSE shows as top recommendation
- ✅ Match percentages displayed
- ✅ Eligibility clearly indicated
- ✅ "Apply" button for eligible schemes
- ✅ Scheme details visible
 
---

## ✅ TEST 2: ADMIN DASHBOARD

### Steps:
1. Logout from client account
2. Login with: `admin` / [password]
3. Should redirect to Admin Dashboard
4. **Check Dashboard Components:**
   - Analytics cards (Total Clients, Bookings, Revenue, Applications)
   - Pending Edit Requests table
   - Recent Clients list
   - Recent Bookings list
   - Recent Applications list

### Expected Results:
- ✅ Analytics show correct counts
- ✅ Navigation sidebar visible
- ✅ All sections load without errors
- ✅ Data displays correctly

---

## ✅ TEST 3: SWAGGER API TESTING

### Steps:
1. Open http://127.0.0.1:8000/api/docs/
2. Click "Authorize" button (top right)
3. Enter: Username: `admin`, Password: [your password]
4. Click "Authorize" then "Close"
5. **Test These Endpoints:**

#### a) GET `/api/schemes/`
- Click "Try it out"
- Click "Execute"
- **Expected:** List of 5 schemes in JSON

#### b) GET `/api/clients/`
- Click "Try it out"
- Click "Execute"
- **Expected:** List with 1 client

#### c) GET `/api/bookings/`
- Click "Try it out"
- Click "Execute"
- **Expected:** List with 1 booking

#### d) POST `/api/applications/` (Create Application)
- Click "Try it out"
- Modify request body:
```json
{
  "client": 1,
  "scheme": 1,
  "applied_amount": "50.00",
  "purpose": "Working capital for business expansion"
}
```
- Click "Execute"
- **Expected:** 201 Created response

### Expected Results:
- ✅ All GET requests return 200 OK
- ✅ Data is properly formatted JSON
- ✅ POST request creates application successfully
- ✅ Response includes all fields

---

## ✅ TEST 4: MANAGER DASHBOARD

### Steps:
1. Logout from admin
2. Login with: `manager1` / [password]
3. Should redirect to Manager Dashboard
4. **Check Components:**
   - Team Overview cards
   - Team Members table
   - Team Clients view
   - Team Bookings view

### Expected Results:
- ✅ Can see assigned team members
- ✅ Can see team clients
- ✅ Navigation works
- ✅ No permission errors

---

## ✅ TEST 5: SALES DASHBOARD

### Steps:
1. Logout from manager
2. Login with: `sales1` / [password]
3. Should redirect to Sales Dashboard
4. **Check Components:**
   - My Stats cards
   - Assigned Clients table
   - My Bookings view
   - Quick actions

### Expected Results:
- ✅ Shows only assigned clients
- ✅ Can view client details
- ✅ Stats are accurate
- ✅ No access to other sales' data

---

## ✅ TEST 6: DJANGO ADMIN INTERFACE

### Steps:
1. Login as admin user
2. Go to http://127.0.0.1:8000/admin/
3. **Navigate through sections:**
   - Accounts → Users
   - Clients → Clients
   - Schemes → Schemes (should show 5)
   - Bookings → Bookings
   - Bookings → Services
   - Applications → Applications
   - Payments → Payments

### Expected Results:
- ✅ All models visible
- ✅ List displays show data
- ✅ Filters work
- ✅ Search works
- ✅ Can view details
- ✅ 5 schemes visible in Schemes section

---

## ✅ TEST 7: PDF GENERATION

### Steps:
1. Open http://127.0.0.1:8000/pdf/payment/1/
2. **Expected:** PDF receipt downloads

### Alternative:
1. Login as admin
2. Go to Payments in Django admin
3. Open payment record
4. Look for "Download Receipt" link

### Expected Results:
- ✅ PDF generates without errors
- ✅ PDF contains payment details
- ✅ Professional formatting
- ✅ Company branding visible

---

## 🎯 TESTING PRIORITIES

### Priority 1 (MUST TEST NOW):
- [ ] Client Dashboard - AI Recommendations
- [ ] Swagger API - GET /api/schemes/
- [ ] Admin Dashboard - Analytics

### Priority 2 (TEST SOON):
- [ ] Manager Dashboard
- [ ] Sales Dashboard
- [ ] Django Admin - All sections
- [ ] PDF Generation

### Priority 3 (WORKFLOW TESTING):
- [ ] **Create new client (Sales → Manager approval)** ⭐ NEW FEATURE
- [ ] Record manual payment (Sales → Manager approval)
- [ ] Create application
- [ ] Edit request workflow

---

## 🔧 TEST 9: SALES DASHBOARD - ALL NAVLINKS ⭐ **UPDATED**

### **Context**: Fixed middleware blocking + URL namespace issues

#### **Issue 1 - NoReverseMatch Fixed**:
- ✅ Added namespace prefixes to redirects in bookings/views.py
- ✅ Added namespace prefixes to redirects in payments/views.py

#### **Issue 2 - "Unauthorized" Error Fixed**:
- ✅ Added "clients" namespace to SALES role in constants.py
- ✅ All roles now have proper namespace access

### **Part A: Test All Navigation Links**

#### Steps:
1. **Restart server first** (middleware changes need reload):
   ```powershell
   # Press Ctrl+C in terminal running server
   python manage.py runserver
   ```

2. Login as `sales1` / `test123`
3. Click each navigation link in order:

   - [ ] **Dashboard** → Should load sales dashboard
   - [ ] **My Clients** → Should open `/clients/my-clients/`
   - [ ] **Pending Approvals** → Should open `/clients/pending-approval/`
   - [ ] **Total Bookings** → Should open `/bookings/sales/`
   - [ ] **My Applications** → Should open `/applications/sales/`
   - [ ] **Payments** → Should open `/payments/sales/`

#### Expected Results:
- ✅ No "NoReverseMatch" errors
- ✅ No "Unauthorized" errors
- ✅ All pages load successfully
- ✅ Each page shows sales-specific data

---

### **Part B: Test Data Isolation**

#### Steps:
1. On **My Clients** page:
   - Should see ONLY clients assigned to sales1
   - Should see "Create New Client" button

2. On **Pending Approvals** page:
   - Should see ONLY clients created by sales1
   - Should see approval status for each

3. On **Total Bookings** page:
   - Should see ONLY bookings for sales1's assigned clients
   - Click "View" button → Should open booking detail

4. On **My Applications** page:
   - Should see ONLY applications assigned to sales1
   - No template syntax errors

5. On **Payments** page:
   - Should see ONLY payments for sales1's clients
   - Professional layout with sales sidebar

#### Expected Results:
- ✅ Each page shows ONLY sales1's data
- ✅ No data from other sales persons visible
- ✅ View buttons work correctly
- ✅ No permission errors

---

### **Part C: Test Client Creation Workflow**

#### Steps:
1. From sales dashboard, click "Create New Client"
2. Fill out client form with test data
3. Submit form

#### Expected Results:
- ✅ Form submits successfully
- ✅ Redirects to pending approvals page
- ✅ New client appears in pending list
- ✅ Status shows "Awaiting Approval"

---

## 🆕 TEST 8: CLIENT CREATION & APPROVAL WORKFLOW

### **Part A: Sales Creates Client (Needs Approval)**

#### Steps:
1. Login as `sales1` / `test123`
2. Go to Sales Dashboard
3. Click **"Create New Client"** button
4. Fill out the form:
   - **Contact Person**: John Doe
   - **Contact Email**: john.doe@testcompany.com
   - **Contact Phone**: +91 9876543210
   - **Company Name**: Test Manufacturing Ltd
   - **Business Type**: Pvt Ltd Company
   - **Sector**: Manufacturing
   - **Company Age**: 5
   - **Address Line 1**: 123 Industrial Area
   - **City**: Mumbai
   - **State**: Maharashtra
   - **Pincode**: 400001
   - **Annual Turnover**: 5000000
   - **Funding Required**: 2000000
   - **Existing Loans**: 500000
5. Submit the form

#### Expected Results:
- ✅ Success message: "Client created successfully! Waiting for manager approval."
- ✅ Redirected to Pending Approvals page
- ✅ New client appears in pending list
- ✅ Client shows "Awaiting Approval" status

---

### **Part B: Manager Reviews and Approves**

#### Steps:
1. Logout from sales1
2. Login as `manager1` / `test123`
3. Should see alert: "1 new client awaiting your approval"
4. Click "Client Approvals" in sidebar
5. See the new client in pending list
6. Click **"Review"** button
7. Review all client details
8. Select **"Approve"** radio button
9. Click **"Submit Decision"**

#### Expected Results:
- ✅ Success message: "Client 'Test Manufacturing Ltd' has been approved!"
- ✅ Client removed from pending list
- ✅ Client now appears in approved clients
- ✅ Client user account activated

---

### **Part C: Test Manager Direct Creation**

#### Steps:
1. Still logged in as `manager1`
2. Click **"Create New Client"** from dashboard
3. Fill out form with different data:
   - **Contact Person**: Jane Smith
   - **Contact Email**: jane.smith@anothercompany.com
   - **Company Name**: Direct Approval Corp
   - (fill other required fields)
4. Submit

#### Expected Results:
- ✅ Success message: "Client created and approved successfully!"
- ✅ No approval needed (manager privilege)
- ✅ Client immediately active
- ✅ Appears in approved clients list

---

### **Part D: Test Rejection Workflow**

#### Steps:
1. Login as `sales1`
2. Create another new client (use different email)
3. Logout, login as `manager1`
4. Go to Pending Approvals
5. Click **"Review"** on new client
6. Select **"Reject"** radio button
7. Enter rejection reason: "Incomplete documentation"
8. Submit

#### Expected Results:
- ✅ Warning message: "Client rejected"
- ✅ Client marked as rejected
- ✅ Rejection reason saved
- ✅ Sales person can see rejection status (TODO: notification)

---

## 📝 TEST RESULTS LOG

### ✅ Server Status
- Status: ✅ RUNNING
- URL: http://127.0.0.1:8000/
- Time: November 7, 2025 - 11:25 AM
- Django Version: 5.2.7
- System Check: 0 issues

### Test 1: Client Dashboard
- Status: ⏳ IN PROGRESS
- Notes: Browser open at login page - ready to test

### Test 2: Admin Dashboard
- Status: ⏳ PENDING
- Notes:

### Test 3: Swagger API
- Status: ⏳ PENDING
- Notes:

### Test 4: AI Recommendations
- Status: ✅ PASSED (Command line test)
- Notes: CGTMSE 100%, SIDBI 75% working correctly

---

## 🚀 QUICK COMMANDS

```powershell
# Check if server is running
# Open new terminal and run:
curl http://127.0.0.1:8000/

# Reset admin password if needed
python manage.py changepassword admin

# Create test data
python manage.py shell
```

---

## 📞 QUICK ACCESS URLS

- **Login:** http://127.0.0.1:8000/login/
- **Dashboard:** http://127.0.0.1:8000/dashboard/
- **Admin:** http://127.0.0.1:8000/admin/
- **API Docs:** http://127.0.0.1:8000/api/docs/
- **API Root:** http://127.0.0.1:8000/api/
- **ReDoc:** http://127.0.0.1:8000/api/redoc/
- **Payment PDF:** http://127.0.0.1:8000/pdf/payment/1/

---

**Start Testing Now!** Browser is open at login page.
**Next Step:** Login as `client1` to test AI recommendations! 🚀
