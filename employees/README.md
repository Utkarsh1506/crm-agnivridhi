# Employee Identity & Verification System

## Overview

A production-ready Employee ID Card and Verification System integrated into the Agnivridhi CRM. This module provides:

- **Automatic Employee ID Generation** - Sequential IDs (AGN-EMP-001, etc.)
- **QR Code Generation** - Secure, non-personal-data-containing QR codes
- **Employee ID Cards** - Professional PDF cards (front & back)
- **Public Verification** - Rate-limited, no-login-required verification pages
- **Audit Logging** - Complete verification attempt tracking
- **Role-Based Access** - Admin/HR only for management

## Features

### 1. Employee Management (Admin/HR Only)

**Create Employees**
- Full name, designation, department
- Employee photo upload
- Auto-generate Employee ID (AGN-EMP-001 format)
- Auto-generate QR code
- Auto-generate verification token

**Manage Employees**
- List all employees with search/filter
- View employee details
- Activate/deactivate status
- Download ID cards as PDF
- View verification logs

**Access Control**
- Roles: SUPERUSER, OWNER, ADMIN
- Sales/other roles: View-only (optional)

### 2. Unique Employee ID Generation

**Format**: `AGN-EMP-001`, `AGN-EMP-002`, etc.

**Thread-Safe Sequence**
- Uses database transactions
- Prevents duplicate IDs
- Atomic increment operation

**No Manual Assignment**
- IDs auto-generate on employee creation
- Immutable after creation
- Unique constraint enforced

### 3. QR Code System

**Security First**
- QR code does NOT contain personal data
- QR code contains only: verification URL
- URL pattern: `https://agnivridhi.com/employee/verify/AGN-EMP-001/`

**Auto-Generated**
- Generated after employee creation
- Stored as image field
- Embedded in PDF cards

### 4. Public Verification Page

**Access**
- No login required
- Anyone can scan QR code and verify
- Public, read-only access

**Display**
- Company name (Agnivridhi)
- Employee photo
- Full name
- Designation
- Department
- Employee ID
- Status (Active/Inactive)

**Inactive Warning**
- Shows clear warning: "This employee is no longer associated with Agnivridhi."
- Different styling for inactive employees

### 5. Rate Limiting

**Protection**
- 10 requests per IP per hour
- Cache-based implementation
- Returns 429 status when exceeded

**Prevents**
- Bot/crawler abuse
- Excessive verification attempts
- Enumeration attacks

### 6. PDF ID Card Generation

**Front Side**
- Company logo/branding
- Employee photo
- Name
- Designation
- Department
- Employee ID

**Back Side**
- QR code
- "SCAN TO VERIFY" text
- Company address/branding
- Professional design

**Specifications**
- Credit card size (85.6 × 53.98 mm)
- High DPI (300) for printing
- One-click download

### 7. Audit Logging

**Tracks**
- Every verification attempt
- IP address
- User agent
- Timestamp
- Employee being verified

**Uses**
- Security monitoring
- Usage analytics
- Compliance audit trail

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- Django 4.2.7
- Pillow (image handling)
- qrcode (QR generation)
- xhtml2pdf (PDF generation)
- reportlab (PDF support)

### 2. Add to INSTALLED_APPS

In `agnivridhi_crm/settings.py`:
```python
INSTALLED_APPS = [
    ...
    'employees',  # Add this
]
```

### 3. Add URLs

In `agnivridhi_crm/urls.py`:
```python
urlpatterns = [
    ...
    path('employees/', include(('employees.urls', 'employees'))),
]
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Seed Initial Data (Optional)

```bash
python manage.py seed_employees
```

Creates 15 sample employees for testing.

## Database Schema

### Employee Model

| Field | Type | Details |
|-------|------|---------|
| id | BigAutoField | Primary key |
| uuid | UUID | Unique internal identifier |
| employee_id | CharField | AGN-EMP-001 format, unique, indexed |
| full_name | CharField | 200 chars, indexed |
| designation | CharField | 100 chars |
| department | CharField | 100 chars, indexed |
| employee_photo | ImageField | Stored in media/employees/photos/ |
| status | CharField | ACTIVE/INACTIVE, indexed |
| date_of_joining | DateField | Employment start date |
| date_of_exit | DateField | Termination date (optional) |
| qr_code | ImageField | Auto-generated, stored in media/employees/qrcodes/ |
| verification_token | CharField | UUID-based unique token |
| created_at | DateTimeField | Auto timestamp |
| updated_at | DateTimeField | Auto timestamp |
| created_by | ForeignKey | User who created record |

**Indexes**
- employee_id
- status
- department
- created_at

### EmployeeIDSequence Model

Manages auto-incrementing ID generation.

| Field | Type | Details |
|-------|------|---------|
| id | BigAutoField | Primary key |
| last_sequence_number | IntegerField | Current sequence |
| prefix | CharField | Always "AGN-EMP-" |
| updated_at | DateTimeField | Last update |

### EmployeeVerificationLog Model

Audit trail for verification attempts.

| Field | Type | Details |
|-------|------|---------|
| id | BigAutoField | Primary key |
| employee | ForeignKey | Employee verified |
| timestamp | DateTimeField | Verification time, indexed |
| ip_address | GenericIPAddressField | Verification source IP |
| user_agent | TextField | Browser info |

## API/Views

### Admin Views (Login Required)

#### List Employees
```
GET /employees/list/
Parameters: search, status, page
```

#### Create Employee
```
GET/POST /employees/create/
```

#### View Employee Details
```
GET /employees/<id>/
```

#### Toggle Employee Status
```
POST /employees/<id>/status-toggle/
```

#### Download ID Card
```
GET /employees/<id>/download-id-card/
Returns: PDF file
```

#### View Verification Logs
```
GET /employees/<id>/verification-logs/
```

### Public Views (No Login)

#### Verify Employee
```
GET /employees/verify/<employee_id>/
Parameters: None
Rate Limited: 10 per hour per IP
Returns: HTML verification page or 404
```

## Code Examples

### Creating an Employee

```python
from employees.models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

# Employee ID and QR code auto-generate on save
employee = Employee.objects.create(
    full_name="John Doe",
    designation="Senior Manager",
    department="Sales",
    date_of_joining="2024-01-15",
    employee_photo=uploaded_file,  # ImageField
    created_by=request.user,  # Current admin user
)

print(f"Created: {employee.employee_id}")  # Output: AGN-EMP-001
print(f"Verification URL: {employee.get_verification_url()}")
```

### Deactivating an Employee

```python
employee = Employee.objects.get(employee_id="AGN-EMP-001")
employee.deactivate()  # Sets status=INACTIVE, date_of_exit=today
```

### Reactivating an Employee

```python
employee = Employee.objects.get(employee_id="AGN-EMP-001")
employee.reactivate()  # Sets status=ACTIVE, date_of_exit=None
```

### Generating QR Code Manually

```python
from employees.qr_generator import QRCodeGenerator

url = "https://agnivridhi.com/employee/verify/AGN-EMP-001/"
qr_file = QRCodeGenerator.generate_qr_code(url)
employee.qr_code.save('qr_code.png', qr_file)
```

### Generating ID Card PDF

```python
from employees.pdf_generator import EmployeeIDCardPDF

employee = Employee.objects.get(employee_id="AGN-EMP-001")
pdf_file = EmployeeIDCardPDF.generate_id_card_pdf(employee)

# Return as HTTP response
from django.http import FileResponse
response = FileResponse(pdf_file, content_type='application/pdf')
response['Content-Disposition'] = f'attachment; filename="{employee.employee_id}_ID_Card.pdf"'
return response
```

### Checking Rate Limiting

```python
from employees.views import apply_rate_limit

ip_address = "192.168.1.1"
is_allowed, remaining, reset_time = apply_rate_limit(ip_address)

if not is_allowed:
    print(f"Rate limited. Reset in {reset_time} seconds")
else:
    print(f"Allowed. {remaining} requests remaining")
```

### Getting Verification Logs

```python
from employees.models import EmployeeVerificationLog

employee = Employee.objects.get(employee_id="AGN-EMP-001")
logs = EmployeeVerificationLog.objects.filter(employee=employee)

for log in logs:
    print(f"{log.timestamp} - {log.ip_address}")
```

## Django Admin Interface

Access: `/admin/employees/`

### Employee Admin

- View all employees
- Search by ID, name, designation, department
- Filter by status, department, joining date
- View employee photos (thumbnails)
- View QR codes (preview)
- Bulk actions: activate/deactivate
- Read-only: employee_id, uuid, qr_code, verification_token

### Verification Logs Admin

- View all verification attempts
- Filter by employee and timestamp
- Read-only (no manual edits)
- Cannot be deleted (audit trail)

### ID Sequence Admin

- View current sequence number
- See next employee ID to be assigned
- Read-only (prevent corruption)

## Security Considerations

### QR Code Security
- ✅ QR does NOT contain personal data
- ✅ QR only contains public verification URL
- ✅ Verification page is read-only
- ✅ No sensitive data in URL

### Rate Limiting
- ✅ 10 requests per IP per hour
- ✅ Prevents brute force enumeration
- ✅ Prevents bot abuse
- ✅ Cache-based (efficient)

### Access Control
- ✅ Admin/HR only for management
- ✅ No login required for public verification
- ✅ Role-based decorator enforcement
- ✅ Superuser bypass for testing

### Data Protection
- ✅ Audit logs all verification attempts
- ✅ IP tracking for compliance
- ✅ User agent logging
- ✅ Immutable employee IDs
- ✅ Status field is the only mutable attribute

## Scalability

### Database
- **Indexes** on: employee_id, status, department, created_at
- **Partitioning ready** - employee_id can be partitioned by date
- **Supports 10,000+ employees** without performance degradation

### File Storage
- **Media directory structure**: `media/employees/photos/<YYYY>/<MM>/`
- **Separate QR storage**: `media/employees/qrcodes/<YYYY>/<MM>/`
- **S3-compatible** for cloud deployment

### Caching
- **Cache-based rate limiting** (configurable)
- **Database query optimization** (select_related, prefetch_related ready)
- **Verification page cacheable** (read-only)

## Testing

Run tests:
```bash
python manage.py test employees
```

Test coverage includes:
- Employee ID generation
- Employee model creation/deactivation
- QR code generation
- Public verification views
- Rate limiting
- Access control
- Logging

## Future Enhancements

- [ ] Bulk employee import (CSV)
- [ ] QR code design customization
- [ ] Multiple ID card templates
- [ ] Email verification notifications
- [ ] Employee directory (internal)
- [ ] ID card reissue workflow
- [ ] Biometric integration
- [ ] Mobile app verification

## Troubleshooting

### QR Code not generating

Check:
- `qrcode` package installed
- Media directory is writable
- `MEDIA_ROOT` is configured in settings

### PDF generation fails

Check:
- `xhtml2pdf` and `reportlab` installed
- Pillow installed for image handling
- Employee photo is valid image
- Template path is correct

### Rate limiting not working

Check:
- Django cache is configured
- Cache backend is running (Redis if used)
- IP detection is correct (proxy headers)

### Employee ID gaps

Employee IDs are strictly sequential. Gaps indicate:
- Failed employee creation (rolled back transaction)
- Manual database intervention
- To prevent gaps, use atomic transactions

## Support

For issues or questions:
1. Check Django admin interface
2. Review verification logs
3. Check application logs
4. Run test suite

## License

© 2024-2025 Agnivridhi India. All rights reserved.
