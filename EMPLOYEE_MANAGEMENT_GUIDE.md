# Employee Management in Agnivridhi CRM

## Overview
The Employee System is fully integrated into the Agnivridhi CRM. Both Owner and Admin roles can view and manage all employees with automatic ID and barcode generation.

## Access Points

### 1. **Admin Dashboard** (Primary Management Interface)
**URL:** `/admin/employees/employee/`

- **Access Required:** Owner or Admin role
- **Features:**
  - List all 17 employees with their details
  - View employee ID, name, designation, department, status
  - See generated barcodes for each employee
  - Search by name, employee ID, designation, or department
  - Filter by status (Active/Inactive) and department
  - Edit employee details
  - Deactivate/Activate employees in bulk
  - Export employee data

### 2. **Employee List Page** (CRM Frontend)
**URL:** `/employees/` or Dashboard → Employees menu

- **Access Required:** Owner or Admin role
- **Features:**
  - Clean, organized list view
  - Search and filter employees
  - View employee details with barcode
  - Quick actions (Edit, View, Deactivate)
  - Pagination (20 employees per page)
  - Total employee count

## Features Available to Owner & Admin

### Create New Employee
When a new employee is created:
✅ Employee ID auto-generated (0101-0999 format)
✅ Barcode auto-generated (Code128 format)
✅ Verification token auto-generated
✅ Employee photo uploaded
✅ Designation and department assigned
✅ Joining date recorded

### Employee Details You Can See
- **ID & Identification:** Employee ID, UUID, Full Name
- **Professional:** Designation, Department, Photo
- **Status:** Active/Inactive, Joining Date, Exit Date
- **System:** Barcode, Verification Token, Timestamps
- **Audit:** Created by user, Creation and update times

### Manage Employees
- **Edit:** Update designation, department, status, dates
- **Search:** By name, ID, designation, or department
- **Filter:** By status (Active/Inactive), department, date range
- **Bulk Actions:**
  - Deactivate multiple employees at once
  - Activate multiple inactive employees
- **Export:** Download employee list (with Django admin export feature)

## Viewing Barcodes

### In Admin Interface
1. Go to `/admin/employees/employee/`
2. You'll see barcode preview (thumbnail) in the list view
3. Click any employee to see full-size barcode
4. Barcode shows:
   - Code128 barcode image
   - Employee ID below barcode
   - Easy to scan with barcode scanner

### Employee Details Page
Open any employee record to:
- View full barcode image
- See all employee information
- Edit any field
- Update status
- View generated dates and timestamps

## How Barcode Works

### Auto-Generation
When you create an employee:
1. Employee ID is auto-assigned (e.g., 0101)
2. Barcode is immediately generated
3. Barcode is saved to employee record
4. Barcode is available instantly

### Barcode Content
- **Encodes:** Employee ID (e.g., 0101)
- **Format:** Code128 (standard barcode format)
- **Scannable:** Yes, with any standard barcode scanner
- **Includes:** ID number displayed below barcode

### Using the Barcode
- **Attendance:** Scan barcode to mark attendance
- **Access Control:** Use for entry/exit management
- **Document Reference:** Print on ID cards
- **Quick Lookup:** Scan to pull employee details

## Current Employees (All with Auto-Generated IDs & Barcodes)

| ID | Name | Designation | Department |
|----|------|-------------|-----------|
| 0101 | Rahul Kumar Singh | CEO & Founder | Management |
| 0102 | Urvashi Nandan Srivastava | Data Analyst | Finance |
| 0103 | Akash Tyagi | Branch Manager | Operations |
| 0104 | Harshit Tyagi | Manager | Management |
| 0105 | Ayush Tomer | Business Development Executive | Sales |
| 0106 | Himadri Sharma | Business Development Executive | Sales |
| 0107 | Bhoomika Sharma | Business Development Executive | Sales |
| 0108 | Sharik Khan | Business Development Executive | Sales |
| 0109 | Rajdeep Singh | Team Leader | Sales |
| 0110 | Aaryav Singh | Business Development Executive | Sales |
| 0111 | Mohd Rihan | Business Development Executive | Sales |
| 0112 | Utkarsh Choudhary | Web Developer | Engineering |
| 0113 | Rahul Kumar Pant | Business Development Executive | Sales |
| 0114 | Vaibhav Garg | Business Development Executive | Sales |
| 0115 | Babita Goswami | Business Development Executive | Sales |
| 0116 | Sanklp | Business Development Executive | Sales |
| 0117 | Vinay Kannaujiya | Business Development Executive | Sales |

## Access Control

### Owner Role
✅ View all employees
✅ Create new employees
✅ Edit all employee details
✅ Deactivate/Activate employees
✅ Export employee data
✅ View all audit information
✅ Bulk manage employees

### Admin Role
✅ View all employees
✅ Create new employees
✅ Edit all employee details
✅ Deactivate/Activate employees
✅ Export employee data
✅ View all audit information
✅ Bulk manage employees

### Other Roles
❌ Cannot access employee management

## Steps to View Employees

### Method 1: Admin Interface (Quickest)
1. Log in to Agnivridhi CRM
2. Go to Admin dashboard
3. Click "Employees" section
4. You'll see all 17 employees with barcodes
5. Click any employee to see details and full-size barcode

### Method 2: CRM Frontend
1. Log in as Owner or Admin
2. Navigate to Employees from dashboard menu
3. View list with search and filter options
4. Click on employee name to view details

### Method 3: Django Admin
1. Go to `/admin/`
2. Select "Employees" under "Employees" app
3. See full list with all details
4. Click to edit or view individual records

## Troubleshooting

### Barcode Not Showing
**Issue:** Barcode field appears empty
**Solution:**
- Barcode generates automatically after employee creation
- Refresh the page
- If still empty, go to admin and click Save to regenerate

### Employee ID Not Generated
**Issue:** Employee ID field is empty
**Solution:**
- Employee ID auto-generates on save
- Make sure all required fields are filled
- Employee ID should appear after saving

### Search Not Working
**Issue:** Cannot find employee by name/ID
**Solution:**
- Make sure search terms match exactly
- Try partial name search
- Check spelling
- Use filter dropdown for department or status

## Permission Notes
- Only logged-in Owner/Admin can see employees
- Employee data is protected and not visible to other roles
- All actions are logged (who created/edited, when)
- Inactive employees are still visible but marked as inactive

## API Access (If Enabled)

If API is enabled, employees can be accessed via:
- **Endpoint:** `/api/employees/`
- **Method:** GET
- **Authentication:** Token required
- **Permission:** Owner or Admin role required

## Next Steps

1. **Log in** as Owner or Admin
2. **Go to** `/admin/employees/employee/`
3. **View** all 17 employees with barcodes
4. **Search** or filter as needed
5. **Click** any employee to see full details
6. **Edit** designation, department, or status as needed
7. **Download** barcode for ID card printing

## Support

For questions about:
- Employee management: Contact Admin
- Barcode generation: It's automatic, no action needed
- Access permissions: Contact Owner

---

**Status:** ✅ Fully Deployed  
**Employees:** 17 with IDs 0101-0117  
**Barcodes:** Auto-generated for all  
**Roles:** Owner & Admin access enabled  
**Database:** PostgreSQL (production ready)
