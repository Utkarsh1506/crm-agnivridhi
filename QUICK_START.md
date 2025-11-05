# 🚀 QUICK START - Agnivridhi CRM

## ⚡ 5-Minute Setup

### Step 1: Create .env file
```bash
python setup_env.py
```

### Step 2: Edit .env file
```bash
notepad .env  # or your preferred editor
```

Add your credentials:
- **Email:** `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`
- **Twilio:** `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` (optional)

### Step 3: Run migrations
```bash
python manage.py migrate
```

### Step 4: Create superuser (if not exists)
```bash
python manage.py createsuperuser
```

### Step 5: Test system
```bash
python test_system.py
```

### Step 6: Start server
```bash
python manage.py runserver
```

---

## 🌐 Access URLs

| Service | URL |
|---------|-----|
| **Admin Dashboard** | http://localhost:8000/dashboard/ |
| **Django Admin** | http://localhost:8000/admin/ |
| **Swagger API** | http://localhost:8000/api/docs/ |
| **ReDoc** | http://localhost:8000/api/redoc/ |
| **API Root** | http://localhost:8000/api/ |

---

## 🧪 Quick Tests

### Test Email
```python
python manage.py shell

from django.core.mail import send_mail
send_mail('Test', 'Test email', 'noreply@agnivridhiindia.com', ['your_email@gmail.com'])
```

### Test WhatsApp
```python
python manage.py shell

from accounts.whatsapp_utils import send_custom_whatsapp
send_custom_whatsapp('+919876543210', 'Test from CRM!')
```

### Test PDF
Visit: http://localhost:8000/pdf/payment/1/

### Test API
Visit: http://localhost:8000/api/docs/

---

## 📋 Configuration Checklist

- [ ] `.env` file created
- [ ] `SECRET_KEY` generated
- [ ] `EMAIL_HOST_USER` configured
- [ ] `EMAIL_HOST_PASSWORD` configured (Gmail App Password)
- [ ] `TWILIO_ACCOUNT_SID` configured (optional)
- [ ] `TWILIO_AUTH_TOKEN` configured (optional)
- [ ] Phone added to Twilio sandbox (if using WhatsApp)
- [ ] Database migrated
- [ ] Superuser created
- [ ] `test_system.py` passed all tests

---

## 🔑 Get Credentials

### Gmail App Password
1. Go to: https://myaccount.google.com/security
2. Enable 2-Step Verification
3. App Passwords → Generate new
4. Select "Mail" and "Other"
5. Copy 16-character password

### Twilio Credentials
1. Sign up: https://www.twilio.com/try-twilio
2. Dashboard: https://console.twilio.com/
3. Copy Account SID and Auth Token
4. WhatsApp Sandbox: https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox
5. Send join code from your phone

---

## 🎯 Main Features

✅ **REST API** - Full CRUD with Swagger docs  
✅ **Email Notifications** - Payment, booking, application updates  
✅ **WhatsApp Notifications** - Twilio integration  
✅ **PDF Generation** - Receipts, confirmations, forms  
✅ **CSV Export** - Clients, bookings, payments  
✅ **Global Search** - Multi-entity search  
✅ **Activity Logging** - Complete audit trail  
✅ **Advanced Reporting** - Analytics dashboard  

---

## 📚 Documentation

- **Setup Guide:** `SETUP_AND_TESTING_GUIDE.md`
- **Feature Guide:** `NEW_FEATURES_GUIDE.md`
- **System Status:** `COMPLETE_SYSTEM_STATUS.md`
- **API Docs:** http://localhost:8000/api/docs/ (when server running)

---

## 🆘 Troubleshooting

### Email not sending?
- Check Gmail App Password (16 chars, no spaces)
- Verify 2-Step Verification enabled
- Test with console backend first: `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend`

### WhatsApp not working?
- Verify Twilio credentials in .env
- Add your phone to sandbox
- Check phone format: +919876543210

### PDF not generating?
- Check WeasyPrint installed: `pip install weasyprint`
- Test simple PDF in shell

### API 401 error?
- Authenticate in Swagger UI
- Click "Authorize" button
- Enter credentials

---

## 🚀 Production Deployment

Before deploying:
1. Set `DEBUG=False`
2. Generate new `SECRET_KEY`
3. Configure production database
4. Set `ALLOWED_HOSTS`
5. Enable SSL: `SECURE_SSL_REDIRECT=True`
6. Run `python manage.py collectstatic`
7. Use Gunicorn/uWSGI
8. Set up Nginx reverse proxy
9. Install SSL certificate
10. Configure backups

---

## 📞 Support

Check logs:
```bash
# Django logs
python manage.py runserver  # Check console output

# Twilio logs
https://console.twilio.com/us1/monitor/logs/sms
```

Test components individually:
```bash
python test_system.py
```

---

**Quick Reference Version:** 1.0  
**Last Updated:** November 5, 2025  
**Project:** Agnivridhi India CRM System
