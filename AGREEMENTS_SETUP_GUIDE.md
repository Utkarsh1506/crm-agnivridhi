# Agreement Generation System - Setup Guide

## Overview
Agreement system successfully created for generating Funding and Website agreements in your CRM.

## What Has Been Created

### 1. Django App Structure
- **App Name**: `agreements`
- **Location**: `C:\Users\Admin\Desktop\agni\CRM\agreements\`

### 2. Models (`agreements/models.py`)
Agreement model with following fields:
- `agreement_number` - Auto-generated unique ID (FA-YYYYMMDD-001 for Funding, WA-YYYYMMDD-001 for Website)
- `agreement_type` - Choice: 'funding' or 'website'
- `service_receiver_name` - Name of service receiver
- `service_receiver_address` - Complete address
- `date_of_agreement` - Agreement date
- `service_description` - Service details
- `total_amount_pitched` - Total amount
- `received_amount_stage1` - Received amount without GST (Stage 1)
- `pending_amount_stage2` - Optional pending amount (Stage 2)
- `commission_percentage` - Commission % after disbursement
- `commission_stage` - When commission applies
- `client` - Optional link to Client
- `employee` - Optional link to Employee
- `notes` - Additional notes
- Status fields: `is_active`, `is_completed`

### 3. Forms (`agreements/forms.py`)
Complete form with:
- All required field validations
- Optional pending amount
- Client and employee selection (filtered by user role)
- Automatic validation to ensure received amount doesn't exceed total

### 4. Views (`agreements/views.py`)
**Sales/Employee Views:**
- `agreement_list` - List all user's agreements
- `agreement_create` - Create new agreement
- `agreement_detail` - View agreement details
- `agreement_edit` - Edit agreement
- `agreement_delete` - Delete agreement
- `agreement_pdf` - Generate and download PDF

**Manager/Admin Views:**
- `manager_agreement_list` - View all agreements

**Features:**
- Auto-generate agreement numbers
- Role-based permissions
- Filter by type and client
- PDF generation with WeasyPrint

### 5. Templates Created
**Main Templates:**
- `templates/agreements/agreement_list.html` - List view with filters
- `templates/agreements/agreement_form.html` - Create/Edit form
- `templates/agreements/agreement_detail.html` - Detail view
- `templates/agreements/agreement_confirm_delete.html` - Delete confirmation
- `templates/agreements/manager_agreement_list.html` - Manager view

**PDF Templates:**
- `templates/agreements/pdf/funding_agreement.html` - Funding agreement PDF
- `templates/agreements/pdf/website_agreement.html` - Website agreement PDF

### 6. URLs (`agreements/urls.py`)
All routes configured with namespace 'agreements'

### 7. Integration
- Added 'agreements' to `INSTALLED_APPS` in settings.py
- Added URL routing in main urls.py
- Added sidebar navigation in templates

## Setup Steps

### Step 1: Fix Migration Dependencies (REQUIRED)
There's a migration dependency issue in the clients app. Run:

```powershell
# Check existing migrations
python manage.py showmigrations clients

# If 0009 doesn't exist but 0010 references it, you need to fix the dependency
# Edit the migration file or create the missing migration
```

### Step 2: Create Migrations
```powershell
python manage.py makemigrations agreements
```

### Step 3: Apply Migrations
```powershell
python manage.py migrate agreements
```

### Step 4: Install WeasyPrint for PDF Generation
WeasyPrint is required for PDF generation. Install it:

```powershell
pip install weasyprint
```

**Note**: WeasyPrint requires GTK3 runtime on Windows. Download from:
https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases

Or use alternative:
```powershell
pip install xhtml2pdf  # Alternative PDF library
```

If using xhtml2pdf, update `agreements/views.py` in the `agreement_pdf` function.

### Step 5: Update Navigation (Optional)
Add agreements link to your dashboard sidebar by editing:
- `templates/accounts/sales_dashboard.html`
- `templates/accounts/manager_dashboard.html`
- `templates/accounts/admin_dashboard.html`

Add this to the sidebar:
```html
<li class="nav-item">
    <a class="nav-link" href="{% url 'agreements:agreement_list' %}">
        <i class="bi bi-file-text"></i> Agreements
    </a>
</li>
```

## Usage

### For Sales/Employees:
1. Go to `/agreements/` or click "Agreements" in sidebar
2. Click "Create New Agreement"
3. Select agreement type (Funding or Website)
4. Fill in all required fields:
   - Service receiver details
   - Date of agreement
   - Service description
   - Financial details
   - Commission percentage
5. Optionally link to client and employee
6. Submit to create agreement
7. Download PDF from detail view

### For Managers/Admins:
- Access `/agreements/manager/` to view all agreements
- Can filter by type and client
- View and download any agreement PDF

## Variable Fields in PDF
The following fields are dynamic and will be filled from the form:
1. **Service Receiver Name** - From form input
2. **Date of Agreement** - Selected date
3. **Service Description** - Detailed service description
4. **Address** - Complete address of service receiver
5. **Total Amount Pitched** - Total project/loan amount
6. **Received Amount (Stage 1)** - Amount received without GST
7. **Pending Amount (Stage 2)** - Optional, only if pending payment exists
8. **Commission Percentage** - Commission % after disbursement
9. **Commission Stage** - Stage 2 or Stage 3 based on selection

## Customizing PDF Templates

### For Funding Agreements:
Edit: `templates/agreements/pdf/funding_agreement.html`

### For Website Agreements:
Edit: `templates/agreements/pdf/website_agreement.html`

**To add your actual agreement format:**
1. Keep the existing HTML structure
2. Replace company details in the header
3. Update terms and conditions section
4. Modify styling in `<style>` tag
5. Keep all `{{ agreement.field_name }}` template variables intact

## Testing

### Test Agreement Creation:
1. Login as sales user
2. Navigate to Agreements
3. Create a funding agreement with:
   - Receiver: "Test Company Pvt Ltd"
   - Address: "123 Test Street, Mumbai"
   - Service: "Business loan facilitation for ₹50 lakhs"
   - Total Amount: 5000000.00
   - Received Stage 1: 25000.00
   - Pending Stage 2: 25000.00
   - Commission: 2.5%

4. Verify:
   - Agreement number auto-generated (FA-YYYYMMDD-001)
   - All details display correctly
   - PDF downloads successfully

### Test Website Agreement:
Similar to above but with website development details.

## Security Features
- Role-based access control
- Users can only see/edit their own agreements
- Managers can view all agreements
- Admins have full access
- SQL injection protected (Django ORM)
- CSRF protection on all forms

## API Integration (Future)
If you want to add REST API endpoints:
1. Create `agreements/serializers.py`
2. Add ViewSets in `agreements/api_views.py`
3. Register routes in `api/urls.py`

## Deployment Notes

### For PythonAnywhere:
1. Upload all files
2. Run migrations:
   ```bash
   python manage.py migrate agreements
   ```
3. Collect static files:
   ```bash
   python manage.py collectstatic
   ```
4. Install WeasyPrint or xhtml2pdf in virtual environment
5. Restart web app

### Database Backup:
Before deployment, backup database:
```powershell
python manage.py dumpdata agreements > agreements_backup.json
```

## Troubleshooting

### Issue: Migration error
**Solution**: Fix clients app migration dependency first:
```powershell
python manage.py showmigrations
# Check which migrations exist
# Fix dependencies in migration files
```

### Issue: PDF not generating
**Solution**: 
- Check WeasyPrint installation
- Verify GTK3 runtime (Windows)
- Or switch to xhtml2pdf

### Issue: Employee field error
**Solution**: Already fixed - uses `status='ACTIVE'` instead of `is_active=True`

### Issue: Template not found
**Solution**: 
- Verify templates are in `templates/agreements/` directory
- Check `TEMPLATES` setting in settings.py includes template directories

## Next Steps

1. **Fix Migration Issue**: Resolve the clients app migration dependency
2. **Run Migrations**: Create and apply agreement migrations
3. **Add Sample Agreements**: Upload your actual PDF samples
4. **Customize Templates**: Edit PDF templates with your agreement format
5. **Test Thoroughly**: Create test agreements and generate PDFs
6. **Update Navigation**: Add links to dashboards
7. **Deploy**: Push to production when ready

## File Locations

```
CRM/
├── agreements/
│   ├── __init__.py
│   ├── admin.py          # Admin interface
│   ├── apps.py
│   ├── forms.py          # Agreement form
│   ├── models.py         # Agreement model
│   ├── urls.py           # URL routing
│   ├── views.py          # Views and PDF generation
│   └── migrations/       # (Will be created)
│
└── templates/
    └── agreements/
        ├── agreement_list.html
        ├── agreement_form.html
        ├── agreement_detail.html
        ├── agreement_confirm_delete.html
        ├── manager_agreement_list.html
        └── pdf/
            ├── funding_agreement.html
            └── website_agreement.html
```

## Support
For issues or questions:
1. Check Django logs: `python manage.py runserver`
2. Review error messages
3. Check permissions and role assignments
4. Verify database migrations are applied

---

**Created**: January 28, 2026
**System**: Django 5.2+
**Python**: 3.14+
**Status**: Ready for migration and testing
