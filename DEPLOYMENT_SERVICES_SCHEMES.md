# Deployment Guide - Services & Schemes Update

## Local Changes Summary

### ✅ Completed on Local:
1. **31 Active Services** added across 6 categories
2. **9 Active Schemes** including new Startup Growth Program
3. Scripts committed to GitHub

### 📦 What's in Git:
- Code files (templates, views) - Already pushed (commit eee598f)
- Setup scripts - Just pushed (commit 6290da0)

### 🗄️ What's NOT in Git:
- **Database records** (services and schemes data)
- These exist only in local `db.sqlite3`

## Deployment to PythonAnywhere

### Step 1: Pull Latest Code
```bash
cd ~/crm-agnivridhi
git pull origin main
```

### Step 2: Run Setup Scripts
```bash
# Activate virtual environment
source venv/bin/activate  # or workon your-venv-name

# Add all services (28 new services)
python add_services_and_schemes.py

# Add Startup Growth Program scheme
python add_startup_growth_program.py

# Verify setup
python verify_services_schemes.py
```

### Step 3: Reload Web App
- Go to PythonAnywhere Web tab
- Click "Reload" button
- Or touch WSGI file:
```bash
touch /var/www/yourusername_pythonanywhere_com_wsgi.py
```

### Step 4: Verify on Production
1. Login as manager1
2. Go to: Create Booking page
3. Check:
   - Service dropdown shows 31 services in categories
   - Scheme dropdown shows 9 schemes including "Startup Growth Program"

## Expected Results

### Services Dropdown:
```
Funding Services
  ├─ CGTMSE Loan Application - ₹10,000
  ├─ PMEGP Loan & Subsidy Application - ₹15,000
  ├─ Mudra Loan Application - ₹8,000
  ├─ Startup India Seed Fund Application - ₹20,000
  ├─ Stand-Up India Loan Application - ₹12,000
  ├─ Scheme Application Documentation - ₹5,000
  └─ Working Capital Advisory - ₹25,000

Incorporation Services (5 services)
Certification Services (5 services)
Growth Services (5 services)
CSR Services (4 services)
Consulting Services (4 services)
```

### Schemes Dropdown:
```
Loan/Credit Guarantee
  ├─ Agriculture Loan
  ├─ Credit Guarantee Scheme (CGTMSE)
  ├─ Mudra Loan Scheme
  └─ SIDBI Stand-Up India Scheme

Grant/Subsidy
  ├─ Prime Minister Employment Generation Programme (PMEGP)
  ├─ Startup Growth Program ⭐ (NEW - Agnivridhi's Own)
  ├─ Startup India
  └─ Startup India Seed Fund Scheme (SISFS)

Capital/Interest Subsidy
  └─ PMEGP
```

## Troubleshooting

### If services don't show in dropdown:
1. Check if script ran successfully
2. Verify in Django admin: `/admin/bookings/service/`
3. Check `is_active=True` for all services

### If schemes don't show:
1. Verify script output
2. Check Django admin: `/admin/schemes/scheme/`
3. Ensure `status='ACTIVE'`

### Database Issues:
```bash
# Check database
python manage.py shell
>>> from bookings.models import Service
>>> Service.objects.count()
31  # Should show 31

>>> from schemes.models import Scheme
>>> Scheme.objects.filter(status='ACTIVE').count()
9  # Should show 9
```

## Important Notes

⚠️ **Database Sync**: Services and schemes are database records, not code
- Local and production databases are separate
- Must run scripts on BOTH environments
- Or export/import database (more complex)

✅ **No Migrations Needed**: These are data additions, not schema changes

🔄 **Future Updates**: To add more services/schemes, create similar scripts

---
**Date**: November 14, 2025
**Commit**: 6290da0 (scripts), eee598f (booking form)
**Status**: Ready for PythonAnywhere Deployment
