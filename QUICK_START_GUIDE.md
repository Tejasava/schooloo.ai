# 🚀 Schooloo AI - Quick Start Guide

## Step-by-Step Instructions to Run the Project

### **STEP 1: Open the Project in VS Code**
1. Open VS Code
2. Click **File** → **Open Folder**
3. Navigate to: `/Users/tejasavayadav/Desktop/schooloo.ai-main`
4. Click **Open**

You should now see the project structure in the left sidebar.

---

### **STEP 2: Open the Terminal in VS Code**

There are 3 ways to open a terminal:

**Option A (Easiest):**
- Press `Ctrl + `` (backtick/grave accent key)

**Option B:**
- Click **Terminal** menu → **New Terminal**

**Option C:**
- Click the **Terminal** tab at the bottom of VS Code

You should now see a terminal window at the bottom of VS Code.

---

### **STEP 3: Verify You're in the Right Directory**

In the terminal, type:
```bash
pwd
```

You should see:
```
/Users/tejasavayadav/Desktop/schooloo.ai-main
```

If not, type:
```bash
cd /Users/tejasavayadav/Desktop/schooloo.ai-main
```

---

### **STEP 4: Start the Application (Choose ONE Method)**

#### **METHOD A: Automated (Recommended - Easiest)**

Copy and paste this command in the terminal:
```bash
bash start_local.sh
```

**What this does:**
- ✅ Starts backend server on port 5002
- ✅ Starts frontend server on port 8000
- ✅ Shows server status
- ✅ Monitors both servers
- ✅ Tells you when it's ready

**You should see output like:**
```
✅ Backend server is running!
✅ Frontend server is running!

Backend Server:     http://localhost:5002
Status:             ✅ RUNNING

Frontend Server:    http://localhost:8000
Status:             ✅ RUNNING

🎉 Application is ready! Open http://localhost:8000
```

---

#### **METHOD B: Manual (If automated method fails)**

**In the same terminal:**

**Step A - Start Backend Server:**
```bash
FLASK_PORT=5002 python3 app.py
```

You should see:
```
* Running on http://localhost:5002
```

**IMPORTANT:** Keep this terminal window open!

**Step B - Open a NEW terminal tab:**
- Press `Ctrl + Shift + `` (backtick)
- OR Click the **+** icon next to Terminal tab

**In the new terminal, start Frontend Server:**
```bash
cd /Users/tejasavayadav/Desktop/schooloo.ai-main
python3 -m http.server 8000
```

You should see:
```
Serving HTTP on 0.0.0.0 port 8000
```

**Now you have 2 terminals open:**
- Terminal 1: Backend running (port 5002)
- Terminal 2: Frontend running (port 8000)

---

### **STEP 5: Open the Application in Browser**

**Option A - Using VS Code Browser:**
1. Look at the output from the terminal
2. Click on `http://localhost:8000` (it should be clickable)

**Option B - Using Your Default Browser:**
1. Open any web browser (Chrome, Safari, Firefox, etc.)
2. In the address bar, type: `http://localhost:8000`
3. Press Enter

You should see a chatbot interface that says **"Schooloo AI"**

---

### **STEP 6: Test the Application**

1. **Click on the message input box** at the bottom
2. **Type a question**, for example:
   ```
   Best schools in Delhi under 50000 fees
   ```
3. **Press Enter or click Send button**
4. **Wait for the response** (should appear in 5-10 seconds)

**Expected Result:**
- You should see a detailed response about schools
- NO error message like "Could not reach server"
- The AI lists school names, fees, facilities, boards

---

### **Sample Queries to Try**

```
1. "Best schools in Delhi under 50000 fees"
2. "ICSE schools in Mumbai with sports facilities"
3. "Girls schools in Prayagraj"
4. "International schools in Bangalore"
5. "What documents are needed for school admission?"
6. "Best CBSE schools in Chennai"
7. "Affordable schools in Hyderabad for girls"
```

---

### **STEP 7: Stop the Application**

**If using Automated Method (METHOD A):**
1. Go to the terminal where you ran `bash start_local.sh`
2. Press `Ctrl + C` (Control + C)
3. You should see:
   ```
   Shutting down servers...
   ```

**If using Manual Method (METHOD B):**
1. In **Terminal 1** (Backend): Press `Ctrl + C`
2. In **Terminal 2** (Frontend): Press `Ctrl + C`
3. You can close the terminal tabs

---

## ✅ Verification Checklist

Before opening the app, verify everything is ready:

### **Check 1: API Key is Configured**
```bash
cat .env
```

You should see:
```
API_KEY=AIzaSyAUkQPWJFcLCD9ssIkvh7t7fnxDJR6t7J8
FLASK_PORT=5002
```

✅ If you see the API_KEY, you're good!

### **Check 2: Python Dependencies are Installed**
```bash
pip3 list | grep -E "flask|google-generativeai"
```

You should see:
```
flask                3.1.2
google-generativeai  0.8.5
```

✅ If you see these packages, dependencies are installed!

### **Check 3: Ports are Available**
```bash
lsof -i :5002
lsof -i :8000
```

If these show output, it means ports are in use. Kill them:
```bash
pkill -f "python3.*app.py" || true
pkill -f "http.server" || true
sleep 2
```

---

## 🛠️ Troubleshooting

### **Problem: "Could not reach server" error in browser**

**Solution:**
1. Open a new terminal
2. Check if both servers are running:
   ```bash
   ps aux | grep python3
   ```
3. You should see 2 Python processes
4. If not, restart using METHOD A or METHOD B above

---

### **Problem: "Port 5002 already in use" error**

**Solution:**
```bash
pkill -f "python3.*app.py" || true
sleep 2
bash start_local.sh
```

---

### **Problem: "Port 8000 already in use" error**

**Solution:**
```bash
pkill -f "http.server" || true
sleep 2
bash start_local.sh
```

---

### **Problem: "No module named 'flask'" or similar**

**Solution:**
Install dependencies:
```bash
pip3 install -r requirements.txt
```

---

### **Problem: "API_KEY not found in .env file"**

**Solution:**
1. Check if `.env` file exists:
   ```bash
   cat .env
   ```
2. If missing or empty, the API key should be there (we added it)
3. Restart the app:
   ```bash
   bash start_local.sh
   ```

---

### **Problem: "API Key is invalid" error**

**Solution:**
1. The API key we added is valid
2. Check internet connection is working
3. Make sure Google Generative AI API is enabled on your Google account
4. Try again

---

## 📱 Quick Reference Commands

**Start application (Recommended):**
```bash
bash start_local.sh
```

**Check if servers are running:**
```bash
ps aux | grep python3
```

**Test backend health:**
```bash
curl http://localhost:5002/api/health
```

**Test a chat message:**
```bash
curl -X POST http://localhost:5002/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Best schools in Delhi"}'
```

**Kill all Python processes:**
```bash
pkill -9 -f "python3" || true
```

**View backend logs:**
```bash
tail -f /tmp/schooloo_backend.log
```

**View frontend logs:**
```bash
tail -f /tmp/schooloo_frontend.log
```

---

## 🎯 Summary: The Fastest Way

If you just opened VS Code with the schooloo.ai-main folder, here's the FASTEST way:

1. **Press `Ctrl + `` to open terminal**
2. **Type:** `bash start_local.sh`
3. **Wait for:** "Application is ready!" message
4. **Open browser:** `http://localhost:8000`
5. **Type your question** and press Enter
6. **Get your answer!**

That's it! 🎉

---

## 📞 Need Help?

If you encounter any issues:

1. **Check all servers are running:**
   ```bash
   ps aux | grep python3
   ```

2. **View error logs:**
   ```bash
   tail /tmp/schooloo_backend.log
   tail /tmp/schooloo_frontend.log
   ```

3. **Try the automated restart:**
   ```bash
   pkill -9 -f "python3" || true
   sleep 2
   bash start_local.sh
   ```

4. **Check backend is responding:**
   ```bash
   curl http://localhost:5002/api/health
   ```

---

**Last Updated:** 20 November 2025  
**Status:** ✅ Ready to Use  
**API Key:** ✅ Configured  
**Backend:** ✅ Flask 3.1.2  
**Frontend:** ✅ HTML5 + JavaScript  
**Model:** ✅ Gemini 2.0 Flash
