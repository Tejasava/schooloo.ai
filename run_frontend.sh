#!/bin/bash
# Schooloo AI - Frontend & Backend Startup Script

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         🎓 SCHOOLOO AI - FRONTEND & BACKEND LAUNCHER 🎓      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if running from correct directory
if [ ! -f "app.py" ] || [ ! -f "index.html" ]; then
    echo "❌ Error: app.py or index.html not found!"
    echo "Please run this script from /tmp/schooloo-agent directory"
    exit 1
fi

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

echo "✅ Python 3 found"

# Check required packages
echo "📦 Checking dependencies..."

python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Flask not found. Installing..."
    pip install flask -q
fi

python3 -c "import flask_cors" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Flask-CORS not found. Installing..."
    pip install flask-cors -q
fi

python3 -c "import google.generativeai" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ google-generativeai not found. Installing..."
    pip install google-generativeai -q
fi

echo "✅ All dependencies installed"

# Check .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env file..."
    cat > .env << EOF
API_KEY=AIzaSyAUkQPWJFcLCD9ssIkvh7t7fnxDJR6t7J8
AGENT_MODEL=gemini-2.0-flash
FLASK_PORT=5000
FLASK_ENV=development
FLASK_DEBUG=true
EOF
    echo "✅ .env file created"
fi

# Check if port is available
PORT=${1:-5000}
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Port $PORT is already in use"
    echo "   Choose a different port: ./run_frontend.sh 8000"
    exit 1
fi

echo ""
echo "🚀 Starting Schooloo AI Backend..."
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "📊 Configuration:"
echo "   • Python: $(python3 --version)"
echo "   • Flask: $(python3 -c 'import flask; print(flask.__version__)')"
echo "   • Port: $PORT"
echo "   • Mode: Development"
echo ""
echo "🌐 Frontend will be available at:"
echo "   → http://localhost:$PORT"
echo ""
echo "📚 API Endpoints:"
echo "   → http://localhost:$PORT/api/health"
echo "   → http://localhost:$PORT/api/chat"
echo "   → http://localhost:$PORT/api/info"
echo ""
echo "💡 Usage:"
echo "   1. Open http://localhost:$PORT in your browser"
echo "   2. Type your questions about schools"
echo "   3. Press Enter or click the send button"
echo ""
echo "⏹️  To stop the server: Press Ctrl+C"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Start the Flask app
FLASK_PORT=$PORT python3 app.py
