#!/usr/bin/env python3
"""
Quick start script for Schooloo AI Agent
Run this to get started immediately
"""
import subprocess
import os
import sys
import time

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def run_command(cmd, description):
    """Run a command and report status"""
    print(f"▶ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False)
        if result.returncode == 0:
            print(f"✅ {description} - Done!\n")
            return True
        else:
            print(f"❌ {description} - Failed!\n")
            return False
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False

def main():
    """Main quickstart flow"""
    print_header("SCHOOLOO AI AGENT - QUICKSTART")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    print("✅ Python version OK\n")
    
    # Install dependencies
    print_header("Step 1: Installing Dependencies")
    if not run_command("pip install -r requirements.txt", "Installing packages"):
        print("Try installing manually: pip install -r requirements.txt")
        return
    
    # Check if .env exists
    print_header("Step 2: Configuration Check")
    if not os.path.exists(".env"):
        print("⚠️  .env file not found")
        print("Creating from .env.example...\n")
        run_command("cp .env.example .env", "Creating .env")
        print("⚠️  Please edit .env with your Google API credentials\n")
    else:
        print("✅ .env file found\n")
    
    # Show system structure
    print_header("Step 3: Project Structure")
    print("""
    📁 schooloo-agent/
    ├── 🔧 backend/
    │   ├── app.py           (Flask API - 200+ lines)
    │   ├── database.py      (Data models - sample data included)
    │   └── config.py        (Configuration)
    │
    ├── 🤖 agent/
    │   ├── schooloo_agent.py (Main agent with Google ADK)
    │   ├── tools.py          (13 agent tools)
    │   └── query_processor.py (Smart routing)
    │
    ├── 🚀 main.py           (Entry point - multiple modes)
    ├── 📖 README.md         (Full documentation)
    └── 📋 requirements.txt  (All dependencies)
    """)
    
    # Show available modes
    print_header("Step 4: How to Use")
    print("""
    Run the agent in different modes:
    
    1️⃣  View all examples:
        python main.py
    
    2️⃣  Parent mode (interactive):
        python main.py --mode parent
    
    3️⃣  Student mode:
        python main.py --mode student
    
    4️⃣  Admin mode:
        python main.py --mode admin
    
    5️⃣  Interactive chat:
        python main.py --mode interactive
    
    6️⃣  API examples:
        python main.py --mode api
    
    7️⃣  Start backend server:
        python backend/app.py
    """)
    
    # Ask user what to do
    print_header("Ready to Start!")
    
    while True:
        print("What would you like to do?")
        print("1. View examples")
        print("2. Start interactive chat (parent)")
        print("3. See API examples")
        print("4. View documentation")
        print("5. Exit\n")
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == "1":
            print("\n▶ Running examples...\n")
            subprocess.run("python main.py", shell=True)
        
        elif choice == "2":
            print("\n▶ Starting interactive chat...\n")
            subprocess.run("python main.py --mode interactive", shell=True)
        
        elif choice == "3":
            print("\n▶ Running API examples...\n")
            subprocess.run("python main.py --mode api", shell=True)
        
        elif choice == "4":
            print("\n📖 README.md:\n")
            with open("README.md", "r") as f:
                print(f.read()[:1000] + "\n... (see full README.md)\n")
        
        elif choice == "5":
            print("\n👋 Thank you for using Schooloo AI Agent!\n")
            break
        
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
        sys.exit(0)
