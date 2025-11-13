# 🔐 Current User Credentials - Agnivridhi CRM

**Date:** November 12, 2025  
**Environment:** Local Development (SQLite)  
**Total Users:** 15

---

## 📋 All Active Users

### 🎯 ADMIN USER (Superuser - Full Access)

| Username | Password | Email | Dashboard URL |
|----------|----------|-------|---------------|
| **admin** | Try: `Admin@123` or earlier set password | admin@agnivridhiindia.com | http://127.0.0.1:8000/admin-dashboard/ |

**Access:** Full system access, Django admin panel, all CRUD operations

---

### 👔 MANAGER USERS (Team Management)

| Username | Password | Email | Dashboard URL |
|----------|----------|-------|---------------|
| **manager1** | Try: `Manager@123` | manager1@agnivridhiindia.com | http://127.0.0.1:8000/manager-dashboard/ |
| **manager2** | Try: `Manager@123` | manager2@agnivridhiindia.com | http://127.0.0.1:8000/manager-dashboard/ |
| **manager3** | Try: `Manager@123` | manager3@agnivridhiindia.com | http://127.0.0.1:8000/manager-dashboard/ |

**Access:** Approve clients, assign tasks, view team performance, manage assigned clients

---

### 💼 SALES USERS (Sales Operations)

| Username | Password | Email | Dashboard URL |
|----------|----------|-------|---------------|
| **sales1** | Try: `Sales@123` | sales1@agnivridhiindia.com | http://127.0.0.1:8000/sales/dashboard/ |
| **sales2** | Try: `Sales@123` | sales2@agnivridhiindia.com | http://127.0.0.1:8000/sales/dashboard/ |
| **sales3** | Try: `Sales@123` | sales3@agnivridhiindia.com | http://127.0.0.1:8000/sales/dashboard/ |
| **sales4** | Try: `Sales@123` | sales4@agnivridhiindia.com | http://127.0.0.1:8000/sales/dashboard/ |
| **sales5** | Try: `Sales@123` | sales5@agnivridhiindia.com | http://127.0.0.1:8000/sales/dashboard/ |
| **sales6** | Try: `Sales@123` | sales6@agnivridhiindia.com | http://127.0.0.1:8000/sales/dashboard/ |
| **sales7** | Try: `Sales@123` | sales7@agnivridhiindia.com | http://127.0.0.1:8000/sales/dashboard/ |
| **sales8** | Try: `Sales@123` | sales8@agnivridhiindia.com | http://127.0.0.1:8000/sales/dashboard/ |
| **sales9** | Try: `Sales@123` | sales9@agnivridhiindia.com | http://127.0.0.1:8000/sales/dashboard/ |

**Access:** Create clients, bookings, applications; View assigned clients only; Record payments

---

### 👤 CLIENT USER (Client Portal)

| Username | Password | Email | Dashboard URL |
|----------|----------|-------|---------------|
| **client1** | Try: `Client@123` | client1@agnivridhiindia.com | http://127.0.0.1:8000/clients/dashboard/ |

**Access:** View own applications, payment history, upload documents (read-only mostly)

---

### 🏢 OWNER USER (Special Admin)

| Username | Password | Email | Dashboard URL |
|----------|----------|-------|---------------|
| **owner** | Try: `Owner@123` or `Admin@123` | akash@agnivridhiindia.com | http://127.0.0.1:8000/owner-dashboard/ or admin-dashboard |

**Access:** Owner-level analytics, full admin capabilities, special reports

---

## 🔑 Password Information

**⚠️ Important:** Passwords are **hashed** in the database for security. Actual passwords are NOT stored.

**Common Passwords to Try:**
- `Admin@123`
- `Manager@123`
- `Sales@123`
- `Client@123`
- `Owner@123`

**If password doesn't work:**

### Option 1: Reset Password via Django Command
```bash
.\venv\Scripts\python.exe manage.py changepassword admin
.\venv\Scripts\python.exe manage.py changepassword manager1
.\venv\Scripts\python.exe manage.py changepassword sales1
```

### Option 2: Set Known Password via Shell
```bash
.\venv\Scripts\python.exe manage.py shell
```
Then run:
```python
from accounts.models import User
user = User.objects.get(username='admin')
user.set_password('Admin@123')
user.save()
exit()
```

### Option 3: Create New Superuser
```bash
.\venv\Scripts\python.exe manage.py createsuperuser
```

---

## 🎯 Quick Login Test

**Test each role:**

1. **Admin Test:**
   ```
   URL: http://127.0.0.1:8000/login/
   Username: admin
   Password: Admin@123 (or try your remembered password)
   ```

2. **Manager Test:**
   ```
   Username: manager1
   Password: Manager@123
   ```

3. **Sales Test:**
   ```
   Username: sales1
   Password: Sales@123
   ```

4. **Client Test:**
   ```
   Username: client1
   Password: Client@123
   ```

---

## 📱 Dashboard URLs Quick Reference

| Role | Dashboard URL |
|------|---------------|
| Login Page | http://127.0.0.1:8000/login/ |
| Admin | http://127.0.0.1:8000/admin-dashboard/ |
| Manager | http://127.0.0.1:8000/manager-dashboard/ |
| Sales | http://127.0.0.1:8000/sales/dashboard/ |
| Client | http://127.0.0.1:8000/clients/dashboard/ |
| Owner | http://127.0.0.1:8000/owner-dashboard/ |
| Django Admin | http://127.0.0.1:8000/admin/ |

---

## 🔧 Troubleshooting

### If Login Fails:

1. **Check Server is Running:**
   ```bash
   # Should see: Starting development server at http://127.0.0.1:8000/
   ```

2. **Verify User Exists:**
   ```bash
   .\venv\Scripts\python.exe manage.py shell -c "from accounts.models import User; print(User.objects.filter(username='admin').exists())"
   ```

3. **Reset Password:**
   ```bash
   .\venv\Scripts\python.exe manage.py changepassword admin
   ```

4. **Check for Errors:**
   - Look at terminal where server is running
   - Check for any error messages

---

## 💡 Pro Tips

- **Remember:** Passwords are case-sensitive!
- **Default Pattern:** `RoleName@123` (capitalize first letter)
- **Admin has superuser:** Can access Django admin panel at `/admin/`
- **Owner role:** Special admin with owner privileges
- **Client:** Limited read-only access

---

**Last Updated:** November 12, 2025  
**Status:** ✅ All users active in local database

---

## 🚀 Ready to Test!

**Start with Admin:**
1. Go to http://127.0.0.1:8000
2. Username: `admin`
3. Password: `Admin@123` (or your set password)
4. Should redirect to admin dashboard

**Happy Testing! 🎉**
