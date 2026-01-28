# Git Push Instructions

## Problem
The PowerShell terminal has PSReadLine rendering errors preventing command execution.

## Solution: Manual Git Push

### Option 1: Run the Batch Script (Easiest)
1. Open File Explorer
2. Navigate to: `c:\Users\Admin\Desktop\agni\CRM`
3. Double-click the file: `push_to_git.bat`
4. The script will automatically:
   - Add all files to git
   - Commit with message
   - Push to remote repository
5. Press any key when complete

### Option 2: Open New Terminal (Recommended)
1. Open a **NEW** PowerShell or Command Prompt window (don't use the existing one)
2. Navigate to the project:
   ```
   cd c:\Users\Admin\Desktop\agni\CRM
   ```
3. Run the git commands:
   ```
   git add .
   git commit -m "Add complete agreements system with PDF generation"
   git push
   ```

### Option 3: Use VS Code Terminal
1. Close the broken terminal in VS Code (click X or trash icon)
2. Open a new terminal: Terminal → New Terminal (Ctrl + Shift + `)
3. Run:
   ```
   git add .
   git commit -m "Add complete agreements system with PDF generation"
   git push
   ```

## What Will Be Committed

All new agreements system files:
- **agreements/** app directory (7 files)
  - models.py, views.py, forms.py, urls.py, admin.py
  - migrations/0001_initial.py
  - __init__.py

- **templates/agreements/** (7 template files)
  - agreement_list.html
  - agreement_form.html
  - agreement_detail.html
  - agreement_confirm_delete.html
  - manager_agreement_list.html
  - pdf/funding_agreement.html
  - pdf/website_agreement.html
  - pdf/funding_agreement_old_backup.html

- **Documentation** (9 Markdown files)
  - START_AGREEMENTS.md
  - AGREEMENTS_SYSTEM_READY.md
  - AGREEMENTS_COMPLETION_REPORT.md
  - AGREEMENTS_HINDI_QUICK_GUIDE.md
  - DEPLOYMENT_CHECKLIST_AGREEMENTS.md
  - AGREEMENTS_FEATURES.md
  - AGREEMENTS_PDF_TEMPLATES.md
  - AGREEMENTS_TECHNICAL_DETAILS.md
  - AGREEMENTS_QUICK_REFERENCE.md

- **Modified Core Files** (3 files)
  - agnivridhi_crm/settings.py (added 'agreements' app)
  - agnivridhi_crm/urls.py (added agreements URLs)
  - clients/migrations/0010_fix_utf8mb4_charset.py (fixed charset)

- **Test Scripts** (2 files)
  - test_agreements_system.py
  - check_agreements_table.py

- **Helper Scripts**
  - push_to_git.bat (new batch file)
  - GIT_PUSH_INSTRUCTIONS.md (this file)

## Commit Message
```
Add complete agreements system with PDF generation, templates, and documentation

- Create agreements Django app with models, views, forms
- Add two agreement types: Funding and Website
- Implement PDF generation with xhtml2pdf
- Add professional PDF templates based on actual agreements
- Create role-based views (Sales/Manager/Admin)
- Add comprehensive documentation (9 files)
- Include test scripts and verification tools
- Integrate with existing Clients and Employees models
- Implement auto-generated agreement numbers (FA/WA-YYYYMMDD-XXX)
- Add full CRUD operations with delete confirmation
- Fix charset migration for SQLite compatibility
```

## After Successful Push

Your agreements system is now in version control! ✅

You can:
1. Start using it: `python manage.py runserver`
2. Navigate to: http://localhost:8000/agreements/
3. Create your first agreement
4. Download as professional PDF

## Troubleshooting

**If git push asks for credentials:**
- Enter your GitHub/GitLab username
- Use personal access token as password (not your account password)

**If remote is not set:**
```
git remote add origin <your-repo-url>
git push -u origin main
```

**To check what will be committed:**
```
git status
```

---

**Note:** The PowerShell PSReadLine error is a terminal display bug, not a project error. Your agreements system is fully functional and ready to use!
