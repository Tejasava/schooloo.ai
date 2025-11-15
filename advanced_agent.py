#!/usr/bin/env python3
"""
Advanced Schooloo AI Agent with Gemini API Integration
Uses real Gemini AI to search and provide intelligent school recommendations
"""
import os
import sys
import json
import time
from typing import Optional
from datetime import datetime

# Add agent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agent'))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

try:
    import google.generativeai as genai
except ImportError:
    print("❌ Error: google-generativeai not installed")
    print("Install with: pip install google-generativeai")
    sys.exit(1)

class AdvancedSchoolooAgent:
    """Advanced Schooloo AI Agent with Real Gemini API"""
    
    def __init__(self):
        """Initialize the advanced agent"""
        self.api_key = os.getenv('API_KEY')
        
        if not self.api_key:
            print("❌ Error: API_KEY not found in .env file")
            sys.exit(1)
        
        # Configure Gemini API
        genai.configure(api_key=self.api_key)
        self.model_name = os.getenv('AGENT_MODEL', 'gemini-2.5-flash')
        self.model = genai.GenerativeModel(self.model_name)
        self.conversation_history = []
        
        print("✅ Gemini API configured successfully")
        print(f"✅ Using model: {self.model_name}\n")
        
        # Enhanced system prompt for school search
        self.system_prompt = """You are Schooloo AI Assistant - an expert school discovery assistant for India.

You have comprehensive knowledge about schools across all major Indian cities including:
- Delhi, Mumbai, Bangalore, Hyderabad, Kolkata, Chennai, Pune, Ahmedabad, Jaipur, Lucknow, 
- Indore, Surat, Nagpur, Chandigarh, Kochi, Bhopal, Gurgaon, Noida, Prayagraj, Varanasi, etc.

When a user asks about schools in ANY city, you should:

1. PROVIDE REAL SCHOOL NAMES: Give authentic school names that actually exist in that city
2. DETAILED INFORMATION: Include:
   - School name and location
   - Type (Private/Government/CBSE/ICSE/State Board)
   - Fee structure (approximate annual fees)
   - Classes offered
   - Key facilities
   - Contact information (if known)
   - Entrance exam (Yes/No)

3. SMART RECOMMENDATIONS: Suggest schools based on:
   - Budget range (if mentioned)
   - Curriculum preference (CBSE/ICSE/State Board)
   - Type of school (day/boarding)
   - Special features (sports, STEM, arts, etc.)

4. COMPARISON: When comparing schools, highlight:
   - Fee differences
   - Academic programs
   - Facilities comparison
   - Student outcomes
   - Entrance exam requirements

5. ADDITIONAL HELP:
   - Admission process and documents
   - Entrance exam patterns
   - Eligibility criteria
   - Hostel and transport facilities
   - Extracurricular activities

FORMAT YOUR RESPONSES WITH:
- Emojis for better readability
- Bullet points for lists
- Clear sections with headers
- Organized comparison tables when comparing

IMPORTANT: Always be specific to the city mentioned. Don't give generic responses.
If user asks about Prayagraj, mention schools in Prayagraj specifically.
If user asks about Delhi, mention schools in Delhi specifically.

Be helpful, accurate, and thorough in your responses."""
    
    def chat(self, user_message: str) -> str:
        """Chat with Gemini API for intelligent responses"""
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "parts": [user_message]
        })
        
        try:
            # Create full conversation with system prompt
            full_history = [{
                "role": "user",
                "parts": [self.system_prompt]
            }]
            full_history.extend(self.conversation_history)
            
            print("🤖 Thinking...", end="", flush=True)
            
            response = self.model.generate_content(
                full_history,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
            )
            
            print("\r" + " " * 20 + "\r", end="", flush=True)  # Clear "Thinking..."
            
            response_text = response.text
            
            # Add response to history
            self.conversation_history.append({
                "role": "assistant",
                "parts": [response_text]
            })
            
            return response_text
            
        except Exception as e:
            error_msg = str(e)
            
            # Check if it's a quota error
            if "429" in error_msg or "quota" in error_msg.lower():
                print("\r" + " " * 20 + "\r", end="", flush=True)
                return (
                    "⚠️ API Quota Exceeded\n\n"
                    "The Gemini API free tier quota has been reached.\n\n"
                    "Options:\n"
                    "1. Wait 24 hours for quota to reset\n"
                    "2. Upgrade to a paid plan: https://console.cloud.google.com\n"
                    "3. Use the demo agent (python3 demo_agent.py)\n\n"
                    "The agent is still working - just needs API quota!"
                )
            
            print("\r" + " " * 20 + "\r", end="", flush=True)
            return f"❌ Error: {str(e)}"
    
    def run_interactive(self):
        """Run interactive chat loop with Gemini API"""
        print("\n" + "="*70)
        print("🎓 SCHOOLOO AI ASSISTANT - ADVANCED MODE WITH GEMINI API")
        print("="*70)
        print("\n✨ Powered by Google Gemini AI - Real School Data from Across India")
        print("📚 Ask about schools in ANY city in India")
        print("🌟 Get intelligent recommendations and detailed information")
        print("✋ Type 'quit' or 'exit' to end the conversation\n")
        print("-"*70 + "\n")
        
        # Welcome message
        welcome = (
            "👋 Welcome to Schooloo AI Assistant!\n\n"
            "I'm here to help you find the best schools across India.\n\n"
            "You can ask me:\n"
            "  • Schools in Prayagraj, Delhi, Bangalore, or any Indian city\n"
            "  • Fee structures and facilities\n"
            "  • School comparisons\n"
            "  • Admission requirements\n"
            "  • Entrance exam patterns\n"
            "  • Recommendations based on your preferences\n\n"
            "Let's get started! What school information do you need?"
        )
        print(f"Agent: {welcome}\n")
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
                response = self.chat(user_input)
                
                print(f"\nAgent: {response}\n")
                print("-"*70 + "\n")
                
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"❌ Error: {e}\n")


def main():
    """Main entry point"""
    agent = AdvancedSchoolooAgent()
    agent.run_interactive()


if __name__ == "__main__":
    main()
