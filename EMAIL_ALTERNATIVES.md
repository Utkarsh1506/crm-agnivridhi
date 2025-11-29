# Email Service Alternatives for Agnivridhi CRM on PythonAnywhere

## 🏆 Recommended: SendGrid (Best for Production)

### Why SendGrid?
✅ **Free Tier**: 100 emails/day forever (enough for small CRM)
✅ Works on PythonAnywhere free accounts
✅ Professional email deliverability
✅ Email analytics and tracking
✅ No "sent via Gmail" label
✅ Can use your domain: noreply@agnivridhiindia.com

### Setup (5 minutes):

1. **Sign up**: https://signup.sendgrid.com/
2. **Verify email** and complete setup
3. **Create API Key**:
   - Settings → API Keys → Create API Key
   - Name: "Agnivridhi CRM"
   - Permissions: "Full Access" or "Mail Send"
   - Copy the API key (starts with `SG.`)

4. **Update WSGI file** on PythonAnywhere:

```python
# Email Configuration - SendGrid
os.environ['EMAIL_BACKEND'] = 'django.core.mail.backends.smtp.EmailBackend'
os.environ['EMAIL_HOST'] = 'smtp.sendgrid.net'
os.environ['EMAIL_PORT'] = '587'
os.environ['EMAIL_USE_TLS'] = 'True'
os.environ['EMAIL_HOST_USER'] = 'apikey'  # Literally "apikey", don't change
os.environ['EMAIL_HOST_PASSWORD'] = 'SG.your_api_key_here'  # Paste your API key
os.environ['DEFAULT_FROM_EMAIL'] = 'Agnivridhi CRM <noreply@agnivridhiindia.com>'
```

5. **Verify Domain** (Optional but recommended):
   - Settings → Sender Authentication → Domain Authentication
   - Add DNS records to your domain registrar
   - Emails won't go to spam anymore

---

## 🥈 Alternative 1: Mailgun

### Why Mailgun?
✅ Free tier: 5,000 emails/month (first 3 months), then 1,000/month
✅ Works on PythonAnywhere free accounts
✅ Good deliverability
✅ Detailed logs and analytics

### Setup:

1. Sign up: https://www.mailgun.com/
2. Get SMTP credentials from Settings → API Keys
3. Update WSGI:

```python
# Email Configuration - Mailgun
os.environ['EMAIL_BACKEND'] = 'django.core.mail.backends.smtp.EmailBackend'
os.environ['EMAIL_HOST'] = 'smtp.mailgun.org'
os.environ['EMAIL_PORT'] = '587'
os.environ['EMAIL_USE_TLS'] = 'True'
os.environ['EMAIL_HOST_USER'] = 'postmaster@your-mailgun-domain.mailgun.org'
os.environ['EMAIL_HOST_PASSWORD'] = 'your_mailgun_password'
os.environ['DEFAULT_FROM_EMAIL'] = 'Agnivridhi CRM <noreply@agnivridhiindia.com>'
```

---

## 🥉 Alternative 2: Brevo (formerly Sendinblue)

### Why Brevo?
✅ Free tier: **300 emails/day** forever
✅ Works on PythonAnywhere
✅ SMS capability included
✅ Marketing automation features

### Setup:

1. Sign up: https://www.brevo.com/
2. Get SMTP credentials: Settings → SMTP & API → SMTP
3. Update WSGI:

```python
# Email Configuration - Brevo
os.environ['EMAIL_BACKEND'] = 'django.core.mail.backends.smtp.EmailBackend'
os.environ['EMAIL_HOST'] = 'smtp-relay.brevo.com'
os.environ['EMAIL_PORT'] = '587'
os.environ['EMAIL_USE_TLS'] = 'True'
os.environ['EMAIL_HOST_USER'] = 'your_brevo_email@gmail.com'
os.environ['EMAIL_HOST_PASSWORD'] = 'your_brevo_smtp_key'
os.environ['DEFAULT_FROM_EMAIL'] = 'Agnivridhi CRM <noreply@agnivridhiindia.com>'
```

---

## 🥉 Alternative 3: Amazon SES (AWS)

### Why Amazon SES?
✅ Cheapest for high volume: $0.10 per 1,000 emails
✅ Extremely reliable
✅ Part of AWS ecosystem

### Cons:
❌ Requires AWS account
❌ More complex setup
❌ No free tier (but very cheap)

---

## 📊 Comparison Table

| Service | Free Emails/Day | Free Emails/Month | Deliverability | Setup Difficulty | Best For |
|---------|----------------|-------------------|----------------|-----------------|----------|
| **SendGrid** | 100 | ~3,000 | ⭐⭐⭐⭐⭐ | Easy | **Production CRM** |
| **Brevo** | 300 | 9,000 | ⭐⭐⭐⭐ | Easy | High volume free |
| **Mailgun** | 33 (1K/mo) | 1,000 | ⭐⭐⭐⭐⭐ | Medium | Developers |
| **Gmail** | ~500 | ~15,000 | ⭐⭐⭐ | Very Easy | Testing only |
| **Amazon SES** | N/A | Pay-per-use | ⭐⭐⭐⭐⭐ | Hard | Enterprise |

---

## 🎯 My Recommendation for Agnivridhi CRM

### Use SendGrid because:
1. **Professional**: No "via Gmail" labels
2. **Reliable**: Industry standard for transactional emails
3. **Free tier sufficient**: 100 emails/day = 3,000/month
4. **Easy domain setup**: Can use noreply@agnivridhiindia.com properly
5. **Analytics**: See delivery rates, opens, clicks
6. **Scalable**: Easy to upgrade when you grow

### For your use case (client onboarding emails):
- **100 emails/day** = enough for **100 new clients/day**
- If you onboard 10 clients/day, you'll never hit the limit
- No "sent from Gmail" stigma for professional clients

---

## 🚀 Quick Start with SendGrid (Recommended)

### Step 1: Sign up (2 minutes)
https://signup.sendgrid.com/

### Step 2: Get API Key (1 minute)
1. Dashboard → Settings → API Keys
2. Create API Key → Full Access
3. Copy the key (starts with `SG.`)

### Step 3: Update PythonAnywhere WSGI (2 minutes)
```python
os.environ['EMAIL_HOST'] = 'smtp.sendgrid.net'
os.environ['EMAIL_HOST_USER'] = 'apikey'
os.environ['EMAIL_HOST_PASSWORD'] = 'SG.your_api_key_here'
```

### Step 4: Reload & Test (1 minute)
- Reload web app
- Create a test client
- Email sent! 🎉

---

## 💡 Pro Tips

### For Best Deliverability:
1. **Verify your domain** (agnivridhiindia.com) in SendGrid
2. Add SPF, DKIM, DMARC records to DNS
3. Use a real "from" email: noreply@agnivridhiindia.com
4. Don't use free email addresses in "From" field

### For Testing:
- Use Gmail initially (already configured)
- Switch to SendGrid for production
- Keep Gmail as backup

### For Scaling:
- SendGrid: Free → $20/mo for 50K emails
- Or use Amazon SES: $0.10/1000 emails (cheapest at scale)

---

## ⚡ Want Me to Set Up SendGrid for You?

I can:
1. Generate the exact WSGI config with SendGrid
2. Show you exactly where to paste it
3. Help you verify your domain
4. Test the email sending

Just let me know if you want to proceed with SendGrid!
