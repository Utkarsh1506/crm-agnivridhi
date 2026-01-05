# Employee Identity System - Architecture & Flow Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AGNIVRIDHI CRM SYSTEM                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         EMPLOYEE IDENTITY & VERIFICATION MODULE          │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │                                                           │  │
│  │  ┌─────────────┐    ┌────────────┐    ┌─────────────┐   │  │
│  │  │   Models    │    │   Views    │    │   Admin UI  │   │  │
│  │  │             │    │            │    │             │   │  │
│  │  │  • Employee │────│• Admin     │───→│ • Create    │   │  │
│  │  │  • IDSeq    │    │• Public    │    │ • Manage    │   │  │
│  │  │  • Logs     │    │• Logs      │    │ • Download  │   │  │
│  │  └─────────────┘    └────────────┘    └─────────────┘   │  │
│  │         │                 │                                 │  │
│  │         ▼                 ▼                                 │  │
│  │  ┌──────────────────────────────────┐                      │  │
│  │  │    Automatic Systems             │                      │  │
│  │  │                                  │                      │  │
│  │  │  1. Signals (pre_save/post_save) │                      │  │
│  │  │     ↓ Generate Employee ID       │                      │  │
│  │  │     ↓ Generate Token             │                      │  │
│  │  │     ↓ Generate QR Code           │                      │  │
│  │  │                                  │                      │  │
│  │  │  2. Rate Limiting (Cache)        │                      │  │
│  │  │     ↓ 10 requests/IP/hour        │                      │  │
│  │  │     ↓ Returns 429 if exceeded    │                      │  │
│  │  │                                  │                      │  │
│  │  │  3. Audit Logging                │                      │  │
│  │  │     ↓ Records verification       │                      │  │
│  │  │     ↓ IP + User Agent            │                      │  │
│  │  └──────────────────────────────────┘                      │  │
│  │                                                             │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow - Employee Creation

```
Admin User
    │
    ▼
[Create Employee Form]
    │
    ├─ Full Name
    ├─ Designation
    ├─ Department
    ├─ Date of Joining
    ├─ Photo Upload
    └─ Submit
    
    ▼
[Employee.save()]
    
    ▼
[pre_save Signal]
    ├─ EmployeeIDGenerator.generate_employee_id()
    │  └─ Atomic transaction
    │     ├─ Read last sequence
    │     ├─ Increment
    │     └─ Return AGN-EMP-001
    │
    ├─ EmployeeIDGenerator.generate_verification_token()
    │  └─ Generate UUID
    │
    └─ Save to Database
    
    ▼
[Save to DB]
    ├─ employee_id: AGN-EMP-001
    ├─ verification_token: UUID
    ├─ status: ACTIVE
    └─ created_at: NOW
    
    ▼
[post_save Signal]
    │
    ├─ QRCodeGenerator.generate_qr_code()
    │  ├─ Input: https://agnivridhi.com/employee/verify/AGN-EMP-001/
    │  ├─ Create PNG image
    │  └─ Return ContentFile
    │
    └─ Save QR to Media
       └─ /media/employees/qrcodes/2024/01/AGN-EMP-001_qr.png
    
    ▼
[Employee Created Successfully]
    └─ Ready for PDF download
```

## Data Flow - Public Verification

```
User Scans QR Code
    │
    ├─ QR Content: https://agnivridhi.com/employee/verify/AGN-EMP-001/
    │
    ▼
[Browser Opens URL]
    │
    ├─ No login required
    ├─ GET /employees/verify/AGN-EMP-001/
    │
    ▼
[Rate Limiting Check]
    │
    ├─ Get Client IP
    ├─ Check Cache: "employee_verify_192.168.1.1"
    │  ├─ If count >= 10: Return 429
    │  └─ Else: Increment count
    │
    ▼
[Fetch Employee]
    │
    ├─ Query: SELECT * FROM employee WHERE employee_id = "AGN-EMP-001"
    │  ├─ If not found: Return 404
    │  └─ If found: Continue
    │
    ▼
[Log Verification Attempt]
    │
    ├─ Create EmployeeVerificationLog
    │  ├─ employee: AGN-EMP-001
    │  ├─ ip_address: 192.168.1.1
    │  ├─ user_agent: Mozilla/5.0...
    │  └─ timestamp: NOW
    │
    ▼
[Render Verification Page]
    │
    ├─ If status == ACTIVE
    │  └─ Show green badge: "✓ ACTIVE EMPLOYEE"
    │
    ├─ If status == INACTIVE
    │  └─ Show red warning: "⚠️ INACTIVE EMPLOYEE"
    │     └─ "This employee is no longer associated with Agnivridhi."
    │
    ├─ Display Employee Info
    │  ├─ Photo
    │  ├─ Name
    │  ├─ Designation
    │  ├─ Department
    │  ├─ Employee ID
    │  └─ Status
    │
    ▼
[Return 200 HTML Page]
```

## Database Schema Diagram

```
┌─────────────────────────────────┐
│          Employee               │
├─────────────────────────────────┤
│ PK: id (BigAutoField)           │
│ FK: created_by (User)           │
│                                 │
│ Fields:                         │
│ • uuid (Unique)                 │
│ • employee_id (Unique, Index)   │
│ • full_name (Index)             │
│ • designation                   │
│ • department (Index)            │
│ • employee_photo (Image)        │
│ • status (Index) [ACTIVE/...]   │
│ • date_of_joining               │
│ • date_of_exit (nullable)       │
│ • qr_code (Image, auto-gen)     │
│ • verification_token (Unique)   │
│ • created_at (Index)            │
│ • updated_at                    │
│                                 │
│ Methods:                        │
│ • is_active_employee()          │
│ • deactivate()                  │
│ • reactivate()                  │
│ • get_verification_url()        │
│ • get_qr_content()              │
└─────────────────────────────────┘
           │
           │ 1:Many
           │
           ▼
┌──────────────────────────────────┐
│  EmployeeVerificationLog         │
├──────────────────────────────────┤
│ PK: id (BigAutoField)            │
│ FK: employee (Employee) Index    │
│                                  │
│ Fields:                          │
│ • timestamp (Index)              │
│ • ip_address                     │
│ • user_agent                     │
│                                  │
│ Index: (employee, timestamp)     │
└──────────────────────────────────┘


┌────────────────────────────────────┐
│   EmployeeIDSequence (Singleton)   │
├────────────────────────────────────┤
│ PK: id (BigAutoField)              │
│                                    │
│ Fields:                            │
│ • last_sequence_number = 0         │
│ • prefix = "AGN-EMP-"              │
│ • updated_at                       │
│                                    │
│ Methods:                           │
│ • get_next_employee_id()           │
│   Returns: "AGN-EMP-001" format    │
└────────────────────────────────────┘
```

## URL Routing Map

```
/employees/
│
├── [Admin Routes - Login Required]
│   │
│   ├── list/
│   │   └── GET → employee_list_view()
│   │       Shows all employees with search/filter
│   │
│   ├── create/
│   │   ├── GET → employee_create_view()
│   │   │   Shows create form
│   │   └── POST → employee_create_view()
│   │       Saves new employee
│   │
│   ├── <id>/
│   │   └── GET → employee_detail_view()
│   │       Shows employee details + options
│   │
│   ├── <id>/status-toggle/
│   │   └── POST → employee_status_toggle_view()
│   │       Toggles Active/Inactive
│   │
│   ├── <id>/download-id-card/
│   │   └── GET → employee_download_id_card_view()
│   │       Returns PDF file
│   │
│   └── <id>/verification-logs/
│       └── GET → employee_verification_logs_view()
│           Shows audit trail
│
└── [Public Routes - No Login]
    │
    └── verify/<employee_id>/
        └── GET → employee_verify_public_view()
            Shows verification page (rate limited)
```

## PDF ID Card Layout

```
Front Side:                          Back Side:
┌─────────────────────────┐         ┌─────────────────────────┐
│   AGNIVRIDHI INDIA      │         │                         │
├─────────────────────────┤         │                         │
│  ┌──────────┐ ┌────────┐│         │      ┌──────────┐       │
│  │          │ │ Name   ││         │      │          │       │
│  │  PHOTO   │ │        ││         │      │   QR     │       │
│  │ 38×38mm  │ │ John   ││         │      │  CODE    │       │
│  │          │ │ Doe    ││         │      │ 35×35mm  │       │
│  │ 150dpi   │ ├────────┤│         │      │          │       │
│  │          │ │Desig:  ││         │      └──────────┘       │
│  │          │ │Manager ││         │                         │
│  │          │ ├────────┤│         ├─────────────────────────┤
│  │          │ │Dept:   ││         │   SCAN TO VERIFY        │
│  │          │ │Sales   ││         │                         │
│  │          │ ├────────┤│         │  Agnivridhi India       │
│  │          │ │ID:     ││         │  Employee Verification  │
│  │          │ │AGN-    ││         │       System            │
│  │          │ │EMP-001 ││         │                         │
│  └──────────┘ └────────┘│         │                         │
└─────────────────────────┘         └─────────────────────────┘

Credit Card Size: 85.6mm × 53.98mm
```

## Access Control Flow

```
Request to Admin View
    │
    ▼
[Authentication Decorator]
    ├─ Is user logged in?
    │  ├─ NO → Redirect to login
    │  └─ YES → Continue
    │
    ▼
[Role-Based Decorator]
    │
    ├─ Is user.role in allowed_roles?
    │  ├─ Allowed: SUPERUSER, OWNER, ADMIN
    │  │
    ├─ User role check:
    │  ├─ SUPERUSER → ✓ ALLOW (bypass all)
    │  ├─ OWNER → ✓ ALLOW
    │  ├─ ADMIN → ✓ ALLOW
    │  ├─ MANAGER → ✗ DENY (403)
    │  ├─ SALES → ✗ DENY (403)
    │  └─ CLIENT → ✗ DENY (403)
    │
    ▼
[Execute View]
    │
    ├─ If allowed → Run view logic
    └─ If denied → Return 403 forbidden


Public Verification View (No Auth Required)
    │
    ├─ No decorator
    │ 
    ├─ Anyone can access
    │
    ├─ But rate-limited:
    │  └─ 10 requests per IP per hour
    │
    ▼
[Return 200 or 429]
```

## File Storage Structure

```
media/
│
├── employees/
│   │
│   ├── photos/              # Employee photos
│   │   ├── 2024/
│   │   │   ├── 01/
│   │   │   │   ├── agn-emp-001-photo.jpg
│   │   │   │   ├── agn-emp-002-photo.png
│   │   │   │   └── ...
│   │   │   ├── 02/
│   │   │   │   └── ...
│   │   │   └── ...
│   │   └── ...
│   │
│   └── qrcodes/             # Generated QR codes
│       ├── 2024/
│       │   ├── 01/
│       │   │   ├── AGN-EMP-001_qr.png
│       │   │   ├── AGN-EMP-002_qr.png
│       │   │   └── ...
│       │   ├── 02/
│       │   │   └── ...
│       │   └── ...
│       └── ...
│
└── [Other modules...]
```

## Signal Flow

```
Django ORM
    │
    ├─ Employee.objects.create()
    │
    ▼
[pre_save Signal Dispatched]
    │
    ├─ @receiver(pre_save, sender=Employee)
    ├─ assign_employee_id_and_token()
    │
    ├─ if not instance.employee_id:
    │  ├─ Generate ID (AGN-EMP-001)
    │  ├─ Generate token (UUID)
    │  └─ Set on instance
    │
    ▼
[Model Validation]
    │
    ▼
[Database INSERT]
    │
    ▼
[post_save Signal Dispatched]
    │
    ├─ @receiver(post_save, sender=Employee)
    ├─ generate_employee_qr_code()
    │
    ├─ if created:
    │  ├─ Generate QR code
    │  ├─ Save to media/
    │  └─ Update instance.qr_code
    │
    ▼
[Return to Caller]
    │
    └─ Employee object with all auto-generated fields
```

## State Machine - Employee Status

```
┌─────────────┐
│   ACTIVE    │◄─────────┐
└──────┬──────┘          │
       │                 │
       │ deactivate()    │
       │ (Admin action)  │
       │                 │
       ▼                 │
┌─────────────┐          │
│  INACTIVE   │──────────┘
└─────────────┘
   reactivate()
   (Admin action)

On Deactivate:
  • status = INACTIVE
  • date_of_exit = today
  • Public page shows warning
  • Audit log recorded

On Reactivate:
  • status = ACTIVE
  • date_of_exit = None
  • Public page shows active
  • Audit log recorded
```

## Rate Limiting Mechanism

```
Request comes in
    │
    ▼
[Get Client IP]
    ├─ Check X-Forwarded-For (proxy)
    ├─ Check X-Real-IP (proxy)
    └─ Fall back to REMOTE_ADDR
    
    ▼
[Check Cache]
    │
    ├─ Cache key: "employee_verify_192.168.1.1"
    │
    ├─ Get current count
    │  ├─ If count >= 10 → BLOCKED (429)
    │  └─ If count < 10 → ALLOWED
    │
    ▼
[Increment Count]
    │
    ├─ Set cache[key] = count + 1
    ├─ Timeout: 3600 seconds (1 hour)
    │
    ▼
[Allow Request]
    │
    └─ Proceed to verification page
```

## Scalability Progression

```
Current State (1-100 employees)
    │
    ├─ Single Django instance
    ├─ File-based storage
    ├─ Local cache (in-memory)
    └─ Single database connection

    ▼

Growth Phase 1 (100-500 employees)
    │
    ├─ Add connection pooling
    ├─ Implement Redis cache
    ├─ Move photos to S3
    └─ Enable database query caching

    ▼

Growth Phase 2 (500-1000+ employees)
    │
    ├─ Multiple Django instances
    ├─ Dedicated Redis instance
    ├─ All files on S3
    ├─ Database read replicas
    └─ CDN for static/media

    ▼

Enterprise Scale (1000+ employees)
    │
    ├─ Load balancer
    ├─ Micro services
    ├─ Async job queue (Celery)
    ├─ Distributed cache
    └─ Database sharding/partitioning
```

---

This diagram collection shows the complete system architecture, data flows, and scalability path for the Employee Identity & Verification System.
