# 📱 Vercel Deployment - Step by Step Instructions

## 🎯 Your Goal: Get Your Project Live on the Internet

After deployment, anyone can access your app at a public URL like:
```
https://schooloo-ai.vercel.app
```

---

## 📋 What You Need (All FREE)

1. **GitHub Account** - To store your code
   - Sign up at: https://github.com/signup

2. **Vercel Account** - To deploy your project
   - Sign up at: https://vercel.com/signup

---

## 🚀 STEP-BY-STEP DEPLOYMENT

### **PHASE 1: Create GitHub Account & Push Code**

#### **Step 1A: Create GitHub Account** (5 minutes)

1. Go to: https://github.com/signup
2. Enter your email
3. Create password
4. Choose username (e.g., `your-name`)
5. Click: **Create account**
6. Verify your email

#### **Step 1B: Create Repository on GitHub** (2 minutes)

1. Go to: https://github.com/new
2. **Repository name**: `schooloo-ai`
3. **Description**: "Schooloo AI - School Discovery Assistant"
4. **Public** (required for Vercel)
5. Click: **Create repository**

#### **Step 1C: Push Your Code to GitHub** (5 minutes)

In your terminal (in the schooloo.ai-main folder):

```bash
cd /Users/tejasavayadav/Desktop/schooloo.ai-main

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Schooloo AI project"

# Add your GitHub repository (replace USERNAME)
git remote add origin https://github.com/USERNAME/schooloo-ai.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**You'll be asked for:**
- GitHub username
- GitHub password (or token)

✅ **After this, your code is on GitHub!**

---

### **PHASE 2: Deploy to Vercel**

#### **Step 2A: Create Vercel Account** (5 minutes)

1. Go to: https://vercel.com/signup
2. Click: **Continue with GitHub**
3. Authorize Vercel to access GitHub
4. Verify your email

#### **Step 2B: Deploy Your Project** (3 minutes)

1. Log in to Vercel: https://vercel.com
2. Click: **New Project**
3. Click: **Continue with GitHub**
4. Find your `schooloo-ai` repository
5. Click: **Import**

#### **Step 2C: Configure Project**

When Vercel asks for settings:

**Root Directory:**
- Leave as: `./`

**Framework Preset:**
- Select: **Other** (we're using Flask, not Next.js)

**Environment Variables:**
- Click: **Add Environment Variables**
- Add these 3 variables:

| Variable Name | Value |
|---|---|
| `API_KEY` | `AIzaSyAUkQPWJFcLCD9ssIkvh7t7fnxDJR6t7J8` |
| `FLASK_ENV` | `production` |
| `FLASK_PORT` | `5002` |

#### **Step 2D: Click Deploy**

1. Click: **Deploy**
2. Wait 2-3 minutes for build to complete
3. You'll see: **"Deployment Complete!"**
4. You'll get a URL like: `https://schooloo-ai.vercel.app`

✅ **Your app is now live!**

---

## 📍 Your Public URL

After deployment, your app will be at:

```
https://schooloo-ai.vercel.app
```

**Share this link with anyone!**

---

## ✅ Test Your Deployment

1. Open the Vercel URL in your browser
2. You should see the Schooloo AI chatbot
3. Try asking a question
4. You should get a response

---

## 🔗 Useful Links

| Link | Purpose |
|------|---------|
| `https://github.com/USERNAME/schooloo-ai` | Your GitHub repo |
| `https://vercel.com/dashboard` | Vercel dashboard |
| `https://schooloo-ai.vercel.app` | Your live app |

---

## ⚠️ Important Notes

### **Frontend vs Backend**

- **Frontend** (HTML/CSS/JS) → Deploys on Vercel ✅
- **Backend** (Flask API) → May need separate hosting

If backend doesn't work on Vercel, use:
- **Render.com** (Free tier)
- **Railway.app** (Free credits)
- **Heroku** (Paid)
- **Google Cloud Run** (Free tier)

### **For Just Frontend Deployment**

If you want to deploy ONLY the frontend to Vercel:

1. Create separate folder with just `index.html`
2. Update API endpoint in HTML to point to separate backend
3. Deploy frontend to Vercel
4. Deploy backend to different service

---

## 🔄 How Updates Work

Once your project is on GitHub and Vercel:

**To make changes:**
1. Edit files locally
2. Push to GitHub: `git push origin main`
3. Vercel automatically redeploys
4. Your URL updates automatically

---

## 💡 Next Steps After Deployment

1. **Test the app** at your Vercel URL
2. **Share with friends** - Give them your URL
3. **Make updates** - Git push whenever you change code
4. **Monitor** - Check Vercel dashboard for issues

---

## 🆘 If Deployment Fails

### **Error: "Build Failed"**

In Vercel dashboard:
1. Click: **Deployments** tab
2. Click: Failed deployment
3. Look at build log
4. Common issues:
   - Missing dependencies (add to requirements.txt)
   - Python version (Vercel uses Python 3.9+)
   - Environment variables not set

### **Error: "App loads but no responses"**

Backend might not be deployed:
1. Check Vercel logs
2. Consider separate backend hosting
3. Update API endpoint in HTML

---

## 📞 Support

- **Vercel Help**: https://vercel.com/support
- **GitHub Help**: https://github.com/support
- **Render.com** (for backend): https://render.com

---

## Summary

```
Local Development → GitHub → Vercel → Live on Internet
    (Your PC)      (Code)   (Deploy)   (Public URL)
```

**You now have:**
- ✅ Code stored on GitHub
- ✅ App deployed on Vercel
- ✅ Public URL anyone can access
- ✅ Automatic updates when you push code

---

**Congratulations! Your Schooloo AI is now online! 🎉**

Visit your app at: `https://schooloo-ai.vercel.app`

(Replace `schooloo-ai` with your actual project name if different)
