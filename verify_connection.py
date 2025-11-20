#!/usr/bin/env python3
"""
Schooloo AI - Connection Verification Script
Tests both frontend and backend connectivity
"""

import subprocess
import time
import sys
import json
import urllib.request
import urllib.error

def check_server(url, name):
    """Check if a server is running"""
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            return True, response.status
    except Exception as e:
        return False, str(e)

def main():
    print("\n" + "="*70)
    print("🎓 SCHOOLOO AI - CONNECTION VERIFICATION TEST 🎓")
    print("="*70 + "\n")
    
    # Give servers time to start
    print("⏳ Waiting for servers to initialize...")
    time.sleep(3)
    
    backends = [
        ("Backend API", "http://localhost:5002/api/health"),
        ("Frontend Server", "http://localhost:8000"),
    ]
    
    print("\n📊 CONNECTIVITY STATUS:\n")
    
    all_success = True
    
    for name, url in backends:
        sys.stdout.write(f"  🔍 Checking {name}... ")
        sys.stdout.flush()
        
        success, result = check_server(url, name)
        
        if success:
            print(f"✅ CONNECTED (Status: {result})")
            if "health" in url:
                try:
                    with urllib.request.urlopen(url) as response:
                        data = json.loads(response.read())
                        print(f"     └─ Status: {data.get('status', 'unknown')}")
                        print(f"     └─ Service: {data.get('service', 'Schooloo Backend')}")
                except:
                    pass
        else:
            print(f"❌ FAILED")
            print(f"     └─ Error: {result}")
            all_success = False
    
    print("\n" + "-"*70)
    
    if all_success:
        print("\n✅ ALL SERVERS CONNECTED SUCCESSFULLY!\n")
        print("🌐 Application URLs:")
        print("   • Frontend:   http://localhost:8000")
        print("   • API:        http://localhost:5002/api")
        print("   • Health:     http://localhost:5002/api/health\n")
        
        print("✅ READY TO USE:\n")
        print("   1. Open http://localhost:8000 in your browser")
        print("   2. Type a school-related query")
        print("   3. Get instant AI-powered responses\n")
        
        print("📝 SAMPLE QUERIES TO TRY:")
        print("   • 'Best schools in Delhi under 50000 fees'")
        print("   • 'ICSE schools in Mumbai with sports'")
        print("   • 'Girls schools in Prayagraj'")
        print("   • 'International schools in Bangalore'\n")
        
        return 0
    else:
        print("\n❌ SOME SERVERS ARE NOT RUNNING\n")
        print("🔧 TROUBLESHOOTING:\n")
        print("   1. Make sure start_local.sh is running")
        print("   2. Check logs: tail -f /tmp/schooloo_backend.log")
        print("   3. Ensure ports 5002 and 8000 are not in use")
        print("   4. Verify .env file has correct configuration\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
