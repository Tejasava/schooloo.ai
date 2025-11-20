# GitHub Setup with Personal Access Token (PAT)

## ⚠️ Important: GitHub Password Authentication Not Supported

GitHub no longer supports password authentication for git operations. You need to use a **Personal Access Token (PAT)** instead.

## Step-by-Step: Create PAT and Push Code

### Step 1: Create Personal Access Token on GitHub

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Fill in the form:
   - **Token name:** `schooloo-ai-push`
   - **Expiration:** 90 days (or choose your preference)
   - **Select scopes:** Check these boxes:
     - ☑️ `repo` (Full control of private repositories)
     - ☑️ `workflow` (Update GitHub Actions workflows)

4. Click "Generate token"
5. **COPY THE TOKEN** (it won't show again!)
   - Example token looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Step 2: Use the Token for Git Push

Replace `YOUR_TOKEN` with the token you just copied and run:

```bash
cd /Users/tejasavayadav/Desktop/schooloo.ai-main
git push -u https://tejasavayadav:YOUR_TOKEN@github.com/tejasavayadav/schooloo.ai.agent.git main
```

For example, if your token is `ghp_abc123def456`:
```bash
git push -u https://tejasavayadav:ghp_abc123def456@github.com/tejasavayadav/schooloo.ai.agent.git main
```

### Step 3: Verify Your Code is on GitHub

After successful push, visit:
```
https://github.com/tejasavayadav/schooloo.ai.agent
```

You should see all your files there! ✅

## Alternative: Store Token in Git Config (Safer)

To avoid typing the token every time:

```bash
git config --global credential.helper osxkeychain
```

Then when git asks for password, paste your token. It will be saved securely.

## ✅ After Push is Successful

Once code is on GitHub:

1. Go to https://vercel.com
2. Click "New Project"
3. Click "Import Git Repository"
4. Search for "schooloo.ai.agent"
5. Select it and follow the Vercel setup wizard
6. Add these environment variables:
   - `API_KEY` = `AIzaSyAUkQPWJFcLCD9ssIkvh7t7fnxDJR6t7J8`
   - `FLASK_ENV` = `production`
7. Click "Deploy"

Your app will be live in ~3 minutes!

## Troubleshooting

**"Invalid username or token"**
- Make sure you copied the entire token correctly
- Token must have `repo` scope enabled
- Check token hasn't expired

**"Repository not found"**
- Make sure repository `schooloo.ai.agent` exists on your GitHub
- Check username is correct (tejasavayadav)

**Need Help?**
- GitHub Docs: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
- Vercel Docs: https://vercel.com/docs

---

**Next Steps:**
1. Create PAT at https://github.com/settings/tokens
2. Copy the token
3. Run git push command with token
4. Go to Vercel and deploy
5. Share your live link! 🚀
