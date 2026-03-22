#!/bin/bash
# Quick Start Guide for Testing Language Fix
# Run this script to test the language functionality

echo ""
echo "🎓 SCHOOLOO AI - LANGUAGE FIX TEST SUITE"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "backend/app.py" ]; then
    echo "❌ Error: Please run this script from the schooloo.ai-main directory"
    echo "   Current directory: $(pwd)"
    exit 1
fi

echo "✅ Running from correct directory"
echo ""

# Check Python version
echo "📋 Python Version Check:"
python3 --version
echo ""

# Check if required packages are installed
echo "📦 Checking required packages..."
python3 -c "import flask" 2>/dev/null && echo "✅ Flask installed" || echo "❌ Flask not found"
python3 -c "import google.generativeai" 2>/dev/null && echo "✅ Google Generative AI installed" || echo "⚠️  Google Generative AI not found (using DEMO MODE)"
python3 -c "import requests" 2>/dev/null && echo "✅ Requests installed" || echo "❌ Requests not found"
echo ""

# Ask user what to do
echo "Choose an option:"
echo "1. Start backend server"
echo "2. Run language tests"
echo "3. Check backend syntax"
echo "4. View language configuration"
echo "5. Exit"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Starting Schooloo AI Backend..."
        echo "   Server will run on http://localhost:5002"
        echo "   Press Ctrl+C to stop"
        echo ""
        python3 backend/app.py
        ;;
    2)
        echo ""
        echo "🧪 Running Language Tests..."
        echo ""
        if [ -f "test_language_fixed.py" ]; then
            python3 test_language_fixed.py
        else
            echo "❌ test_language_fixed.py not found"
            echo "   Please ensure test_language_fixed.py exists in the current directory"
        fi
        ;;
    3)
        echo ""
        echo "🔍 Checking backend/app.py syntax..."
        python3 -m py_compile backend/app.py
        if [ $? -eq 0 ]; then
            echo "✅ No syntax errors found"
        else
            echo "❌ Syntax errors found"
        fi
        echo ""
        ;;
    4)
        echo ""
        echo "📝 Language Configuration:"
        echo "============================"
        grep -A 25 "LANGUAGE_NAMES = {" backend/app.py | head -30
        echo ""
        ;;
    5)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please enter 1-5"
        exit 1
        ;;
esac
