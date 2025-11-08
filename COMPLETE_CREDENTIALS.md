# 🔑 COMPLETE TEST USER CREDENTIALS - Agnivridhi CRM

**Last Updated:** Current Session  
**All users password:** `test123`

---

## 🎯 QUICK REFERENCE

| Role | Username | Password | Dashboard URL |
|------|----------|----------|---------------|
| **OWNER** | owner | test123 | /dashboard/owner/ |
| **ADMIN** | admin | test123 | /dashboard/admin/ |
| **MANAGER** | manager1 | test123 | /dashboard/manager/ |
| **SALES** | sales1 | test123 | /dashboard/sales/ |
| **CLIENT** | client1 | test123 | /dashboard/client/ |

---

## 👑 OWNER USER (Company Owner)

| Username | Password | Role | Full Name | Email | Special Access |
|----------|----------|------|-----------|-------|----------------|
| `owner` | test123 | ADMIN (is_owner=True) | Akash | akash@agnivridhiindia.com | Owner Dashboard + All Features |

**Access:**
- Owner Dashboard: http://127.0.0.1:8000/dashboard/owner/
- Admin Dashboard: http://127.0.0.1:8000/dashboard/admin/
- Django Admin: http://127.0.0.1:8000/admin/
- Full system access with owner-level permissions

**Special Features:**
- Company-wide revenue analytics
- All manager team data visibility
- System configuration access
- Complete business intelligence

---

## 👤 ADMIN USER

| Username | Password | Role | Full Name | Email | Dashboard URL |
|----------|----------|------|-----------|-------|---------------|
| `admin` | test123 | ADMIN | Admin User | admin@agnivridhiindia.com | /dashboard/admin/ |

**Access:**
- Admin Dashboard with full system visibility
- All clients, applications, bookings across all teams
- User management and approvals
- System-wide reports

---

## 👔 MANAGER USERS (3 Managers)

| Username | Password | Full Name | Email | Team Size | Dashboard URL |
|----------|----------|-----------|-------|-----------|---------------|
| `manager1` | test123 | Rajesh Kumar | manager1@agnivridhiindia.com | 3 employees | /dashboard/manager/ |
| `manager2` | test123 | Priya Sharma | manager2@agnivridhiindia.com | 3 employees | /dashboard/manager/ |
| `manager3` | test123 | Amit Patel | manager3@agnivridhiindia.com | 3 employees | /dashboard/manager/ |

### Manager Teams

**Manager 1 (Rajesh Kumar):**
- sales1 - Sales One
- sales2 - Neha Gupta
- sales3 - Rohit Singh

**Manager 2 (Priya Sharma):**
- sales4 - Anjali Verma
- sales5 - Vikram Reddy
- sales6 - Pooja Nair

**Manager 3 (Amit Patel):**
- sales7 - Karan Malhotra
- sales8 - Divya Iyer
- sales9 - Arjun Kapoor

---

## 💼 SALES USERS (9 Sales Employees)

### Team 1 - Reports to Manager1 (Rajesh Kumar)

| Username | Password | Full Name | Email | Clients | Dashboard URL |
|----------|----------|-----------|-------|---------|---------------|
| `sales1` | test123 | Sales One | sales1@agnivridhiindia.com | 1 | /dashboard/sales/ |
| `sales2` | test123 | Neha Gupta | sales2@agnivridhiindia.com | 0 | /dashboard/sales/ |
| `sales3` | test123 | Rohit Singh | sales3@agnivridhiindia.com | 0 | /dashboard/sales/ |

### Team 2 - Reports to Manager2 (Priya Sharma)

| Username | Password | Full Name | Email | Clients | Dashboard URL |
|----------|----------|-----------|-------|---------|---------------|
| `sales4` | test123 | Anjali Verma | sales4@agnivridhiindia.com | 0 | /dashboard/sales/ |
| `sales5` | test123 | Vikram Reddy | sales5@agnivridhiindia.com | 0 | /dashboard/sales/ |
| `sales6` | test123 | Pooja Nair | sales6@agnivridhiindia.com | 0 | /dashboard/sales/ |

### Team 3 - Reports to Manager3 (Amit Patel)

| Username | Password | Full Name | Email | Clients | Dashboard URL |
|----------|----------|-----------|-------|---------|---------------|
| `sales7` | test123 | Karan Malhotra | sales7@agnivridhiindia.com | 0 | /dashboard/sales/ |
| `sales8` | test123 | Divya Iyer | sales8@agnivridhiindia.com | 0 | /dashboard/sales/ |
| `sales9` | test123 | Arjun Kapoor | sales9@agnivridhiindia.com | 0 | /dashboard/sales/ |

---

## 👥 CLIENT USERS

| Username | Password | Full Name | Email | Dashboard URL |
|----------|----------|-----------|-------|---------------|
| `client1` | test123 | Client One | client1@agnivridhiindia.com | /dashboard/client/ |

**Assigned to:** sales1 (Manager1's team)

---

## 🌐 LOGIN & ACCESS INFORMATION

### Login Page
**URL:** http://127.0.0.1:8000/login/

### Dashboard URLs (After Login)

| Role | URL | Auto-Redirect |
|------|-----|---------------|
| Owner | http://127.0.0.1:8000/dashboard/owner/ | ✅ Yes |
| Admin | http://127.0.0.1:8000/dashboard/admin/ | ✅ Yes |
| Manager | http://127.0.0.1:8000/dashboard/manager/ | ✅ Yes |
| Sales | http://127.0.0.1:8000/dashboard/sales/ | ✅ Yes |
| Client | http://127.0.0.1:8000/dashboard/client/ | ✅ Yes |

**Note:** After successful login, users are automatically redirected to their respective dashboard based on their role.

---

## 🧪 TESTING SCENARIOS

### Test 1: Owner Dashboard Access
```
1. Login: owner / test123
2. Expected: Redirect to /dashboard/owner/
3. Features to verify:
   ✅ Company-wide revenue analytics
   ✅ All team performance metrics
   ✅ System-wide statistics
   ✅ Link to Admin Dashboard
   ✅ Link to Django Admin
```

### Test 2: Admin Dashboard Access
```
1. Login: admin / test123
2. Expected: Redirect to /dashboard/admin/
3. Features to verify:
   ✅ All users visibility
   ✅ All clients across teams
   ✅ All applications, bookings, payments
   ✅ System-wide reports
```

### Test 3: Manager Dashboard - Unified Pending Approvals
```
1. Login: manager1 / test123
2. Navigate to: Pending Approvals
3. Features to verify:
   ✅ See pending applications from manager1's team
   ✅ See pending applications from sales1, sales2, sales3
   ✅ Approve applications directly inline (POST form)
   ✅ See pending payments with inline approve
   ✅ See pending edit requests with inline approve
   ✅ See pending clients with inline approve
   ✅ After approval, stay on pending approvals page
```

### Test 4: Sales Dashboard
```
1. Login: sales1 / test123
2. Expected: Redirect to /dashboard/sales/
3. Features to verify:
   ✅ View assigned clients
   ✅ Create bookings
   ✅ Record payments
   ✅ Create applications
   ✅ Data isolated from other sales users
```

### Test 5: Client Dashboard
```
1. Login: client1 / test123
2. Expected: Redirect to /dashboard/client/
3. Features to verify:
   ✅ View own bookings
   ✅ View own applications
   ✅ View own documents
   ✅ AI scheme recommendations
   ✅ Cannot see other clients' data
```

### Test 6: Cross-Team Data Isolation
```
1. Login as sales1 (Manager1's team)
2. Note client name: "Test Co Pvt Ltd"
3. Logout
4. Login as sales5 (Manager2's team)
5. Verify: Cannot see "Test Co Pvt Ltd" client
Result: ✅ Data properly isolated between teams
```

### Test 7: Pending Approvals - Team Scope
```
1. Login as manager1
2. Go to Pending Approvals
3. Create test application via sales1
4. Verify manager1 sees it in pending approvals
5. Approve inline from pending approvals page
6. Verify redirect back to pending approvals
7. Verify application now shows as APPROVED
Result: ✅ Unified approval workflow working
```

---

## 📊 USER STATISTICS

- **Total Users:** 14
- **Owner Users:** 1 (owner)
- **Admin Users:** 1 (admin)
- **Manager Users:** 3
- **Sales Users:** 9
- **Client Users:** 1
- **Clients Assigned:** 1 (to sales1)
- **Bookings Created:** 3 (all by sales1)
- **Applications Created:** 3 (all by sales1)

---

## 🔒 SECURITY NOTES

1. **Password:** All test users currently use `test123` for easy testing
2. **Production:** Change all passwords before going live
3. **Roles:** Properly enforced via Django's permission system
4. **Data Isolation:** Verified working between teams
5. **Session Security:** Django's built-in session management
6. **Owner Access:** Special `is_owner` flag for owner-specific dashboard

---

## 🐛 RECENT FIXES

### ✅ Fixed Issues:
1. **Global Search URL:** Fixed NoReverseMatch for 'global_search' → Added 'accounts:' namespace
2. **Clients Navlink:** Updated to show full team scope (manager + sales subordinates)
3. **Pending Approvals:** Added inline approval forms for all approval types
4. **Owner Dashboard:** Fixed URL namespace issues (owner_dashboard → accounts:owner_dashboard)
5. **Rejection Template:** Created reject_application.html template
6. **Team Scope:** Expanded Q filters to include sales subordinate data

### ✅ Working Features:
- Unified pending approvals page with inline actions
- CSRF-protected POST forms for approvals
- Next parameter redirect handling
- JSON/AJAX response support
- Team data visibility for managers
- Data isolation between teams
- Role-based dashboard routing

---

## 🚀 RECOMMENDED TEST SEQUENCE

**For complete system verification:**

1. **Start with Owner** (`owner / test123`)
   - Verify owner dashboard loads
   - Check company-wide analytics
   - Access admin dashboard from owner dashboard

2. **Test Admin** (`admin / test123`)
   - Verify full system visibility
   - Check user management features
   - Access Django admin

3. **Test Manager** (`manager1 / test123`)
   - Navigate to Pending Approvals
   - Verify team scope (sales1, sales2, sales3 data visible)
   - Test inline approvals (Applications, Payments, Edit Requests, Clients)
   - Verify redirect back to pending approvals after approval

4. **Test Sales** (`sales1 / test123`)
   - Create new client
   - Create booking
   - Record payment
   - Create application
   - Verify data appears in manager1's pending approvals

5. **Test Client** (`client1 / test123`)
   - View dashboard
   - Check AI recommendations
   - View applications status

6. **Cross-Team Test**
   - Login as `manager2 / test123`
   - Verify cannot see manager1's team data
   - Confirm data isolation

---

## 📝 NOTES

- **Server must be running:** `python manage.py runserver`
- **Login URL:** http://127.0.0.1:8000/login/
- **Auto-redirect:** After login, users automatically go to their dashboard
- **Logout URL:** http://127.0.0.1:8000/logout/
- **Django Admin:** http://127.0.0.1:8000/admin/ (owner/admin users)

---

**Document Created:** Current Session  
**System:** Agnivridhi CRM v1.0  
**Status:** ✅ All dashboards operational, Owner dashboard fixed
