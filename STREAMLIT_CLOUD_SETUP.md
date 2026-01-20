# Streamlit Cloud Deployment - Email Setup Guide

## 🚀 Quick Setup (5 minutes)

### Why Email Isn't Working

Streamlit Cloud **blocks outbound SMTP ports** (587, 465). Our app now uses **SendGrid API** instead, which works on any platform.

---

## 📧 Step 1: Create SendGrid Account

1. Go to https://sendgrid.com
2. Click "Sign Up Free"
3. Complete registration (free tier: 100 emails/day)
4. Verify email address

---

## 🔑 Step 2: Get SendGrid API Key

1. Log in to SendGrid dashboard
2. Go to **Settings → API Keys**
3. Click **"Create API Key"**
4. Choose **Full Access**
5. Name it "TOPSIS" (or anything)
6. Click **Create & Copy**
7. **Save this key somewhere safe** (you'll need it)

---

## 🔐 Step 3: Add Secrets to Streamlit Cloud

1. Go to your Streamlit Cloud app
   - https://share.streamlit.io
2. Click your app name
3. Click **Settings** (gear icon) → **Secrets**
4. In the text area, paste:

```
SENDGRID_API_KEY = "SG.xxxxxxxxxxxxx"
SENDER_EMAIL = "your@gmail.com"
```

**Replace:**
- `SG.xxxxxxxxxxxxx` with your actual SendGrid API key
- `your@gmail.com` with your email address

5. Click **Save**

---

## ✅ Step 4: Test Email

1. Go back to your app
2. Upload a CSV file
3. Enter email address
4. Click "🚀 Run TOPSIS"
5. Click "📧 Send Results to Email"
6. Check inbox for results!

---

## 📋 Example Configuration

**What to add to Streamlit Secrets:**

```
SENDGRID_API_KEY = "SG.RtZrXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
SENDER_EMAIL = "noreply@mycompany.com"
```

---

## 🔍 Troubleshooting

### "SENDGRID_API_KEY not found"

**Problem:** You didn't add the secret to Streamlit Cloud

**Solution:**
1. Go to app settings → Secrets
2. Add `SENDGRID_API_KEY = "SG.xxxxx"`
3. Save
4. Refresh app (Cmd+R on Mac, Ctrl+R on Windows)

### "Invalid API key"

**Problem:** API key is wrong or expired

**Solution:**
1. Go to SendGrid dashboard
2. Create a new API key
3. Update in Streamlit Secrets
4. Test again

### "Email not received"

**Problem:** Check spam folder or SendGrid limits

**Solution:**
- Check spam folder first
- Free tier is 100 emails/day
- Wait 30 seconds for delivery
- Check SendGrid activity log

---

## 💡 How It Works

**Before (Broken):**
```
App → SMTP Port 587 → Gmail
      (BLOCKED on Streamlit Cloud) ❌
```

**Now (Working):**
```
App → HTTP/HTTPS Port 443 → SendGrid API → Email
      (Works everywhere) ✅
```

SendGrid handles email delivery, so it's more reliable!

---

## 📝 Summary

✅ Email working on Streamlit Cloud
✅ Free: 100 emails/day
✅ Professional delivery
✅ Automatic retry logic

**That's it! Your email system is now production-ready.** 🎉

---

## Alternative Services

If you prefer other email services:

| Service | Free Tier | Setup Time |
|---------|-----------|-----------|
| **SendGrid** (recommended) | 100/day | 5 min |
| Mailgun | 1000/month | 5 min |
| Resend | 100/day | 5 min |

All work the same way - just swap the API key!

---

## Need More Help?

Check:
1. Email correctly configured in secrets
2. SendGrid API key is valid
3. SENDER_EMAIL matches SendGrid account
4. Recipient email is valid

If still stuck, check SendGrid logs for exact error message.
