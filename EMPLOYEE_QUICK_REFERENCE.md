# ⚡ Quick Reference - Employee Management

## 🚀 Where to See Employees

### **Admin Dashboard** (Best Option)
```
📍 URL: /admin/employees/employee/
🔐 Access: Owner & Admin only
👁️ See: All 17 employees with barcodes
```

### **CRM Frontend**
```
📍 URL: /employees/
🔐 Access: Owner & Admin only
📊 Type: Beautiful list view
```

---

## ➕ Add New Employee

1. Go to Admin → Employees
2. Click "Add Employee" button
3. Fill in:
   - Full Name
   - Designation
   - Department
   - Employee Photo
   - Joining Date
4. Click Save
5. **Auto Done:**
   - ✅ Employee ID (0118, 0119, etc.)
   - ✅ Barcode (Code128)
   - ✅ Verification Token

---

## 📊 Manage Employees

### View
- Click employee name → See full details & barcode

### Edit
- Click employee → Edit any field → Save

### Deactivate
- Select employees → "Deactivate selected" → Apply

### Activate
- Select employees → "Activate selected" → Apply

### Search
- Use search box: name, ID, designation, department

### Filter
- Status: Active/Inactive
- Department: dropdown
- Date range: calendar

---

## 🏢 Current Employees (17 Total)

| ID | Name | Designation | Department |
|----|------|-------------|-----------|
| 0101 | Rahul Kumar Singh | CEO & Founder | Management |
| 0102 | Urvashi Nandan Srivastava | Data Analyst | Finance |
| 0103 | Akash Tyagi | Branch Manager | Operations |
| 0104 | Harshit Tyagi | Manager | Management |
| 0105-0111, 0113-0117 | Various | Business Development Exec | Sales |
| 0109 | Rajdeep Singh | Team Leader | Sales |
| 0112 | Utkarsh Choudhary | Web Developer | Engineering |

---

## 🔓 Access Control

### Can Access:
- ✅ Owner role
- ✅ Admin role

### Cannot Access:
- ❌ Other roles
- ❌ Unauthenticated users

---

## 📱 Barcode Info

**What:** Code128 barcode with employee ID
**Auto-Generated:** Yes, on employee creation
**Scannable:** Yes, with any barcode reader
**Use Cases:**
- Attendance tracking
- ID card printing
- Access control
- Quick lookup

---

## 🔧 PythonAnywhere Deployment

```bash
# 1. Pull changes
git pull origin main

# 2. Install barcode library
pip install -r requirements.txt

# 3. Run migration
python manage.py migrate employees

# 4. Collect static files
python manage.py collectstatic --noinput

# 5. Reload app
# Go to Web tab → Click Reload button
```

---

## 📂 Files Changed

- ✅ models.py (barcode field)
- ✅ barcode_utils.py (barcode generation)
- ✅ signals.py (auto-generation)
- ✅ admin.py (UI updates)
- ✅ requirements.txt (python-barcode)
- ✅ Migration 0002 (database update)

---

## 💡 Quick Tips

1. **Barcode not showing?**
   - Refresh page or go to admin and click Save

2. **New employee not appearing?**
   - Refresh or clear browser cache

3. **Search not working?**
   - Try exact spelling or partial match
   - Use filter dropdown instead

4. **Can't access employee management?**
   - Check if logged in as Owner or Admin
   - Check user role in accounts

---

## 📞 Common Tasks

### Print ID Card
1. Go to employee
2. Download barcode
3. Print with employee photo

### Update Status
1. Click employee
2. Change status to Inactive
3. Set exit date
4. Save

### Bulk Manage
1. Select multiple employees
2. Choose action (Deactivate/Activate)
3. Apply

### Export List
1. Go to admin
2. Use Django export feature
3. Download as CSV/Excel

---

## ✨ Key Points

- ✅ Barcode, NOT QR code
- ✅ Auto-generated on employee creation
- ✅ Both Owner & Admin can manage
- ✅ 17 employees with IDs 0101-0117
- ✅ All with barcodes and photos
- ✅ Searchable and filterable
- ✅ Production-ready

---

**Status:** 🟢 **Ready to Use**  
**Latest Commit:** dabb623  
**Next Step:** Deploy to PythonAnywhere
