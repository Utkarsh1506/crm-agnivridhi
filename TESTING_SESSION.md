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
- [ ] Create new client (Sales → Manager approval)
- [ ] Record manual payment (Sales → Manager approval)
- [ ] Create application
- [ ] Edit request workflow

---

## 📝 TEST RESULTS LOG

### Test 1: Client Dashboard
- Status: ⏳ PENDING
- Notes: 

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
