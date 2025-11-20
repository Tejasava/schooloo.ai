# 🎓 SCHOOLOO AI - COMMAND REFERENCE GUIDE

## 🚀 START HERE (Most Important)

### Run the Frontend Server
```bash
cd /tmp/schooloo-agent
bash run_frontend.sh
```

Then open in browser:
```
http://localhost:5000
```

---

## 🎯 QUICK COMMANDS

### Start on Different Port
```bash
bash run_frontend.sh 8000
# Access at http://localhost:8000
```

### Manual Backend Start (without startup script)
```bash
cd /tmp/schooloo-agent
python3 app.py
```

### Interactive Agent (CLI)
```bash
python3 interactive_agent.py
```

### Test Agent (Automated)
```bash
python3 test_agent.py
```

### Demo Agent (No API needed)
```bash
python3 demo_agent.py
```

---

## 📱 API ENDPOINTS

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Send Chat Message
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "help me finding best school at prayagraj"}'
```

### Get Available Models
```bash
curl http://localhost:5000/api/models
```

### Get API Information
```bash
curl http://localhost:5000/api/info
```

---

## 🔧 INSTALLATION & SETUP

### Install Python Dependencies
```bash
pip install flask flask-cors google-generativeai python-dotenv
```

### Check Flask Version
```bash
python3 -c "import flask; print(flask.__version__)"
```

### Check Python Version
```bash
python3 --version
```

### List All Installed Packages
```bash
pip list
```

---

## 🛠️ TROUBLESHOOTING COMMANDS

### Kill Process on Port 5000
```bash
lsof -ti:5000 | xargs kill -9
```

### Check if Port is Available
```bash
lsof -i :5000
```

### View Flask App Logs
```bash
python3 app.py 2>&1 | tee app.log
```

### Test API Connection
```bash
curl -v http://localhost:5000/api/health
```

---

## 📁 FILE & DIRECTORY COMMANDS

### List All Files
```bash
ls -la /tmp/schooloo-agent/
```

### List Frontend Files Only
```bash
ls -lh /tmp/schooloo-agent/ | grep -E '(index|app|run_frontend)'
```

### View Directory Structure
```bash
tree /tmp/schooloo-agent/
```

### Count Files
```bash
ls /tmp/schooloo-agent/ | wc -l
```

### Find All Python Files
```bash
find /tmp/schooloo-agent/ -name "*.py"
```

### Find All HTML Files
```bash
find /tmp/schooloo-agent/ -name "*.html"
```

---

## 📝 CONFIGURATION COMMANDS

### View .env File
```bash
cat /tmp/schooloo-agent/.env
```

### Edit .env File
```bash
nano /tmp/schooloo-agent/.env
# or
vim /tmp/schooloo-agent/.env
```

### Update API Key
```bash
echo "API_KEY=your_new_key_here" >> /tmp/schooloo-agent/.env
```

### Check Current Configuration
```bash
cd /tmp/schooloo-agent && python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API_KEY:', os.getenv('API_KEY')); print('MODEL:', os.getenv('AGENT_MODEL'))"
```

---

## 🚀 PRODUCTION DEPLOYMENT COMMANDS

### Install Gunicorn
```bash
pip install gunicorn
```

### Run with Gunicorn
```bash
cd /tmp/schooloo-agent
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Run with Multiple Workers
```bash
gunicorn -w 8 -b 0.0.0.0:5000 --timeout 120 app:app
```

### Run in Background
```bash
nohup python3 app.py > app.log 2>&1 &
```

---

## 🧪 TESTING COMMANDS

### Test Interactive Agent
```bash
echo "help me finding best school at prayagraj" | python3 interactive_agent.py
```

### Test Multiple Queries
```bash
(echo "schools in prayagraj"; echo "schools in delhi"; echo "quit") | python3 interactive_agent.py
```

### Test Backend API
```bash
python3 app.py &
sleep 2
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'
kill %1
```

---

## 📊 MONITORING COMMANDS

### Monitor Logs
```bash
tail -f /tmp/schooloo-agent/app.log
```

### Watch Process
```bash
watch "ps aux | grep python3"
```

### Check System Resources
```bash
top -o %MEM | head -20
```

### Monitor Network
```bash
netstat -tulpn | grep 5000
```

---

## 🎨 FRONTEND DEVELOPMENT COMMANDS

### Open Frontend in Browser
```bash
# macOS
open http://localhost:5000

# Linux
xdg-open http://localhost:5000

# Windows
start http://localhost:5000
```

### Serve Frontend Only (without backend)
```bash
cd /tmp/schooloo-agent
python3 -m http.server 8000
```

### Watch HTML File for Changes
```bash
watch cat /tmp/schooloo-agent/index.html
```

---

## 🔍 DEBUGGING COMMANDS

### View JavaScript Console Errors
```bash
# In browser: F12 → Console tab
```

### Inspect Network Requests
```bash
# In browser: F12 → Network tab
# Then reload page and check requests
```

### Test API with Different Headers
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"message": "test"}'
```

### Pretty Print JSON Response
```bash
curl -s http://localhost:5000/api/chat | python3 -m json.tool
```

---

## 📚 DOCUMENTATION COMMANDS

### View Frontend Setup Guide
```bash
cat /tmp/schooloo-agent/FRONTEND_SETUP.md
```

### View README
```bash
cat /tmp/schooloo-agent/README_FRONTEND.md
```

### View Quick Reference
```bash
cat /tmp/schooloo-agent/QUICK_REFERENCE.txt
```

### Search for Specific Content
```bash
grep -r "prayagraj" /tmp/schooloo-agent/
```

---

## 🎯 COMMON WORKFLOWS

### Complete Setup from Scratch
```bash
cd /tmp/schooloo-agent
pip install -r requirements.txt  # if exists
bash run_frontend.sh
# Open http://localhost:5000
```

### Develop Locally
```bash
cd /tmp/schooloo-agent
python3 app.py  # Terminal 1
# Edit index.html in text editor
# Refresh browser to see changes
```

### Debug Issues
```bash
# Terminal 1
python3 app.py  # See backend logs

# Terminal 2
curl http://localhost:5000/api/health  # Check health

# Terminal 3
tail -f /tmp/schooloo-agent/app.log  # Watch logs
```

### Performance Testing
```bash
# Install ab (Apache Bench)
ab -n 100 -c 10 http://localhost:5000/

# Or use hey
go get -u github.com/rakyll/hey
hey -n 100 -c 10 http://localhost:5000/
```

---

## 🔑 ENVIRONMENT VARIABLES

### Set Temporary Environment Variable
```bash
export FLASK_PORT=8000
export FLASK_DEBUG=true
```

### Permanent Environment Variable (macOS/Linux)
```bash
echo 'export FLASK_PORT=8000' >> ~/.bashrc
source ~/.bashrc
```

### Check All Environment Variables
```bash
env | grep FLASK
```

---

## 🎓 USEFUL SHORTCUTS

### Navigate to Directory
```bash
cd /tmp/schooloo-agent
```

### Quick Server Start
```bash
bash run_frontend.sh && sleep 2 && open http://localhost:5000
```

### Combined Installation & Start
```bash
pip install flask flask-cors google-generativeai python-dotenv && \
cd /tmp/schooloo-agent && \
bash run_frontend.sh
```

### Kill All Python Processes
```bash
killall python3
```

---

## 📋 CHEAT SHEET

| Command | Purpose |
|---------|---------|
| `bash run_frontend.sh` | Start the server |
| `python3 app.py` | Start backend manually |
| `python3 interactive_agent.py` | CLI interactive chat |
| `python3 test_agent.py` | Run automated tests |
| `curl http://localhost:5000/api/health` | Check API status |
| `curl -X POST http://localhost:5000/api/chat -H "Content-Type: application/json" -d '{"message": "test"}'` | Send API request |
| `open http://localhost:5000` | Open in browser (macOS) |
| `xdg-open http://localhost:5000` | Open in browser (Linux) |
| `lsof -ti:5000 | xargs kill -9` | Kill process on port 5000 |
| `cat .env` | View configuration |
| `npm install -g http-server` | Install simple HTTP server |
| `python3 -m json.tool` | Pretty print JSON |

---

## 🆘 QUICK HELP

### Server Won't Start
```bash
# Check if port is in use
lsof -i :5000

# Kill existing process
lsof -ti:5000 | xargs kill -9

# Try different port
bash run_frontend.sh 8000
```

### Chat Not Working
```bash
# Check backend health
curl http://localhost:5000/api/health

# Restart backend
python3 app.py
```

### Can't Access Frontend
```bash
# Verify server is running
curl http://localhost:5000

# Check firewall
sudo ufw allow 5000
```

---

**For more detailed help, see the documentation files:**
- `README_FRONTEND.md` - Complete guide
- `FRONTEND_SETUP.md` - Setup instructions
- `QUICK_REFERENCE.txt` - Quick commands

Happy coding! 🎓✨
