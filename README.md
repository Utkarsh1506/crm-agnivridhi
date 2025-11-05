# Agnivridhi CRM - Complete Business Consultancy Management System

A production-ready Django CRM system for Agnivridhi India matching your site's theme and color palette.

## 🚀 Quick Start

### 1. Initial Setup
```powershell
cd C:\Users\Admin\Desktop\agni\CRM
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Environment Configuration
```powershell
cp .env.example .env
# Edit .env with your database, email, Razorpay, and WhatsApp credentials
```

### 3. Database Setup
```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 4. Load Initial Data
```powershell
python manage.py loaddata schemes_data.json
python manage.py loaddata services_data.json
```

### 5. Run Development Server
```powershell
python manage.py runserver
```

Visit: http://127.0.0.1:8000

## 📁 Project Structure

```
CRM/
├── agnivridhi_crm/          # Main project settings
├── accounts/                 # User authentication & roles
├── clients/                  # Client management
├── bookings/                 # Service bookings
├── applications/             # Loan applications
├── schemes/                  # Government schemes database
├── edit_requests/            # Edit approval workflow
├── payments/                 # Razorpay integration
├── documents/                # PDF generation
├── notifications/            # Email & WhatsApp alerts
├── templates/                # HTML templates (Agn ivridhi theme)
├── static/                   # CSS, JS, images
├── media/                    # User uploads
└── requirements.txt
```

## 👥 User Roles & Access

### Admin
- Full system access
- Approve/reject edit requests
- Manage users, schemes, services
- View analytics dashboard
- Login: `/admin/` or `/login/`

### Manager
- View all clients & employees
- Create bookings for clients
- Request edits (requires admin approval)
- Generate client credentials (approve sales requests)
- Team performance dashboard
- Login: `/login/`

### Sales Employee
- View assigned clients only
- Request new client creation
- Book services for clients
- Request edits (requires admin approval)
- Login: `/login/`

### Client
- View own applications & bookings
- Apply for schemes
- Download DPR, pitch decks, reports
- Make payments
- Track application status
- Login: `/client-login/`

## 🎨 Frontend Theme

Matches Agnivridhi website theme:
- Primary: Cyan/Teal gradient (#0891b2, #2dd4bf)
- Bootstrap 5
- Responsive design
- Clean, professional UI
- Chart.js for analytics

## 🔐 Authentication Flow

1. **Sales Creates Client** → Request to Manager
2. **Manager Approves** → Generates credentials
3. **Client Receives** → WhatsApp + Email with login details
4. **Client Logs In** → Access portal

## 📊 Core Features

### 1. Client Management
- Full profile (company, sector, turnover, funding needs)
- Assign to sales employee & manager
- Auto-generate unique credentials
- Track all applications & bookings

### 2. Booking System
- Service catalog (DPR, Pitch Deck, Funding Assistance, etc.)
- Status tracking (Pending → In Progress → Completed)
- Payment integration
- Document delivery

### 3. Application Tracking
```
Submitted → Under Review → Query Raised → Approved/Rejected
```
- Real-time status updates
- Progress timeline
- Admin remarks
- Client notifications

### 4. Edit Request Workflow
```
Sales/Manager Request → Admin Reviews → Approve/Reject → Auto-Apply
```
- Track all change requests
- Maintain audit trail
- Email notifications

### 5. Loan Eligibility Engine
- Auto-match clients to schemes
- Check turnover, sector, age, funding limits
- Show eligible/ineligible with reasons
- Database of 50+ government schemes

### 6. AI Recommendations
- Top 3 suggested schemes per client
- Based on: profile, sector, turnover, historical approvals
- Reasoning provided for each recommendation

### 7. Document Generation
Auto-generate PDFs:
- Detailed Project Report (DPR)
- Pitch Deck
- Financial Projections
- Fund Utilisation Report

Template-based with client data pre-filled.

### 8. Payment Integration (Razorpay)
- Online payment for services
- Webhook handling
- Receipt generation
- Payment history

### 9. WhatsApp Notifications
Send automated messages for:
- Client credentials
- Application status updates
- Payment confirmations
- Approval alerts

### 10. Email Notifications
- SMTP-based email system
- Role-specific alerts
- Status change notifications
- Weekly digest reports

## 📈 Analytics Dashboard

### Admin Dashboard
- Total clients
- Applications by status
- Revenue summary
- Top performers
- Monthly trends

### Manager Dashboard
- Team performance
- Client pipeline
- Pending approvals
- Revenue by employee

### Sales Dashboard
- My clients
- Pending bookings
- Commission tracking
- Target vs achieved

### Client Dashboard
- Application status
- Payment history
- Document downloads
- Scheme recommendations

## 🗄️ Database Models

### User (Custom)
- Extends Django User
- Roles: Admin, Manager, Sales, Client
- Phone, designation, team assignment

### Client
- Company details
- Financial profile
- Assigned sales & manager
- Status tracking

### Booking
- Service reference
- Client reference
- Status, payment status
- Created by (sales/manager)

### Application
- Client + Scheme
- Status with timeline
- Documents attached
- Admin remarks

### Scheme
- Name, authority, description
- Eligibility rules (turnover, sector, age)
- Funding limits
- Active status

### EditRequest
- Requested by (user)
- Target (client/application/booking)
- Old value vs new value
- Approval status
- Approved by & timestamp

### Payment
- Booking reference
- Razorpay transaction details
- Amount, status
- Receipt URL

### Document
- Client/Application reference
- Type (DPR, Pitch Deck, etc.)
- File path
- Generated timestamp

### Notification
- User reference
- Type (email/whatsapp)
- Message, status
- Read status

## 🌐 API Endpoints (REST)

```
/api/auth/login/
/api/auth/logout/
/api/clients/
/api/clients/{id}/
/api/bookings/
/api/applications/
/api/schemes/
/api/schemes/eligible/{client_id}/
/api/edit-requests/
/api/payments/create/
/api/payments/verify/
/api/documents/generate/{type}/
/api/notifications/
```

## 🔧 Environment Variables

Required in `.env`:

```ini
# Django
SECRET_KEY=
DEBUG=True
ALLOWED_HOSTS=

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=agnivridhi_crm
DB_USER=
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# Razorpay
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=

# WhatsApp (Gupshup)
WHATSAPP_API_KEY=
WHATSAPP_APP_NAME=
WHATSAPP_SOURCE_NUMBER=

# Redis
REDIS_URL=redis://localhost:6379/0

# Site
SITE_NAME=Agnivridhi CRM
SITE_URL=https://crm.agnivridhiindia.com
COMPANY_PHONE=+919289555190
COMPANY_EMAIL=info@agnivridhiindia.com
```

## 🚀 Deployment (Hostinger)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial CRM setup"
git remote add origin https://github.com/Utkarsh1506/agnivridhi-crm.git
git push -u origin main
```

### Step 2: Hostinger Setup
1. Go to Hostinger hPanel
2. Create Python app
3. Connect GitHub repository
4. Set Python version: 3.11
5. Entry point: `agnivridhi_crm.wsgi:application`
6. Add environment variables from `.env`

### Step 3: Configure Database
```bash
# In Hostinger terminal
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### Step 4: Setup Gunicorn
```bash
gunicorn agnivridhi_crm.wsgi:application --bind 0.0.0.0:8000
```

## 📱 Mobile App (Future)

React Native app can use the REST API:
- JWT authentication
- All CRM features
- Push notifications
- Offline mode

## 🛠️ Development

### Run Tests
```bash
python manage.py test
```

### Create Fake Data
```bash
python manage.py generate_test_data
```

### Export Data
```bash
python manage.py export_clients --format xlsx
python manage.py export_applications --format pdf
```

## 📞 Support

For issues or questions:
- Email: info@agnivridhiindia.com
- Phone: +91 9289555190

## 📄 License

Proprietary - Agnivridhi India Pvt. Ltd. © 2025
