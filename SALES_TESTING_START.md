# 🚀 SALES DASHBOARD TESTING - QUICK START

## ✅ Pre-Test Setup Complete!

### 📊 Test Data Available:
- **Sales User:** `sales1` (Active)
- **Email:** sales1@agnivridhiindia.com
- **Assigned Clients:** 1 (Test Co Pvt Ltd)
- **My Bookings:** 3 (₹35,000 total)
- **My Applications:** 3

---

## 🎯 START TESTING NOW!

### Step 1: Login to Sales Dashboard
```
1. Browser is already open at: http://127.0.0.1:8000/
2. Click logout if someone else is logged in
3. Login with:
   - Username: sales1
   - Password: [Use the password you set, or reset it]
4. Should redirect to Sales Dashboard
```

### If You Need to Reset Password:
```powershell
python manage.py changepassword sales1
# Enter new password when prompted
# Use this password to login
```

---

## 📋 TESTING CHECKLIST (Follow SALES_DASHBOARD_TEST.md)

### Priority 1: Core Dashboard Features (15 min)
- [ ] **Login** - Verify redirect to `/dashboard/sales/`
- [ ] **Stats Cards** - Check counts: 1 client, 3 bookings, 3 applications
- [ ] **My Clients Table** - Should show "Test Co Pvt Ltd"
- [ ] **My Bookings Table** - Should show 3 bookings
- [ ] **Booking Links** - Click booking IDs to view details

### Priority 2: Navigation & Buttons (10 min)
- [ ] **Sidebar Links** - Test all 4 navigation items
- [ ] **My Bookings Link** - Should go to `/bookings/sales/bookings/`
- [ ] **My Applications Link** - Should go to `/applications/sales/applications/`
- [ ] **Action Buttons** - Test "Record Payment" or "Create Application" buttons

### Priority 3: Workflows (15 min)
- [ ] **Record Payment** - Click button and fill payment form
- [ ] **Create Application** - If booking has payment, test application creation
- [ ] **View Details** - Click through to booking and application details

### Priority 4: Security (10 min)
- [ ] **Permissions** - Try accessing manager routes (should get 403)
- [ ] **Data Isolation** - Verify you only see your assigned data
- [ ] **Other Users' Data** - Should NOT see other sales users' clients

---

## 🎬 TESTING WORKFLOW

### Recommended Testing Order:

#### 1️⃣ Visual Inspection (5 min)
```
✓ Dashboard loads correctly
✓ All 3 stat cards visible
✓ Tables display with data
✓ Navigation sidebar present
✓ Agnivridhi branding visible
```

#### 2️⃣ Navigation Testing (5 min)
```
✓ Click "My Bookings" → Check it works
✓ Click "My Applications" → Check it works
✓ Click "Dashboard" → Returns to dashboard
✓ Note: "My Clients" might be href="#"
```

#### 3️⃣ Data Verification (10 min)
```
✓ Client table shows: Test Co Pvt Ltd
✓ Bookings table shows: 3 bookings
✓ Each booking has correct details
✓ Amounts display with ₹ symbol
✓ Status badges visible
```

#### 4️⃣ Action Buttons (10 min)
```
For each booking, check action button:
✓ If no payment: "Record Payment" (green)
✓ If payment captured: "Create Application" (blue)
✓ Click button and verify form loads
```

#### 5️⃣ Permissions (5 min)
```
Try accessing restricted URLs:
✓ http://127.0.0.1:8000/applications/pending/ → Should get 403
✓ http://127.0.0.1:8000/payments/admin/payments/ → Should get 403
✓ Check custom 403 error page displays
```

---

## 📊 Expected Results

### Dashboard Stats:
```
My Clients: 1
My Bookings: 3
My Applications: 3
```

### My Clients Table:
```
| Client ID | Company | Sector | Turnover | Funding Required | Status |
|-----------|---------|--------|----------|------------------|--------|
| [Auto]    | Test Co Pvt Ltd | Service | ₹[X] L | ₹[X] L | Active |
```

### My Bookings Table:
```
| Booking ID | Client | Service | Amount | Status | Action |
|------------|--------|---------|--------|--------|--------|
| BKG-20251106-VYVE | Test Co Pvt Ltd | Scheme Application Documentation | ₹5000.00 | [Status] | [Button] |
| BKG-20251106-RK5M | Test Co Pvt Ltd | Scheme Application Documentation | ₹5000.00 | [Status] | [Button] |
| BKG-20251105-8KEC | Test Co Pvt Ltd | Working Capital Advisory | ₹25000.00 | [Status] | [Button] |
```

---

## 🔍 What to Look For

### ✅ GOOD Signs:
- Dashboard loads within 2 seconds
- All data displays correctly
- Navigation links work (HTTP 200)
- Buttons are clickable and functional
- Only YOUR assigned data visible
- Server logs show HTTP 200 for valid routes
- Custom 403 page for restricted access

### 🔴 BAD Signs:
- Dashboard takes >5 seconds to load
- Stats cards show wrong numbers
- Tables are empty when data exists
- Links give 404 or 500 errors
- Buttons don't respond or give errors
- You see other sales users' data
- Server logs show HTTP 500 errors
- Generic error pages instead of custom ones

---

## 🐛 Known Issues to Verify

### Issue #1: "My Clients" Link
**Location:** Sidebar navigation  
**Problem:** Currently set to `href="#"` (goes nowhere)  
**Test:** Click the link and verify it doesn't navigate  
**Expected Fix:** Should link to filtered clients list  

### Check for More Issues:
- [ ] Any broken links or buttons?
- [ ] Any pages that return 404 or 500?
- [ ] Any data displaying incorrectly?
- [ ] Any permission bypasses?
- [ ] Any UI/UX problems?

---

## 📝 Document Your Findings

### As You Test, Note:
1. **What works perfectly** → Mark in SALES_DASHBOARD_TEST.md
2. **What needs fixing** → Add to "Issues Found" section
3. **Server log errors** → Copy from terminal
4. **Screenshots** → Capture any visual issues

### Quick Issue Template:
```
Issue #X: [Short Title]
- Location: [Where in dashboard]
- What happened: [Describe problem]
- What expected: [What should happen]
- Severity: [Low/Medium/High/Critical]
- Server log: [Copy relevant errors]
```

---

## 🎯 Success Criteria

### Sales Dashboard is PASSING if:
✅ All stats cards show correct numbers  
✅ Tables display assigned data only  
✅ Navigation links work (except known issue)  
✅ Action buttons are functional  
✅ Booking IDs link to detail pages  
✅ Security blocks unauthorized access  
✅ No server errors (500) during normal use  
✅ Responsive design works  

### Sales Dashboard is FAILING if:
❌ Data from other sales users visible  
❌ Critical buttons don't work  
❌ Server errors on normal operations  
❌ Security bypassed  
❌ Dashboard doesn't load  

---

## 🚀 LET'S START!

### Right Now:
1. **Open browser** to http://127.0.0.1:8000/
2. **Logout** if needed (click logout in navbar)
3. **Login** with sales1 credentials
4. **Follow** the testing checklist in SALES_DASHBOARD_TEST.md
5. **Document** everything you find

### Keep These Windows Open:
- ✅ **Browser** - For testing
- ✅ **VS Code** - To view SALES_DASHBOARD_TEST.md
- ✅ **Terminal** - To watch server logs
- ✅ **This File** - For quick reference

---

## 📞 Quick Commands

```powershell
# Reset sales1 password
python manage.py changepassword sales1

# Check sales1 data
python manage.py shell -c "from accounts.models import User; from clients.models import Client; from bookings.models import Booking; sales = User.objects.get(username='sales1'); print(f'Clients: {Client.objects.filter(assigned_sales=sales).count()}'); print(f'Bookings: {Booking.objects.filter(assigned_to=sales).count()}')"

# View server logs
# Just watch the terminal where server is running

# Stop server (if needed)
# Press Ctrl+C in server terminal
```

---

**⏱️ Estimated Testing Time:** 45-60 minutes  
**📋 Detailed Checklist:** See SALES_DASHBOARD_TEST.md  
**🎯 Current Focus:** Sales Dashboard Full Feature Testing  

**LET'S GO! 🚀**
