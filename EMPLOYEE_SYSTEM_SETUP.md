# Employee Identity & Verification System - Quick Setup Guide

## What's New

A complete Employee ID Card and Verification System has been added to your Agnivridhi CRM.

## Files Added

```
employees/
├── __init__.py
├── apps.py                          # App configuration
├── models.py                        # Database models (3 models)
├── views.py                         # Admin + public views
├── urls.py                          # URL routing
├── admin.py                         # Django admin interface
├── tests.py                         # Comprehensive tests
├── id_generator.py                  # Employee ID generation
├── qr_generator.py                  # QR code generation
├── pdf_generator.py                 # PDF card generation
├── utils.py                         # Utility functions
├── signals.py                       # Auto-generation signals
├── README.md                        # Full documentation
├── migrations/
│   ├── __init__.py
│   └── 0001_initial.py             # Database migration
├── management/commands/
│   ├── __init__.py
│   └── seed_employees.py           # Sample data generator
├── templates/employees/
│   ├── employee_list.html          # Employee management list
│   ├── employee_form.html          # Create/edit form
│   ├── employee_detail.html        # Employee details view
│   ├── verification_logs.html      # Audit trail
│   ├── verification_page.html      # Public verification page
│   ├── verification_not_found.html # 404 page
│   ├── verification_rate_limited.html # Rate limit page
│   ├── verification_error.html     # Error page
│   └── id_card_pdf.html            # PDF card template
└── static/employees/               # Static files directory
```

## Quick Start (5 Steps)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages (already added):
- qrcode==7.4.2
- Plus existing: Pillow, xhtml2pdf, reportlab

### 2. Run Migrations

```bash
python manage.py migrate employees
```

This creates 3 database tables:
- employee
- employee_id_sequence
- employee_verification_log

### 3. Create Superuser (if needed)

```bash
python manage.py createsuperuser
```

### 4. Seed Sample Employees (Optional)

```bash
python manage.py seed_employees
```

Creates 15 sample employees across all departments.

### 5. Start Using

**In Admin Interface:**
- Go to `/admin/employees/`
- Create new employees
- Download ID cards
- View verification logs

**In CRM:**
- Navigate to `/employees/list/`
- Manage all employees
- Download ID cards

## Key Features at a Glance

| Feature | Details |
|---------|---------|
| **Employee IDs** | Auto-generated: AGN-EMP-001, AGN-EMP-002, ... |
| **QR Codes** | Auto-generated, non-personal-data, embedded in PDFs |
| **ID Cards** | Professional 2-sided PDF, credit-card sized |
| **Public Verification** | No login required, rate-limited, shows inactive status |
| **Audit Logging** | All verification attempts tracked with IP & timestamp |
| **Role-Based** | Admin/HR only for management, public for verification |

## Database Models

### Employee
- Stores employee information
- Auto-generates ID, QR code, verification token
- Tracks status (Active/Inactive)
- Supports multiple photos, departments, designations

### EmployeeIDSequence
- Manages thread-safe ID generation
- Prevents duplicate IDs

### EmployeeVerificationLog
- Audit trail of all verification page visits
- IP tracking
- User agent logging

## Views & URLs

### Admin Routes (Login Required)

```
GET  /employees/list/                    # List all employees
GET  /employees/create/                  # Create form
GET  /employees/<id>/                    # View details
POST /employees/<id>/status-toggle/      # Deactivate/reactivate
GET  /employees/<id>/download-id-card/   # Download PDF
GET  /employees/<id>/verification-logs/  # View logs
```

### Public Routes (No Login)

```
GET  /employees/verify/<employee_id>/    # Public verification page
```

## Django Admin

Access: `/admin/employees/`

**Features:**
- Employee management with search/filter
- QR code preview
- Photo thumbnails
- Bulk activate/deactivate
- Verification log viewer
- Read-only: ID, UUID, QR code, token

## Testing

```bash
# Run all tests
python manage.py test employees

# Run specific test class
python manage.py test employees.tests.EmployeeIDGeneratorTest

# With verbose output
python manage.py test employees -v 2
```

Test coverage:
- ID generation (uniqueness, format)
- Employee creation/deletion
- QR code generation
- Public verification views
- Rate limiting
- Role-based access
- Logging

## API Examples

### Create Employee Programmatically

```python
from employees.models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(username='admin')

employee = Employee.objects.create(
    full_name="John Doe",
    designation="Sales Manager",
    department="Sales",
    date_of_joining="2024-01-15",
    employee_photo=file,  # Django ImageField file
    created_by=user,
)

print(employee.employee_id)  # AGN-EMP-001
print(employee.get_verification_url())  # https://agnivridhi.com/employee/verify/AGN-EMP-001/
```

### Deactivate/Reactivate

```python
employee = Employee.objects.get(employee_id="AGN-EMP-001")
employee.deactivate()   # Sets status=INACTIVE
employee.reactivate()   # Sets status=ACTIVE
```

### Generate ID Card PDF

```python
from employees.pdf_generator import EmployeeIDCardPDF

employee = Employee.objects.get(employee_id="AGN-EMP-001")
pdf_file = EmployeeIDCardPDF.generate_id_card_pdf(employee)
# Returns: ContentFile with PDF bytes
```

### Check Verification Logs

```python
from employees.models import EmployeeVerificationLog

employee = Employee.objects.get(employee_id="AGN-EMP-001")
logs = EmployeeVerificationLog.objects.filter(employee=employee)

for log in logs:
    print(f"{log.timestamp} - {log.ip_address}")
```

## Security Highlights

✅ **QR Code Security**
- Does NOT contain personal data
- Only contains public verification URL
- Verification page is read-only

✅ **Rate Limiting**
- Max 10 requests per IP per hour
- Prevents bot abuse and enumeration

✅ **Access Control**
- Admin/HR only for management
- Public page with no login
- Role-based decorators enforced

✅ **Audit Trail**
- All verification attempts logged
- IP address tracked
- User agent recorded

✅ **Data Integrity**
- Employee IDs are immutable
- Thread-safe ID generation
- Unique constraints enforced

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'qrcode'"

**Solution:**
```bash
pip install qrcode[pil]==7.4.2
```

### Issue: QR code not generating on employee creation

**Check:**
1. `MEDIA_ROOT` is configured in settings.py
2. Media directory is writable
3. Signals are registered (check apps.py ready() method)

### Issue: PDF generation fails

**Check:**
1. xhtml2pdf and reportlab installed
2. Pillow installed for image support
3. Employee photo is valid image
4. Template path: `employees/id_card_pdf.html`

### Issue: Rate limiting not working

**Check:**
1. Django cache configured (default: locmem)
2. Check IP detection for proxy scenarios
3. Cache timeout is set correctly

## Configuration

### Rate Limiting

In `employees/views.py`:
```python
RATE_LIMIT_REQUESTS = 10      # Max requests
RATE_LIMIT_WINDOW = 3600      # Per 1 hour (seconds)
```

### Media Storage

By default stored in:
- `/media/employees/photos/<YEAR>/<MONTH>/`
- `/media/employees/qrcodes/<YEAR>/<MONTH>/`

For S3, update:
```python
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

## Scalability Notes

✓ **Designed for 1000+ employees**
- Indexed fields: employee_id, status, department, created_at
- Proper pagination (25 employees per page)
- Efficient queries

✓ **Database**
- Thread-safe ID generation
- Connection pooling ready
- Can be partitioned by date

✓ **File Storage**
- Cloud storage compatible (S3, Azure Blob, etc.)
- Organized directory structure
- Automatic timestamp-based folders

## Next Steps

1. **Run migrations**: `python manage.py migrate`
2. **Seed test data**: `python manage.py seed_employees`
3. **Access admin**: `/admin/employees/`
4. **Create first employee**: Use admin interface
5. **Download ID card**: Click "Download ID Card" button
6. **Test verification**: Scan QR code or visit `/employees/verify/AGN-EMP-001/`

## Documentation

For complete documentation, see: `employees/README.md`

Covers:
- Feature overview
- Database schema
- API reference
- Code examples
- Security details
- Troubleshooting

## Support

Issues? Check:
1. Django admin interface for data
2. Application logs for errors
3. Test suite: `python manage.py test employees`
4. Documentation: `employees/README.md`

---

**Ready to use!** The system is production-ready and fully integrated with your Agnivridhi CRM.
