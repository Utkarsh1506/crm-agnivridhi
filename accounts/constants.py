"""
Role constants for Agnivridhi CRM
Centralized role definitions for consistent access control across the application.
"""

# Role string constants
ROLE_SUPERUSER = "superuser"
ROLE_OWNER = "owner"
ROLE_ADMIN = "admin"
ROLE_MANAGER = "manager"
ROLE_SALES = "sales"
ROLE_CLIENT = "client"

# Role choices for model field
ROLE_CHOICES = [
    (ROLE_SUPERUSER, "Superuser"),
    (ROLE_OWNER, "Owner"),
    (ROLE_ADMIN, "Admin"),
    (ROLE_MANAGER, "Manager"),
    (ROLE_SALES, "Sales"),
    (ROLE_CLIENT, "Client"),
]

# Role hierarchy (higher index = more privileges)
ROLE_HIERARCHY = [
    ROLE_CLIENT,      # Level 0
    ROLE_SALES,       # Level 1
    ROLE_MANAGER,     # Level 2
    ROLE_ADMIN,       # Level 3
    ROLE_OWNER,       # Level 4
    ROLE_SUPERUSER,   # Level 5 (highest)
]

# Role namespace access map
# Maps user roles to URL namespaces they can access
ROLE_NAMESPACE_MAP = {
    ROLE_SUPERUSER: [
        "accounts",      # All dashboard and auth routes
        "clients",       # Full client management
        "applications",  # Full application management
        "bookings",      # Full booking management
        "documents",     # Full document access
        "payments",      # Full payment management
        "schemes",       # Scheme catalog
        "api",          # API access
    ],
    ROLE_OWNER: [
        "accounts",
        "clients",
        "applications",
        "bookings",
        "documents",
        "payments",
        "schemes",
        "api",
    ],
    ROLE_ADMIN: [
        "accounts",
        "clients",
        "applications",
        "bookings",
        "documents",
        "payments",
        "schemes",
        "api",
    ],
    ROLE_MANAGER: [
        "accounts",      # Manager dashboard, team views
        "clients",       # Client approvals, team clients
        "applications",  # Team applications, approvals
        "bookings",      # Team bookings, payment approvals
        "documents",     # Team documents
        "payments",      # Team payments, approvals
        "schemes",       # Scheme catalog (read-only)
    ],
    ROLE_SALES: [
        "accounts",      # Sales dashboard, profile
        "clients",       # Client creation, pending approvals, client list
        "applications",  # Own applications, create from booking
        "bookings",      # Own bookings, record payment
        "documents",     # Own documents
        "payments",      # Own payments, record payment
        "schemes",       # Scheme catalog (for client recommendations)
    ],
    ROLE_CLIENT: [
        "accounts",      # Client portal, profile
        "applications",  # Own applications
        "bookings",      # Own bookings
        "documents",     # Own documents
        "payments",      # Own payments
        "schemes",       # Browse and apply for schemes
    ],
}

# Public namespaces accessible without authentication
PUBLIC_NAMESPACES = []

# URLs that should bypass middleware checks (login, logout, static, media, admin)
EXEMPT_URL_PATTERNS = [
    r'^/login/',
    r'^/logout/',
    r'^/static/',
    r'^/media/',
    r'^/admin/',
    r'^/api/schema/',
    r'^/api/docs/',
    r'^/api/redoc/',
]
