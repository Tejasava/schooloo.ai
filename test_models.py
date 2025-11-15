#!/usr/bin/env python3
"""Test available Gemini models"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv('API_KEY')
if not api_key:
    print("❌ API_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)

print("🔍 Checking available models...\n")

try:
    # List all available models
    models = genai.list_models()
    
    print("✅ Available models:\n")
    available_models = []
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            available_models.append(model.name)
            print(f"  • {model.name}")
    
    print(f"\n📊 Total models supporting generateContent: {len(available_models)}\n")
    
    # Try to use the first available model
    if available_models:
        model_name = available_models[0]
        print(f"🧪 Testing with model: {model_name}\n")
        
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello! What's your name?")
        
        print(f"✅ Test successful!\n")
        print(f"Response: {response.text}\n")
        print(f"👉 Use this model: {model_name}")
    
except Exception as e:
    print(f"❌ Error: {e}")
