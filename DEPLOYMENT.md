# Schooloo AI - Deployment Guide

## 🚀 Deployment Steps

### Part 1: Deploy Backend on Render

#### Prerequisites:
- Render account (https://render.com)
- GitHub repository with the code
- Google Gemini API key

#### Steps:
1. **Push code to GitHub**
   ```bash
   git add -A
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Create Render Web Service**
   - Go to https://dashboard.render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Use these settings:
     - **Name**: `schooloo-ai-backend`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python backend/app.py`

3. **Set Environment Variables**
   - In Render dashboard, go to Environment
   - Add:
     - `API_KEY`: Your Google Gemini API key
     - `AGENT_MODEL`: `gemini-2.0-flash`
     - `FLASK_ENV`: `production`

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)
   - Your backend URL will be: `https://schooloo-ai-backend.onrender.com`

---

### Part 2: Deploy Frontend on Vercel

#### Prerequisites:
- Vercel account (https://vercel.com)
- GitHub repository

#### Steps:
1. **Go to Vercel Dashboard**
   - https://vercel.com/dashboard
   - Click "Add New" → "Project"

2. **Import GitHub Repository**
   - Select your Schooloo repository
   - Choose "Import"

3. **Configure Project**
   - **Framework**: Static Site (HTML)
   - **Root Directory**: `.`
   - **Build Command**: `echo 'Static site - no build needed'`
   - **Output Directory**: `frontend`

4. **Set Environment Variables** (if needed)
   - `BACKEND_URL`: `https://schooloo-ai-backend.onrender.com`

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment (1-2 minutes)
   - Your frontend URL will be: `https://schooloo.vercel.app`

---

### Part 3: Update Frontend to Use Production Backend

Update your `frontend/index.html` to point to the Render backend:

```javascript
const API_BASE_URL = 'https://schooloo-ai-backend.onrender.com/api';
```

Or use environment variable:

```javascript
const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:5002/api';
```

---

## 🔗 Final URLs

- **Frontend**: https://schooloo.vercel.app
- **Backend API**: https://schooloo-ai-backend.onrender.com/api
- **API Endpoints**:
  - POST `/api/chat` - Send queries
  - GET `/api/schools` - Get school list

---

## ⚠️ Important Notes

1. **Render Free Tier**: Services spin down after 15 minutes of inactivity. For production, upgrade to paid plan.
2. **API Key**: Keep your `API_KEY` secret! Never commit it to GitHub.
3. **CORS**: Both services have CORS enabled for cross-origin requests.
4. **Backend Start Time**: First request may take 10-30 seconds on free tier (cold start).

---

## 🛠️ Troubleshooting

### Backend not responding:
1. Check Render logs: Dashboard → Service → Logs
2. Verify `API_KEY` is set
3. Restart the service

### Frontend can't reach backend:
1. Check browser console for CORS errors
2. Verify backend URL in frontend code
3. Ensure backend service is running

### Build fails:
1. Check logs on both platforms
2. Ensure all dependencies are in `requirements.txt`
3. Verify Python version compatibility

---

## 📝 Quick Commands

```bash
# Test locally before deployment
python3 backend/app.py

# Push changes to GitHub
git add -A
git commit -m "Update: [Your changes]"
git push origin main

# Check deployment status
# Vercel: https://vercel.com/dashboard
# Render: https://dashboard.render.com
```
