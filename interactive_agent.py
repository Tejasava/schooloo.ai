#!/usr/bin/env python3
"""
Interactive Schooloo AI Agent with Proper Input Handling
Handles both piped input and interactive terminal input gracefully
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai
except ImportError:
    print("❌ Error: google-generativeai not installed")
    sys.exit(1)

# Configure API
api_key = os.getenv('API_KEY')
if not api_key:
    print("❌ Error: API_KEY not found in .env file")
    sys.exit(1)

genai.configure(api_key=api_key)
model_name = os.getenv('AGENT_MODEL', 'gemini-2.0-flash')
model = genai.GenerativeModel(model_name)

system_prompt = """You are Schooloo AI Assistant - an expert school discovery assistant for India.

You have comprehensive knowledge about schools across ALL Indian cities.

CRITICAL RULES:
1. When asked about a SPECIFIC city (e.g., Prayagraj, Delhi, Mumbai), ALWAYS provide schools from THAT EXACT city
2. Provide REAL school names, fees (in ₹), boards (CBSE/ICSE/ISC), and facilities
3. Include follow-up questions to help refine recommendations
4. Be helpful, accurate, and personalized

Example Prayagraj schools:
- St. Mary's Convent School (CBSE, ₹1.5L-2.5L/year, Girls School)
- St. Joseph's College (ICSE, ₹1.2L-2.0L/year, Boys School)
- Colvin College (ICSE/ISC, ₹1.3L-2.2L/year, Co-educational)

Always provide real school information with details."""


def main():
    """Main interactive agent loop"""
    print("\n" + "="*70)
    print("🎓 SCHOOLOO AI AGENT - INTERACTIVE MODE")
    print("="*70)
    print(f"✅ Model: {model_name}")
    print("\n📚 Ask about schools in ANY Indian city!")
    print("💬 Type 'quit' or 'exit' to end\n")
    print("="*70 + "\n")
    
    # Welcome message
    print("🤖 Agent: 👋 Welcome to Schooloo AI Assistant!")
    print("\nI'm here to help you find the best schools across India.")
    print("You can ask me about schools in Prayagraj, Delhi, Mumbai,")
    print("Bangalore, or any other Indian city!\n")
    
    query_count = 0
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using Schooloo AI Agent! Goodbye!\n")
                break
            
            query_count += 1
            
            try:
                # Get response from Gemini
                response = model.generate_content(
                    [system_prompt, user_input],
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,
                        top_p=0.95,
                        max_output_tokens=2048,
                    )
                )
                
                if response.text:
                    print(f"\n🤖 Agent:\n")
                    print(response.text.strip())
                    print()
                else:
                    print("⚠️  No response from agent\n")
            
            except Exception as e:
                error_msg = str(e)
                
                if "429" in error_msg or "quota" in error_msg.lower():
                    print("\n⚠️  API QUOTA EXCEEDED")
                    print("Options:")
                    print("1. Wait 24 hours for daily quota reset")
                    print("2. Upgrade to paid plan: https://console.cloud.google.com")
                    print("3. Use demo agent: python3 demo_agent.py\n")
                    break
                else:
                    print(f"\n❌ Error: {error_msg}\n")
        
        except EOFError:
            # Handle EOF gracefully (for piped input)
            if query_count > 0:
                print(f"\n{'='*70}")
                print(f"✅ Session completed - {query_count} query/queries processed")
                print(f"{'='*70}\n")
            break
        
        except KeyboardInterrupt:
            print("\n\n👋 Exiting... Goodbye!\n")
            sys.exit(0)
        
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}\n")


if __name__ == "__main__":
    main()
