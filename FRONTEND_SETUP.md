# 🎓 Schooloo AI - Frontend Setup Guide

## 📋 Prerequisites

Make sure you have:
- Python 3.8+
- Flask and Flask-CORS installed
- Google Generative AI library
- A web browser
- The `schooloo.png` logo file in the same directory

## 🚀 Quick Setup

### Step 1: Install Required Python Packages

```bash
pip install flask flask-cors google-generativeai python-dotenv
```

### Step 2: Configure Environment

Make sure your `.env` file has:
```
API_KEY=your_google_api_key_here
AGENT_MODEL=gemini-2.0-flash
FLASK_PORT=5000
FLASK_DEBUG=true
```

### Step 3: Prepare Files

Make sure you have these files in the `/tmp/schooloo-agent/` directory:

```
/tmp/schooloo-agent/
├── index.html          (Frontend UI)
├── app.py             (Flask Backend)
├── schooloo.png       (Logo image)
├── .env               (Configuration)
└── interactive_agent.py (Python agent)
```

## 🎯 Running the Application

### Option 1: Run the Flask Backend (Recommended)

```bash
cd /tmp/schooloo-agent
python3 app.py
```

This will:
- Start Flask server on `http://localhost:5000`
- Serve the frontend automatically
- Enable the chat API at `/api/chat`

Then open your browser and visit:
```
http://localhost:5000
```

### Option 2: Serve Frontend with Simple HTTP Server

If you want to use the Python HTTP server for frontend:

```bash
cd /tmp/schooloo-agent
python3 -m http.server 8000
```

Then open:
```
http://localhost:8000
```

But you'll need to start the API separately:

```bash
# In another terminal
cd /tmp/schooloo-agent
python3 app.py
```

## 📱 Using the Application

### Via Frontend UI

1. Open `http://localhost:5000` in your browser
2. Click on the Schooloo AI logo to see the chat interface
3. Type your questions in the input box:
   - "Help me finding best school at prayagraj"
   - "What schools are in Delhi under 2 lakhs?"
   - "CBSE schools in Mumbai"
4. Click send button (📤) or press Enter

### Via Quick Start Buttons

Click the quick-start buttons on the right sidebar:
- Schools in Prayagraj
- Delhi Schools
- Mumbai CBSE
- Bangalore Schools

### Command Line (Alternative)

For pure CLI experience:

```bash
cd /tmp/schooloo-agent

# Interactive mode
python3 interactive_agent.py

# Test mode (3 automatic queries)
python3 test_agent.py

# Piped input
echo "help me finding best school at prayagraj" | python3 interactive_agent.py
```

## 🔧 API Endpoints

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Send Message
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "help me finding best school at prayagraj"}'
```

### Get Models
```bash
curl http://localhost:5000/api/models
```

### Get Info
```bash
curl http://localhost:5000/api/info
```

## 🎨 Customizing the Frontend

### Change Colors

Edit the CSS variables in `index.html`:

```css
:root {
    --primary: #1e88e5;        /* Main blue color */
    --primary-dark: #1565c0;   /* Dark blue */
    --accent: #ff6f00;         /* Orange accent */
    /* ... more colors ... */
}
```

### Add New Quick Questions

In `index.html`, find the quick questions section and add:

```html
<button class="quick-btn" onclick="sendQuickMessage('your question here')">
    Question Label
</button>
```

### Change Welcome Message

Edit the bot message in the messages container:

```html
<div class="message bot">
    <div class="message-content">
        Your custom welcome message here
    </div>
</div>
```

## 🐛 Troubleshooting

### Issue: "Port 5000 already in use"

Change the port in `.env`:
```
FLASK_PORT=8000
```

Or kill the existing process:
```bash
lsof -ti:5000 | xargs kill -9
```

### Issue: "API_KEY not found"

Make sure `.env` file exists and has:
```
API_KEY=your_actual_api_key_here
```

### Issue: "schooloo.png not found"

Add the logo image to the directory or update the image path in `index.html`:

```html
<img src="your-image-path.png" alt="Schooloo Logo">
```

### Issue: Frontend loads but chat doesn't work

1. Check if Flask backend is running: `http://localhost:5000/api/health`
2. Check browser console (F12) for errors
3. Make sure CORS is enabled (flask-cors is installed)
4. Verify API_KEY is valid

### Issue: Quota Exceeded (429 Error)

This means daily API limit reached:
1. Wait 24 hours for quota reset
2. Upgrade to paid plan: https://console.cloud.google.com
3. Use offline demo: `python3 demo_agent.py`

## 📊 Features

✅ **Real-time Chat**
- Instant responses powered by Google Gemini
- City-specific school recommendations

✅ **Beautiful UI**
- Responsive design (works on mobile, tablet, desktop)
- Gradient backgrounds and smooth animations
- Modern card-based layout

✅ **Smart Recommendations**
- AI-powered personalized suggestions
- Real school names and data
- Fee structures and facilities

✅ **Multi-City Support**
- 100+ Indian cities covered
- Prayagraj, Delhi, Mumbai, Bangalore, and more

✅ **Interactive Features**
- Quick-start buttons
- Typing indicators
- Message formatting
- Smooth animations

## 🔐 Security Notes

- Keep your API_KEY private and never commit it to version control
- Use environment variables for sensitive data
- Enable CORS only for trusted domains in production
- Rate limit the API in production

## 📈 Performance Tips

1. **Caching**: Consider caching common queries
2. **Lazy Loading**: Load features on demand
3. **CDN**: Use CDN for static assets in production
4. **Database**: Store conversation history in database for persistence

## 🚀 Deployment

### Local Development

```bash
python3 app.py
# Access at http://localhost:5000
```

### Production Deployment

Use production WSGI server:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Or with Heroku:

```bash
git push heroku main
```

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review browser console errors (F12)
3. Check Flask terminal output
4. Verify API key and internet connection

## 🎉 You're All Set!

Your Schooloo AI Frontend is now ready to use!

Visit: **http://localhost:5000**

Enjoy finding the perfect school! 🎓✨
