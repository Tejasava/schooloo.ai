#!/usr/bin/env python3
"""
Flask Backend for Schooloo AI Frontend
Connects the HTML/CSS/JS frontend with the Python Gemini AI agent
"""
import os
import sys
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Import Gemini
try:
    import google.generativeai as genai
except ImportError:
    logger.error("google-generativeai not installed")
    sys.exit(1)

# Configure Gemini API
api_key = os.getenv('API_KEY')
model = None
model_name = os.getenv('AGENT_MODEL', 'gemini-2.0-flash')
DEMO_MODE = False

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        logger.info("✅ Gemini API configured successfully")
    except Exception as e:
        logger.warning(f"⚠️ API key configuration failed: {e}")
        logger.warning("🎯 Switching to DEMO MODE with mock responses")
        DEMO_MODE = True
else:
    logger.warning("⚠️ API_KEY not found in .env file")
    logger.warning("🎯 Switching to DEMO MODE with mock responses")
    DEMO_MODE = True

# System prompt for the agent
system_prompt = """🎓 SCHOOLOO AI ASSISTANT - ADVANCED SCHOOL DISCOVERY SYSTEM 🎓

You are an expert school discovery assistant for India with comprehensive knowledge about ALL schools across Indian cities.

═══════════════════════════════════════════════════════════════════════════════
📋 CORE RESPONSIBILITIES:
═══════════════════════════════════════════════════════════════════════════════

1. 🏫 COMPREHENSIVE SCHOOL DETAILS
   • ALWAYS provide COMPLETE details for EVERY school in the requested city
   • Include: School name, location, exact GPS coordinates, fees, board type
   • Show facilities, contact info, entrance exams, admission process
   • Format: One school per section with all available information

2. 📍 LOCATION & GPS COORDINATES  
   • Provide EXACT GPS coordinates (latitude, longitude) for each school
   • Include landmark directions for easy navigation
   • Show distance from city center in kilometers
   • Example: "St. Mary's Convent School - Prayagraj | 25.4358°N, 81.8463°E | 2.3 km from city center"

3. 💼 PROFESSIONAL TONE & ASSISTANT BEHAVIOR
   • Speak like a knowledgeable educational consultant
   • Ask clarifying questions: budget, board preference, facilities needed
   • Be polite, professional, and solution-oriented
   • Provide personalized recommendations based on user preferences
   • Offer expert insights and guidance for decision-making

4. 🌍 MULTILINGUAL SUPPORT (CRITICAL INSTRUCTION)
   • The user has selected their preferred language
   • You MUST respond ENTIRELY in that selected language ONLY
   • DO NOT mix languages - stay consistent throughout the conversation
   • Translate ALL content to match the user's language preference
   • Even if user types in English, respond in their selected language
   • Example: If Hindi is selected, respond completely in Hindi with devanagari script

5. 📋 RESPONSE FORMAT STANDARDS
   • Use clear hierarchical structure with headings
   • Bullet points for easy reading
   • One school per detailed paragraph
   • Include emojis for visual clarity
   • Professional spacing between sections
   • Complete information in each school entry

6. 🎯 CITY-SPECIFIC COMPLETENESS
   • When asked about schools in a city (e.g., Prayagraj), list ALL known schools
   • Do NOT limit to "top 4" - provide comprehensive list
   • Include school type (Boys/Girls/Co-ed)
   • Show annual fees clearly
   • List 3-5 key facilities
   • Mention entrance exam requirements

═══════════════════════════════════════════════════════════════════════════════
📝 EXAMPLE RESPONSE FORMAT:
═══════════════════════════════════════════════════════════════════════════════

🏫 **School Name** - City
📍 Location: Area, City
🗺️  GPS Coordinates: XX.XXXX°N, XX.XXXX°E
💰 Annual Fees: ₹X.XL - ₹Y.YL/year
📚 Board: CBSE/ICSE/ISC
👥 Type: Co-ed/Boys/Girls
🏢 Facilities: Library, Lab, Sports, Auditorium, etc.
📞 Contact: +91-XXXXXXXXXX
📧 Website: www.school.edu.in
✓ Entrance Exam: Yes/No
📋 Classes: KG-12

═══════════════════════════════════════════════════════════════════════════════
🎓 KEY INSTRUCTIONS:
═══════════════════════════════════════════════════════════════════════════════

✓ ALWAYS verify city name (e.g., Prayagraj vs Allahabad)
✓ ALWAYS include GPS coordinates for navigation
✓ ALWAYS respond in user's selected language
✓ MAINTAIN professional, consultative tone
✓ PROVIDE complete school information (not summaries)
✓ ASK clarifying questions about preferences
✓ SUGGEST best matches based on requirements
✓ INCLUDE follow-up options for further assistance

═══════════════════════════════════════════════════════════════════════════════
🌟 SAMPLE CITIES COVERED:
═══════════════════════════════════════════════════════════════════════════════

Delhi, Mumbai, Bangalore, Prayagraj, Pune, Kolkata, Chennai, Hyderabad,
Ahmedabad, Jaipur, Indore, Lucknow, Patna, Chandigarh, and 100+ Indian cities.

Start every conversation by asking for language preference, then provide expert guidance!"""

# Language mapping dictionary
LANGUAGE_NAMES = {
    'en': 'English',
    'hi': 'हिंदी (Hindi)',
    'bn': 'বাংলা (Bengali)',
    'te': 'తెలుగు (Telugu)',
    'mr': 'मराठी (Marathi)',
    'ta': 'தமிழ் (Tamil)',
    'gu': 'ગુજરાતી (Gujarati)',
    'kn': 'ಕನ್ನಡ (Kannada)',
    'ml': 'മലയാളം (Malayalam)',
    'or': 'ଓଡ଼ିଆ (Odia)',
    'pa': 'ਪੰਜਾਬੀ (Punjabi)',
    'as': 'অসমীয়া (Assamese)',
    'ks': 'کشمیری (Kashmiri)',
    'ne': 'नेपाली (Nepali)',
    'sd': 'سندھی (Sindhi)',
    'sa': 'संस्कृतम् (Sanskrit)',
    'ur': 'اردو (Urdu)',
    'bo': 'བོད་སྐད། (Tibetan)',
    'mni': 'ꯃꯤꯇꯩꯁꯨꯡ (Manipuri)',
    'mai': 'मैथिली (Maithili)',
    'si': 'සිංහල (Sinhala)',
    'doi': 'डोगरी (Dogri)'
}

def get_language_aware_system_prompt(language_code):
    """Generate a system prompt that instructs AI to respond in the specified language"""
    lang_name = LANGUAGE_NAMES.get(language_code, 'English')
    
    language_instruction = f"""
🌐 LANGUAGE REQUIREMENT: {lang_name.upper()}
═══════════════════════════════════════════════════════════════════════════════
⚠️ CRITICAL: The user has selected {lang_name} as their preferred language.
• You MUST respond ENTIRELY in {lang_name} for ALL messages
• Do NOT use English or any other language in your response
• Translate all school information, recommendations, and guidance to {lang_name}
• Maintain professional formatting while using {lang_name}
• Use appropriate script for {lang_name} (e.g., Devanagari for Hindi)
• If user asks in English, still respond in {lang_name}
═══════════════════════════════════════════════════════════════════════════════
"""
    
    return system_prompt + language_instruction

# Store conversation history (in-memory)
conversation_history = []

# Session tracking for login popup (after 5 responses)
session_responses = {}  # {session_id: response_count}
session_languages = {}  # {session_id: language}
sessions_with_accounts = set()  # Set of session_ids that have created accounts (NEVER show popup again)

# Demo data for fallback mode
DEMO_SCHOOLS = {
    "delhi": [
        "🏫 **Delhi Public School (DPS)** - New Delhi | CBSE | ₹3.5L-4.5L/year | Co-ed | Top ranked school with excellent sports and academics",
        "🏫 **Greenfield Public School** - Delhi | CBSE/ISC | ₹2.5L-3.8L/year | Co-ed | Modern infrastructure with digital learning",
        "🏫 **St. Columba's School** - New Delhi | CBSE | ₹2L-3L/year | Boys | Known for academics and character building",
        "🏫 **Springdales School** - New Delhi | CBSE | ₹2.2L-3.5L/year | Co-ed | Emphasis on holistic development",
    ],
    "mumbai": [
        "🏫 **Cathedral and John Connon School** - Mumbai | ICSE | ₹3L-4.5L/year | Co-ed | Premier institution with global curriculum",
        "🏫 **Bombay Scottish School** - Mumbai | ICSE | ₹2.8L-4L/year | Co-ed | Heritage school with modern facilities",
        "🏫 **Jamnabai Narsee School** - Mumbai | CBSE/IGCSE | ₹3.2L-4.8L/year | Co-ed | Focuses on innovation and creativity",
        "🏫 **Dhirubhai Ambani International School** - Mumbai | IB | ₹4L-6L/year | Co-ed | High-end international curriculum",
    ],
    "bangalore": [
        "🏫 **Bangalore International School** - Bangalore | IGCSE/IB | ₹4L-6.5L/year | Co-ed | World-class infrastructure and faculty",
        "🏫 **National Public School** - Bangalore | CBSE | ₹2.5L-4L/year | Co-ed | Known for academics and sports excellence",
        "🏫 **Inventure Academy** - Bangalore | CBSE/IGCSE | ₹3.5L-5.5L/year | Co-ed | Innovation-focused curriculum",
        "🏫 **Jyoti Nivas College** - Bangalore | CBSE | ₹1.8L-3L/year | Girls | Strong academics with character education",
    ],
    "prayagraj": [
        "🏫 **St. Mary's Convent School** - Prayagraj | CBSE | ₹1.5L-2.5L/year | Girls | Established institution with strong academics",
        "🏫 **St. Joseph's College** - Prayagraj | ICSE | ₹1.2L-2L/year | Boys | Known for values and discipline",
        "🏫 **Colvin College** - Prayagraj | ICSE/ISC | ₹1.3L-2.2L/year | Co-ed | Heritage school with modern amenities",
        "🏫 **Adarsh Public School** - Prayagraj | CBSE | ₹1L-1.8L/year | Co-ed | Affordable quality education with good facilities",
    ],
    "pune": [
        "🏫 **Symbiosis International School** - Pune | ICSE/ISC | ₹2.5L-4L/year | Co-ed | Excellent academics and extracurriculars",
        "🏫 **Vibgyor High** - Pune | CBSE | ₹2.2L-3.5L/year | Co-ed | Focus on modern pedagogy and technology",
        "🏫 **MIT World Peace University School** - Pune | CBSE/IB | ₹2.8L-4.2L/year | Co-ed | Research-based learning approach",
        "🏫 **Aditya Birla World Academy** - Pune | CBSE/IGCSE | ₹3L-4.5L/year | Co-ed | Global standard education with Indian values",
    ]
}

def get_demo_response(message: str) -> str:
    """Generate demo responses for testing"""
    message_lower = message.lower()
    
    # Extract city from query
    city = None
    for city_name in DEMO_SCHOOLS.keys():
        if city_name in message_lower:
            city = city_name
            break
    
    if city:
        schools = DEMO_SCHOOLS[city]
        response = f"📚 **Best Schools in {city.capitalize()}** 📚\n\n"
        response += "Here are the top-rated schools in the area:\n\n"
        for school in schools:
            response += f"{school}\n\n"
        response += "✨ **What would you like to know more about?**\n"
        response += "• Admission process and timeline\n"
        response += "• Fees and scholarships\n"
        response += "• Entrance exams required\n"
        response += "• Sports and extracurricular activities"
        return response
    
    # Generic responses
    if "hello" in message_lower or "hi" in message_lower:
        return """👋 **Welcome to Schooloo AI Assistant!** 👋

I'm here to help you find the perfect school for you or your child. I can assist with:

✨ **What I can help with:**
• Find best schools in your city
• Compare school fees and facilities
• Information about admission process
• Details about entrance exams
• Extracurricular activities
• School location and transport

📍 **Just tell me:**
• Your city (e.g., Delhi, Mumbai, Bangalore, Prayagraj, Pune)
• Your preferences (fees, board, type of school)
• Any specific requirements

Let's get started! 🚀 Which city are you looking for schools in?"""
    
    if "fee" in message_lower or "cost" in message_lower or "price" in message_lower:
        return """💰 **School Fee Information** 💰

Typical fee ranges in India:

**Premium Schools (Top tier):**
• Annual Fees: ₹4L - ₹6.5L+
• Best for: International curriculum, World-class facilities
• Examples: Bombay Scottish, DPS, Bangalore International School

**Mid-range Schools (Quality education):**
• Annual Fees: ₹2L - ₹4L
• Best for: Good academics, modern facilities, balanced fees
• Examples: Greenfield, Symbiosis, National Public School

**Affordable Schools (Value for money):**
• Annual Fees: ₹1L - ₹2L
• Best for: Quality education at reasonable costs
• Examples: St. Joseph's, Adarsh Public School

**Additional Costs:**
• Transport: ₹20K - ₹60K/year
• Uniform & Books: ₹10K - ₹30K/year
• Extracurricular: ₹5K - ₹20K/year

Which fee range are you comfortable with?"""
    
    if "admission" in message_lower or "enroll" in message_lower:
        return """📝 **Admission Process** 📝

Typical admission timeline and steps:

**Timeline:**
• March-April: Admission forms released
• April-May: Entrance exams (if applicable)
• May-June: Results declared
• June-July: Admissions finalized
• July-August: School year begins

**Required Documents:**
✓ Birth certificate
✓ Transfer certificate (from previous school)
✓ Character certificate
✓ Medical records/vaccination details
✓ Recent passport-size photos (6-8)
✓ Parents' ID proofs and address proof
✓ Bank statements (for scholarship applications)

**Entrance Exams:**
Most schools conduct entrance tests for classes 6, 9, and 11
Tests cover: Math, English, Reasoning, General Knowledge

**Next Steps:**
1. Visit school website for prospectus
2. Complete online application
3. Appear for entrance exam
4. Attend interview (if shortlisted)
5. Pay admission fee

Would you like specific information about a particular school?"""
    
    return """🎓 **Schooloo AI Assistant** 🎓

I can help you with school-related queries. To get the best recommendations:

**Please mention:**
1. 📍 Your city (e.g., Delhi, Mumbai, Bangalore, Prayagraj)
2. 💰 Budget/Fee range (optional)
3. 📋 Preferences (CBSE/ICSE/ISC, co-ed/single gender, etc.)

**Example queries:**
• "Find best CBSE schools in Delhi"
• "Budget-friendly schools in Prayagraj under ₹2L"
• "Top schools with sports facilities in Bangalore"
• "Girls schools in Mumbai"

What can I help you find today? 🌟"""


@app.route('/', methods=['GET'])
def index():
    """Serve the frontend HTML file"""
    frontend_path = os.path.join(os.path.dirname(__file__), 'index.html')
    if os.path.exists(frontend_path):
        with open(frontend_path, 'r', encoding='utf-8') as f:
            return f.read()
    return jsonify({'error': 'Frontend not found'}), 404


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'message': 'Schooloo AI Backend is running',
        'model': model_name
    }), 200


@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint - receives user message and returns AI response"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Invalid request',
                'message': 'Please provide a message'
            }), 400
        
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        user_language = data.get('language', 'en')  # Language preference
        
        if not user_message:
            return jsonify({
                'error': 'Empty message',
                'message': 'Please provide a non-empty message'
            }), 400
        
        logger.info(f"Received message: {user_message} (Session: {session_id}, Language: {user_language})")
        
        # Track response count for this session
        if session_id not in session_responses:
            session_responses[session_id] = 0
            session_languages[session_id] = user_language
        
        session_responses[session_id] += 1
        response_count = session_responses[session_id]
        
        # Check if login popup should be shown (every 5 responses)
        # BUT NEVER if user already has an account
        show_login_popup = (response_count % 5 == 0) and (session_id not in sessions_with_accounts)
        
        # Use demo mode if API is not configured
        if DEMO_MODE:
            logger.info("🎯 Using DEMO MODE for response")
            demo_response = get_demo_response(user_message)
            response_dict = {
                'success': True,
                'message': demo_response,
                'response': demo_response,
                'model': 'Schooloo AI (Demo Mode)',
                'mode': 'demo',
                'session_id': session_id,
                'response_count': response_count,
                'show_login_popup': show_login_popup,
                'popup_message': 'Create an account to save your preferences!' if show_login_popup else None,
                'popup_form_url': 'https://formspree.io/f/xovklyjw'
            }
            logger.info(f"📤 Returning response with keys: {list(response_dict.keys())}")
            return jsonify(response_dict), 200
        
        try:
            # Call Gemini API with language-aware system prompt
            language_aware_prompt = get_language_aware_system_prompt(user_language)
            lang_name = LANGUAGE_NAMES.get(user_language, 'Unknown')
            logger.info(f"🌐 Using language-aware prompt for: {lang_name}")
            response = model.generate_content(
                [language_aware_prompt, user_message],
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.95,
                    max_output_tokens=2048,
                )
            )
            
            if not response.text:
                return jsonify({
                    'error': 'No response from AI',
                    'message': 'The AI model did not return a response'
                }), 500
            
            agent_response = response.text.strip()
            logger.info(f"Generated response: {agent_response[:100]}...")
            
            return jsonify({
                'success': True,
                'message': agent_response,
                'response': agent_response,
                'model': model_name,
                'session_id': session_id,
                'response_count': response_count,
                'show_login_popup': show_login_popup,
                'popup_message': 'Create an account to save your preferences!' if show_login_popup else None,
                'popup_form_url': 'https://formspree.io/f/xovklyjw'
            }), 200
        
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Gemini API error: {error_msg[:200]}...")
            
            # Always use demo mode on any API error for better UX
            logger.warning("⚠️ API error occurred, using DEMO MODE for response")
            demo_response = get_demo_response(user_message)
            return jsonify({
                'success': True,
                'message': demo_response,
                'response': demo_response,
                'model': 'Schooloo AI (Demo Mode)',
                'mode': 'demo',
                'session_id': session_id,
                'response_count': response_count,
                'show_login_popup': show_login_popup,
                'popup_message': 'Create an account to save your preferences!' if show_login_popup else None,
                'popup_form_url': 'https://formspree.io/f/xovklyjw'
            }), 200
    
    except ValueError as e:
        return jsonify({
            'error': 'Invalid JSON',
            'message': str(e)
        }), 400
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'error': 'Server Error',
            'message': 'An unexpected error occurred'
        }), 500


@app.route('/api/user/login', methods=['POST'])
def user_login():
    """Handle user login/registration information"""
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'unknown')
        
        user_info = {
            'name': data.get('name', ''),
            'email': data.get('email', ''),
            'phone': data.get('phone', ''),
            'session_id': session_id,
            'timestamp': str(os.environ.get('TIMESTAMP', 'N/A'))
        }
        
        logger.info(f"📝 User Registration: {user_info}")
        
        # Mark this session as having an account - NEVER show popup again
        sessions_with_accounts.add(session_id)
        logger.info(f"✅ Session {session_id} marked as having account - popup will NEVER show again")
        
        # Log user information to file for reference
        with open('/tmp/schooloo_users.log', 'a') as f:
            f.write(f"\n{user_info}\n")
        
        return jsonify({
            'success': True,
            'message': 'User information received. Thank you for registering!',
            'user_info': user_info
        }), 200
    
    except Exception as e:
        logger.error(f"User login error: {str(e)}")
        return jsonify({
            'error': 'Registration Error',
            'message': str(e)
        }), 500


@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """Streaming chat endpoint for real-time responses"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        def generate():
            try:
                response = model.generate_content(
                    [system_prompt, user_message],
                    stream=True,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,
                        top_p=0.95,
                        max_output_tokens=2048,
                    )
                )
                
                for chunk in response:
                    if chunk.text:
                        yield f"data: {chunk.text}\n\n"
            
            except Exception as e:
                yield f"data: ERROR: {str(e)}\n\n"
        
        return app.response_class(
            generate(),
            mimetype='text/event-stream'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/', methods=['GET'])
def serve_frontend():
    """Serve the frontend HTML file"""
    try:
        frontend_path = os.path.join(os.path.dirname(__file__), 'index.html')
        if os.path.exists(frontend_path):
            with open(frontend_path, 'r', encoding='utf-8') as f:
                return f.read()
        return jsonify({'error': 'Frontend not found'}), 404
    except Exception as e:
        logger.error(f"Error serving frontend: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/models', methods=['GET'])
def get_models():
    """Get available Gemini models"""
    try:
        return jsonify({
            'current_model': model_name,
            'available_models': [
                'gemini-2.0-flash',
                'gemini-1.5-pro',
                'gemini-1.5-flash'
            ],
            'status': 'operational'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/info', methods=['GET'])
def get_info():
    """Get API information"""
    return jsonify({
        'name': 'Schooloo AI Backend',
        'version': '1.0.0',
        'description': 'AI-powered school finder for India',
        'model': model_name,
        'features': [
            'City-specific school search',
            'Real school data',
            'Fee comparisons',
            'Board information',
            'Admission guidance'
        ],
        'endpoints': {
            '/api/health': 'Health check',
            '/api/chat': 'Send message and get response',
            '/api/models': 'Get available models',
            '/api/info': 'Get API information'
        }
    }), 200


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested endpoint does not exist',
        'available_endpoints': {
            '/api/health': 'Health check',
            '/api/chat': 'Send message and get response',
            '/api/models': 'Get available models',
            '/api/info': 'Get API information'
        }
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Server Error',
        'message': 'An unexpected server error occurred'
    }), 500


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    
    logger.info(f"🚀 Starting Schooloo AI Backend on port {port}")
    logger.info(f"📊 Using model: {model_name}")
    logger.info(f"🌐 API endpoints available at: http://localhost:{port}/api/")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        use_reloader=False
    )
 