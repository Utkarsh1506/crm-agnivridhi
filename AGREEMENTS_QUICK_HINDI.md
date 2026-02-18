# Agreement System - Quick Summary (हिंदी)

## ✅ Jo Kaam Complete Ho Gaya

### 1. Django App Bana Diya ✓
- **App Name**: `agreements`
- Successfully created with all required files

### 2. Database Model Ready ✓
**Agreement Model** mein ye fields hain:
- Agreement Number (Auto-generate hoga: FA-20260128-001 ya WA-20260128-001)
- Agreement Type (Funding ya Website)
- Service Receiver ka Naam
- Address
- Date of Agreement
- Service Description
- Total Amount Pitched
- Received Amount Stage 1 (without GST)
- Pending Amount Stage 2 (optional - agar pending hai toh)
- Commission Percentage
- Commission Stage (Stage 2 ya Stage 3)

### 3. Forms Bana Diye ✓
- Create Agreement form with validation
- Edit Agreement form
- All required fields ka validation
- Optional fields properly handled

### 4. Views Complete ✓
**Sales/Employee ke liye:**
- Agreement list dekh sakte hain (filter by type, client)
- Naya agreement create kar sakte hain
- Agreement edit kar sakte hain
- Agreement delete kar sakte hain
- PDF download kar sakte hain

**Manager/Admin ke liye:**
- Sab agreements dekh sakte hain
- Filter kar sakte hain

### 5. Templates Bana Diye ✓
- Agreement list page
- Agreement create/edit form
- Agreement detail page
- Manager view
- **2 PDF Templates**:
  - Funding Agreement PDF
  - Website Agreement PDF

### 6. Navigation Added ✓
- URLs configured
- App integrated in settings.py
- Sidebar links ready

## 🔧 Ab Kya Karna Hai

### Step 1: Migration Issue Fix Karo (IMPORTANT!)
Pehle clients app ka migration issue fix karna hoga:

```powershell
python manage.py showmigrations clients
```

Agar migration dependency issue hai toh fix karo, phir:

```powershell
# Agreements ke migrations banao
python manage.py makemigrations agreements

# Migrations apply karo
python manage.py migrate agreements
```

### Step 2: PDF Library Install Karo
PDF generate karne ke liye WeasyPrint chahiye:

```powershell
pip install weasyprint
```

**Note**: Windows pe GTK3 runtime bhi install karna padega: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases

Ya phir alternative use karo:
```powershell
pip install xhtml2pdf
```

### Step 3: Sample PDF Templates Customize Karo
Tumhare actual agreement ke format ke hisaab se in files ko edit karo:
- `templates/agreements/pdf/funding_agreement.html`
- `templates/agreements/pdf/website_agreement.html`

**Dhyan Rakho:**
- Header mein company details update karo
- Terms & Conditions update karo
- Styling customize karo
- Lekin {{ agreement.field_name }} variables ko change mat karna!

## 📝 Variable Fields (Jo Input Leni Hai)

Jab agreement create karoge toh ye sab fields input leni padegi:

1. **Service Receiver Name** - Jisko service provide kar rahe ho
2. **Date of Agreement** - Agreement ki date
3. **Service** - Service ka complete description
4. **Address** - Service receiver ka pura address
5. **Total Amount Pitched** - Total amount (loan ya website ka)
6. **Received Amount Stage 1** - Jo amount receive ho gaya without GST
7. **Pending Amount Stage 2** - Agar koi pending amount hai (optional)
8. **Commission Percentage** - Commission percentage
9. **Commission Stage** - Kab commission apply hoga (Stage 2 ya 3)

## 🎯 Kaise Use Karein

### Sales/Employee Login Karke:
1. `/agreements/` pe jao ya sidebar se "Agreements" click karo
2. "Create New Agreement" button dabao
3. Agreement type select karo (Funding ya Website)
4. Sari details bharo
5. Commission details daalo
6. Client aur Employee optional link kar sakte ho
7. Submit karo
8. PDF download kar lo

### Manager/Admin Login Karke:
1. `/agreements/manager/` pe jao
2. Sare agreements dikh jayenge
3. Filter kar sakte ho type aur client se
4. Kisi bhi agreement ka PDF download kar sakte ho

## 📂 Files Kaha Hain

```
CRM/
├── agreements/                          # New app
│   ├── models.py                       # Database model
│   ├── forms.py                        # Forms
│   ├── views.py                        # Views + PDF generation
│   ├── urls.py                         # URL routing
│   └── admin.py                        # Admin panel
│
├── templates/agreements/               # Templates
│   ├── agreement_list.html            # List page
│   ├── agreement_form.html            # Create/Edit form
│   ├── agreement_detail.html          # Detail view
│   ├── manager_agreement_list.html   # Manager view
│   └── pdf/
│       ├── funding_agreement.html     # Funding PDF template
│       └── website_agreement.html     # Website PDF template
│
├── agnivridhi_crm/
│   ├── settings.py                    # 'agreements' app added
│   └── urls.py                        # Routes added
│
└── AGREEMENTS_SETUP_GUIDE.md          # Complete English guide
```

## ⚠️ Important Notes

1. **Migration Fix**: Pehle clients app ka migration issue fix karo, tabhi agreements ka migration chalega
2. **PDF Library**: WeasyPrint ya xhtml2pdf install karna zaruri hai
3. **Templates**: Apne actual agreement format ke according customize karna padega
4. **Testing**: Test kar lo local pe pehle, phir deploy karo

## 🚀 Testing Kaise Karein

1. Sales user se login karo
2. Agreement create karo test data se
3. Check karo:
   - Agreement number auto-generate ho raha hai?
   - Sari details sahi display ho rahi hain?
   - PDF download ho raha hai?
   - Pending amount optional field kaam kar rahi hai?

## 📱 Features

- ✅ Auto-generate agreement numbers
- ✅ Two types: Funding & Website
- ✅ Role-based access control
- ✅ PDF generation
- ✅ Filter by type and client
- ✅ Optional pending amount (Stage 2)
- ✅ Commission calculation
- ✅ Client and Employee linking
- ✅ Edit/Delete functionality
- ✅ Manager overview

## 🔐 Security

- User apne hi agreements dekh sakta hai
- Manager sab dekh sakta hai
- Admin full access
- Form validation included
- CSRF protection

## 💡 Next Steps

1. **Abhi**: Migration issue fix karo
2. **Phir**: Migrations run karo for agreements app
3. **Customize**: PDF templates ko apne format me edit karo
4. **Test**: Local pe test karo thoroughly
5. **Deploy**: Production pe deploy karo

---

**Status**: ✅ Code Ready - Sirf migration aur testing baaki hai
**Created**: January 28, 2026

Detailed English guide: `AGREEMENTS_SETUP_GUIDE.md` dekho

Koi doubt ho toh batao! 🚀
