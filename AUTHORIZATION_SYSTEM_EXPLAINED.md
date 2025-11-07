# 🔐 AUTHORIZATION & DATA ISOLATION SYSTEM

## ✅ Already Implemented!

Your CRM **already has** a complete user-specific authorization system with ID-based filtering. Here's how it works:

---

## 🆔 User ID System

### **Every User Has**:
1. **Primary Key (ID)**: Auto-generated unique ID (e.g., `user.id = 5`)
2. **Username**: Unique username (e.g., `sales1`, `manager1`, `client1`)
3. **Role**: User role (SALES, MANAGER, CLIENT, ADMIN, etc.)
4. **Employee ID**: Optional custom employee ID for staff

### **User Model Structure**:
```python
class User(AbstractUser):
    id                  # Primary Key (auto-generated)
    username            # Unique username
    email               # Email address
    role                # SUPERUSER/OWNER/ADMIN/MANAGER/SALES/CLIENT
    employee_id         # Custom employee ID (optional)
    manager             # ForeignKey → Points to manager's User ID
    phone               # Contact phone
    designation         # Job title
    profile_picture     # Profile image
```

---

## 🔗 Relationship Hierarchy

### **Manager → Sales → Clients**

```
┌─────────────────────────────────────────────────────┐
│                   MANAGER                            │
│  (user.id=2, username=manager1, role=MANAGER)       │
└──────────────────┬──────────────────────────────────┘
                   │
                   │ manager = ForeignKey(User)
                   │
        ┌──────────┴──────────┬─────────────┐
        ▼                     ▼             ▼
┌────────────────┐   ┌────────────────┐   ┌────────────────┐
│    SALES 1     │   │    SALES 2     │   │    SALES 3     │
│  (user.id=3)   │   │  (user.id=4)   │   │  (user.id=5)   │
│  manager_id=2  │   │  manager_id=2  │   │  manager_id=2  │
└────────┬───────┘   └────────┬───────┘   └────────┬───────┘
         │                    │                    │
         │ assigned_sales     │                    │
         │                    │                    │
    ┌────┴─────┐         ┌───┴────┐          ┌───┴────┐
    ▼          ▼         ▼        ▼          ▼        ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│CLIENT 1│ │CLIENT 2│ │CLIENT 3│ │CLIENT 4│ │CLIENT 5│
│ (id=10)│ │ (id=11)│ │ (id=12)│ │ (id=13)│ │ (id=14)│
└────────┘ └────────┘ └────────┘ └────────┘ └────────┘
```

---

## 🎯 Data Filtering by User ID

### **1. SALES Dashboard** (sales1 with user.id=3)

#### **View: `sales_dashboard`**
```python
def sales_dashboard(request):
    # Get ONLY clients assigned to THIS sales person
    assigned_clients = Client.objects.filter(
        assigned_sales=request.user,  # Filter by sales person's ID
        is_approved=True
    )
    
    # Get ONLY bookings for THIS sales person's clients
    my_bookings = Booking.objects.filter(
        client__assigned_sales=request.user  # Filter by relationship
    )
    
    # Get ONLY applications assigned to THIS sales person
    my_applications = Application.objects.filter(
        assigned_to=request.user  # Filter by assignment
    )
```

**Result**: sales1 sees **ONLY** data where:
- `assigned_sales_id = 3` (their user ID)
- `assigned_to_id = 3` (their user ID)

---

### **2. CLIENT Dashboard** (client1 with user.id=10)

#### **View: `client_portal`**
```python
def client_portal(request):
    # Get THIS client's profile
    client = request.user.client_profile  # OneToOne relationship
    
    # Get ONLY this client's bookings
    bookings = Booking.objects.filter(
        client=client  # Filter by client's ID
    )
    
    # Get ONLY this client's applications
    applications = Application.objects.filter(
        client=client  # Filter by client's ID
    )
    
    # Get ONLY this client's payments
    payments = Payment.objects.filter(
        client=client  # Filter by client's ID
    )
```

**Result**: client1 sees **ONLY** their own data where:
- `client_id = 10` (their client profile ID)

---

### **3. MANAGER Dashboard** (manager1 with user.id=2)

#### **View: `manager_dashboard`**
```python
def manager_dashboard(request):
    # Get ONLY team members assigned to THIS manager
    team_members = User.objects.filter(
        manager=request.user  # Filter by manager's ID
    )
    
    # Get ONLY clients assigned to THIS manager's team
    team_clients = Client.objects.filter(
        Q(assigned_manager=request.user) |  # Direct assignment
        Q(assigned_sales__manager=request.user)  # Sales in manager's team
    )
    
    # Get ONLY bookings for THIS manager's team clients
    team_bookings = Booking.objects.filter(
        client__assigned_sales__manager=request.user  # Through relationship
    )
```

**Result**: manager1 sees **ONLY** data for:
- Team members where `manager_id = 2`
- Clients where `assigned_manager_id = 2` OR `assigned_sales.manager_id = 2`

---

## 🔒 Cross-Access Prevention

### **How It Works**:

1. **View-Level Filtering**: Every view filters by `request.user`
2. **Query-Level Security**: Django ORM filters by user ID relationships
3. **Permission Checks**: Middleware and decorators verify role access

### **Example - Preventing Cross Access**:

```python
# sales1 (id=3) tries to access sales2's (id=4) client
client = Client.objects.get(id=10)

# Permission check in view:
if client.assigned_sales != request.user:
    # sales1.id (3) != client.assigned_sales_id (4)
    messages.error(request, 'You can only view clients assigned to you.')
    return redirect('accounts:dashboard')
```

### **What Happens**:
- ❌ sales1 **CANNOT** see sales2's clients
- ❌ sales1 **CANNOT** see sales2's bookings
- ❌ sales1 **CANNOT** see sales2's applications
- ✅ sales1 **ONLY** sees data where `assigned_sales_id = 3`

---

## 📊 Database Relationships

### **Client Model**:
```python
class Client(models.Model):
    id = AutoField(primary_key=True)  # Unique client ID
    user = ForeignKey(User)            # Links to User.id (client login)
    assigned_sales = ForeignKey(User)  # Links to User.id (sales person)
    assigned_manager = ForeignKey(User)  # Links to User.id (manager)
    created_by = ForeignKey(User)      # Links to User.id (who created)
```

### **Booking Model**:
```python
class Booking(models.Model):
    id = AutoField(primary_key=True)   # Unique booking ID
    client = ForeignKey(Client)        # Links to Client.id
    assigned_to = ForeignKey(User)     # Links to User.id (assigned staff)
```

### **Application Model**:
```python
class Application(models.Model):
    id = AutoField(primary_key=True)   # Unique application ID
    client = ForeignKey(Client)        # Links to Client.id
    assigned_to = ForeignKey(User)     # Links to User.id (assigned staff)
```

### **Payment Model**:
```python
class Payment(models.Model):
    id = AutoField(primary_key=True)   # Unique payment ID
    client = ForeignKey(Client)        # Links to Client.id
    booking = ForeignKey(Booking)      # Links to Booking.id
    received_by = ForeignKey(User)     # Links to User.id (who received)
```

---

## 🎯 Real Example Walkthrough

### **Scenario**: 3 Sales Persons, Each with Clients

```sql
-- Users Table
| id | username  | role    | manager_id |
|----|-----------|---------|------------|
| 2  | manager1  | MANAGER | NULL       |
| 3  | sales1    | SALES   | 2          |
| 4  | sales2    | SALES   | 2          |
| 5  | sales3    | SALES   | 2          |

-- Clients Table
| id | company_name      | assigned_sales_id | assigned_manager_id |
|----|-------------------|-------------------|---------------------|
| 10 | ABC Company       | 3 (sales1)        | 2 (manager1)        |
| 11 | XYZ Industries    | 3 (sales1)        | 2 (manager1)        |
| 12 | DEF Corp          | 4 (sales2)        | 2 (manager1)        |
| 13 | GHI Ltd           | 4 (sales2)        | 2 (manager1)        |
| 14 | JKL Enterprises   | 5 (sales3)        | 2 (manager1)        |
```

### **What Each User Sees**:

#### **sales1 Login** (user.id=3):
```python
# Query: Client.objects.filter(assigned_sales=request.user)
# Where: assigned_sales_id = 3
```
**Sees**: Client 10, Client 11 ✅  
**Cannot See**: Client 12, 13, 14 ❌

#### **sales2 Login** (user.id=4):
```python
# Query: Client.objects.filter(assigned_sales=request.user)
# Where: assigned_sales_id = 4
```
**Sees**: Client 12, Client 13 ✅  
**Cannot See**: Client 10, 11, 14 ❌

#### **manager1 Login** (user.id=2):
```python
# Query: Client.objects.filter(
#     Q(assigned_manager=request.user) |
#     Q(assigned_sales__manager=request.user)
# )
# Where: assigned_manager_id = 2 OR assigned_sales.manager_id = 2
```
**Sees**: Client 10, 11, 12, 13, 14 (ALL team clients) ✅

---

## 🛡️ Security Layers

### **Layer 1: Middleware** (`RoleAccessMiddleware`)
- Checks if user can access URL namespace
- Blocks unauthorized namespace access

### **Layer 2: View Decorators**
```python
@sales_required
def sales_clients_list(request):
    # Only SALES role can access
```

### **Layer 3: Query Filtering**
```python
# Automatic filtering by user ID
clients = Client.objects.filter(assigned_sales=request.user)
```

### **Layer 4: Object-Level Permissions**
```python
# Check specific object access
if client.assigned_sales != request.user:
    return HttpResponseForbidden()
```

---

## ✅ Current Implementation Status

| Feature | Status | How It Works |
|---------|--------|--------------|
| **User IDs** | ✅ Working | Django auto-generated primary keys |
| **Sales → Clients** | ✅ Working | `Client.assigned_sales = ForeignKey(User)` |
| **Manager → Sales** | ✅ Working | `User.manager = ForeignKey(User)` |
| **Manager → Clients** | ✅ Working | `Client.assigned_manager = ForeignKey(User)` |
| **Data Isolation** | ✅ Working | All views filter by `request.user` |
| **Cross-Access Prevention** | ✅ Working | Permission checks in views |
| **Namespace Security** | ✅ Working | `RoleAccessMiddleware` |

---

## 🧪 Testing Data Isolation

### **Test 1: Sales Person Isolation**

1. **Create Test Users**:
   ```python
   # In Django shell
   from accounts.models import User
   
   manager = User.objects.create_user(
       username='manager1', password='test123', role='MANAGER'
   )
   
   sales1 = User.objects.create_user(
       username='sales1', password='test123', 
       role='SALES', manager=manager
   )
   
   sales2 = User.objects.create_user(
       username='sales2', password='test123',
       role='SALES', manager=manager
   )
   ```

2. **Assign Clients**:
   ```python
   # Client 1 → sales1
   client1.assigned_sales = sales1
   client1.save()
   
   # Client 2 → sales2
   client2.assigned_sales = sales2
   client2.save()
   ```

3. **Test Login**:
   - Login as **sales1**: Should see ONLY client1 ✅
   - Login as **sales2**: Should see ONLY client2 ✅
   - sales1 **CANNOT** see client2 ❌
   - sales2 **CANNOT** see client1 ❌

---

### **Test 2: Manager Team View**

1. **Manager Login**:
   ```
   Username: manager1
   Password: test123
   ```

2. **Manager Should See**:
   - ✅ All team members (sales1, sales2)
   - ✅ All team clients (client1, client2)
   - ✅ All team bookings
   - ✅ All team applications

---

### **Test 3: Client Isolation**

1. **Client Logins**:
   ```
   client1: Should see ONLY their own data
   client2: Should see ONLY their own data
   ```

2. **Verification**:
   - ✅ client1 sees own bookings/applications/payments
   - ✅ client2 sees own bookings/applications/payments
   - ❌ client1 CANNOT see client2's data
   - ❌ client2 CANNOT see client1's data

---

## 📋 Current User IDs in System

To see current user IDs:

```python
# In Django shell
from accounts.models import User

# List all users with their IDs
for user in User.objects.all():
    print(f"ID: {user.id}, Username: {user.username}, Role: {user.role}")
```

**Expected Output**:
```
ID: 1, Username: admin, Role: ADMIN
ID: 2, Username: manager1, Role: MANAGER
ID: 3, Username: sales1, Role: SALES
ID: 4, Username: client1, Role: CLIENT
```

---

## 🎯 Summary

### **Your System ALREADY Has**:

1. ✅ **User IDs**: Every user has unique ID
2. ✅ **Manager → Sales Relationship**: `User.manager` field
3. ✅ **Sales → Clients Relationship**: `Client.assigned_sales` field
4. ✅ **Data Filtering**: All views filter by user ID
5. ✅ **Authorization**: Role-based access control
6. ✅ **Cross-Access Prevention**: Permission checks in views
7. ✅ **Namespace Security**: Middleware blocks unauthorized access

### **No Additional Implementation Needed!**

The system is **already working** exactly as you described. Each user:
- ✅ Has a unique ID
- ✅ Sees ONLY their own data
- ✅ Cannot access other users' data
- ✅ Has proper relationships (manager → sales → clients)

---

## 🚀 What You Can Do Now

1. **Test the isolation**: Login as different users to verify
2. **View user IDs**: Use Django admin to see user IDs
3. **Assign relationships**: Use admin to assign sales to managers
4. **Create test data**: Create multiple users to test isolation

**Everything is ready to use!** 🎉
