# 🎯 COMPLETE VISUAL GUIDE

## The Complete Flow (What Happens When You Run It)

```
┌─────────────────────────────────────────────────────────────────┐
│                    YOUR COMPUTER                                │
│                                                                  │
│  ┌──────────────┐        ┌──────────────┐  ┌──────────────┐    │
│  │  VS Code     │        │   Browser    │  │   Terminal   │    │
│  │              │        │              │  │              │    │
│  │ File Editor  │        │ Shows App    │  │ Runs server  │    │
│  └──────────────┘        └──────────────┘  └──────────────┘    │
│         │                       │                   │           │
│         └───────────────────────┼───────────────────┘           │
│                                 │                               │
│                        ┌────────▼────────┐                      │
│                        │  Local Network  │                      │
│                        │  (localhost)    │                      │
│                        └────────┬────────┘                      │
│                                 │                               │
│              ┌──────────────────┼──────────────────┐            │
│              │                  │                  │            │
│       ┌──────▼──────┐    ┌──────▼──────┐   ┌─────▼─────┐      │
│       │ Frontend     │    │  Backend API │   │ Database  │      │
│       │ Port 8000    │◄──►│  Port 5002   │   │ (in-mem)  │      │
│       │ (HTML/JS)    │    │  (Flask)     │◄──┤ (schools) │      │
│       └──────────────┘    └──────┬───────┘   └───────────┘      │
│                                  │                               │
│                          ┌───────▼────────┐                     │
│                          │ Google API     │                     │
│                          │ (Gemini AI)    │                     │
│                          └────────────────┘                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Visual Guide

### **STEP 1: Open VS Code with Schooloo Folder**

```
┌─────────────────────────────────────────────┐
│ VS Code                                     │
│                                             │
│ ┌──────────────────────────────────────┐  │
│ │ EXPLORER                      ✖      │  │
│ ├──────────────────────────────────────┤  │
│ │ 📁 schooloo.ai-main                  │  │
│ │  ├── 📄 app.py       (Backend)      │  │
│ │  ├── 📄 index.html   (Frontend)     │  │
│ │  ├── 📄 start_local.sh              │  │
│ │  ├── 📄 requirements.txt             │  │
│ │  ├── 📄 .env         (API Key) ✅    │  │
│ │  └── ...                            │  │
│ │                                      │  │
│ └──────────────────────────────────────┘  │
│                                             │
└─────────────────────────────────────────────┘
```

**What you see:**
- All project files on the left side
- Code editors in the middle
- Terminal at the bottom (if opened)

---

### **STEP 2: Open Terminal in VS Code**

```
┌─────────────────────────────────────────────┐
│ VS Code                                     │
├─────────────────────────────────────────────┤
│ EDITOR                                      │
├─────────────────────────────────────────────┤
│ TERMINAL  ^                                 │
├─────────────────────────────────────────────┤
│ tejasavayadav@... schooloo.ai-main % █     │
│                                             │
└─────────────────────────────────────────────┘
```

**Press:** `Ctrl + `` (Control + Backtick)

---

### **STEP 3: Type the Command**

```
┌─────────────────────────────────────────────┐
│ TERMINAL                                    │
├─────────────────────────────────────────────┤
│ tejasavayadav@... schooloo.ai-main % █     │
│ bash start_local.sh                         │
│                                             │
└─────────────────────────────────────────────┘
```

**Type:** `bash start_local.sh`  
**Press:** Enter

---

### **STEP 4: See the Output**

```
┌─────────────────────────────────────────────┐
│ TERMINAL OUTPUT                             │
├─────────────────────────────────────────────┤
│ ✅ Backend server is running!               │
│    URL: http://localhost:5002                │
│    Status: RUNNING (PID: 12345)             │
│                                             │
│ ✅ Frontend server is running!              │
│    URL: http://localhost:8000                │
│    Status: RUNNING (PID: 12346)             │
│                                             │
│ 🎉 Application is ready!                    │
│    Open http://localhost:8000 in browser    │
│                                             │
└─────────────────────────────────────────────┘
```

---

### **STEP 5: Open Browser & Click Link**

**Option A (Click in Terminal):**
- Click on `http://localhost:8000` in the terminal
- Browser opens automatically

**Option B (Manual):**
1. Open any browser (Chrome, Safari, Firefox)
2. Type in address bar: `http://localhost:8000`
3. Press Enter

**Result:**
```
┌─────────────────────────────────────────────┐
│ Browser - http://localhost:8000             │
├─────────────────────────────────────────────┤
│                                             │
│          🎓 Schooloo AI Chatbot             │
│                                             │
│    ┌────────────────────────────────┐     │
│    │ Chat History here              │     │
│    │                                │     │
│    │                                │     │
│    │                                │     │
│    │                                │     │
│    └────────────────────────────────┘     │
│                                             │
│    ┌────────────────────────────────┐     │
│    │ Type message here...    [Send] │     │
│    └────────────────────────────────┘     │
│                                             │
└─────────────────────────────────────────────┘
```

---

### **STEP 6: Ask a Question**

```
┌─────────────────────────────────────────────┐
│ Browser - http://localhost:8000             │
├─────────────────────────────────────────────┤
│          🎓 Schooloo AI Chatbot             │
│                                             │
│    ┌────────────────────────────────┐     │
│    │ You: Best schools in Delhi?    │     │
│    │                                │     │
│    │ Schooloo: Here are some great │     │
│    │ schools in Delhi...             │     │
│    │ • DPS R.K. Puram               │     │
│    │ • Vasant Valley School          │     │
│    │ • Modern School                 │     │
│    │                                │     │
│    └────────────────────────────────┘     │
│                                             │
│    ┌────────────────────────────────┐     │
│    │ Ask another question...  [Send]│     │
│    └────────────────────────────────┘     │
│                                             │
└─────────────────────────────────────────────┘
```

**That's it!** ✅

---

## What's Happening Behind the Scenes

```
User Types Question
        │
        ▼
    Browser (8000)
        │
        ▼ (HTTP Request)
    ┌─────────────────┐
    │ Frontend JS Code│
    │ (index.html)    │
    └────────┬────────┘
             │
        ▼ (Sends to http://localhost:5002/api/chat)
    ┌─────────────────────────────────────┐
    │ Backend Server (Flask)              │
    │ Port 5002                           │
    ├─────────────────────────────────────┤
    │ Takes user question                 │
    │ Adds system prompt                  │
    │ Calls Google Gemini AI API          │
    └────────┬────────────────────────────┘
             │
             ▼
    ┌─────────────────┐
    │ Google API      │
    │ (Gemini 2.0)    │
    └────────┬────────┘
             │
             ▼ (Processes question)
    ┌──────────────────────┐
    │ AI Generates Answer: │
    │ "Best schools are..."│
    └────────┬─────────────┘
             │
             ▼
    ┌─────────────────────┐
    │ Backend sends JSON  │
    │ response back       │
    └────────┬────────────┘
             │
             ▼ (HTTP Response)
    ┌─────────────────────┐
    │ Browser receives    │
    │ response            │
    └────────┬────────────┘
             │
             ▼
    ┌──────────────────────────┐
    │ JavaScript displays      │
    │ answer in chat window    │
    └──────────────────────────┘
             │
             ▼
    User sees the answer!
```

---

## Common Actions & Commands

### **Start Application**
```
bash start_local.sh
```
✅ **Easiest** - One command starts everything

---

### **Check if Running**
```
ps aux | grep python3
```
✅ You should see 2 Python processes

---

### **Stop Application**
```
Ctrl + C
```
✅ In the terminal where you ran the command

---

### **View Logs**
```
tail -f /tmp/schooloo_backend.log
```
✅ Shows backend activity

---

### **Test Backend**
```
curl http://localhost:5002/api/health
```
✅ Should return: `{"status": "online", ...}`

---

### **Kill All Processes**
```
pkill -9 -f "python3" || true
```
⚠️ Use only if stuck - terminates all Python processes

---

## Quick Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + `` | Open/Close Terminal in VS Code |
| `Ctrl + C` | Stop running command in terminal |
| `Ctrl + Shift + `` | Open new terminal tab |
| `Ctrl + L` | Clear terminal (macOS) |
| `Ctrl + +` | Zoom in browser |
| `Ctrl + -` | Zoom out browser |
| `Cmd + W` | Close tab (macOS) |

---

## 🎯 The Complete Checklist

```
Before Running:
  ☑ VS Code opened
  ☑ Project folder opened (schooloo.ai-main)
  ☑ API key in .env ✅ (Already done!)

Running:
  ☑ Terminal opened in VS Code
  ☑ Typed: bash start_local.sh
  ☑ Both servers showing "RUNNING"

Testing:
  ☑ Browser opened to http://localhost:8000
  ☑ App displays
  ☑ Typed a question
  ☑ Got a response (no errors!)

Success:
  ✅ Your Schooloo AI is running!
```

---

## 📱 If You See Errors

### **"Could not reach server"**
```bash
# Check servers
ps aux | grep python3

# Restart
bash start_local.sh
```

### **"Port already in use"**
```bash
# Kill the process
pkill -9 -f "python3" || true
sleep 2

# Restart
bash start_local.sh
```

### **"Module not found"**
```bash
# Install dependencies
pip3 install -r requirements.txt

# Then restart
bash start_local.sh
```

---

## 🎓 Architecture Overview

```
┌────────────────────────────────────────────────────────┐
│                    Your Computer                       │
│                                                        │
│  ┌─────────────────────────────────────────────────┐ │
│  │            VS Code Terminal                     │ │
│  │  $ bash start_local.sh                          │ │
│  └──────────────────┬────────────────────────────┬─┘ │
│                     │                            │    │
│         ┌───────────▼────────┐    ┌──────────────▼──┐ │
│         │ Backend (Flask)    │    │ Frontend (HTTP) │ │
│         │ Port 5002          │    │ Port 8000       │ │
│         │ - API endpoints    │    │ - Web interface │ │
│         │ - AI processing    │    │ - Chat UI       │ │
│         │ - Database lookup  │    │ - User input    │ │
│         └────────┬───────────┘    └────────┬────────┘ │
│                  │                         │          │
│                  │ (API calls)             │          │
│                  │ (JSON responses)        │          │
│                  └────────────┬────────────┘          │
│                               │                       │
│                               │ (via localhost)      │
│                    ┌──────────▼──────────┐            │
│                    │  Your Web Browser   │            │
│                    │ http://localhost:8000            │
│                    │                     │            │
│                    │  Shows: School List │            │
│                    │  Gets: User Input   │            │
│                    └─────────────────────┘            │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## ✨ You're Ready!

Everything is set up. Just follow these 4 simple steps:

```
1️⃣  Open VS Code → File → Open Folder → schooloo.ai-main

2️⃣  Press Ctrl + ` to open Terminal

3️⃣  Type: bash start_local.sh

4️⃣  Open: http://localhost:8000 in browser

🎉 Start asking questions!
```

**Status: ✅ Ready to Run**  
**API Key: ✅ Configured**  
**Servers: ✅ Configured**  
**Documentation: ✅ Complete**

---

**Happy Learning! 🚀**
