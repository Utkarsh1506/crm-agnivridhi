# Clerk OTP Authentication - Visual Architecture Guide

## System Flow Diagram

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                     CLERK OTP AUTHENTICATION SYSTEM                        ║
╚═══════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 1: CLIENT CREATION & APPROVAL                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│   Admin creates client in Django Admin:                                  │
│   ┌──────────────────────────────────────────┐                          │
│   │ Client Form                              │                          │
│   │ ├─ Name: "ABC Corp"                      │                          │
│   │ ├─ Contact Email: "client@abc.com"   ◄───┼─ KEY FIELD              │
│   │ ├─ Is Approved: ☑ (checked)             │                          │
│   │ └─ [Save]                                │                          │
│   └──────────────────────────────────────────┘                          │
│           │                                                               │
│           ▼                                                               │
│   ✓ Client saved in database                                             │
│           │                                                               │
│           ▼                                                               │
│   Signal Triggered: post_save(sender=Client)                            │
│   ├─ Check: is_approved changed to True?                                │
│   ├─ Get: client.contact_email                                          │
│   ├─ Call: send_clerk_auth_welcome_email(client)                       │
│   └─ Result: 📧 Email sent to client@abc.com                            │
│           │                                                               │
│           ▼                                                               │
│   Welcome Email Received by Client:                                      │
│   ╔════════════════════════════════════════════╗                        │
│   ║          WELCOME TO AGNIVRIDHI!            ║                        │
│   ║    Your account has been approved ✅       ║                        │
│   ║                                            ║                        │
│   ║    [📍 LOG IN TO YOUR ACCOUNT]             ║                        │
│   ║    Visit: /accounts/client-login/          ║                        │
│   ║    Email: client@abc.com                   ║                        │
│   ╚════════════════════════════════════════════╝                        │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 2: CLIENT LOGIN FLOW - PART A (EMAIL ENTRY)                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│   Client visits: /accounts/client-login/                                │
│                                                                           │
│   ┌─────────────────────────────────────────┐                           │
│   │                                         │                           │
│   │    🔐 CLIENT PORTAL                     │                           │
│   │                                         │                           │
│   │    Email Address:                       │                           │
│   │    [____ client@abc.com ____]           │                           │
│   │                                         │                           │
│   │    [Send OTP Code →]                    │                           │
│   │                                         │                           │
│   └─────────────────────────────────────────┘                           │
│           │                                                               │
│           ▼ (POST /accounts/client-login/)                              │
│   ClientEmailLoginView processes:                                        │
│   ├─ Get email from form                                                │
│   ├─ Check: Client with this email exists?                             │
│   │  └─ NO → Error: "No account found"                                  │
│   ├─ Check: client.is_approved == True?                                │
│   │  └─ NO → Error: "Account not approved yet"                         │
│   └─ YES → Generate OTP                                                 │
│           │                                                               │
│           ▼                                                               │
│   clerk_service.send_otp("client@abc.com"):                             │
│   ├─ Generate: 6-digit code (e.g., "523987")                           │
│   ├─ Cache Key: "client_otp_client@abc.com"                            │
│   ├─ Cache Value: "523987"                                              │
│   ├─ TTL (Timeout): 600 seconds (10 minutes)                            │
│   └─ Result: Code cached ✓                                              │
│           │                                                               │
│           ▼                                                               │
│   Send Email to client@abc.com:                                          │
│   ╔════════════════════════════════════════════╗                        │
│   ║  Your verification code is: 523987         ║                        │
│   ║  This code expires in 10 minutes            ║                        │
│   ║  Never share this code with anyone          ║                        │
│   ╚════════════════════════════════════════════╝                        │
│           │                                                               │
│           ▼                                                               │
│   Redirect: → /accounts/client-verify-otp/                             │
│   Session Data: login_email = "client@abc.com"                         │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 3: CLIENT LOGIN FLOW - PART B (OTP VERIFICATION)                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│   Client receives email with code: 523987                               │
│                                                                           │
│   Client visits: /accounts/client-verify-otp/                           │
│                                                                           │
│   ┌─────────────────────────────────────────┐                           │
│   │                                         │                           │
│   │    📧 Verify Your Email                 │                           │
│   │                                         │                           │
│   │    Verification Code:                   │                           │
│   │    [5 2 3 9 8 7]                        │                           │
│   │                                         │                           │
│   │    [Verify Code →]                      │                           │
│   │                                         │                           │
│   │    ⏱️ Code expires in 10 minutes         │                           │
│   │                                         │                           │
│   └─────────────────────────────────────────┘                           │
│           │                                                               │
│           ▼ (POST /accounts/client-verify-otp/)                         │
│   ClientVerifyOTPView processes:                                         │
│   ├─ Get OTP from form: "523987"                                        │
│   ├─ Get email from session: "client@abc.com"                          │
│   ├─ Track attempts: otp_attempts = 0                                   │
│   └─ Call: clerk_service.verify_otp()                                   │
│           │                                                               │
│           ▼                                                               │
│   clerk_service.verify_otp("client@abc.com", "523987"):                │
│   ├─ Cache Key: "client_otp_client@abc.com"                            │
│   ├─ Get cached code: "523987"                                          │
│   ├─ Check: Code exists in cache?                                       │
│   │  └─ NO → Error: "OTP expired"                                       │
│   ├─ Check: Input OTP matches cached OTP?                              │
│   │  └─ NO → otp_attempts++                                             │
│   │  └─ If otp_attempts >= 3 → Block login                             │
│   │  └─ Result: Error "Invalid OTP"                                     │
│   └─ YES → Success!                                                      │
│           │                                                               │
│           ▼                                                               │
│   Create Authenticated Session:                                          │
│   ├─ Get Client from database                                           │
│   ├─ Get User (client.user)                                             │
│   ├─ Call: django.contrib.auth.login()                                 │
│   ├─ Create: REST API Token (optional)                                  │
│   ├─ Clear: cache.delete(otp_key)                                       │
│   ├─ Clear: session["login_email"]                                      │
│   └─ Result: User authenticated ✓                                        │
│           │                                                               │
│           ▼                                                               │
│   Success Message: "Welcome back, ABC Corp!"                             │
│   Redirect: → /accounts/dashboard/client/                              │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│ INTERNAL ARCHITECTURE                                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│   ┌──────────────────────────────────────────────────────────────┐      │
│   │ Django Request/Response                                      │      │
│   │                                                              │      │
│   │  HTTP GET /accounts/client-login/                          │      │
│   │       ↓                                                      │      │
│   │  URL Router: urls.py                                        │      │
│   │       ↓                                                      │      │
│   │  View: ClientEmailLoginView                                │      │
│   │       ↓                                                      │      │
│   │  Service: clerk_service.send_otp()                         │      │
│   │       ↓                                                      │      │
│   │  Cache: django.core.cache                                  │      │
│   │       ↓                                                      │      │
│   │  Email: django.core.mail.send_mail()                       │      │
│   │       ↓                                                      │      │
│   │  Response: 302 Redirect                                     │      │
│   │                                                              │      │
│   └──────────────────────────────────────────────────────────────┘      │
│                                                                           │
│   File Organization:                                                     │
│   ┌──────────────────────────────────────────────────────────────┐      │
│   │ accounts/                                                    │      │
│   │ ├─ clerk_auth.py ◄─ OTP Service (business logic)           │      │
│   │ ├─ views_otp_auth.py ◄─ Views (HTTP handlers)              │      │
│   │ ├─ urls.py ◄─ Routes (URL mappings)                        │      │
│   │                                                              │      │
│   │ clients/                                                    │      │
│   │ ├─ clerk_signals.py ◄─ Approval signal handler             │      │
│   │ ├─ models.py (uses contact_email field)                    │      │
│   │                                                              │      │
│   │ templates/                                                  │      │
│   │ ├─ accounts/                                                │      │
│   │ │  ├─ client_email_login.html ◄─ Step 1 form              │      │
│   │ │  └─ client_verify_otp.html ◄─ Step 2 form               │      │
│   │ ├─ emails/                                                  │      │
│   │ │  └─ clerk_auth_welcome.html ◄─ Welcome email            │      │
│   │                                                              │      │
│   │ agnivridhi_crm/                                             │      │
│   │ └─ settings.py ◄─ Cache + Clerk config                     │      │
│   │                                                              │      │
│   └──────────────────────────────────────────────────────────────┘      │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│ DATA FLOW DIAGRAM                                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Input                Service             Storage         Output         │
│  ════════════════════════════════════════════════════════════════════   │
│                                                                           │
│  Email Address                                                           │
│     │                                                                    │
│     ▼                                                                    │
│  clerk_service.send_otp()                                              │
│     │                                                                    │
│     ├─→ Generate 6-digit code ─┐                                        │
│     │                           ├─→ Cache                               │
│     └─→ Create cache entry  ────┤    (10 min TTL)                      │
│                                │                                        │
│                                ▼                                        │
│                           Email Service                                 │
│                                │                                        │
│                                ▼                                        │
│                        Email Provider (SMTP)                            │
│                                │                                        │
│                                ▼                                        │
│                          Client Inbox 📧                                │
│                                                                           │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                           │
│  OTP Code                                                                │
│     │                                                                    │
│     ▼                                                                    │
│  clerk_service.verify_otp()                                            │
│     │                                                                    │
│     ├─→ Get cached code                                                 │
│     ├─→ Compare                                                         │
│     └─→ If match: delete cache ─┐                                       │
│                                 ├─→ Session Created                     │
│     ├─→ Call django.login()    ─┤                                       │
│     └─→ Generate auth token ───┘                                        │
│                                                                           │
│                                ▼                                        │
│                          Authenticated Client                            │
│                        (can access dashboard)                            │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│ SECURITY CONSIDERATIONS                                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  🔒 Threat: Brute Force OTP Guessing                                    │
│     └─ Protection: 3-attempt limit per session                          │
│     └─ 6-digit code: 1 million possibilities                            │
│     └- Probability of random guess: 0.0001%                            │
│                                                                           │
│  🔒 Threat: OTP Interception                                            │
│     └─ Protection: Sent via encrypted email (TLS/SSL)                   │
│     └─ Never logged to files or databases                               │
│     └─ Stored only in cache, not database                               │
│                                                                           │
│  🔒 Threat: Session Hijacking                                           │
│     └─ Protection: SESSION_COOKIE_HTTPONLY = True                       │
│     └─ JavaScript cannot access session cookie                          │
│     └─ CSRF token required for all POST requests                        │
│                                                                           │
│  🔒 Threat: Code Reuse                                                  │
│     └─ Protection: Code deleted immediately after verification          │
│     └─ One-time use only                                                │
│                                                                           │
│  🔒 Threat: Expired Code Misuse                                         │
│     └─ Protection: 10-minute expiration                                 │
│     └─ Expired codes return "OTP expired" error                         │
│     └─ User must request new OTP                                        │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│ CONFIGURATION MATRIX                                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Setting                Default              Configurable Via           │
│  ═══════════════════════════════════════════════════════════════════   │
│  OTP Length             6 digits             Hard-coded in code         │
│  OTP Expiration         10 minutes           Hard-coded in code         │
│  Attempt Limit          3 failures           Hard-coded in code         │
│  Cache Backend          LocMemCache          .env CACHE_BACKEND         │
│  Cache Timeout          5 minutes            .env CACHE_TIMEOUT         │
│  Email Backend          SMTP                 .env EMAIL_* settings      │
│  Company Name           "Agnivridhi India"   .env COMPANY_NAME          │
│  Site URL               "localhost:8000"     .env SITE_URL              │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

## Component Interaction Diagram

```
                           ┌─────────────────────────┐
                           │   CLIENT BROWSER        │
                           └──────────┬──────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
            GET /client-login/   POST email        GET OTP verify
                    │                 │                 │
                    └─────────────────┼─────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────┐
                    │      Django URL Dispatcher      │
                    │      (accounts/urls.py)         │
                    └─────────────────┬───────────────┘
                                      │
                    ┌─────────────────┼──────────────────┐
                    │                 │                  │
                    ▼                 ▼                  ▼
           ┌──────────────────┐ ┌──────────────┐ ┌──────────────┐
           │ ClientEmailLogin │ │ ClientVerify │ │  ClientLogout│
           │      View        │ │    OTPView   │ │    View      │
           └────────┬─────────┘ └──────┬───────┘ └──────┬───────┘
                    │                 │                  │
                    └─────────────────┼──────────────────┘
                                      │
                                      ▼
                    ┌────────────────────────────┐
                    │   clerk_auth Service       │
                    │ (Business Logic)           │
                    │ ├─ send_otp()              │
                    │ ├─ verify_otp()            │
                    │ └─ create_session()        │
                    └────────────┬───────────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
                ▼                ▼                ▼
        ┌──────────────┐  ┌─────────────┐ ┌──────────────┐
        │ Django Cache │  │ Django Mail │ │Django Auth   │
        │ (OTP Store)  │  │ (SMTP)      │ │(Session)     │
        └──────────────┘  └─────────────┘ └──────────────┘
```

## Approval Signal Flow

```
Admin saves Client with is_approved=True
        │
        ▼
  ┌──────────────────────────────────┐
  │ post_save signal dispatched      │
  └──────────────────────────────────┘
        │
        ▼
  ┌──────────────────────────────────┐
  │ clients/clerk_signals.py         │
  │ setup_clerk_auth_on_approval()   │
  └──────────────────────────────────┘
        │
        ├─ Check: is_approved changed to True? (YES)
        │
        ├─ Get: client.contact_email = "client@example.com"
        │
        ├─ Call: send_clerk_auth_welcome_email(client)
        │   │
        │   ├─ Load: templates/emails/clerk_auth_welcome.html
        │   ├─ Render: with context (client_name, login_url, etc.)
        │   ├─ Send: via EMAIL_BACKEND (SMTP)
        │   └─ Log: "Welcome email sent to..."
        │
        └─ Done! ✅

Result: Client receives professional welcome email with login link
```

---

**Visual Reference Guide for Clerk OTP System Architecture**  
✅ Complete system flow from client creation to authenticated access  
✅ Security considerations and threat mitigations  
✅ Component interactions and data flow  
✅ Configuration options and settings

For detailed implementation, see `CLERK_OTP_AUTH_README.md`
