# 🚀 SCHOOLOO AI - COMPLETE DEPLOYMENT GUIDE

## Step-by-Step Deployment Instructions

### ✅ Prerequisites
- [ ] GitHub account with the repository pushed
- [ ] Google Gemini API key (from https://makersuite.google.com/app/apikey)
- [ ] Render account (https://render.com)
- [ ] Vercel account (https://vercel.com)

---

## 🔧 PART 1: RENDER DEPLOYMENT (BACKEND)

### Step 1: Push Code to GitHub

```bash
cd /Users/tejasavayadav/Desktop/"git hub projects"/schooloo.ai-main
git add -A
git commit -m "Deploy: Schooloo AI Backend"
git push origin main
```

### Step 2: Create Render Web Service

1. Go to **https://dashboard.render.com**
2. Click **"New +"** button
3. Select **"Web Service"**
4. Connect your GitHub account if not already done
5. Search for and select the **Schooloo repository**

### Step 3: Configure Render Service

Fill in the configuration form:

| Setting | Value |
|---------|-------|
| **Name** | `schooloo-ai-backend` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python backend/app.py` |
| **Region** | Choose closest to you |
| **Plan** | `Free` (or paid for production) |

### Step 4: Set Environment Variables

In Render dashboard → Environment section, add:

| Key | Value |
|-----|-------|
| `API_KEY` | Your Google Gemini API key |
| `AGENT_MODEL` | `gemini-2.0-flash` |
| `FLASK_ENV` | `production` |
| `FLASK_PORT` | `5002` |

**⚠️ Important**: Paste your Gemini API key from https://makersuite.google.com/app/apikey

### Step 5: Deploy

1. Click **"Create Web Service"** button
2. Wait 2-3 minutes for deployment
3. Once deployed, you'll see a green "Live" status
4. Your backend URL: `https://schooloo-ai-backend.onrender.com`

### Step 6: Test Backend

Open in browser or terminal:
```bash
curl https://schooloo-ai-backend.onrender.com/api/
```

---

## 🎨 PART 2: VERCEL DEPLOYMENT (FRONTEND)

### Step 1: Go to Vercel Dashboard

1. Visit **https://vercel.com/dashboard**
2. Click **"Add New"** → **"Project"**

### Step 2: Import GitHub Repository

1. Click **"Import Project"**
2. Paste GitHub URL: `https://github.com/Tejasava/schooloo.ai-main`
3. Click **"Import"** (or connect GitHub if not already done)

### Step 3: Configure Project

Leave default settings OR configure as:

| Setting | Value |
|---------|-------|
| **Framework Preset** | `Other` or `HTML` |
| **Root Directory** | `.` |
| **Build Command** | (Leave empty or `echo 'Static'`) |
| **Output Directory** | `frontend` |

### Step 4: Set Environment Variables (Optional)

If your frontend needs backend URL:

| Key | Value |
|-----|-------|
| `NEXT_PUBLIC_BACKEND_URL` | `https://schooloo-ai-backend.onrender.com` |

### Step 5: Deploy

1. Click **"Deploy"** button
2. Wait 1-2 minutes for deployment
3. Once deployed, click **"Visit"** to view your site
4. Your frontend URL: `https://schooloo-ai-main.vercel.app`

---

## 🔗 PART 3: CONNECT FRONTEND TO BACKEND

### Update Frontend API URL

Edit `frontend/index.html` and find the API configuration:

**Current (Local Development):**
```javascript
const API_BASE_URL = 'http://localhost:5002/api';
```

**Update to Production:**
```javascript
const API_BASE_URL = 'https://schooloo-ai-backend.onrender.com/api';
```

OR use environment variable:
```javascript
const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://schooloo-ai-backend.onrender.com/api';
```

### Push Changes

```bash
git add frontend/index.html
git commit -m "Update: Backend API URL to production"
git push origin main
```

**Vercel will automatically redeploy!** ✅

---

## ✨ FINAL URLS

| Component | URL |
|-----------|-----|
| **Frontend** | https://schooloo-ai-main.vercel.app |
| **Backend API** | https://schooloo-ai-backend.onrender.com |
| **API Chat Endpoint** | https://schooloo-ai-backend.onrender.com/api/chat |

---

## 🧪 Testing

### Test Backend API

```bash
# Test if backend is running
curl https://schooloo-ai-backend.onrender.com/api/

# Test chat endpoint
curl -X POST https://schooloo-ai-backend.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Find schools in Prayagraj", "language": "en"}'
```

### Test Frontend

1. Visit: https://schooloo-ai-main.vercel.app
2. Try searching for a school
3. Check browser console (F12) for any errors
4. Verify API calls go to backend

---

## ⚠️ IMPORTANT NOTES

### Render Free Tier Limitations
- ❌ Services spin down after 15 minutes of inactivity
- ❌ Cold start takes 10-30 seconds on first request
- ✅ Free for testing/development
- 💰 Upgrade to paid for production reliability

### Vercel Benefits
- ✅ Free tier for frontend
- ✅ Automatic deployments on git push
- ✅ Unlimited bandwidth
- ✅ No cold start issues

### API Key Security
- 🔒 Never commit API keys to GitHub
- 🔒 Only set in platform environment variables
- 🔒 Use `.env` locally (in .gitignore)
- 🔒 Regenerate if accidentally exposed

---

## 🐛 TROUBLESHOOTING

### Backend Not Starting
**Symptoms**: Render shows "Deploy failed"
**Solutions**:
1. Check Render logs: Dashboard → Service → Logs tab
2. Verify `API_KEY` environment variable is set
3. Check if all dependencies are in `requirements.txt`
4. Restart the service

### Frontend Can't Reach Backend
**Symptoms**: Console shows CORS error or 404
**Solutions**:
1. Open browser Developer Tools (F12)
2. Check Console tab for errors
3. Check Network tab for API requests
4. Verify backend URL is correct in `index.html`
5. Ensure backend service is running

### Slow First Load
**Symptoms**: First request takes 30+ seconds
**Solutions**:
- This is normal on Render free tier (cold start)
- Upgrade to paid plan for production
- Or use a paid backend provider

### Build Fails on Vercel
**Symptoms**: Build shows "Exit with code 1"
**Solutions**:
1. Check Vercel build logs
2. Verify `package.json` has correct scripts
3. Check if static files are in correct directory
4. Try rebuilding from Vercel dashboard

---

## 📝 QUICK COMMAND REFERENCE

```bash
# Push latest changes
git add -A && git commit -m "Update" && git push origin main

# Check git status
git status

# View git log
git log --oneline -5

# Undo last commit (before push)
git reset --soft HEAD~1

# Force redeploy on Vercel
# Go to: Vercel Dashboard → Project → Deployments → Redeploy

# View Render logs
# Go to: Render Dashboard → Service → Logs
```

---

## 🎉 SUCCESS INDICATORS

✅ Backend deployed successfully when:
- Render dashboard shows "Live" status
- `curl https://schooloo-ai-backend.onrender.com/api/` returns data
- Logs show "✅ Gemini API configured successfully"

✅ Frontend deployed successfully when:
- Vercel dashboard shows "Ready"
- Can access the site in browser
- API calls reach the backend

✅ Full integration working when:
- Frontend loads with Schooloo branding
- Can search for schools
- Results appear from backend
- No console errors

---

## 🤝 Need Help?

- **Gemini API Issues**: Check https://makersuite.google.com/app/apikey
- **Render Help**: Visit https://docs.render.com
- **Vercel Help**: Visit https://vercel.com/docs
- **GitHub Issues**: Check repository issues/discussions

---

**Happy Deploying! 🚀**
