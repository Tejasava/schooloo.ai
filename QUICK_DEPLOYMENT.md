# ⚡ QUICK DEPLOYMENT - DO THIS NOW

## Step 1️⃣: Create Personal Access Token (2 min)

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Fill in:
   - **Name:** schooloo-ai-push
   - **Expiration:** 90 days
   - **Check:** repo + workflow
4. Click "Generate token"
5. **COPY THE TOKEN** and save it

---

## Step 2️⃣: Push to GitHub (Copy & Paste)

Replace `YOUR_TOKEN` with the token from Step 1:

```bash
git push -u https://tejasavayadav:YOUR_TOKEN@github.com/tejasavayadav/schooloo.ai.agent.git main
```

**Example (with fake token):**
```bash
git push -u https://tejasavayadav:ghp_abc123xyz789@github.com/tejasavayadav/schooloo.ai.agent.git main
```

Wait for "✓ Compressing objects" → "✓ Writing objects" → success message

---

## Step 3️⃣: Deploy to Vercel (3 min)

1. Go to: https://vercel.com/tejasava-singh-yadavs-projects
2. Click "Add New..." → "Project"
3. Click "Import Git Repository"
4. Search for and select: `schooloo.ai.agent`
5. On "Configure Project" page, add environment variables:
   
   | Name | Value |
   |------|-------|
   | API_KEY | AIzaSyAUkQPWJFcLCD9ssIkvh7t7fnxDJR6t7J8 |
   | FLASK_ENV | production |
   | FLASK_PORT | 5002 |

6. Click "Deploy"
7. Wait 2-3 minutes for build to complete

---

## Step 4️⃣: Test Your Live App (1 min)

1. Copy the Vercel URL (looks like: https://schooloo-ai-xxxxx.vercel.app)
2. Open in browser
3. Test with a query: "Best schools in Delhi under 50000 fees"
4. Should get a response (no "Could not reach server" error!)

---

## ✅ DONE! Your App is LIVE 🚀

**GitHub Repo:** https://github.com/tejasavayadav/schooloo.ai.agent
**Live App:** https://schooloo-ai-xxxxx.vercel.app (actual URL from Vercel)

---

## 📖 Need Help?

- **GitHub authentication:** See `GITHUB_SETUP_PAT.md`
- **Detailed steps:** See `DEPLOYMENT_COMPLETE_GUIDE.md`
- **Troubleshooting:** See `VERCEL_QUICK_DEPLOY.md`

---

**Total Time: ~10 minutes**

Good luck! 🎉
