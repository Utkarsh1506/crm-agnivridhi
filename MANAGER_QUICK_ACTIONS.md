# Manager Quick Actions Guide

## Manager Dashboard Updates - November 13, 2025

### What Was Added

Added **Quick Actions** section to the Manager Dashboard with:
- 🟢 **Create Client** - Directly create a new client
- 🔵 **View Clients** - Go to team clients list
- 🟣 **View Bookings** - Go to team bookings list
- 🟡 **View Applications** - Go to team applications list

Plus an info tip explaining the workflow.

### Workflow for Manager

#### To Create a Booking:
1. **Manager Dashboard** → Click **"View Clients"**
2. **Team Clients List** → Find and click on a client
3. **Client Detail Page** → Click **"Create Booking"** (in Quick Actions section)
4. **Booking Form** → Select service, add requirements, submit

#### To Create an Application:
1. **Manager Dashboard** → Click **"View Clients"**
2. **Team Clients List** → Find and click on a client
3. **Client Detail Page** → Click **"Create Application"** (in Quick Actions section)
4. **Application Form** → Fill details and submit

#### To Create a Client:
1. **Manager Dashboard** → Click **"Create Client"**
2. **Client Form** → Fill 4 fields (company name, contact person, email, phone)
3. Submit → Client auto-approved (no need for manager approval)

### Manager Dashboard URL
http://127.0.0.1:8000/accounts/manager-dashboard/

### Files Modified

1. **templates/dashboards/manager_dashboard.html**
   - Added Quick Actions card with 4 buttons
   - Added info tip explaining workflow
   - Location: After alerts, before Team Overview stats

### What Manager Can Do

✅ **Create** clients directly (auto-approved)
✅ **Create** bookings for team clients
✅ **Create** applications for team clients
✅ **Approve** client requests from sales team
✅ **Approve** payment requests from team
✅ **View** all team activities (bookings, applications, payments, documents)
✅ **Manage** team members

### Button Locations

| Action | Location | Button |
|--------|----------|--------|
| Create Client | Manager Dashboard OR Clients List | "Create New Client" / "Create Client" |
| Create Booking | Client Detail Page | "Create Booking" |
| Create Application | Client Detail Page | "Create Application" |
| View Clients | Manager Dashboard | "View Clients" |
| View Bookings | Manager Dashboard | "View Bookings" |
| View Applications | Manager Dashboard | "View Applications" |

---
**Note**: Booking and Application creation must be done from the client detail page because they require a specific client to be selected first.

**Test Now**: http://127.0.0.1:8000/accounts/manager-dashboard/
