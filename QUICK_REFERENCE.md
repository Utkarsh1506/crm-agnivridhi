# 🎯 QUICK REFERENCE CARD - PythonAnywhere OTP Fix

```
┌─────────────────────────────────────────────────────────────────┐
│  PRODUCTION ERROR QUICK FIX                                     │
│  Time Required: 2-15 minutes                                    │
│  Difficulty: Easy                                               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: SET ENVIRONMENT VARIABLES (2 minutes) ⭐ CRITICAL       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Go to: https://www.pythonanywhere.com/user/agnivridhicrm/     │
│                                                                 │
│ Click: webapps → agnivridhicrm.pythonanywhere.com              │
│                                                                 │
│ Scroll to: Environment variables (or Web app settings)          │
│                                                                 │
│ Add these lines:                                                │
│                                                                 │
│   CLERK_SECRET_KEY=                                             │
│   sk_test_Uzd7yFdLxr5B13dlOktPvYp5hST63dS0l3bEsuMyKz          │
│                                                                 │
│   CLERK_PUBLIC_KEY=                                             │
│   pk_test_dGVuZGVyLXNlYXNuYWlsLTk5LmNsZXJrLmFjY291bnRzLmRldiQ │
│                                                                 │
│ Click: Save / Reload                                            │
│                                                                 │
│ Result: ✅ /client-login/ page loads without errors             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: TEST IT (1 minute)                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Visit: http://agnivridhicrm.pythonanywhere.com/client-login/   │
│                                                                 │
│ Should see:                                                     │
│   ✅ Email input form                                            │
│   ✅ "Send OTP" button                                           │
│   ✅ No error messages                                           │
│                                                                 │
│ If errors: Check Step 1 again                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STEP 3 (OPTIONAL): FIX EMAIL SENDING (10 minutes)               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ For testing only - use console backend:                         │
│   EMAIL_BACKEND='django.core.mail.backends.console.Email'      │
│                                                                 │
│ For production - use SendGrid:                                  │
│   1. Get account: https://sendgrid.com                          │
│   2. Get API key with "Mail Send" permission                    │
│   3. pip install django-sendgrid-v5                             │
│   4. Update settings.py (see PRODUCTION_ERROR_FIX_GUIDE.md)    │
│   5. Set SENDGRID_API_KEY on PythonAnywhere                     │
│                                                                 │
│ Result: ✅ Emails can be sent                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ TROUBLESHOOTING                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Problem: Still seeing "not configured" error                   │
│ Solution:                                                       │
│   • Check variable spelling (case-sensitive!)                   │
│   • Wait 30 seconds for reload to complete                      │
│   • Check env variable is actually saved                        │
│   • Try bash console method instead                             │
│                                                                 │
│ Problem: Page still shows "Reverse for 'client_email_login'"   │
│ Solution:                                                       │
│   • This is secondary error, fix Step 1 first                   │
│   • Reload browser (Ctrl+F5)                                    │
│   • Wait 60 seconds for full reload                             │
│                                                                 │
│ Problem: "Network is unreachable" in logs                       │
│ Solution:                                                       │
│   • PythonAnywhere blocks SMTP                                  │
│   • Use SendGrid instead (Step 3)                               │
│   • Or console backend for testing                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ DOCUMENTATION                                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Quick Fix (This card):                                          │
│   PYTHONANYWHERE_QUICK_FIX.md                                   │
│                                                                 │
│ Detailed Troubleshooting:                                       │
│   PYTHONANYWHERE_TROUBLESHOOTING.md                             │
│                                                                 │
│ Environment Setup Options:                                      │
│   PYTHONANYWHERE_ENV_SETUP.md                                   │
│                                                                 │
│ Complete Production Guide:                                      │
│   PRODUCTION_ERROR_FIX_GUIDE.md                                │
│                                                                 │
│ Summary of All Changes:                                         │
│   PRODUCTION_ERROR_RESOLUTION.md                                │
│                                                                 │
│ All files in: https://github.com/Utkarsh1506/crm-agnivridhi    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ WHAT WENT WRONG?                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Error #1: CLERK_SECRET_KEY not configured                       │
│   Why: .env file not on production server                       │
│   Fix: Set as environment variable (Step 1 above)               │
│                                                                 │
│ Error #2: NoReverseMatch 'client_email_login'                   │
│   Why: Secondary error from Error #1                            │
│   Fix: Automatically resolved by fixing Error #1                │
│                                                                 │
│ Error #3: OSError Network is unreachable (SMTP)                │
│   Why: PythonAnywhere blocks outbound SMTP                      │
│   Fix: Use SendGrid instead (Step 3 above)                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ AFTER SWITCHING TO LIVE KEYS                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ When ready for production (after testing with test keys):       │
│                                                                 │
│ 1. Get live keys from: https://dashboard.clerk.com             │
│                                                                 │
│ 2. Update on PythonAnywhere:                                    │
│                                                                 │
│    CLERK_SECRET_KEY=sk_live_YOUR_LIVE_SECRET_KEY               │
│    CLERK_PUBLIC_KEY=pk_live_YOUR_LIVE_PUBLIC_KEY               │
│                                                                 │
│ 3. Click Reload                                                 │
│                                                                 │
│ 4. Test again to confirm                                        │
│                                                                 │
│ ⚠️ DO NOT expose live keys in code or git!                      │
│    Only set them as environment variables on PythonAnywhere     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ QUICK COMMANDS                                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Check env vars are loaded:                                      │
│   python -c "import os; print(os.getenv('CLERK_SECRET_KEY'))"   │
│                                                                 │
│ View logs:                                                      │
│   tail -f /var/log/agnivridhicrm_pythonanywhere_com_error.log   │
│                                                                 │
│ Test OTP:                                                       │
│   python manage.py shell                                        │
│   from accounts.clerk_otp_service import clerk_service         │
│   clerk_service.send_otp('test@example.com')                   │
│                                                                 │
│ Reload web app:                                                 │
│   touch /var/www/agnivridhicrm_pythonanywhere_com_wsgi.py      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

                    ✅ YOU'RE ALL SET! ✅
                  Follow the 3 steps above and you're done.
              Questions? Check the documentation files above.
```

---

## Testing Checklist

After implementing fixes, verify:

```
BEFORE FIX:                          AFTER FIX:
❌ /client-login/ shows error        ✅ Page loads normally
❌ "not configured" in logs           ✅ "API key loaded" in logs
❌ Cannot enter email                ✅ Can type and submit email
❌ OTP not sent                      ✅ OTP arrives in email
❌ SMTP errors in logs               ✅ No network errors
```

---

## When to Use Each Document

| Situation | Read This |
|-----------|-----------|
| "Fix this in 5 minutes!" | PYTHONANYWHERE_QUICK_FIX.md |
| "Why isn't it working?" | PYTHONANYWHERE_TROUBLESHOOTING.md |
| "Show me all options" | PYTHONANYWHERE_ENV_SETUP.md |
| "Complete setup guide" | PRODUCTION_ERROR_FIX_GUIDE.md |
| "What changed?" | PRODUCTION_ERROR_RESOLUTION.md |

---

## Save This Card

Print this page or bookmark:
```
Quick Reference: PYTHONANYWHERE_QUICK_FIX.md
Detailed Help: PYTHONANYWHERE_TROUBLESHOOTING.md
GitHub: https://github.com/Utkarsh1506/crm-agnivridhi
```

**Expected Time to Complete: 2 minutes for OTP, 15 minutes for complete setup**

