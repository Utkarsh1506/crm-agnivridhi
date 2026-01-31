# 🧪 Clerk OTP Testing - Local Development

## ✅ Server Status

Your Django server is running at:
```
http://localhost:8000/
```

## ✅ Configuration Status

```
CLERK_PUBLIC_KEY:  pk_test_dGVuZGVyLXNlYXNuYWlsLTk5LmNsZXJrLmFjY291bnRzLmRldiQ
CLERK_SECRET_KEY:  sk_test_Uz...dS0l3bEsuMyKz (hidden)
Service Status:    ✅ INITIALIZED
```

---

## 🧪 How to Test Clerk OTP Locally

### Step 1: Access Login Page

Open in your browser:
```
http://localhost:8000/accounts/client-login/
```

### Step 2: Enter Test Email

Use a real email address you have access to (or test email):
```
Example: your-email@example.com
test-client@gmail.com
your-work-email@company.com
```

### Step 3: Send OTP

Click "Send OTP" button

You should see:
- ✅ "OTP sent to your-email@example.com"
- ✅ Message says "Check your inbox"

### Step 4: Check Email Inbox

Wait 10-30 seconds for the email to arrive.

Look for email from Clerk with subject like:
```
"Your sign in code"
or
"Authentication code for your account"
```

### Step 5: Enter OTP Code

The email contains a 6-digit code. Copy it and paste into the form:
```
Example: 123456
```

### Step 6: Verify OTP

Click "Verify OTP" button

You should see:
- ✅ "OTP verified successfully"
- ✅ Redirected to client dashboard or logged in

---

## 🐛 Troubleshooting Local Testing

### Email Not Received?

**Possible Causes & Fixes:**

1. **Check Spam/Promotions Folder**
   - Gmail: Check "Promotions" tab
   - Outlook: Check "Junk" folder
   - Check spam filter settings

2. **Wrong Email Address**
   - Make sure you spelled it correctly
   - Check for typos

3. **Try Again**
   - Clerk has rate limiting
   - Wait 30 seconds before requesting new OTP

4. **Test with Different Email**
   - Try Gmail, Yahoo, or work email
   - Some domains might block test emails

5. **Check Django Logs**
   - Terminal should show: "Sending OTP to email@example.com via Clerk API"
   - Look for errors or warnings

### "OTP Service Not Configured"?

This means CLERK_SECRET_KEY wasn't loaded. Solution:
```bash
# 1. Verify .env has the keys
cat .env | grep CLERK

# 2. Restart Django
# Press CTRL-C in terminal
# Then: python manage.py runserver 8000
```

### "Invalid OTP Code"?

- Code might be expired (expires after 10 min)
- Try requesting a new OTP
- Make sure you copied the code correctly (no spaces)

### API Connection Issues?

Check server logs for:
```
ERROR: Request error sending OTP
ERROR: Clerk API error (status XXX)
```

This means the API key might be invalid. Verify with:
```bash
python test_clerk_service.py
```

---

## 📊 Testing Checklist

```
☐ Django server running (http://localhost:8000)
☐ Can access /accounts/client-login/
☐ Can submit email
☐ OTP email received
☐ Can enter OTP code
☐ OTP verification successful
☐ User logged in
☐ No errors in console
```

---

## 🔍 Advanced Testing

### Via Python Shell

Test the service directly:

```bash
python manage.py shell
```

Then run:

```python
from accounts.clerk_otp_service import clerk_service

# Test 1: Send OTP
result = clerk_service.send_otp('test@example.com')
print(result)
# Expected: {'success': True, 'message': '...', 'sign_in_id': 'signin_xxx'}

# Test 2: Get service info
print(clerk_service.clerk_api_key[:10] + '...')  # Should show sk_test_...
```

### Check Service Initialization

```bash
python test_clerk_service.py
```

Should show:
```
✓ Configuration Check: PASSED
✓ API Connectivity: OK
✓ Service Methods: Available
✅ CLERK OTP SERVICE READY FOR TESTING
```

---

## 📝 Notes for Testing

- **Test Keys:** You're using test keys (pk_test_, sk_test_) which is perfect for development
- **Email Domain:** Test emails work fine for development
- **Rate Limiting:** Clerk limits OTP requests to ~10 per email per hour
- **OTP Expiry:** Codes expire after 10 minutes
- **No Real Users:** Test users are not synced to production

---

## 🚀 Next Steps After Testing

Once local testing works:

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Deploy to PythonAnywhere**
   - SSH and `git pull`
   - Set environment variables with production keys
   - Reload web app

3. **Switch to Production Keys**
   - In Clerk Dashboard: Get pk_live_ and sk_live_ keys
   - Update PythonAnywhere environment variables
   - Test in production

---

## 📚 Documentation

For more details, see:
- [CLERK_OTP_SETUP_GUIDE.md](CLERK_OTP_SETUP_GUIDE.md) - Full setup
- [CLERK_OTP_QUICK_REFERENCE.md](CLERK_OTP_QUICK_REFERENCE.md) - Quick ref
- [accounts/clerk_otp_service.py](accounts/clerk_otp_service.py) - Code

---

## 💡 Testing Tips

1. **Use Multiple Email Addresses**
   - Gmail (might be slow to deliver test emails)
   - Yahoo
   - Work email
   - Try different providers

2. **Check the Network Tab**
   - In browser DevTools (F12)
   - Look for API calls to clerk API
   - Check response status codes

3. **Monitor Server Logs**
   - Watch terminal for "Sending OTP..."
   - Look for "OTP verified successfully"
   - Check for any error messages

4. **Test the Error Path**
   - Try entering wrong OTP to see error handling
   - Try expired OTP (wait >10 min)
   - Test with invalid email

---

**Status:** ✅ Ready for Testing
**Server:** Running at http://localhost:8000/
**Clerk Keys:** Configured (test keys)
**Next:** Visit the login page and test!
