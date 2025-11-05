# 🚀 SETUP & TESTING GUIDE
**Agnivridhi CRM - Complete Configuration and Testing Instructions**

---

## 📋 STEP 1: Configure Environment Variables

### 1.1 Create .env file

```bash
# Copy the example file
cp .env.example .env
```

### 1.2 Edit .env and configure the following:

#### **Django Settings** (Required)
```env
SECRET_KEY=django-insecure-CHANGE-THIS-TO-RANDOM-50-CHARACTER-STRING
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Generate SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

#### **Email Configuration** (Required for Notifications)

**Option A: Gmail**
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_16_char_app_password
DEFAULT_FROM_EMAIL=noreply@agnivridhiindia.com
```

**How to get Gmail App Password:**
1. Go to Google Account Settings: https://myaccount.google.com/
2. Security → 2-Step Verification (enable if not enabled)
3. App Passwords → Generate new app password
4. Select "Mail" and "Other (Custom name)" → Enter "Agnivridhi CRM"
5. Copy the 16-character password

**Option B: For Development (Console Backend)**
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```
*Emails will print to console instead of sending*

---

#### **Twilio WhatsApp Configuration** (Required for WhatsApp)

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

**How to get Twilio credentials:**

1. **Sign up for Twilio:**
   - Go to: https://www.twilio.com/try-twilio
   - Sign up (free $15 credit)
   - Verify your email and phone

2. **Get Account SID and Auth Token:**
   - Login to Twilio Console: https://console.twilio.com/
   - Dashboard → Account Info section
   - Copy `Account SID` and `Auth Token`

3. **Enable WhatsApp Sandbox (Development):**
   - Go to: https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox
   - Follow instructions to activate sandbox
   - Send the code from your phone to the sandbox number
   - Use sandbox number: `whatsapp:+14155238886`

4. **For Production (Optional):**
   - Apply for WhatsApp Business API
   - Get approved WhatsApp number
   - Create message templates
   - Update `TWILIO_WHATSAPP_FROM` with your number

---

#### **CORS Configuration** (Required for API)

```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

*Add your frontend URL if different*

---

### 1.3 Verify Configuration

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Check Django settings
python manage.py check

# Test database connection
python manage.py migrate
```

---

## 🧪 STEP 2: Test REST API via Swagger UI

### 2.1 Start Development Server

```bash
python manage.py runserver
```

### 2.2 Access Swagger UI

Open browser: **http://localhost:8000/api/docs/**

### 2.3 Authenticate

1. Click the **"Authorize"** button (top right)
2. Enter your credentials:
   - Username: `admin` (or your superuser username)
   - Password: your password
3. Click **"Authorize"** then **"Close"**

### 2.4 Test Endpoints

#### **Test 1: Get All Clients**
1. Navigate to **GET /api/clients/**
2. Click **"Try it out"**
3. Click **"Execute"**
4. Verify response (should return list of clients)

#### **Test 2: Create a Client**
1. Navigate to **POST /api/clients/**
2. Click **"Try it out"**
3. Modify the request body:
```json
{
  "company_name": "Test Company Ltd",
  "contact_name": "John Doe",
  "contact_email": "john@testcompany.com",
  "contact_phone": "+919876543210",
  "pan_number": "ABCDE1234F",
  "address": "123 Test Street",
  "city": "Mumbai",
  "state": "Maharashtra",
  "pincode": "400001",
  "sector": "TECHNOLOGY",
  "status": "ACTIVE"
}
```
4. Click **"Execute"**
5. Verify response (should return created client with ID)

#### **Test 3: Get Client Details**
1. Navigate to **GET /api/clients/{id}/**
2. Click **"Try it out"**
3. Enter the client ID from previous test
4. Click **"Execute"**
5. Verify detailed response

#### **Test 4: Filter Clients**
1. Navigate to **GET /api/clients/**
2. Click **"Try it out"**
3. Add parameters:
   - `sector`: TECHNOLOGY
   - `status`: ACTIVE
4. Click **"Execute"**
5. Verify filtered results

#### **Test 5: Search Clients**
1. Navigate to **GET /api/clients/**
2. Click **"Try it out"**
3. Add parameter:
   - `search`: Test Company
4. Click **"Execute"**
5. Verify search results

#### **Test 6: Create Booking**
1. Navigate to **POST /api/bookings/**
2. Click **"Try it out"**
3. Modify request body:
```json
{
  "client": 1,
  "service": 1,
  "booking_date": "2025-11-15",
  "amount": 50000,
  "status": "PENDING",
  "notes": "Test booking from API"
}
```
4. Click **"Execute"**
5. Verify booking created

#### **Test 7: Approve Payment** (If payment exists)
1. Navigate to **POST /api/payments/{id}/approve/**
2. Click **"Try it out"**
3. Enter payment ID
4. Click **"Execute"**
5. Check email console for notification
6. Verify response shows approved status

---

## 📱 STEP 3: Test WhatsApp Notifications

### 3.1 Verify Twilio Configuration

```python
# Open Django shell
python manage.py shell

# Test Twilio connection
from accounts.whatsapp_utils import get_twilio_client
client = get_twilio_client()
if client:
    print("✅ Twilio configured successfully!")
else:
    print("❌ Twilio not configured. Check .env credentials.")
```

### 3.2 Test WhatsApp Sandbox

**Important:** First add your phone number to Twilio sandbox:
1. Go to: https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox
2. Send the join code from your WhatsApp to the sandbox number
3. Wait for confirmation message

### 3.3 Test Payment Approval WhatsApp

```python
# In Django shell
from payments.models import Payment
from accounts.whatsapp_utils import send_payment_approval_whatsapp

# Get a payment (create one if needed)
payment = Payment.objects.first()

# Make sure the client has a phone number in format: +919876543210
print(f"Client phone: {payment.client.contact_phone}")

# Send WhatsApp notification
result = send_payment_approval_whatsapp(payment)
print(f"WhatsApp sent: {result}")
```

**Expected Result:**
- Should receive WhatsApp message on your phone
- Check Twilio console logs: https://console.twilio.com/us1/monitor/logs/sms

### 3.4 Test Custom WhatsApp Message

```python
# In Django shell
from accounts.whatsapp_utils import send_custom_whatsapp

# Replace with your phone number (must be in sandbox)
result = send_custom_whatsapp(
    "+919876543210",  # Your phone number
    "🎉 Test message from Agnivridhi CRM!"
)
print(f"Sent: {result}")
```

### 3.5 Test All WhatsApp Functions

```python
from bookings.models import Booking
from applications.models import Application
from accounts.whatsapp_utils import (
    send_booking_confirmation_whatsapp,
    send_application_status_whatsapp
)

# Test booking confirmation
booking = Booking.objects.first()
send_booking_confirmation_whatsapp(booking)

# Test application status
application = Application.objects.first()
send_application_status_whatsapp(application)
```

---

## 📄 STEP 4: Test PDF Generation

### 4.1 Test via Browser

1. Start server: `python manage.py runserver`
2. Login to admin: http://localhost:8000/admin/
3. Test PDF downloads:

**Payment Receipt:**
```
http://localhost:8000/pdf/payment/1/
```

**Booking Confirmation:**
```
http://localhost:8000/pdf/booking/1/
```

**Application Form:**
```
http://localhost:8000/pdf/application/1/
```

*Replace `1` with actual IDs from your database*

### 4.2 Test via Django Shell

```python
python manage.py shell

# Test payment receipt PDF
from payments.models import Payment
from accounts.pdf_utils import generate_payment_receipt_pdf

payment = Payment.objects.first()
pdf_response = generate_payment_receipt_pdf(payment)

print(f"Content-Type: {pdf_response['Content-Type']}")
print(f"Content-Disposition: {pdf_response['Content-Disposition']}")
print(f"PDF Size: {len(pdf_response.content)} bytes")
```

### 4.3 Test Booking Confirmation PDF

```python
from bookings.models import Booking
from accounts.pdf_utils import generate_booking_confirmation_pdf

booking = Booking.objects.first()
pdf_response = generate_booking_confirmation_pdf(booking)
print(f"PDF generated: {len(pdf_response.content)} bytes")
```

### 4.4 Test All PDF Functions

```python
from applications.models import Application
from clients.models import Client
from accounts.pdf_utils import (
    generate_application_form_pdf,
    generate_dpr_report_pdf,
    generate_invoice_pdf
)
from datetime import datetime, timedelta

# Application form
app = Application.objects.first()
generate_application_form_pdf(app)

# DPR Report
client = Client.objects.first()
date_from = datetime.now() - timedelta(days=30)
date_to = datetime.now()
generate_dpr_report_pdf(client, date_from, date_to)

# Invoice
payment = Payment.objects.first()
generate_invoice_pdf(payment)

print("✅ All PDF functions working!")
```

---

## 🎯 STEP 5: Integration Testing

### 5.1 Complete Payment Approval Flow

```python
python manage.py shell

from payments.models import Payment
from accounts.email_utils import send_payment_approval_email
from accounts.whatsapp_utils import send_payment_approval_whatsapp
from accounts.pdf_utils import generate_payment_receipt_pdf

# Get payment
payment = Payment.objects.filter(status='PENDING').first()

# Approve payment
payment.status = 'APPROVED'
payment.save()

# Send email notification
send_payment_approval_email(payment, payment.received_by)

# Send WhatsApp notification
send_payment_approval_whatsapp(payment)

# Generate PDF receipt
pdf = generate_payment_receipt_pdf(payment)

print("✅ Complete payment flow tested!")
```

### 5.2 Test API Payment Approval

```bash
# Using curl
curl -X POST http://localhost:8000/api/payments/1/approve/ \
  -u admin:your_password \
  -H "Content-Type: application/json"

# Should:
# 1. Approve payment in database
# 2. Send email notification
# 3. Log activity
# 4. Return updated payment JSON
```

### 5.3 Test Complete Booking Flow

```python
from clients.models import Client
from bookings.models import Booking, Service
from payments.models import Payment
from accounts.whatsapp_utils import send_booking_confirmation_whatsapp
from accounts.pdf_utils import generate_booking_confirmation_pdf

# Create booking
client = Client.objects.first()
service = Service.objects.first()

booking = Booking.objects.create(
    client=client,
    service=service,
    booking_date=datetime.now().date(),
    amount=50000,
    status='CONFIRMED'
)

# Send WhatsApp
send_booking_confirmation_whatsapp(booking)

# Generate PDF
pdf = generate_booking_confirmation_pdf(booking)

# Create payment
payment = Payment.objects.create(
    client=client,
    booking=booking,
    amount=50000,
    payment_method='UPI',
    payment_date=datetime.now().date(),
    status='PENDING'
)

print("✅ Complete booking flow created!")
```

---

## 🐛 TROUBLESHOOTING

### Email Issues

**Problem:** Emails not sending
```python
# Test email configuration
python manage.py shell

from django.core.mail import send_mail

send_mail(
    'Test Email',
    'This is a test email from Agnivridhi CRM',
    'noreply@agnivridhiindia.com',
    ['your_email@gmail.com'],
    fail_silently=False,
)
```

**Common Issues:**
- Gmail App Password incorrect → Regenerate
- 2-Step Verification not enabled → Enable it
- Less secure app access → Use App Password instead

---

### WhatsApp Issues

**Problem:** WhatsApp not sending

1. **Check Twilio credentials:**
```python
import os
print(f"SID: {os.getenv('TWILIO_ACCOUNT_SID')}")
print(f"Token: {os.getenv('TWILIO_AUTH_TOKEN')[:10]}...")
print(f"From: {os.getenv('TWILIO_WHATSAPP_FROM')}")
```

2. **Check phone number format:**
   - Must include country code: `+919876543210`
   - Must be added to Twilio sandbox

3. **Check Twilio logs:**
   - https://console.twilio.com/us1/monitor/logs/sms

**Common Issues:**
- Phone not in sandbox → Send join code
- Invalid phone format → Use +[country][number]
- Twilio trial account → Verify recipient phone

---

### PDF Issues

**Problem:** PDF not generating

1. **Check WeasyPrint installation:**
```python
import weasyprint
print(f"WeasyPrint version: {weasyprint.__version__}")
```

2. **Test simple PDF:**
```python
from weasyprint import HTML
html = HTML(string="<h1>Test PDF</h1>")
pdf = html.write_pdf()
print(f"PDF size: {len(pdf)} bytes")
```

**Common Issues:**
- Missing dependencies → Reinstall weasyprint
- Template not found → Check template path
- Font issues on Windows → Install GTK+ runtime

---

### API Issues

**Problem:** API returns 401 Unauthorized
- Solution: Authenticate in Swagger UI or send credentials

**Problem:** API returns 403 Forbidden
- Solution: Check user permissions (is_staff required)

**Problem:** CORS errors
- Solution: Add frontend URL to CORS_ALLOWED_ORIGINS in .env

---

## ✅ VERIFICATION CHECKLIST

Use this checklist to verify all features:

### Configuration:
- [ ] .env file created with all required variables
- [ ] SECRET_KEY generated (50+ characters)
- [ ] Email SMTP configured (Gmail App Password)
- [ ] Twilio credentials configured
- [ ] Phone number added to Twilio sandbox

### REST API:
- [ ] Swagger UI accessible at /api/docs/
- [ ] Can authenticate in Swagger
- [ ] GET /api/clients/ returns data
- [ ] POST /api/clients/ creates client
- [ ] Filtering works (sector, status)
- [ ] Search works
- [ ] Pagination works (50 items per page)

### Email Notifications:
- [ ] Test email sent successfully
- [ ] Payment approval email received
- [ ] Payment rejection email received
- [ ] Email templates rendering correctly

### WhatsApp Notifications:
- [ ] Twilio client initializes
- [ ] Phone number in sandbox
- [ ] Payment approval WhatsApp received
- [ ] Booking confirmation WhatsApp received
- [ ] Custom message works

### PDF Generation:
- [ ] Payment receipt PDF downloads
- [ ] Booking confirmation PDF downloads
- [ ] Application form PDF downloads
- [ ] PDFs are properly formatted
- [ ] Company branding visible

### Integration:
- [ ] API payment approval sends email
- [ ] API payment approval logs activity
- [ ] Complete booking flow works
- [ ] All notifications triggered correctly

---

## 🚀 PRODUCTION DEPLOYMENT

Once all tests pass, proceed with production deployment:

### 1. Security Configuration

```env
# Production .env
DEBUG=False
SECRET_KEY=<generate-new-strong-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 2. Database Migration

```bash
# Backup SQLite database
cp db.sqlite3 db.sqlite3.backup

# Or migrate to PostgreSQL (recommended)
# Update DATABASE settings in .env
python manage.py migrate
```

### 3. Static Files

```bash
python manage.py collectstatic --noinput
```

### 4. Production Server

Use Gunicorn + Nginx:

```bash
pip install gunicorn
gunicorn agnivridhi_crm.wsgi:application --bind 0.0.0.0:8000
```

### 5. SSL Certificate

Install Let's Encrypt SSL:
```bash
sudo certbot --nginx -d yourdomain.com
```

### 6. Monitoring

- Set up error monitoring (Sentry)
- Configure logging
- Set up backup automation
- Monitor Twilio usage and costs

---

## 📞 SUPPORT

If you encounter issues:

1. Check Django logs
2. Check Twilio console logs
3. Test email configuration separately
4. Verify .env variables loaded correctly
5. Check firewall/network settings

**Documentation:**
- Django: https://docs.djangoproject.com/
- DRF: https://www.django-rest-framework.org/
- Twilio: https://www.twilio.com/docs/whatsapp
- WeasyPrint: https://weasyprint.readthedocs.io/

---

**Setup Guide Version:** 1.0  
**Last Updated:** November 5, 2025  
**Project:** Agnivridhi India CRM System
