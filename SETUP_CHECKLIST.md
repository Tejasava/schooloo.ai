# 📋 COMPLETE SETUP CHECKLIST

## ✅ What's Already Done For You

- [x] API Key configured in `.env` file
- [x] All Python dependencies installed
- [x] Backend Flask server configured
- [x] Frontend HTML/CSS/JS ready
- [x] API endpoint routing fixed
- [x] CORS enabled for cross-port communication
- [x] Startup automation script created (`start_local.sh`)
- [x] Error handling and fallbacks implemented
- [x] Project is **100% Ready to Run** ✅

---

## 🎯 What You Need to Do

### **The Easiest Way (Just 4 Steps)**

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  STEP 1: Open VS Code                                      │
│  └─ File → Open Folder → schooloo.ai-main                  │
│                                                             │
│  STEP 2: Open Terminal                                     │
│  └─ Press Ctrl + ` (backtick)                              │
│                                                             │
│  STEP 3: Run the startup command                           │
│  └─ Type: bash start_local.sh                              │
│     Press: Enter                                           │
│                                                             │
│  STEP 4: Open in Browser                                   │
│  └─ Go to: http://localhost:8000                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### **That's It! You're Ready!** 🚀

---

## 📝 Detailed Step-by-Step

### **Opening the Project**

1. Launch VS Code
2. Click the **File** menu at the top
3. Select **Open Folder**
4. Navigate to: `/Users/tejasavayadav/Desktop/schooloo.ai-main`
5. Click the **Open** button

You should now see the project files in the left sidebar.

---

### **Opening the Terminal**

Inside VS Code:

**Method 1 (Keyboard):**
- Press: `Ctrl + `` (Control + Backtick)

**Method 2 (Menu):**
- Click: Terminal menu → New Terminal

**Method 3 (Mouse):**
- Look at the bottom of VS Code
- Click the Terminal tab

A terminal window will appear at the bottom of VS Code.

---

### **Starting the Application**

In the terminal, type:
```bash
bash start_local.sh
```

Then press **Enter**.

**You should see output like:**
```
🚀 Starting Schooloo AI...

✅ Backend server is running!
   URL: http://localhost:5002
   Status: RUNNING

✅ Frontend server is running!
   URL: http://localhost:8000
   Status: RUNNING

🎉 Application is ready!
   Open http://localhost:8000 in your browser
```

---

### **Opening in Your Browser**

**In VS Code (Easiest):**
- Look for the URL in the terminal output
- Click on `http://localhost:8000`

**In Your Browser:**
1. Open Chrome, Safari, Firefox, or Edge
2. In the address bar, type: `http://localhost:8000`
3. Press Enter

You should see a clean chatbot interface.

---

### **Testing the Application**

1. Click in the **message input box** at the bottom
2. Type a question like:
   ```
   What are the best schools in Mumbai?
   ```
3. Press **Enter** or click the **Send** button
4. Wait 5-10 seconds for the response

**You should see:**
- School names
- Fees in rupees (₹)
- Board information (CBSE/ICSE)
- Facilities available
- NO error messages ✅

---

## 🧪 Example Queries

Try asking:

| Question | What You'll Get |
|----------|-----------------|
| "Best schools in Delhi under 50000 fees" | Schools with fees, location, facilities |
| "ICSE schools in Mumbai" | Schools in Mumbai with ICSE board |
| "Girls schools in Prayagraj" | Schools for girls in that city |
| "International schools in Bangalore" | Schools with international curriculum |
| "How to get admission in a school?" | General admission guidance |

---

## 🛑 How to Stop

### **If using the automated script:**
1. Go to the terminal where you ran `bash start_local.sh`
2. Press `Ctrl + C` (Control + C)
3. You'll see: "Shutting down..."

### **If using manual terminals:**
1. Click on Terminal 1 (Backend)
2. Press `Ctrl + C`
3. Click on Terminal 2 (Frontend)
4. Press `Ctrl + C`

---

## ⚠️ If Something Goes Wrong

### **Error: "Could not reach server"**

```bash
# Kill all processes
pkill -9 -f "python3" || true

# Wait
sleep 2

# Restart
bash start_local.sh
```

### **Error: "Address already in use"**

```bash
# Find and kill the process using the port
lsof -i :5002 | grep -v COMMAND | awk '{print $2}' | xargs kill -9
lsof -i :8000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9

# Restart
bash start_local.sh
```

### **Error: "No module named 'flask'"**

```bash
# Install dependencies
pip3 install -r requirements.txt

# Then restart
bash start_local.sh
```

### **Nothing appears to happen**

```bash
# Check if servers are running
ps aux | grep python3

# You should see 2 Python processes
# If not, manually start them:

# Terminal 1:
FLASK_PORT=5002 python3 app.py

# Terminal 2 (new terminal):
cd /Users/tejasavayadav/Desktop/schooloo.ai-main
python3 -m http.server 8000
```

---

## 📊 System Check Commands

**Check 1: Verify API Key**
```bash
cat .env | grep API_KEY
```
Expected: `API_KEY=AIzaSyAUkQPWJFcLCD9ssIkvh7t7fnxDJR6t7J8`

**Check 2: Verify Servers Running**
```bash
ps aux | grep python3
```
Expected: 2 Python processes (backend and frontend)

**Check 3: Verify Backend Responding**
```bash
curl http://localhost:5002/api/health
```
Expected: JSON response with `"status": "online"`

**Check 4: Verify Frontend Accessible**
```bash
curl http://localhost:8000 | head -20
```
Expected: HTML content of index.html

---

## 🎓 What's Running

| Component | Port | Technology | Status |
|-----------|------|------------|--------|
| **Backend API** | 5002 | Flask + Python | ✅ Running |
| **Frontend UI** | 8000 | HTML/CSS/JavaScript | ✅ Running |
| **AI Model** | API | Google Gemini 2.0 Flash | ✅ Configured |
| **Database** | N/A | In-Memory (No setup needed) | ✅ Ready |

---

## 📱 Important URLs

| URL | Purpose |
|-----|---------|
| `http://localhost:8000` | **Main App** - Open this in browser |
| `http://localhost:5002/api/chat` | API endpoint for queries |
| `http://localhost:5002/api/health` | Server health check |

---

## ✨ Features Available

✅ Search schools by city  
✅ Filter by budget/fees  
✅ Filter by board (CBSE/ICSE)  
✅ Filter by special preferences  
✅ Get facility information  
✅ Admission guidance  
✅ School comparison  
✅ Real-time AI responses  

---

## 📚 Files You Need to Know About

| File | Purpose | Status |
|------|---------|--------|
| `.env` | Configuration (API Key, Port) | ✅ Ready |
| `app.py` | Backend Flask server | ✅ Ready |
| `index.html` | Frontend interface | ✅ Ready |
| `start_local.sh` | Startup automation | ✅ Ready |
| `requirements.txt` | Python dependencies | ✅ Ready |

---

## 🎉 You're All Set!

Everything is configured and ready to use. Just:

1. **Open VS Code**
2. **Press Ctrl + `` to open terminal**
3. **Type `bash start_local.sh`**
4. **Open `http://localhost:8000`**
5. **Ask your first question!**

---

**Last Updated:** 20 November 2025  
**Created for:** Smooth local development  
**Status:** ✅ Production Ready
