# 🧪 Quick Manual Testing - Error Pages

## Setup Instructions
```powershell
# 1. Start development server
cd c:\Users\Admin\Desktop\agni\CRM
python manage.py runserver

# 2. Create test users (if not already exist)
python manage.py createsuperuser  # For SUPERUSER testing
# Or use Django admin to create CLIENT, SALES, MANAGER users
```

---

## Test 1: 404 Not Found Page ⏱️ 2 minutes

### As Unauthenticated User
1. **Navigate:** http://localhost:8000/fake-page
2. **Verify:**
   - ✅ Compass icon bouncing
   - ✅ "404" in large text
   - ✅ "Login" button in quick links
3. **Click:** "Go to Dashboard" → Should redirect to login page

### As CLIENT User
1. **Login** as client
2. **Navigate:** http://localhost:8000/nonexistent/url
3. **Verify:**
   - ✅ Shows your name and "Client" role badge
   - ✅ Quick links: "Browse Schemes" + "My Applications"
4. **Click:** "Browse Schemes" → Should work

### As SALES User
1. **Login** as sales
2. **Navigate:** http://localhost:8000/missing
3. **Verify:**
   - ✅ Quick links: "My Bookings" + "My Applications"
   - ✅ "Search" button visible (staff member)
4. **Click:** "Search" → Should open global search

### As ADMIN/MANAGER User
1. **Login** as admin or manager
2. **Navigate:** http://localhost:8000/wrong
3. **Verify:**
   - ✅ Quick links: "Team Applications" + "Team Bookings"
4. **Click:** Both links → Should work

**Pass Criteria:** All role-specific links display and work correctly

---

## Test 2: 403 Forbidden Page ⏱️ 3 minutes

### CLIENT → Manager Route
1. **Login** as CLIENT
2. **Navigate:** http://localhost:8000/applications/pending/
3. **Verify:**
   - ✅ Shield icon shaking
   - ✅ "403" in large text
   - ✅ "Access Denied" title
   - ✅ Shows "Client" role badge
   - ✅ Shows requested path `/applications/pending/`
   - ✅ Message: "You attempted to access..."
4. **Click:** "Go to Dashboard" → Should redirect to client dashboard

### SALES → Manager Route
1. **Login** as SALES
2. **Navigate:** http://localhost:8000/applications/team/
3. **Verify:**
   - ✅ Shows "Sales" role
   - ✅ Shows correct path
4. **Click:** "Logout" → Should logout successfully

### CLIENT → Admin Route (Payments)
1. **Login** as CLIENT
2. **Navigate:** http://localhost:8000/payments/approve/123/
3. **Verify:**
   - ✅ 403 page displays (even if payment ID doesn't exist)
   - ✅ Middleware blocks before checking payment

**Pass Criteria:** All unauthorized access blocked with proper 403 page

---

## Test 3: 500 Server Error ⏱️ 5 minutes

### Method A: Temporary Test View (Recommended)
1. **Add to `accounts/views.py`:**
```python
def test_500_view(request):
    raise Exception("Testing 500 error page")
```

2. **Add to `accounts/urls.py`:**
```python
path('test-500/', test_500_view, name='test_500'),
```

3. **Navigate:** http://localhost:8000/test-500/
4. **Verify (with DEBUG = False):**
   - ✅ Red/orange gradient
   - ✅ Warning triangle pulsing
   - ✅ "500" in large text
   - ✅ "Internal Server Error" title
   - ✅ Troubleshooting steps listed
   - ✅ "Try Again" and "Go Home" buttons

5. **Clean up:** Delete test view and URL after testing

### Method B: Change DEBUG Setting
1. **Edit `agnivridhi_crm/settings.py`:**
```python
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']
```

2. **Restart server**
3. **Trigger any error** (navigate to test_500_view or cause database error)
4. **Verify:** 500 page displays
5. **IMPORTANT:** Set `DEBUG = True` again after testing

**Pass Criteria:** 500 page renders without showing stack trace

---

## Test 4: Middleware Blocking ⏱️ 3 minutes

### Test Namespace-Level Protection
1. **Login** as CLIENT
2. **Try accessing these URLs directly:**
   - http://localhost:8000/applications/pending/
   - http://localhost:8000/applications/admin/applications/
   - http://localhost:8000/bookings/team/
   - http://localhost:8000/payments/
3. **Verify:**
   - ✅ All blocked with 403 page
   - ✅ Middleware blocks before view execution
   - ✅ No database queries attempted

### Test Exempt URLs (Should Work)
1. **Logout** (become unauthenticated)
2. **Try accessing:**
   - http://localhost:8000/accounts/login/
   - http://localhost:8000/static/css/styles.css (if exists)
   - http://localhost:8000/admin/
3. **Verify:**
   - ✅ No 403 blocking
   - ✅ Login page loads
   - ✅ Static files serve
   - ✅ Admin login page loads

**Pass Criteria:** Middleware blocks unauthorized namespaces but allows exempt URLs

---

## Test 5: Role Change Session Reset ⏱️ 4 minutes

### Setup
1. **Login** as CLIENT user
2. **Note:** You're logged in successfully
3. **Open Django admin** in another tab: http://localhost:8000/admin/
4. **Login** as superuser/admin

### Test Role Change
1. **In admin:** Navigate to Users → Find your CLIENT user
2. **Note:** User is currently logged in with CLIENT role
3. **Change role:** CLIENT → SALES
4. **Save** the user

### Verify Session Reset
1. **Go back to CLIENT user tab**
2. **Try to navigate** to any page (e.g., dashboard)
3. **Verify:**
   - ✅ Redirected to login page
   - ✅ Session was cleared automatically
   - ✅ Must re-authenticate with new SALES role

4. **Login again** with same credentials
5. **Verify:**
   - ✅ Now shows SALES dashboard
   - ✅ Has SALES permissions
   - ✅ Can access `/bookings/` (sales-allowed)

**Pass Criteria:** Role change forces logout and new permissions apply

---

## Test 6: Superuser Bypass ⏱️ 2 minutes

### Test Unrestricted Access
1. **Login** as SUPERUSER
2. **Try accessing ALL these URLs:**
   - http://localhost:8000/applications/pending/ (manager)
   - http://localhost:8000/applications/admin/applications/ (admin)
   - http://localhost:8000/bookings/team/ (manager)
   - http://localhost:8000/payments/ (admin)
   - http://localhost:8000/schemes/ (all)
3. **Verify:**
   - ✅ NO 403 errors
   - ✅ All pages load successfully
   - ✅ Middleware allows all namespaces

**Pass Criteria:** Superuser can access everything without restrictions

---

## Quick Checklist ✓

Copy this checklist and mark as you test:

```
404 Error Page:
[ ] Unauthenticated user sees login button
[ ] CLIENT sees scheme/application links
[ ] SALES sees booking links + search
[ ] ADMIN/MANAGER sees team links
[ ] Compass icon animates (bounce)

403 Error Page:
[ ] CLIENT blocked from /applications/pending/
[ ] SALES blocked from /applications/team/
[ ] CLIENT blocked from /payments/
[ ] Shield icon animates (shake)
[ ] Shows correct role and path
[ ] "Go to Dashboard" works

500 Error Page:
[ ] Red/orange gradient displays
[ ] Warning triangle animates (pulse)
[ ] No stack trace visible
[ ] Troubleshooting steps listed
[ ] "Try Again" and "Go Home" work

Middleware:
[ ] Blocks unauthorized namespaces
[ ] Allows exempt URLs (login, static, admin)
[ ] Superuser bypasses all restrictions
[ ] <1ms performance overhead

Role Changes:
[ ] Changing role clears last_login
[ ] User forced to re-authenticate
[ ] New permissions apply immediately
[ ] Session deleted automatically

System:
[ ] python manage.py check → 0 issues
[ ] All pages load without errors
[ ] Navigation works correctly
[ ] Custom error pages render properly
```

---

## Expected Results Summary

| Test | Expected Behavior | Pass/Fail |
|------|-------------------|-----------|
| 404 (unauthenticated) | Login button shown | ☐ |
| 404 (CLIENT) | Scheme/app links | ☐ |
| 404 (SALES) | Booking links + search | ☐ |
| 404 (ADMIN) | Team links | ☐ |
| 403 (CLIENT → manager) | Blocked with shield page | ☐ |
| 403 (SALES → manager) | Blocked with shield page | ☐ |
| 500 (any error) | Red warning page | ☐ |
| Middleware (unauthorized) | 403 before view | ☐ |
| Middleware (exempt) | Allows access | ☐ |
| Superuser | Access everything | ☐ |
| Role change | Forces logout | ☐ |
| System check | 0 issues | ☐ |

---

## Troubleshooting During Testing

### Problem: Custom error pages not showing
**Solution:** Set `DEBUG = False` in settings.py (custom handlers only work when DEBUG is False)

### Problem: NoReverseMatch errors
**Solution:** Check all URLs use namespace format: `{% url 'accounts:dashboard' %}`

### Problem: 403 page but then redirects
**Solution:** This is correct! Middleware shows 403 for namespace blocks, decorators redirect for view-level blocks

### Problem: 500 page not rendering
**Solution:** 
1. Check templates/errors/500.html exists
2. Verify handler500 in settings.py
3. Ensure DEBUG = False

### Problem: Role change doesn't force logout
**Solution:**
1. Verify signals registered in accounts/apps.py
2. Check accounts/signals.py imported
3. Run: `python manage.py shell` → `from accounts.signals import *`

---

## Performance Check

After testing, verify middleware performance:

```python
# In accounts/middleware.py, temporarily add timing:
import time

class RoleAccessMiddleware:
    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        elapsed = (time.time() - start) * 1000
        print(f"RoleAccessMiddleware: {elapsed:.2f}ms")
        return response
```

**Expected:** <1ms per request
**If >2ms:** Review ROLE_NAMESPACE_MAP lookup logic

---

## Post-Testing Cleanup

After completing all tests:

1. **Remove test view** (if added):
   - Delete `test_500_view` from accounts/views.py
   - Remove URL from accounts/urls.py

2. **Restore DEBUG setting:**
   - Set `DEBUG = True` in settings.py
   - Remove wildcard from ALLOWED_HOSTS if added

3. **Review logs:**
   - Check console for any warnings
   - Verify no unexpected errors

4. **Document results:**
   - Mark checklist items
   - Note any issues found
   - Take screenshots if needed

---

**Testing Time:** ~20 minutes total
**Status:** Ready for production after all tests pass ✅
