# 🎓 Schooloo AI Agent - GitHub & Vercel Deployment Guide

This is the **Schooloo AI School Discovery Agent** - a powerful Flask-based AI chatbot that helps users find perfect schools across India using Google's Gemini AI.

## 📋 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup & Installation](#setup--installation)
- [Local Development](#local-development)
- [Vercel Deployment](#vercel-deployment)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

- 🤖 **AI-Powered Search**: Uses Google Gemini 2.0 Flash for intelligent school recommendations
- 🌍 **Pan-India Coverage**: Find schools across all major Indian cities
- 💡 **Smart Filtering**: Filter by location, budget, curriculum (CBSE/ICSE/State), specializations
- ⚡ **Real-time Streaming**: Stream responses for interactive chat experience
- 🎯 **Quick Actions**: Pre-built quick-action buttons for common queries
- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- 🔒 **Privacy First**: No user data stored; conversations are ephemeral

---

## 🛠 Tech Stack

**Backend:**
- Python 3.11+
- Flask 3.0+
- Google Generative AI (Gemini 2.0 Flash)
- Flask-CORS for cross-origin requests

**Frontend:**
- Vanilla HTML5, CSS3, JavaScript
- No external frameworks (lightweight, fast)
- Responsive gradient design with animations

**Deployment:**
- Vercel (serverless functions + static hosting)
- GitHub (source control)

---

## 📦 Setup & Installation

### Prerequisites
- Python 3.11 or higher
- Git
- GitHub account (for version control)
- Vercel account (for deployment) - [Sign up free](https://vercel.com/signup)
- Google API key for Gemini 2.0 Flash - [Get API key](https://ai.google.dev/)

### Step 1: Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/schooloo-agent.git
cd schooloo-agent
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
```bash
# Copy the example .env file
cp .env.example .env

# Edit .env and add your Google API key
nano .env  # or use your preferred editor
```

Add your Google API key:
```env
API_KEY=your_google_gemini_api_key_here
AGENT_MODEL=gemini-2.0-flash
FLASK_PORT=5000
```

### Step 5: Run Locally
```bash
./run_frontend.sh
# or manually:
python3 app.py
```

Visit: http://localhost:5000

---

## 🚀 Local Development

### Start the Flask Backend
```bash
FLASK_PORT=5000 python3 app.py
```

The API will be available at `http://localhost:5000`

### API Endpoints
- `GET /` - Serves the frontend (index.html)
- `GET /api/health` - Health check
- `POST /api/chat` - Send message and get response
- `POST /api/chat/stream` - Stream responses (SSE)
- `GET /api/models` - List available models
- `GET /api/info` - Get API information

### Test with curl
```bash
# Health check
curl http://localhost:5000/api/health

# Send a message
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Best CBSE schools in Delhi"}'
```

---

## 🌐 Vercel Deployment

### Step 1: Push to GitHub

If not already done, create a new GitHub repository and push your code:

```bash
# Initialize git (if not done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Schooloo AI Agent"

# Add remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/schooloo-agent.git

# Push to main branch
git branch -M main
git push -u origin main
```

### Step 2: Connect to Vercel

1. **Sign in to Vercel**: https://vercel.com/dashboard
2. **Click "New Project"**
3. **Select "Import Git Repository"**
4. **Paste your GitHub repo URL**: `https://github.com/YOUR_USERNAME/schooloo-agent.git`
5. **Authorize Vercel** to access your GitHub account
6. **Select the repository** and click "Import"

### Step 3: Configure Environment Variables

In the Vercel project dashboard:

1. Go to **Settings** → **Environment Variables**
2. Add the following variables:
   - `API_KEY`: Your Google Gemini API key
   - `AGENT_MODEL`: `gemini-2.0-flash`
   - `FLASK_ENV`: `production`

3. Click **Save**

### Step 4: Deploy

Vercel will automatically:
1. Detect Python runtime
2. Install dependencies from `requirements.txt`
3. Deploy the Flask app to serverless functions
4. Serve the static `index.html` frontend

**Your app will be live at**: `https://schooloo-agent.vercel.app` (or your custom domain)

---

### Deploy Updates

Every time you push to GitHub, Vercel automatically redeploys:

```bash
# Make changes
nano app.py

# Commit and push
git add .
git commit -m "Update: Add new feature"
git push origin main
```

Vercel will automatically rebuild and redeploy within 1-2 minutes.

---

## 🔐 Environment Variables

### Required
- `API_KEY`: Your Google Gemini API key (get from [ai.google.dev](https://ai.google.dev/))
- `AGENT_MODEL`: Model name (default: `gemini-2.0-flash`)

### Optional
- `FLASK_PORT`: Port for local development (default: 5000)
- `FLASK_ENV`: Set to `production` on Vercel

**Never commit `.env` to GitHub!** It's in `.gitignore` by default.

---

## 📚 API Endpoints

### POST `/api/chat`
Send a message and get a response.

**Request:**
```json
{
  "message": "Best CBSE schools in Mumbai under ₹50000"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Here are the best CBSE schools in Mumbai...",
  "model": "gemini-2.0-flash"
}
```

### GET `/api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "online",
  "message": "Schooloo AI Backend is running",
  "model": "gemini-2.0-flash"
}
```

### GET `/api/models`
Get available models.

**Response:**
```json
{
  "available_models": ["gemini-2.0-flash"],
  "active_model": "gemini-2.0-flash"
}
```

---

## 🐛 Troubleshooting

### "Could not reach the server" error
- ✅ Check backend is running: `curl http://localhost:5000/api/health`
- ✅ Verify port is not in use: `lsof -i :5000` (macOS/Linux)
- ✅ Check CORS is enabled (Flask-CORS is configured in app.py)
- ✅ Verify API_BASE_URL in frontend matches backend port

### "API key not found" error
- Ensure `API_KEY` is set in `.env` file
- On Vercel, verify environment variables in Settings → Environment Variables

### "Rate limit exceeded" (429 error)
- Google Gemini has rate limits; wait a moment and retry
- Check quota: `grep -r "quota\|429" logs/`

### Vercel deployment fails
- Check build logs: Vercel Dashboard → Deployments → Failed deployment → Logs
- Ensure `requirements.txt` has all dependencies
- Verify Python version is 3.11+: `python3 --version`

---

## 📝 Project Structure

```
schooloo-agent/
├── app.py                 # Main Flask application
├── index.html            # Frontend (served at /)
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment file
├── .gitignore           # Git ignore rules
├── vercel.json          # Vercel configuration
├── api/
│   └── index.py         # Serverless handler for Vercel
├── agent/               # AI agent modules
│   ├── schooloo_agent.py
│   ├── query_processor.py
│   └── tools.py
├── backend/             # Additional backend modules
│   ├── app.py
│   ├── config.py
│   └── database.py
└── docs/               # Documentation files
    ├── API_EXAMPLES.md
    ├── README_FRONTEND.md
    └── GETTING_STARTED.md
```

---

## 🎯 Next Steps

1. **Customize the system prompt** in `app.py` to match your use case
2. **Add more quick actions** in `index.html` (line ~530)
3. **Style the frontend** - modify CSS in `index.html` `<style>` section
4. **Extend the API** - add new endpoints as needed
5. **Monitor usage** - set up Vercel Analytics and logs

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 💬 Support

- **Documentation**: See `/docs` folder for detailed guides
- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions

---

**Made with ❤️ by Schooloo Team**

**Happy School Hunting! 🎓**
