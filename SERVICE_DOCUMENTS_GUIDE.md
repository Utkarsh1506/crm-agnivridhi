# Service-Based Document Collection System

## Overview

This system handles the complete onboarding flow for services, including:
1. **Profile Completion** - Client fills in business details
2. **Service Activation** - Booking transitions to document collection status
3. **Document Submission** - Client uploads required documents with reference numbers
4. **Auto-Activation** - Booking automatically becomes ACTIVE when all documents are submitted

## Flow Diagram

```
Client Dashboard
    ↓
Profile Incomplete? → Complete Profile (business_type, sector, etc.)
    ↓
Bookings in PENDING status → Changed to DOCUMENT_COLLECTION
    ↓
Service Card Shows "Awaiting Documents" → Click "Submit Documents"
    ↓
Document Collection Form (service-specific)
    ↓
Upload Documents with Reference Numbers
    ↓
All Mandatory Documents Submitted? → Status Automatically Changes to ACTIVE
    ↓
Service Card Shows "Active - In Progress"
```

## Setup Instructions

### 1. Run Database Migrations

After pulling the latest code, run:

```bash
python manage.py migrate bookings
```

### 2. Add Document Requirements to Services

In Django Admin (`/admin/`):

1. Go to **Bookings** → **Service Document Requirements**
2. Click **"Add Service Document Requirement"**
3. For each service, add required documents:
   - **Service**: Select the service (e.g., "Scheme Application Documentation")
   - **Document Type**: Choose from the dropdown (e.g., "GST Registration Certificate")
   - **Is Mandatory**: Check if this document is required
   - **Display Order**: Set the order documents appear in the form
   - **Description**: Explain why this document is needed

#### Quick Setup Script

Alternatively, run the setup script to auto-add common document requirements:

```bash
python manage.py shell < setup_service_documents.py
```

Or run interactively:

```bash
python manage.py shell
>>> exec(open('setup_service_documents.py').read())
```

### 3. Booking Status Options

New booking statuses added:

```python
PENDING              # Initial state after booking creation
PAID                 # Payment received (can transition to DOCUMENT_COLLECTION)
DOCUMENT_COLLECTION  # Awaiting document submission from client
ACTIVE               # All documents submitted, work in progress
COMPLETED            # Service completed
CANCELLED            # Booking cancelled
REFUNDED             # Refund issued
```

## Client-Side Features

### 1. Service Card Display

On the client dashboard, bookings show different states:

- **PENDING**: Shows profile completion prompt
- **PAID/DOCUMENT_COLLECTION**: Shows "Awaiting Documents" card with upload button
- **ACTIVE**: Shows progress bar and active service details
- **COMPLETED**: Shows completed badge

### 2. Document Submission Form

When client clicks "Submit Documents":

1. **Dynamic Form**: Shows only documents required for that service
2. **For Each Document**:
   - **Reference Number**: Client enters document number/ID (e.g., "GST/HR/12345")
   - **File Upload**: Client uploads PDF/DOCX/JPEG file
   - **Optional Notes**: Client can add notes about the document

3. **Form Validation**:
   - Mandatory documents must be uploaded
   - File size limits enforced
   - Supported formats: PDF, JPEG, PNG, DOC, DOCX

### 3. Auto-Activation

When all **mandatory** documents are uploaded:
- Booking status automatically changes to `ACTIVE`
- Client receives success message
- Service card updates to show "Active - In Progress"
- Team receives notification to begin work

## Backend Architecture

### Models

#### ServiceDocumentRequirement

Maps which documents are required for each service:

```python
class ServiceDocumentRequirement(models.Model):
    service              # ForeignKey to Service
    document_type        # CharField (COMPANY_REG, GST_CERT, PAN_CARD, etc.)
    is_mandatory         # Boolean (required field or optional)
    description          # TextField (why this document is needed)
    display_order        # IntegerField (order in form)
```

#### Booking (Updated)

Added new status choices and methods:

```python
# New Status Options
DOCUMENT_COLLECTION = 'DOCUMENT_COLLECTION'
ACTIVE = 'ACTIVE'

# New Methods
get_required_documents()           # Get all required documents for service
get_mandatory_documents()          # Get only mandatory documents
get_submitted_documents()          # Get documents already uploaded
get_pending_documents()            # Get mandatory documents not yet submitted
are_all_documents_complete()       # Check if all documents uploaded
can_activate()                     # Check if ready to activate
```

### Views

#### collect_documents (bookings/views.py)

```python
@login_required
def collect_documents(request, booking_id: int):
    """
    Client collects and uploads required documents for a booking.
    - Only accessible to clients for their own bookings
    - Booking must be in PAID or DOCUMENT_COLLECTION status
    - Shows dynamic form based on service requirements
    - Auto-activates booking when all documents submitted
    """
```

**URL**: `/bookings/<booking_id>/documents/`

**Methods**:
- `GET`: Display form with required documents
- `POST`: Process and save uploaded documents

**Redirects**:
- On success: Back to booking detail with success message
- If documents incomplete: Back to form with warning
- When complete: Auto-redirects to booking detail

### Forms

#### DocumentCollectionForm (bookings/forms.py)

Dynamically generates form fields based on service requirements:

- One field group per required document:
  - Reference number field
  - File upload field
  - Optional notes textarea

## Document Tracking

### Document Status Flow

```
DRAFT → GENERATED → SENT → DOWNLOADED
```

When client uploads via this system:
- **Status**: Set to `GENERATED`
- **Booking**: Linked to the booking
- **Client**: Linked to the client
- **Reference**: Stored in generation_data

### Document Fields

```python
document_type       # Type of document (COMPANY_REG, GST_CERT, etc.)
title               # "{Document Type} - {Reference Number}"
file                # Uploaded file
status              # GENERATED (when submitted)
booking             # Link to booking
client              # Link to client
file_format         # PDF, DOCX, etc.
generation_data     # Stores reference_number and notes
generated_by        # User (the client who uploaded)
```

## Admin Interface

### Viewing Document Requirements

1. Go to Django Admin → **Bookings** → **Service Document Requirements**
2. Filter by:
   - Service name
   - Is Mandatory (Yes/No)
3. Bulk actions: Edit multiple requirements at once

### Creating Requirements

Click **"Add Service Document Requirement"**:

```
Service:           [Dropdown] Select service
Document Type:     [Dropdown] COMPANY_REG, GST_CERT, PAN_CARD, etc.
Is Mandatory:      [Checkbox]
Display Order:     [Number] 1, 2, 3... (order in form)
Description:       [Text] Why this document is needed
```

### Editing Existing Bookings

In **Bookings** admin:
1. Click on a booking
2. See status: PENDING, DOCUMENT_COLLECTION, ACTIVE, etc.
3. View linked documents in the Documents tab
4. Manually change status if needed

## Common Use Cases

### Case 1: Client Completes Profile

**Action**: Client fills profile → clicks "Start Onboarding"

**System Does**:
1. Profile marked 100% complete
2. All PENDING bookings → DOCUMENT_COLLECTION
3. Client redirected to dashboard
4. Service cards now show "Awaiting Documents"

### Case 2: Client Uploads Documents

**Action**: Client clicks "Submit Documents" on service card

**System Does**:
1. Shows form with required documents (service-specific)
2. Client enters reference numbers and uploads files
3. Form validates all mandatory fields
4. Documents saved to system
5. System checks: Are all mandatory documents complete?
   - YES → Booking status → ACTIVE, Success message
   - NO → Warning with count of pending documents

### Case 3: Team Reviews Submitted Documents

**Action**: Admin/Sales views booking detail

**View Shows**:
1. Document section with all uploaded documents
2. Download links for each document
3. Reference numbers and upload dates
4. Option to request additional documents

### Case 4: Incomplete Submission

**Scenario**: Client uploads some documents but not all mandatory ones

**Result**:
1. Booking stays in DOCUMENT_COLLECTION
2. Client sees warning: "X document(s) still needed"
3. Form shows which documents still pending
4. Client can come back anytime to complete

## API Endpoints

### Booking Document Status

```python
# Check if all documents complete
booking.are_all_documents_complete()  # Returns: True/False

# Get documents submitted
booking.get_submitted_documents()     # Returns: QuerySet of Documents

# Get pending documents
booking.get_pending_documents()       # Returns: List of ServiceDocumentRequirements

# Get all required
booking.get_required_documents()      # Returns: QuerySet of requirements
```

## Email Notifications

When documents are submitted:
- Client gets confirmation email with receipt
- Team gets notification with document list

(Email templates can be added in notifications app)

## Troubleshooting

### Problem: Service Card Not Showing After Onboarding

**Check**:
1. Is booking in DOCUMENT_COLLECTION status?
   - SQL: `SELECT status FROM bookings_booking WHERE client_id=X;`
2. Does service have document requirements?
   - SQL: `SELECT * FROM bookings_servicedocumentrequirement WHERE service_id=X;`

**Fix**: Add document requirements to service in admin

### Problem: Booking Not Auto-Activating After Document Upload

**Check**:
1. Are all mandatory documents uploaded?
   - Compare: booking.get_submitted_documents() vs booking.get_mandatory_documents()
2. Check logs for any errors during document save

**Fix**: Manually change booking status to ACTIVE if documents are complete

### Problem: Form Not Showing Correctly

**Check**:
1. Verify JavaScript console for errors
2. Check Bootstrap version (needs Bootstrap 5+)
3. Verify document form includes in template

## Performance Considerations

### Database Queries

For booking detail page with documents:
```python
# Optimized with select_related
booking = Booking.objects.select_related(
    'client', 'service', 'assigned_to'
).get(id=id)

# Prefetch related documents
.prefetch_related('documents', 'service__document_requirements')
```

### File Upload Limits

- Max file size: 10MB per file (configure in settings)
- Allowed formats: PDF, DOCX, XLSX, JPEG, PNG
- Virus scan on upload (optional - add virus scanner integration)

## Future Enhancements

1. **Document Templates**: Provide downloadable templates for each document type
2. **Automated Validation**: Use OCR to extract and validate document data
3. **Approval Workflow**: Admin review before status changes to ACTIVE
4. **Reminders**: Email reminders if documents not submitted after X days
5. **Digital Signatures**: Support for digitally signed documents
6. **Document Versioning**: Track document updates and versions
7. **Custom Requirements**: Allow per-client custom document requirements
8. **Bulk Upload**: Support ZIP file upload with multiple documents
9. **SMS Notifications**: SMS reminders to clients for pending documents
10. **Document Status Dashboard**: Admin dashboard showing all clients' document status

## References

- Django Model Documentation: https://docs.djangoproject.com/en/4.2/topics/db/models/
- Django Forms Documentation: https://docs.djangoproject.com/en/4.2/topics/forms/
- File Upload Documentation: https://docs.djangoproject.com/en/4.2/topics/files/
