# 🚀 QUICK START: Deploy Schooloo AI to Vercel in 5 Minutes

## Step 1️⃣: Visit Vercel
Go to **https://vercel.com/dashboard**

## Step 2️⃣: Import Your Repository
1. Click **"Add New"** button (top right)
2. Select **"Project"**
3. Click **"Import Git Repository"**
4. Search: `schooloo.ai`
5. Click **"Import"**

## Step 3️⃣: Configure Environment Variables
When asked for environment variables, add:

**Variable Name:** `API_KEY`
**Value:** Paste your Google Gemini API Key

Get API Key here: https://ai.google.dev/api-keys

(If you don't have one, click the link, sign up, create a new API key, copy it)

## Step 4️⃣: Deploy
Click **"Deploy"** button

Vercel will now:
- Pull code from GitHub
- Install dependencies
- Build the project
- Deploy to production

This takes about 1-2 minutes ⏳

## Step 5️⃣: Access Your App
Once deployment is complete, you'll see:

```
✅ Deployment Successful!
Visit: https://schooloo-ai.vercel.app
```

🎉 **Your app is now LIVE!**

---

## 🧪 Test It

1. Open the URL in your browser
2. Try clicking one of the blue buttons (quick actions)
3. Or type a question and hit Send
4. Watch the AI respond!

---

## ⚠️ If It Doesn't Work

### Check 1: API Key Configured?
- Go back to Vercel Dashboard
- Click your project
- Go to **Settings** → **Environment Variables**
- Verify `API_KEY` is set with your actual key
- Click **Redeploy** (from Deployments tab)

### Check 2: GitHub Connected?
- Make sure your GitHub repo is public, OR
- Add your Vercel account as a collaborator on GitHub

### Check 3: See the Logs
- In Vercel Dashboard
- Click **Deployments** tab
- Click the latest deployment
- Click **Logs** to see what went wrong

---

## 📱 What You Just Deployed

✨ A full-stack AI chatbot that:
- Runs on Vercel's serverless infrastructure
- Uses Google Gemini AI to answer questions about schools
- Has a beautiful dark-mode chat interface
- Works on mobile and desktop
- Scales automatically with traffic

---

## 🔗 Your Deployment Links

| Component | URL |
|-----------|-----|
| **Live App** | https://schooloo-ai.vercel.app |
| **GitHub Repo** | https://github.com/Tejasava/schooloo.ai |
| **Vercel Dashboard** | https://vercel.com/dashboard |
| **API Health** | https://schooloo-ai.vercel.app/api/health |

---

## 🎯 Next Steps (Optional)

1. **Custom Domain** - Use your own domain instead of vercel.app
   - In Vercel Settings → Domains
   - Add your domain and follow DNS setup

2. **Monitoring** - Get alerts if something breaks
   - Set up monitoring in Vercel
   - Configure Slack/email notifications

3. **Analytics** - See how many people use your app
   - Add Vercel Analytics
   - Track performance metrics

---

## 📞 Support

**Stuck?** Read these files in your repo:
- `DEPLOYMENT_ON_VERCEL.md` - Detailed guide
- `VERCEL_DEPLOYMENT.md` - Troubleshooting
- `README.md` - General info

Or check Vercel docs: https://vercel.com/docs

---

**Congratulations!** 🎉 Your Schooloo AI is now deployed on Vercel!
