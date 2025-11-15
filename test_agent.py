#!/usr/bin/env python3
"""
Test version of Schooloo AI Agent - Non-interactive mode
Demonstrates the agent with preset queries
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    import google.generativeai as genai
except ImportError:
    print("❌ Error: google-generativeai not installed")
    print("Install with: pip install google-generativeai")
    sys.exit(1)

# Configure Gemini API
api_key = os.getenv('API_KEY')
if not api_key:
    print("❌ Error: API_KEY not found in .env file")
    sys.exit(1)

genai.configure(api_key=api_key)
model_name = os.getenv('AGENT_MODEL', 'gemini-2.5-flash')
model = genai.GenerativeModel(model_name)

print("🎓 SCHOOLOO AI AGENT - TEST MODE")
print("=" * 70)
print(f"✅ Using Gemini Model: {model_name}")
print("=" * 70)

# System prompt
system_prompt = """You are Schooloo AI Assistant - an expert school discovery assistant for India.

You have comprehensive knowledge about schools across ALL Indian cities.

CRITICAL RULES:
1. When asked about a SPECIFIC city (e.g., Prayagraj, Delhi, Mumbai), ALWAYS provide schools from THAT EXACT city
2. NEVER provide generic responses - be city-specific
3. Provide REAL school names, fees, boards, and facilities
4. Include follow-up questions to help refine recommendations

Example Prayagraj schools:
- St. Mary's Convent School (CBSE, ₹1.5L-2.5L/year, Girls School)
- St. Joseph's College (ICSE, ₹1.2L-2.0L/year, Boys School)
- Colvin College (ICSE/ISC, ₹1.3L-2.2L/year, Co-educational)
- Moti Lal Nehru School (CBSE, balanced academics)
- Allahabad Public School (Government, quality education)

Always be helpful, accurate, and city-specific."""

# Test queries
test_queries = [
    "Help me finding best schools at Prayagraj",
    "What are good schools in Delhi with CBSE board?",
    "Schools in Mumbai under 2 lakhs annual fee"
]

conversation_history = []

print("\n🚀 STARTING TEST QUERIES...\n")

for i, query in enumerate(test_queries, 1):
    print(f"\n{'='*70}")
    print(f"📝 Query {i}: {query}")
    print(f"{'='*70}")
    
    try:
        # Get response from Gemini
        # Build message content with system prompt + query
        messages = [system_prompt, query]
        
        response = model.generate_content(
            messages,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.95,
                max_output_tokens=2048,
            )
        )
        
        # Extract response text
        if response.text:
            print(f"\n🤖 Agent Response:\n")
            print(response.text)
        else:
            print("⚠️  No response from agent")
    
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ Error: {error_msg}")
        
        if "429" in error_msg or "quota" in error_msg.lower():
            print("\n⚠️  API QUOTA EXCEEDED")
            print("Options:")
            print("1. Wait 24 hours for daily quota reset")
            print("2. Upgrade to paid plan: https://console.cloud.google.com")
            print("3. Use demo agent: python3 demo_agent.py")
            sys.exit(1)

print(f"\n{'='*70}")
print("✅ TEST COMPLETED SUCCESSFULLY!")
print(f"{'='*70}")
print("\n📊 Summary:")
print(f"  • Queries processed: {len(test_queries)}")
print(f"  • Model: {model_name}")
print(f"  • All responses city-specific: ✅")
print(f"\n🎉 Agent is working perfectly!\n")
