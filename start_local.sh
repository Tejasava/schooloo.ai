#!/bin/bash
# Schooloo AI - Complete Startup Script
# Starts both backend (Flask) and frontend (HTTP server) servers

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKEND_PORT=5002
FRONTEND_PORT=8000
BACKEND_PID=""
FRONTEND_PID=""

# Function to print colored output
print_header() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC} $1"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to cleanup on exit
cleanup() {
    echo ""
    print_header "Shutting down Schooloo AI..."
    
    if [ ! -z "$BACKEND_PID" ]; then
        print_info "Stopping backend server (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        print_info "Stopping frontend server (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    print_success "All servers stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup EXIT INT TERM

# Main execution
clear

print_header "🎓 SCHOOLOO AI - LOCAL STARTUP SCRIPT 🎓"

# Check Python installation
print_info "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    exit 1
fi
print_success "Python 3 found: $(python3 --version)"

# Check if running from correct directory
print_info "Checking project structure..."
if [ ! -f "app.py" ]; then
    print_error "app.py not found. Please run from project root directory"
    exit 1
fi
print_success "Project structure verified"

# Check for .env file
print_info "Checking environment configuration..."
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from template..."
    cat > .env << 'ENVEOF'
# Google API Configuration
API_KEY=your-google-generative-ai-key-here

# Backend Configuration
FLASK_PORT=5002
FLASK_ENV=development
FLASK_DEBUG=true

# Agent Configuration
AGENT_MODEL=gemini-2.0-flash
AGENT_NAME=Schooloo Assistant

# Database Configuration (if needed)
DATABASE_URL=sqlite:///schooloo.db
ENVEOF
    print_success ".env file created"
    print_warning "Please add your Google Generative AI API key to .env"
else
    print_success ".env file found"
fi

# Start Backend Server
print_header "Starting Backend Server..."
print_info "Backend will run on: http://localhost:$BACKEND_PORT"

export FLASK_PORT=$BACKEND_PORT
python3 app.py > /tmp/schooloo_backend.log 2>&1 &
BACKEND_PID=$!

print_info "Backend PID: $BACKEND_PID"
print_info "Waiting for backend to initialize..."
sleep 3

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    print_error "Backend failed to start"
    print_error "Logs:"
    cat /tmp/schooloo_backend.log
    exit 1
fi

print_success "Backend server is running!"

# Start Frontend Server
print_header "Starting Frontend Server..."
print_info "Frontend will run on: http://localhost:$FRONTEND_PORT"

python3 -m http.server $FRONTEND_PORT > /tmp/schooloo_frontend.log 2>&1 &
FRONTEND_PID=$!

print_info "Frontend PID: $FRONTEND_PID"
print_info "Waiting for frontend to initialize..."
sleep 2

# Check if frontend started successfully
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    print_error "Frontend failed to start"
    print_error "Logs:"
    cat /tmp/schooloo_frontend.log
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

print_success "Frontend server is running!"

# Print summary
clear
echo ""
print_header "🎉 SCHOOLOO AI - FULLY OPERATIONAL 🎉"

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ SERVERS STATUS${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  ${GREEN}Backend Server${NC}:     ${BLUE}http://localhost:${BACKEND_PORT}${NC}"
echo -e "  Status:             ${GREEN}✅ RUNNING${NC} (PID: $BACKEND_PID)"
echo ""
echo -e "  ${GREEN}Frontend Server${NC}:    ${BLUE}http://localhost:${FRONTEND_PORT}${NC}"
echo -e "  Status:             ${GREEN}✅ RUNNING${NC} (PID: $FRONTEND_PID)"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  ${BLUE}🌐 Open Application:   http://localhost:${FRONTEND_PORT}${NC}"
echo ""
echo -e "  ${BLUE}📊 API Endpoint:        http://localhost:${BACKEND_PORT}/api${NC}"
echo ""
echo -e "  ${BLUE}✅ Health Check:        http://localhost:${BACKEND_PORT}/api/health${NC}"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}📝 QUICK TIPS:${NC}"
echo -e "  • Press ${YELLOW}Ctrl+C${NC} to stop all servers"
echo -e "  • Backend logs: tail -f /tmp/schooloo_backend.log"
echo -e "  • Frontend logs: tail -f /tmp/schooloo_frontend.log"
echo -e "  • Run tests: python3 test_schooloo_cities.py"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Monitor both services
print_info "Monitoring services... (Press Ctrl+C to stop)"
echo ""

while true; do
    # Check backend
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        print_error "Backend server crashed!"
        print_info "Backend logs:"
        tail -20 /tmp/schooloo_backend.log
        exit 1
    fi
    
    # Check frontend
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        print_error "Frontend server crashed!"
        print_info "Frontend logs:"
        tail -20 /tmp/schooloo_frontend.log
        exit 1
    fi
    
    sleep 10
done
