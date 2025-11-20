# 🎓 Schooloo AI - LOCAL SETUP & RUNNING GUIDE

## ✅ CURRENT STATUS: FULLY OPERATIONAL

Both the backend and frontend servers are now running and connected properly, preventing the "Could not reach server" error.

---

## 🚀 Quick Start (Recommended Method)

### Option 1: Using the Automated Startup Script (EASIEST)

```bash
cd /Users/tejasavayadav/Desktop/schooloo.ai-main
bash start_local.sh
```

**This will:**
- ✅ Start Flask backend on `http://localhost:5002`
- ✅ Start frontend server on `http://localhost:8000`
- ✅ Display server status and PIDs
- ✅ Monitor both servers automatically
- ✅ Handle graceful shutdown with Ctrl+C

### Option 2: Manual Startup (If script fails)

**Terminal 1 - Start Backend:**
```bash
cd /Users/tejasavayadav/Desktop/schooloo.ai-main
FLASK_PORT=5002 python3 app.py
```

**Terminal 2 - Start Frontend:**
```bash
cd /Users/tejasavayadav/Desktop/schooloo.ai-main
python3 -m http.server 8000
```

---

## 🌐 Access the Application

Once servers are running:

- **Frontend**: `http://localhost:8000`
- **API**: `http://localhost:5002/api`
- **Health Check**: `http://localhost:5002/api/health`

---

## 🔧 What Was Fixed

### 1. **Port Configuration Issue** ✅
**Problem:** Frontend was trying to call API on same port as frontend
**Solution:** Updated `index.html` to detect localhost and use correct backend port (5002)

**Before:**
```javascript
const API_BASE_URL = window.location.origin + '/api';  // Wrong! Uses 8000
```

**After:**
```javascript
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5002/api'    // Correct! Uses 5002
    : window.location.origin + '/api';
```

### 2. **Startup Script Created** ✅
- Automated script to start both servers simultaneously
- Health checking for both services
- Proper error handling and logging
- Graceful shutdown on Ctrl+C

### 3. **Environment Configuration** ✅
- `.env` file is properly configured
- FLASK_PORT set to 5002
- CORS enabled for cross-port communication

---

## 📋 Server Status

```
✅ BACKEND SERVER
   URL: http://localhost:5002
   Status: RUNNING
   Model: Gemini 2.0 Flash
   Port: 5002

✅ FRONTEND SERVER
   URL: http://localhost:8000
   Status: RUNNING
   Type: Static HTTP Server
   Port: 8000
```

---

## 🧪 Testing the Connection

### Method 1: Using Verification Script
```bash
python3 verify_connection.py
```

### Method 2: Using curl
```bash
# Check backend health
curl http://localhost:5002/api/health

# Expected output:
# {
#   "status": "online",
#   "message": "Schooloo AI Backend is running",
#   "model": "gemini-2.0-flash"
# }
```

### Method 3: Manual Testing in Browser
1. Open `http://localhost:8000`
2. Type a query like "Best schools in Delhi"
3. If you see a response (not an error), connection is working! ✅

---

## 🐛 Troubleshooting

### Error: "Could not reach the server"

**Check 1: Are both servers running?**
```bash
ps aux | grep -E "python3.*app.py|http.server"
```

**Check 2: Are ports 5002 and 8000 available?**
```bash
# Check port 5002
lsof -i :5002

# Check port 8000
lsof -i :8000
```

**Check 3: Check backend logs**
```bash
tail -f /tmp/schooloo_backend.log
```

**Check 4: Check frontend logs**
```bash
tail -f /tmp/schooloo_frontend.log
```

### Error: "Port already in use"

Kill existing processes:
```bash
# Kill Flask processes
pkill -f "python3.*app.py"

# Kill HTTP server processes
pkill -f "http.server"

# Wait 2 seconds
sleep 2

# Start fresh
bash start_local.sh
```

### Error: "Connection refused"

**This means the server isn't running. Solution:**
1. Ensure you're in the project directory
2. Verify Python 3 is installed
3. Check `.env` file exists
4. Run: `bash start_local.sh`

---

## 📁 Project Files Summary

| File | Purpose |
|------|---------|
| `start_local.sh` | **New** - Automated startup script |
| `verify_connection.py` | **New** - Connection verification |
| `index.html` | **Updated** - Fixed API endpoint detection |
| `app.py` | Backend Flask server |
| `.env` | Configuration file |
| `requirements.txt` | Python dependencies |

---

## 💡 Sample Queries to Try

Once the application is running, try these queries:

### Parent Queries
- "Best schools in Delhi under 50000 fees"
- "ICSE schools in Mumbai with good sports facilities"
- "Girls schools in Prayagraj"
- "International schools in Bangalore"
- "Schools with hostel facilities near me"

### Student Queries
- "What documents do I need for school admission?"
- "Tell me about entrance exams for schools"
- "What are the eligibility criteria?"
- "Information about school transport and hostel"
- "Co-ed vs single-gender schools comparison"

### Admin Queries
- "Show me all new leads"
- "Update lead status to contacted"
- "List of schools in Delhi"
- "Add FAQ about admissions"
- "Generate school report by board"

---

## 🔐 Important Notes

### API Key Configuration

The application uses Google's Generative AI (Gemini). To enable full AI features:

1. Get an API key from: https://makersuite.google.com/app/apikey
2. Add it to `.env`:
   ```
   API_KEY=your-key-here
   ```
3. Restart the backend

Without a valid API key, the chatbot will return an error, but the application structure remains functional.

### Development vs Production

**Development (Current Setup):**
- ✅ CORS enabled
- ✅ Debug mode ON
- ✅ Live reload active
- ✅ Detailed error messages
- ⚠️ Use only for local testing

**For Production:**
- Use a production WSGI server (Gunicorn, uWSGI)
- Set `FLASK_DEBUG=false`
- Configure proper SSL/HTTPS
- Use environment-specific `.env` files
- Set up proper logging and monitoring

---

## 📊 Performance Tips

### Optimize Frontend Performance
```bash
# Clear browser cache
# In Chrome DevTools: DevTools → Application → Clear storage
```

### Monitor Server Performance
```bash
# Backend CPU/Memory
ps aux | grep app.py

# Network connections
netstat -an | grep 500
```

### Check Response Times
Open browser DevTools (F12) → Network tab → Check response times

---

## 🛑 Stopping the Servers

### Using Ctrl+C (Recommended)
```
Press Ctrl+C in the terminal running start_local.sh
```

The script will:
- Gracefully stop both servers
- Close connections properly
- Display shutdown message

### Manual Shutdown
```bash
# Kill by process name
pkill -f "python3.*app.py"
pkill -f "http.server"

# Or by PID (shown in start script output)
kill 44229  # Backend PID
kill 44234  # Frontend PID
```

---

## 🎯 Next Steps

### Immediate (Now)
1. ✅ Both servers are running
2. ✅ Frontend accessible at http://localhost:8000
3. ✅ Backend accessible at http://localhost:5002
4. ✅ API endpoint ready at http://localhost:5002/api

### Short Term (Next 1-2 hours)
- [ ] Add Google API key to `.env`
- [ ] Test with various city queries
- [ ] Run all test suites
- [ ] Check logs for any issues

### Medium Term (Next day)
- [ ] Set up database persistence
- [ ] Configure production deployment
- [ ] Set up monitoring and logging
- [ ] Test with larger dataset

### Long Term (Next week)
- [ ] Deploy to cloud (Vercel/AWS/GCP)
- [ ] Set up CI/CD pipeline
- [ ] Configure SSL/HTTPS
- [ ] Add authentication if needed

---

## 📞 Support & Help

### Quick Reference Commands

```bash
# View startup script
cat start_local.sh

# View verification script
python3 verify_connection.py

# View backend logs (real-time)
tail -f /tmp/schooloo_backend.log

# View frontend logs (real-time)
tail -f /tmp/schooloo_frontend.log

# Run tests
python3 test_schooloo_cities.py

# Check processes
ps aux | grep -E "python3.*app|http.server"
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Port in use | Kill existing processes: `pkill -f app.py` |
| Server won't start | Check logs: `tail /tmp/schooloo_*.log` |
| Cannot reach server | Verify both servers running: `ps aux \| grep python3` |
| API returns 500 error | Check API key in `.env` |
| No response from queries | Verify backend health: `curl http://localhost:5002/api/health` |

---

## ✅ Verification Checklist

Run this checklist to ensure everything is working:

- [ ] Both servers started successfully
- [ ] Can access http://localhost:8000 in browser
- [ ] Can access http://localhost:5002/api/health
- [ ] Health check returns JSON with "status": "online"
- [ ] No error messages in logs
- [ ] Can type and submit a query in UI
- [ ] Response appears (even if generic)
- [ ] No "Could not reach server" error

---

## 🎉 Success!

If you can:
1. ✅ See the Schooloo UI in browser
2. ✅ Type a message
3. ✅ Get a response (even a generic one)
4. ✅ See no server connection errors

**Then your setup is SUCCESSFUL!** 🎉

---

**Last Updated:** 20 November 2025
**Status:** ✅ FULLY OPERATIONAL
**Version:** 1.0

For detailed testing information, refer to `TEST_REPORT.md`
