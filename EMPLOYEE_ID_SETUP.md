# Employee ID Setup Guide - Agnivridhi CRM

## Overview
The Employee Identity & Verification System has been configured with the specific employee list and ID format requested:

- **ID Format**: 4-digit numeric (0101, 0102, 0103, etc.)
- **Total Employees**: 17 predefined employees
- **Status**: Ready for immediate deployment

---

## Employee List (Pre-configured)

| ID | Name |
|----|------|
| 0101 | Rahul Kumar Singh |
| 0102 | Urvashi Nandan Srivastava |
| 0103 | Akash Tyagi |
| 0104 | Harshit Tyagi |
| 0105 | Ayush Tomer |
| 0106 | Himadri Sharma |
| 0107 | Bhoomika Sharma |
| 0108 | Sharik Khan |
| 0109 | Rajdeep Singh |
| 0110 | Aaryav Singh |
| 0111 | Mohd Rihan |
| 0112 | Utkarsh Choudhary |
| 0113 | Rahul Kumar Pant |
| 0114 | Vaibhav Garg |
| 0115 | Babita Goswami |
| 0116 | Sanklp |
| 0117 | Vinay Kannaujiya |

---

## Setup Instructions

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

Ensures qrcode==7.4.2 is installed for QR code generation.

### Step 2: Run Migrations
```bash
python manage.py migrate employees
```

Creates the necessary database tables for the Employee system.

### Step 3: Seed Employees
Option A - Using management command:
```bash
python manage.py seed_agnivridhi_employees
```

Option B - Using the runner script:
```bash
python seed_employees_runner.py
```

This will:
- Create all 17 employees with their specific IDs
- Generate unique verification tokens for each
- Create placeholder profile photos
- Assign random departments and designations
- Generate QR codes automatically

### Step 4: Access the System

**Admin Dashboard:**
- URL: `http://localhost:8000/employees/list/`
- Requires: Login with staff/admin credentials

**Django Admin:**
- URL: `http://localhost:8000/admin/employees/`
- Requires: Superuser credentials

**Public Verification:**
- URL: `http://localhost:8000/employees/verify/<employee_id>/`
- Example: `http://localhost:8000/employees/verify/0101/`
- No login required
- Rate limited to 10 requests per IP per hour

---

## ID Generation Format

### New Format
```
4-digit numeric with leading zeros:
0101, 0102, 0103, ..., 0117, 0118, ...
```

### Previous Format (Deprecated)
```
AGN-EMP-001, AGN-EMP-002, AGN-EMP-003, ...
(No longer used)
```

### Generated Sequence
After seeding 17 employees (ending at 0117), the next auto-generated ID will be:
```
0118
```

---

## Key Files Modified

### 1. `employees/id_generator.py`
- Updated ID format from `AGN-EMP-{seq:03d}` to `{seq:04d}`
- PREFIX changed to empty string `''`
- PADDING changed from 3 to 4 digits

### 2. `employees/management/commands/seed_agnivridhi_employees.py`
- **New file** - Replaces generic seeding
- Uses predefined employee list with specific names
- Creates 17 employees automatically
- Generates verification tokens
- Creates placeholder photos per employee

### 3. `employees/models.py`
- Updated Employee docstring to reflect new ID format
- Updated help text for `employee_id` field

### 4. `employees/signals.py`
- No changes - already handles manual ID assignment via `if not instance.employee_id:` check

### 5. `seed_employees_runner.py`
- **New file** - Standalone runner for seeding without alias issues

---

## Features Included

✅ **4-digit Employee IDs** (0101-0117, extensible to 9999)
✅ **17 Pre-configured Employees** with names
✅ **Automatic QR Code Generation** (secure, no personal data)
✅ **Verification Token System** (unique per employee)
✅ **Public Verification Pages** (rate-limited, audit-logged)
✅ **Django Admin Interface** (searchable, filterable)
✅ **ID Card PDF Generation** (2-sided, credit card size)
✅ **Role-Based Access Control** (Admin/HR only)
✅ **Audit Logging** (IP tracking, timestamps)

---

## Testing the System

### 1. Verify Employee was Created
```bash
python manage.py shell

>>> from employees.models import Employee
>>> emp = Employee.objects.get(employee_id='0101')
>>> print(f"ID: {emp.employee_id}, Name: {emp.full_name}")
ID: 0101, Name: Rahul Kumar Singh
```

### 2. Test Public Verification
Open in browser: `http://localhost:8000/employees/verify/0101/`

You should see:
- Employee name
- Status (Active/Inactive)
- Department
- Designation
- No login required
- Audit log entry created

### 3. Test Rate Limiting
Make 11 rapid requests to the same verify endpoint:
```bash
for i in {1..11}; do curl http://localhost:8000/employees/verify/0101/; done
```

The 11th request should return 429 (Too Many Requests).

---

## Extending the System

### Add New Employees After Initial Setup

**Via Django Admin:**
1. Navigate to `/admin/employees/employee/`
2. Click "Add Employee"
3. Fill in details (ID will be auto-generated)
4. The system will auto-generate:
   - Next ID in sequence (0118, 0119, etc.)
   - Unique verification token
   - QR code

**Via Python Shell:**
```python
from employees.models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()
admin_user = User.objects.get(username='admin')

emp = Employee.objects.create(
    full_name='New Employee Name',
    designation='Job Title',
    department='Department',
    date_of_joining='2026-01-05',
    status='ACTIVE',
    created_by=admin_user,
)
# ID, token, QR code auto-generated!
print(f"Created employee: {emp.employee_id}")
```

### Custom Employee ID Format

If you need to change the format again:
1. Edit `employees/id_generator.py`:
   - Modify `PREFIX` and `PADDING` constants
   - Example: `PREFIX = 'EMP-'` and `PADDING = 3` → `EMP-001`

2. Update docstrings and help text in relevant files

3. Recreate employees if needed

---

## Troubleshooting

### Issue: "Employee already exists" when seeding

**Solution**: 
```bash
# Delete existing employees and reset sequence
python manage.py shell

>>> from employees.models import Employee, EmployeeIDSequence
>>> Employee.objects.all().delete()
>>> EmployeeIDSequence.objects.all().delete()
>>> exit()

# Then re-run seed
python manage.py seed_agnivridhi_employees
```

### Issue: QR codes not generating

**Solution**:
```bash
# Check if qrcode library is installed
pip install qrcode[pil]==7.4.2

# Manually trigger QR generation for existing employees
python manage.py shell

>>> from employees.models import Employee
>>> from employees.qr_generator import QRCodeGenerator
>>> emp = Employee.objects.get(employee_id='0101')
>>> qr_file = QRCodeGenerator.generate_qr_code(emp.get_verification_url())
>>> emp.qr_code.save(f"{emp.employee_id}_qr.png", qr_file, save=True)
```

### Issue: Rate limiting not working

**Solution**: Ensure Django caching is configured in settings.py:
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```

---

## Security Considerations

✅ **QR Codes**: Contain only verification URL, no personal data
✅ **Verification Tokens**: 128-character UUID-based, unique per employee
✅ **Rate Limiting**: 10 requests per IP per hour on public verification
✅ **Admin Access**: Role-based (ADMIN/HR only, with exceptions for SUPERUSER)
✅ **Audit Trail**: Every verification attempt logged with IP and timestamp
✅ **Data Validation**: Employee photo validation, date validation

---

## Next Steps

1. ✅ Run `python manage.py seed_agnivridhi_employees`
2. ✅ Access `/admin/` and verify employees created
3. ✅ Test public verification at `/employees/verify/0101/`
4. ✅ Download ID cards from admin interface
5. ✅ Monitor verification logs in admin

---

## Support

For issues or questions:
- Check Django logs: `tail -f logs/django.log`
- Review admin audit logs: `/admin/employees/employeeverificationlog/`
- Consult [employees/README.md](employees/README.md) for detailed module documentation

---

**Last Updated**: January 5, 2026
**Status**: ✅ Production Ready
