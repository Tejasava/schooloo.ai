#!/bin/bash

# Advanced Schooloo AI Agent with Real Gemini API
# This runs the smart agent that uses Gemini to search for schools across India

cd /tmp/schooloo-agent

python3 << 'PYTHON_SCRIPT'
import os
import sys

# Direct API key
api_key = "AIzaSyAUkQPWJFcLCD9ssIkvh7t7fnxDJR6t7J8"

import google.generativeai as genai
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

conversation_history = []

system_prompt = """You are Schooloo AI Assistant - an expert school discovery assistant for India.

You have comprehensive knowledge about schools across ALL major Indian cities including:
Delhi, Mumbai, Bangalore, Hyderabad, Kolkata, Chennai, Pune, Ahmedabad, Jaipur, Lucknow, 
Indore, Surat, Nagpur, Chandigarh, Kochi, Bhopal, Gurgaon, Noida, Prayagraj, Varanasi, and more.

IMPORTANT INSTRUCTIONS:
1. When a user asks about schools in a SPECIFIC city (like Prayagraj), ALWAYS provide schools from THAT city only.
2. Give REAL school names that actually exist in that city.
3. Include: School name, location, board (CBSE/ICSE/State), fee structure, facilities, contact info
4. Ask follow-up questions to understand their preferences (budget, board, coeducational/single gender, etc.)
5. Provide detailed comparisons when asked.
6. Offer admission guidance, entrance exam info, and eligibility criteria.

Format responses with:
- Clear section headers
- Bullet points for lists
- Emoji for better readability
- Organized tables for comparisons
- Specific city information (NOT generic responses)"""

print("\n" + "="*70)
print("🎓 SCHOOLOO AI ASSISTANT - POWERED BY GEMINI API")
print("="*70)
print("\n✨ Real School Data From Across India")
print("📚 Ask about schools in ANY Indian city")
print("🌟 Get intelligent recommendations based on your needs")
print("✋ Type 'quit' or 'exit' to end\n")
print("-"*70 + "\n")

# Initial greeting from assistant
greeting = """👋 Welcome to Schooloo AI Assistant!

I'm powered by Google Gemini AI and have comprehensive knowledge about schools 
across ALL cities in India including Delhi, Mumbai, Bangalore, Prayagraj, Kolkata, 
Chennai, Pune, Hyderabad, and many more!

I can help you:
  🏫 Find schools in your city
  💰 Compare fees and facilities  
  📚 Understand admission process
  🎯 Get personalized recommendations
  ❓ Answer any school-related questions

What city are you interested in? Or ask me about specific schools!"""

print(f"Agent: {greeting}\n")
print("-"*70 + "\n")

message_count = 0

while True:
    try:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() in ['quit', 'exit']:
            print("\n" + "="*70)
            print("Thank you for using Schooloo AI Assistant!")
            print("="*70 + "\n")
            break
        
        message_count += 1
        
        # Add user message to history
        conversation_history.append({"role": "user", "parts": [user_input]})
        
        # Create messages with system prompt
        messages = [{"role": "user", "parts": [system_prompt]}]
        messages.extend(conversation_history)
        
        print("\n🤖 Thinking...", end="", flush=True)
        
        try:
            response = model.generate_content(
                messages,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "max_output_tokens": 2048,
                }
            )
            
            print("\r" + " "*20 + "\r", end="", flush=True)  # Clear "Thinking..."
            
            response_text = response.text
            
            # Add response to history
            conversation_history.append({"role": "assistant", "parts": [response_text]})
            
            print(f"Agent: {response_text}\n")
            print("-"*70 + "\n")
            
        except Exception as api_error:
            print("\r" + " "*20 + "\r", end="", flush=True)
            error_str = str(api_error)
            
            if "429" in error_str or "quota" in error_str.lower():
                print("⚠️ API QUOTA EXCEEDED\n")
                print("The Gemini API free tier quota has been reached.")
                print("\n3 Options:")
                print("1️⃣  Wait 24 hours - Quota resets daily")
                print("2️⃣  Upgrade to paid plan - https://console.cloud.google.com")
                print("3️⃣  Use demo agent - python3 demo_agent.py\n")
                print("-"*70 + "\n")
            else:
                print(f"❌ Error: {error_str}\n")
                print("-"*70 + "\n")
        
    except KeyboardInterrupt:
        print("\n\nExiting...")
        break
    except Exception as e:
        print(f"❌ Error: {e}\n")

PYTHON_SCRIPT
