# 🔑 TEST USER CREDENTIALS - Agnivridhi CRM

**Last Updated:** November 7, 2025  
**All users password:** `test123`

---

## 🎯 Quick Access

| Role | Count | Example Login |
|------|-------|---------------|
| Admin | 1 | admin / test123 |
| Manager | 3 | manager1 / test123 |
| Sales | 9 | sales1 / test123 |

---

## 👤 ADMIN USERS

| Username | Password | Full Name | Email | Dashboard URL |
|----------|----------|-----------|-------|---------------|
| `admin` | test123 | Admin User | admin@agnivridhiindia.com | /dashboard/admin/ |

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

## 📋 Complete List (All Users)

```
ADMIN:
  admin / test123

MANAGERS:
  manager1 / test123 → Rajesh Kumar
  manager2 / test123 → Priya Sharma
  manager3 / test123 → Amit Patel

SALES (Manager 1's Team):
  sales1 / test123 → Sales One
  sales2 / test123 → Neha Gupta
  sales3 / test123 → Rohit Singh

SALES (Manager 2's Team):
  sales4 / test123 → Anjali Verma
  sales5 / test123 → Vikram Reddy
  sales6 / test123 → Pooja Nair

SALES (Manager 3's Team):
  sales7 / test123 → Karan Malhotra
  sales8 / test123 → Divya Iyer
  sales9 / test123 → Arjun Kapoor
```

---

## 🌐 Access URLs

**Login Page:** http://127.0.0.1:8000/login/

**After Login - Automatic Redirects:**
- Admin users → http://127.0.0.1:8000/dashboard/admin/
- Manager users → http://127.0.0.1:8000/dashboard/manager/
- Sales users → http://127.0.0.1:8000/dashboard/sales/

---

## 🧪 Testing Scenarios

### Scenario 1: Test Sales Dashboard
```
Login: sales1 / test123
Expected: Redirect to /dashboard/sales/
Features: View assigned clients, bookings, applications
```

### Scenario 2: Test Manager Dashboard
```
Login: manager1 / test123
Expected: Redirect to /dashboard/manager/
Features: View team performance, approve payments, see team data
```

### Scenario 3: Test Admin Dashboard
```
Login: admin / test123
Expected: Redirect to /dashboard/admin/
Features: Full system access, all users, all data
```

### Scenario 4: Test Data Isolation
```
1. Login as sales1 (Manager1's team)
2. Note the client name: "Test Co Pvt Ltd"
3. Logout
4. Login as sales5 (Manager2's team)
5. Verify: Cannot see "Test Co Pvt Ltd" (different manager's team)
Result: ✅ Data isolated correctly
```

### Scenario 5: Test Permission Boundaries
```
Login: sales1 / test123
Try to access: http://127.0.0.1:8000/dashboard/manager/
Expected: 302 redirect (not authorized)
Result: ✅ Permission boundary enforced
```

---

## 📊 User Statistics

- **Total Users:** 13
- **Admin Users:** 1
- **Manager Users:** 3
- **Sales Users:** 9
- **Clients Assigned:** 1 (only to sales1)
- **Bookings Created:** 3 (all by sales1)
- **Applications Created:** 3 (all by sales1)

---

## 🔒 Security Notes

1. **Password:** All test users use `test123` for easy testing
2. **Production:** Change all passwords before going live
3. **Roles:** Properly enforced via Django's permission system
4. **Data Isolation:** Verified working between teams
5. **Session Security:** Django's built-in session management

---

## 🚀 Quick Start

**To test the system:**

1. Open browser: http://127.0.0.1:8000/
2. Login with any credentials above
3. Explore the respective dashboard
4. Test workflows (record payment, create application, etc.)

**Most Common Test Users:**
- `sales1 / test123` - Has existing data (1 client, 3 bookings)
- `manager1 / test123` - Manages 3 sales employees
- `admin / test123` - Full system access

---

**Document Version:** 1.0  
**Created:** November 7, 2025  
**System:** Agnivridhi CRM v1.0
