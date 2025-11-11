# 🚀 Quick Start - PythonAnywhere Deployment

## ⚡ 5-Minute Setup

### 1. Create Account
→ https://www.pythonanywhere.com/registration/register/beginner/
→ Choose username (e.g., `agnivridhi`)

### 2. Upload Code
**Option A - Git (Recommended):**
```bash
# In PythonAnywhere Bash console
git clone https://github.com/Utkarsh1506/crm-agnivridhi.git
```

**Option B - Upload ZIP:**
→ Files tab → Upload ZIP → Extract

### 3. Create Database
→ Databases tab → Initialize MySQL → Set password
→ Create database: `agnivridhi$crm_agnivridhi`

### 4. Run Deployment Script
```bash
cd ~/crm-agnivridhi
chmod +x deploy-pythonanywhere.sh
./deploy-pythonanywhere.sh
```

### 5. Configure Web App
→ Web tab → Add new web app → Manual configuration (Python 3.10)

**Set these:**
- Source code: `/home/agnivridhi/crm-agnivridhi`
- Virtualenv: `/home/agnivridhi/.virtualenvs/crm-env`
- WSGI: Copy from `pythonanywhere_wsgi.py`

**Static files:**
- URL: `/static/` → Directory: `/home/agnivridhi/crm-agnivridhi/staticfiles`
- URL: `/media/` → Directory: `/home/agnivridhi/crm-agnivridhi/media`

### 6. Reload & Test
→ Click green "Reload" button
→ Visit: `https://agnivridhi.pythonanywhere.com`

---

## 📋 Files You Need

✅ **PYTHONANYWHERE_DEPLOYMENT.md** - Complete guide
✅ **.env.pythonanywhere** - Environment template
✅ **pythonanywhere_wsgi.py** - WSGI config
✅ **deploy-pythonanywhere.sh** - Auto deployment script

---

## 🔑 Key Differences from Hostinger

| What                  | Hostinger                          | PythonAnywhere           |
|-----------------------|------------------------------------|--------------------------|
| Python version        | 3.6 (too old!)                     | 3.10+ ✓                  |
| Setup time            | 2-3 hours (complex)                | 10 minutes (easy)        |
| Database              | Manual MySQL via cPanel            | One-click MySQL          |
| WSGI config           | passenger_wsgi.py (tricky)         | Web interface (simple)   |
| Static files          | Manual collectstatic + .htaccess   | Automatic mapping        |
| Reload app            | touch tmp/restart.txt              | Click "Reload" button    |
| View logs             | SSH + hunt for logs                | Click "Error log"        |
| SSL/HTTPS             | Manual setup                       | Automatic ✓              |

---

## 💰 Cost Comparison

**PythonAnywhere Free:**
- ✓ Perfect for testing/development
- ✓ `username.pythonanywhere.com` domain
- ✓ MySQL database
- ✗ No custom domain

**PythonAnywhere Hacker ($5/month):**
- ✓ Custom domain (crm.agnivridhiindia.com)
- ✓ More resources
- ✓ SSH access
- ✓ Always-on tasks

**Hostinger Shared ($2.99/month):**
- ✗ Outdated Python 3.6
- ✗ Complex Django setup
- ✗ Manual everything
- ⚠️ Not recommended for Django

---

## 🎯 Recommended Path

1. **Start Free:** Test on PythonAnywhere free tier
2. **Upgrade to Hacker:** Once ready for production ($5/month)
3. **Custom Domain:** Point crm.agnivridhiindia.com to PythonAnywhere

---

## 📞 Need Help?

→ **Full Guide:** PYTHONANYWHERE_DEPLOYMENT.md
→ **Support:** https://www.pythonanywhere.com/forums/
→ **Docs:** https://help.pythonanywhere.com/

---

**Bottom line:** PythonAnywhere is 10x easier than Hostinger for Django! 🎉
