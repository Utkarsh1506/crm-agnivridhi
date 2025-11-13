# 📋 Complete Manual Testing Checklist - Agnivridhi CRM

## 🎯 Testing Overview
**Date:** November 12, 2025  
**Server:** http://127.0.0.1:8000  
**Status:** ✅ Server Running  
**Database:** SQLite (Local)

---

## 🔐 Test Users Available

| Role | Username | Email | Description |
|------|----------|-------|-------------|
| SUPERUSER | admin | admin@agnivridhiindia.com | Full system access |
| OWNER | owner | akash@agnivridhiindia.com | Owner dashboard |
| MANAGER | manager1 | manager1@agnivridhiindia.com | Manager dashboard |
| MANAGER | manager2 | manager2@agnivridhiindia.com | Secondary manager |
| MANAGER | manager3 | manager3@agnivridhiindia.com | Third manager |
| SALES | sales1 | sales1@agnivridhiindia.com | Sales employee #1 |
| SALES | sales2-9 | sales2-9@agnivridhiindia.com | More sales users |
| CLIENT | client1 | client1@agnivridhiindia.com | Test client |

**Note:** Password verify karein. Typically `Admin@123`, `Manager@123`, `Sales@123`, `Client@123` ya pehle set kiya hua password.

---

## 📝 Testing Checklist

### 1. ✅ Authentication & Login
**URL:** http://127.0.0.1:8000/login/

- [ ] Login page loads properly
- [ ] Login with admin credentials
- [ ] Login with manager credentials
- [ ] Login with sales credentials
- [ ] Login with client credentials
- [ ] Invalid credentials show error
- [ ] Logout works properly
- [ ] Redirect after login works

**Expected:** Each role redirects to their respective dashboard

---

### 2. 🎯 ADMIN Dashboard
**URL:** http://127.0.0.1:8000/admin-dashboard/  
**Login as:** `admin`

#### Dashboard Overview
- [ ] Dashboard loads without errors
- [ ] All statistics cards visible:
  - [ ] Total Clients
  - [ ] Total Applications
  - [ ] Total Bookings
  - [ ] Total Payments
- [ ] Charts/graphs display properly
- [ ] Recent activity feed shows

#### Navigation Menu
- [ ] All menu items visible
- [ ] Dashboard link works
- [ ] Clients link works
- [ ] Applications link works
- [ ] Bookings link works
- [ ] Schemes link works
- [ ] Payments link works
- [ ] Reports link works

#### Admin Features
- [ ] Can view all clients
- [ ] Can create new client
- [ ] Can edit any client
- [ ] Can delete client
- [ ] Can approve/reject clients
- [ ] Can assign sales to clients
- [ ] Can view all applications
- [ ] Can manage schemes
- [ ] Can view all payments

---

### 3. 👔 MANAGER Dashboard
**URL:** http://127.0.0.1:8000/manager-dashboard/  
**Login as:** `manager1`

#### Dashboard Overview
- [ ] Manager dashboard loads
- [ ] Team statistics visible:
  - [ ] Assigned clients
  - [ ] Pending approvals
  - [ ] Team performance
- [ ] Assigned sales team list
- [ ] Pending tasks visible

#### Manager Features
- [ ] Can view assigned clients
- [ ] Can approve client registrations
- [ ] Can reject clients with reason
- [ ] Can assign clients to sales
- [ ] Can reassign applications
- [ ] Can view team performance
- [ ] Can view all bookings in team
- [ ] Can access reports

---

### 4. 💼 SALES Dashboard
**URL:** http://127.0.0.1:8000/sales/dashboard/  
**Login as:** `sales1`

#### Dashboard Overview
- [ ] Sales dashboard loads
- [ ] Personal statistics:
  - [ ] My clients count
  - [ ] My applications count
  - [ ] My bookings count
  - [ ] Commission earned
- [ ] Task list visible
- [ ] Follow-up reminders

#### Sales Features
- [ ] Can create new client
- [ ] Can view assigned clients only
- [ ] Can create booking for client
- [ ] Can create application
- [ ] Can upload documents
- [ ] Can add payment records
- [ ] Can update application status
- [ ] Can add notes to client
- [ ] Cannot see other sales' clients
- [ ] Cannot delete clients

---

### 5. 👤 CLIENT Dashboard
**URL:** http://127.0.0.1:8000/clients/dashboard/  
**Login as:** `client1`

#### Dashboard Overview
- [ ] Client dashboard loads
- [ ] Client profile visible
- [ ] Application status cards
- [ ] Payment summary
- [ ] Document list

#### Client Features
- [ ] Can view own applications
- [ ] Can track application status
- [ ] Can view payment history
- [ ] Can download documents
- [ ] Can upload required documents
- [ ] Can view scheme details
- [ ] Can update profile (limited)
- [ ] Cannot see other clients' data
- [ ] Cannot create applications (sales creates)

---

### 6. 📊 SCHEMES Module
**URL:** http://127.0.0.1:8000/schemes/

#### Schemes List
- [ ] All schemes display in grid/list
- [ ] Scheme count: **5 schemes**
- [ ] Each scheme shows:
  - [ ] Name
  - [ ] Description
  - [ ] Eligibility
  - [ ] Benefits
  - [ ] Funding amount

#### Expected Schemes
1. Prime Minister Employment Generation Programme (PMEGP)
2. Others (check in database)

#### Scheme Features (Admin/Manager)
- [ ] Can create new scheme
- [ ] Can edit scheme details
- [ ] Can delete scheme
- [ ] Can view scheme applications
- [ ] Can filter schemes by category

#### Scheme Features (Sales/Client)
- [ ] Can view all schemes
- [ ] Can search schemes
- [ ] Can filter by eligibility
- [ ] Can view full details
- [ ] Cannot edit/delete

---

### 7. 👥 CLIENTS Module
**URL:** http://127.0.0.1:8000/clients/

#### Clients List
- [ ] All clients display (based on role)
- [ ] Client count visible
- [ ] Search functionality works
- [ ] Filter by status works
- [ ] Filter by sales person works
- [ ] Filter by sector works

#### Client Details
- [ ] Click on client opens detail page
- [ ] Company information visible:
  - [ ] Company name: **Test Co Pvt Ltd**
  - [ ] Business type
  - [ ] Sector
  - [ ] Annual turnover
  - [ ] Funding required
- [ ] Contact information visible
- [ ] Address details shown
- [ ] Assigned sales/manager shown
- [ ] Status badge visible

#### Client Creation (Sales/Admin)
- [ ] Create client form loads
- [ ] All fields present:
  - [ ] Company information section
  - [ ] Contact details section
  - [ ] Address section
  - [ ] Financial information section
- [ ] Form validation works
- [ ] Required fields enforce input
- [ ] Email format validation
- [ ] Phone number validation
- [ ] GST/PAN validation (if applicable)
- [ ] Submit creates client
- [ ] Redirect to client detail page
- [ ] Success message shows

#### Client Edit
- [ ] Edit button visible (based on role)
- [ ] Form pre-fills with data
- [ ] Can update information
- [ ] Save updates client
- [ ] Cannot change client ID
- [ ] Validation still applies

---

### 8. 📅 BOOKINGS Module
**URL:** http://127.0.0.1:8000/bookings/

#### Bookings List
- [ ] All bookings display (role-based)
- [ ] Booking count: **3 bookings**
- [ ] Each booking shows:
  - [ ] Booking ID: **BKG-YYYYMMDD-XXXX**
  - [ ] Client name
  - [ ] Service name
  - [ ] Status badge
  - [ ] Created date

#### Booking Details
- [ ] Click opens detail page
- [ ] Client information shown
- [ ] Service/scheme details
- [ ] Booking status
- [ ] Payment status
- [ ] Documents list
- [ ] Activity timeline

#### Create Booking (Sales/Admin)
- [ ] Create booking form loads
- [ ] Select client dropdown
- [ ] Select service/scheme dropdown
- [ ] Service type options visible
- [ ] Amount fields
- [ ] Notes field
- [ ] Submit creates booking
- [ ] Auto-generates booking ID
- [ ] Redirects to booking detail
- [ ] Success notification

#### Booking Status Update
- [ ] Can change status
- [ ] Status options:
  - [ ] NEW
  - [ ] IN_PROGRESS
  - [ ] COMPLETED
  - [ ] CANCELLED
- [ ] Status change reflects immediately
- [ ] Activity log updated

---

### 9. 📄 APPLICATIONS Module
**URL:** http://127.0.0.1:8000/applications/

#### Applications List
- [ ] All applications display
- [ ] Application count: **6 applications**
- [ ] Each application shows:
  - [ ] Application ID: **APP-YYYYMMDD-XXXX**
  - [ ] Client name
  - [ ] Scheme name
  - [ ] Status badge
  - [ ] Submission date

#### Application Details
- [ ] Opens detail page
- [ ] Client information
- [ ] Scheme details
- [ ] Application status
- [ ] Assigned person
- [ ] Documents attached
- [ ] Payment information
- [ ] Timeline/history

#### Create Application (Sales/Admin)
- [ ] Form loads
- [ ] Select client
- [ ] Select scheme
- [ ] Fill application details
- [ ] Upload documents (optional)
- [ ] Submit creates application
- [ ] Auto-generates application ID
- [ ] Email notification sent (if configured)

#### Application Status Flow
- [ ] Can update status:
  - [ ] DRAFT
  - [ ] SUBMITTED
  - [ ] UNDER_REVIEW
  - [ ] APPROVED
  - [ ] REJECTED
  - [ ] DOCUMENTS_REQUIRED
- [ ] Status change triggers notifications
- [ ] Comments can be added
- [ ] History tracked

#### Application Assignment
- [ ] Can assign to manager
- [ ] Can reassign
- [ ] Assigned user receives notification
- [ ] Shows in assigned user's dashboard

---

### 10. 💰 PAYMENTS Module
**URL:** http://127.0.0.1:8000/payments/

#### Payments List
- [ ] All payments display
- [ ] Payment count: **3 payments**
- [ ] Each payment shows:
  - [ ] Payment ID
  - [ ] Amount
  - [ ] Client name
  - [ ] Payment method
  - [ ] Status
  - [ ] Date

#### Payment Details
- [ ] Opens detail page
- [ ] Transaction details
- [ ] Client information
- [ ] Related booking/application
- [ ] Payment proof (if uploaded)
- [ ] Receipt available for download

#### Record Payment (Sales/Admin)
- [ ] Form loads
- [ ] Select booking/application
- [ ] Enter amount
- [ ] Select payment method:
  - [ ] CASH
  - [ ] CHEQUE
  - [ ] ONLINE_TRANSFER
  - [ ] CARD
  - [ ] UPI
- [ ] Upload payment proof
- [ ] Add notes
- [ ] Submit records payment
- [ ] Updates booking payment status

#### Payment Status
- [ ] PENDING
- [ ] RECEIVED
- [ ] VERIFIED
- [ ] FAILED
- [ ] REFUNDED

---

### 11. 📁 DOCUMENTS Module

#### Document Upload
- [ ] Can upload from application
- [ ] Can upload from booking
- [ ] Supported formats: PDF, JPG, PNG
- [ ] File size validation
- [ ] Preview available

#### Document Management
- [ ] List all documents
- [ ] Filter by client
- [ ] Filter by type
- [ ] Download document
- [ ] Delete document (admin only)
- [ ] View document history

---

### 12. 🔔 NOTIFICATIONS

#### Notification Center
- [ ] Bell icon shows unread count
- [ ] Click opens notification dropdown
- [ ] Recent notifications listed
- [ ] Mark as read works
- [ ] Mark all as read works
- [ ] Click notification navigates to related item

#### Notification Types
- [ ] New client registration (Manager)
- [ ] Application status change (Client)
- [ ] Payment received (Sales)
- [ ] Document uploaded (Assigned user)
- [ ] Assignment notification
- [ ] Approval/rejection notification

---

### 13. 🔍 SEARCH & FILTERS

#### Global Search
- [ ] Search bar in navbar
- [ ] Search clients by name
- [ ] Search by client ID
- [ ] Search applications
- [ ] Search bookings
- [ ] Search results paginated

#### Filters
- [ ] Date range filter works
- [ ] Status filter works
- [ ] Multi-select filters
- [ ] Clear filters button
- [ ] Filter combinations work
- [ ] Filtered results accurate

---

### 14. 📊 REPORTS & ANALYTICS

#### Admin Reports
- [ ] Sales performance report
- [ ] Revenue report
- [ ] Client acquisition report
- [ ] Application status report
- [ ] Payment collection report
- [ ] Export to PDF
- [ ] Export to Excel

#### Manager Reports
- [ ] Team performance
- [ ] Assigned clients report
- [ ] Pending approvals report

#### Sales Reports
- [ ] Personal performance
- [ ] Commission report
- [ ] Client list
- [ ] Bookings report

---

### 15. ⚙️ SETTINGS & PROFILE

#### User Profile
- [ ] View profile page
- [ ] Edit personal information
- [ ] Change password
- [ ] Update phone number
- [ ] Upload profile picture

#### System Settings (Admin Only)
- [ ] Site settings page
- [ ] Session timeout configuration
- [ ] Email configuration
- [ ] WhatsApp configuration
- [ ] Security settings

---

### 16. 🔒 PERMISSIONS & ACCESS CONTROL

#### Admin Permissions
- [ ] Access all modules
- [ ] Create/Edit/Delete all records
- [ ] Approve clients
- [ ] Manage users
- [ ] View all reports
- [ ] Access system settings

#### Manager Permissions
- [ ] View assigned team data
- [ ] Approve/reject clients
- [ ] Assign/reassign applications
- [ ] View team reports
- [ ] Cannot delete records
- [ ] Cannot access system settings

#### Sales Permissions
- [ ] Create clients
- [ ] View assigned clients only
- [ ] Create bookings/applications
- [ ] Upload documents
- [ ] Record payments
- [ ] Cannot approve clients
- [ ] Cannot access other sales' data
- [ ] Cannot delete records

#### Client Permissions
- [ ] View own data only
- [ ] View own applications
- [ ] View payment history
- [ ] Upload documents
- [ ] Cannot create applications
- [ ] Cannot view other clients
- [ ] Read-only access mostly

---

### 17. 📱 RESPONSIVE DESIGN

#### Desktop View (> 1024px)
- [ ] Full sidebar visible
- [ ] All cards in grid layout
- [ ] Tables show all columns
- [ ] Charts render properly

#### Tablet View (768px - 1024px)
- [ ] Sidebar collapsible
- [ ] Cards adjust to 2 columns
- [ ] Table columns adjust
- [ ] Touch-friendly buttons

#### Mobile View (< 768px)
- [ ] Hamburger menu
- [ ] Cards stack vertically
- [ ] Tables scroll horizontally
- [ ] Form fields stack
- [ ] Bottom navigation (if implemented)

---

### 18. 🚨 ERROR HANDLING

#### Form Validation
- [ ] Required field errors show
- [ ] Email validation messages
- [ ] Phone validation messages
- [ ] File size error messages
- [ ] Format validation errors

#### System Errors
- [ ] 404 page loads for invalid URL
- [ ] 403 page for unauthorized access
- [ ] 500 page for server errors (test by causing error)
- [ ] User-friendly error messages
- [ ] Error doesn't expose sensitive data

#### Network Errors
- [ ] Loading indicators show
- [ ] Timeout messages
- [ ] Retry options
- [ ] Graceful degradation

---

### 19. ⚡ PERFORMANCE

#### Page Load Times
- [ ] Dashboard loads < 2 seconds
- [ ] List pages load < 3 seconds
- [ ] Forms load instantly
- [ ] Search results < 1 second

#### Data Loading
- [ ] Pagination works smoothly
- [ ] Lazy loading for images
- [ ] API calls optimized
- [ ] No unnecessary requests

#### Caching
- [ ] Static files cached
- [ ] User session persists
- [ ] Data refreshes appropriately

---

### 20. 🔐 SECURITY TESTS

#### Authentication
- [ ] Cannot access dashboard without login
- [ ] Session expires after timeout
- [ ] Logout clears session
- [ ] Multiple concurrent logins handled

#### Authorization
- [ ] Sales cannot access admin functions
- [ ] Client cannot access sales functions
- [ ] Direct URL access blocked for unauthorized
- [ ] API endpoints protected

#### Data Security
- [ ] Passwords not visible in HTML
- [ ] No sensitive data in console
- [ ] CSRF protection active
- [ ] SQL injection prevented (try ' OR '1'='1)
- [ ] XSS prevented (try <script>alert('XSS')</script>)

---

## 📈 Test Summary Template

```
==============================================
  MANUAL TESTING SUMMARY
==============================================
Date: _______________
Tester: ______________
Environment: Local (http://127.0.0.1:8000)

RESULTS:
✅ Total Tests Passed: _____ / _____
⚠️  Tests with Issues: _____
❌ Tests Failed: _____

CRITICAL ISSUES:
1. _______________________
2. _______________________

MINOR ISSUES:
1. _______________________
2. _______________________

SUGGESTIONS:
1. _______________________
2. _______________________

Overall Status: ✅ PASS / ⚠️ PASS WITH ISSUES / ❌ FAIL

Tester Signature: ______________
==============================================
```

---

## 🎯 Priority Testing Order

### 🔥 HIGH PRIORITY (Must Test First)
1. Login/Authentication
2. Admin Dashboard
3. Client Creation
4. Booking Creation
5. Application Creation
6. Payment Recording

### ⚡ MEDIUM PRIORITY
7. Manager Dashboard
8. Sales Dashboard
9. Client Dashboard
10. Schemes Management
11. Notifications
12. Search & Filters

### ✨ LOW PRIORITY (Nice to Have)
13. Reports
14. Settings
15. Responsive Design
16. Performance Tests
17. Advanced Filters

---

## 🐛 Bug Reporting Template

```
BUG REPORT #___
================
Title: [Short description]
Module: [Dashboards/Clients/Applications/etc.]
Priority: [Critical/High/Medium/Low]
User Role: [Admin/Manager/Sales/Client]

STEPS TO REPRODUCE:
1. 
2. 
3. 

EXPECTED RESULT:


ACTUAL RESULT:


SCREENSHOTS:
[Attach if available]

BROWSER: [Chrome/Firefox/Edge]
DATE: _______________
REPORTED BY: _______________
```

---

## ✅ Testing Completion Checklist

- [ ] All authentication tests completed
- [ ] All dashboard tests completed
- [ ] All module tests completed
- [ ] All permission tests completed
- [ ] Responsive design verified
- [ ] Error handling verified
- [ ] Performance acceptable
- [ ] Security tests passed
- [ ] Test summary documented
- [ ] Critical bugs logged
- [ ] Ready for deployment? (Y/N)

---

## 🚀 Next Steps After Testing

1. **Fix Critical Bugs** - Sabse pehle critical issues resolve karo
2. **Optimize Performance** - Slow pages ko improve karo
3. **Enhance UI/UX** - User experience improvements
4. **Add Missing Features** - Pending features implement karo
5. **Documentation** - User guide complete karo
6. **Deployment Prep** - Production deployment ki taiyaari

---

**Happy Testing! 🎉**

*Is checklist ko print karke step by step test karo. Har test ko mark karte jao. Koi issue mile toh turant note kar lo.*
