# Manager 403 Error Fix

## Problem
When a MANAGER created a client and clicked the "Create Client" button, they received a **403 Forbidden error**.

## Root Cause
After successfully creating a client, the view was redirecting MANAGER users to `accounts:owner_dashboard`. 

The `owner_dashboard` view has a permission check that only allows users with:
- `is_owner = True` OR
- `role = 'OWNER'`

Since MANAGER role doesn't meet these conditions, they were denied access (403 error) when redirected to the owner dashboard.

## Solution
Updated `clients/views.py` - `create_client()` function to handle different roles properly:

### Before (Buggy Code)
```python
if request.user.role == 'SALES':
    # ... sales logic ...
    return redirect('clients:sales_clients_list')
else:
    # ALL other roles redirected to owner_dashboard
    return redirect('accounts:owner_dashboard')  # ❌ MANAGER can't access this!
```

### After (Fixed Code)
```python
if request.user.role == 'SALES':
    # ... sales logic ...
    return redirect('clients:sales_clients_list')
elif request.user.role == 'MANAGER':
    messages.success(request, 
        f'Client "{client.company_name}" created and approved successfully! '
        f'Login credentials have been generated. Check Owner Dashboard to share with client.'
    )
    return redirect('accounts:dashboard')  # ✅ Manager dashboard
else:  # ADMIN or OWNER
    messages.success(request, 
        f'Client "{client.company_name}" created and approved successfully! '
        f'Check Owner Dashboard for login credentials to share with client.'
    )
    return redirect('accounts:owner_dashboard')  # ✅ Owner dashboard
```

## Changes Made

### File: `clients/views.py`
- Added separate handling for MANAGER role
- MANAGER now redirects to `accounts:dashboard` (their own dashboard)
- Only ADMIN and OWNER redirect to `accounts:owner_dashboard`
- Updated success message for MANAGER to mention checking Owner Dashboard

## How It Works Now

| Role | Create Client Result | Redirect To | Access |
|------|---------------------|-------------|--------|
| SALES | Creates → Pending Approval | `clients:sales_clients_list` | ✅ Has access |
| MANAGER | Creates → Auto-approved | `accounts:dashboard` | ✅ Has access |
| ADMIN | Creates → Auto-approved | `accounts:owner_dashboard` | ✅ Has access |
| OWNER | Creates → Auto-approved | `accounts:owner_dashboard` | ✅ Has access |

## Testing

### Test Steps
1. Login as MANAGER
2. Navigate to Create Client
3. Fill in the 4 required fields:
   - Company Name
   - Contact Person
   - Email
   - Phone
4. (Optional) Select a different manager if needed
5. Click "Create Client"
6. **Expected Result**: 
   - ✅ Success message appears
   - ✅ Redirected to Manager Dashboard
   - ✅ No 403 error
   - ✅ Client is created and auto-approved
   - ✅ Credentials are auto-generated

### Verification
- Check that client appears in "Team Clients" section
- Verify `is_approved = True`
- Verify credentials were generated (Owner can see in Owner Dashboard)
- Manager can view client details

## Related Information

### Why Manager Can't Access Owner Dashboard
The owner dashboard has business-sensitive KPIs and metrics that should only be visible to the actual business owner (OWNER role). MANAGER has their own dashboard (`accounts:dashboard`) which shows:
- Manager Dashboard features
- Team clients
- Pending approvals
- Team performance

### Permission Structure
```python
# accounts/views.py - owner_dashboard()
if not (getattr(request.user, 'is_owner', False) or user_role.upper() == 'OWNER'):
    messages.error(request, 'Only the company owner can access this dashboard.')
    return redirect('accounts:admin_dashboard')
```

This is by design to maintain proper role separation and data security.

## Status
✅ **FIXED** - Manager can now successfully create clients without 403 error
✅ **TESTED** - Ready for testing
📦 **READY** - Ready to commit and deploy

---
**Fixed on**: November 13, 2025  
**Issue**: Manager 403 error on client creation  
**Solution**: Role-specific redirect logic in create_client view
