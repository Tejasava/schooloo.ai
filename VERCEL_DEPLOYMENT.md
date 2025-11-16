# 🚀 Schooloo AI - Vercel Deployment Guide

## Prerequisites
- GitHub account with your Schooloo repo pushed
- Vercel account (free at https://vercel.com)
- Google API Key for Gemini (stored in `.env`)

## Step 1: Prepare Your Repository

Your repo should already have these files (created during setup):
- ✅ `vercel.json` - Vercel configuration
- ✅ `api/index.py` - Serverless function handler
- ✅ `.env.example` - Environment variables template
- ✅ `index.html` - Frontend with dynamic API_BASE_URL

## Step 2: Connect to Vercel

### Option A: Using Vercel Dashboard (Recommended)

1. Go to https://vercel.com/dashboard
2. Click **"Add New..." → "Project"**
3. Select **"Import Git Repository"**
4. Find and select your **schooloo-agent** repository
5. Click **"Import"**

### Option B: Using Vercel CLI

```bash
npm i -g vercel
cd /path/to/schooloo.ai
vercel login
vercel
```

## Step 3: Configure Environment Variables

After importing, Vercel will ask for environment variables:

1. In Vercel Dashboard, go to your project settings
2. Click **"Environment Variables"**
3. Add the following:

| Variable | Value | Notes |
|----------|-------|-------|
| `API_KEY` | Your Google Gemini API Key | Get from https://ai.google.dev |
| `FLASK_ENV` | `production` | For production mode |
| `FLASK_PORT` | `3000` | Vercel default port |

4. Click **"Save"**

## Step 4: Deploy

**Automatic Deployment:**
- Every push to `main` branch triggers automatic deployment
- Watch deployment progress in Vercel Dashboard

**Manual Deployment:**
```bash
vercel --prod
```

## Step 5: Verify Deployment

Once deployment completes:

1. You'll get a URL like: `https://schooloo-ai.vercel.app`
2. Test the API health check:
   ```bash
   curl https://schooloo-ai.vercel.app/api/health
   ```
   Should return:
   ```json
   {
     "message": "Schooloo AI Backend is running",
     "model": "gemini-2.0-flash",
     "status": "online"
   }
   ```

3. Open the frontend in your browser:
   ```
   https://schooloo-ai.vercel.app
   ```

## Troubleshooting

### Issue: "Module not found" or import errors
**Solution:** Ensure `requirements.txt` includes all dependencies:
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements for Vercel"
git push
```

### Issue: Environment variables not loading
**Solution:** 
- Check Vercel Dashboard → Project Settings → Environment Variables
- Restart deployment: Go to Deployments tab, click the latest, then "Redeploy"

### Issue: Frontend can't reach backend API
**Solution:**
- Check `index.html` uses `window.location.origin + '/api'` for API_BASE_URL
- Open browser DevTools → Network tab, verify requests go to your Vercel domain

### Issue: 500 error on /api/chat
**Solution:**
- Check Google API Key is correctly set in environment variables
- Verify API Key has Generative Language API enabled
- Check Vercel logs: Dashboard → Deployments → Latest → Logs

## Monitoring & Logs

View real-time logs:
```bash
vercel logs <project-url> --follow
```

Or in Dashboard:
1. Go to your project
2. Click **"Deployments"** tab
3. Select the latest deployment
4. Click **"Logs"**

## Custom Domain (Optional)

To use a custom domain:
1. In Vercel Dashboard, go to **"Settings"** → **"Domains"**
2. Add your domain
3. Follow DNS configuration instructions
4. Update DNS records at your domain registrar

## Database (If Needed)

For production with persistent data:
- **Option 1:** PostgreSQL on Vercel
- **Option 2:** MongoDB Atlas (free tier)
- **Option 3:** Firebase Realtime Database

Add connection string to environment variables and update `app.py` accordingly.

## Production Best Practices

1. **CORS:** Already configured for all origins in `app.py`
2. **Error Handling:** App returns meaningful error messages
3. **Rate Limiting:** Consider adding rate limiting for API endpoints
4. **Monitoring:** Set up alerts in Vercel Dashboard

## Next Steps

After successful deployment:
- [ ] Test all quick action buttons
- [ ] Test custom chat input
- [ ] Verify API responses with different queries
- [ ] Monitor logs for errors
- [ ] Set up analytics (optional)
- [ ] Configure custom domain (optional)

## Support

For Vercel-specific issues:
- Docs: https://vercel.com/docs
- Community: https://vercel.com/help
- Status: https://status.vercel.com

For Schooloo AI issues:
- Check the logs in Vercel Dashboard
- Review `app.py` implementation
- Test locally: `FLASK_PORT=5002 python app.py`
