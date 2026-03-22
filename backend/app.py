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

# ═══════════════════════════════════════════════════════════════════════════════
# REAL-TIME SCHOOL DATA DATABASE
# ═══════════════════════════════════════════════════════════════════════════════

SCHOOL_DATABASE = {
    'delhi': [
        {
            'name': 'Delhi Public School (DPS), R.K. Puram',
            'city': 'Delhi',
            'location': 'R.K. Puram, South Delhi',
            'coordinates': '28.5244°N, 77.1855°E',
            'board': 'CBSE',
            'type': 'Co-ed',
            'classes': 'Nursery to 12',
            'fees_annual': '₹3,50,000 - ₹5,00,000',
            'facilities': ['Library', 'Labs', 'Sports', 'Swimming Pool', 'Auditorium'],
            'contact': '+91-11-4141-0041',
            'website': 'www.dpsr.edu.in',
            'entrance_exam': 'DPS-EYE (for admission)',
            'rating': '4.8/5'
        },
        {
            'name': 'Shiv Nadar School, Noida',
            'city': 'Delhi',
            'location': 'Noida, National Capital Region',
            'coordinates': '28.5355°N, 77.3711°E',
            'board': 'IB (International Baccalaureate)',
            'type': 'Co-ed',
            'classes': 'Grade 1 to 12',
            'fees_annual': '₹4,00,000 - ₹7,00,000',
            'facilities': ['Advanced Labs', 'Sports Complex', 'Art Studios', 'Library', 'Cafeteria'],
            'contact': '+91-120-7106-666',
            'website': 'www.shivnadarschool.org',
            'entrance_exam': 'Entrance Test',
            'rating': '4.9/5'
        },
        {
            'name': 'Sanskriti School, Chanakyapuri',
            'city': 'Delhi',
            'location': 'Chanakyapuri, New Delhi',
            'coordinates': '28.5929°N, 77.1865°E',
            'board': 'CBSE',
            'type': 'Co-ed',
            'classes': 'Nursery to 12',
            'fees_annual': '₹2,50,000 - ₹4,50,000',
            'facilities': ['Labs', 'Sports Field', 'Library', 'Computer Center', 'Auditorium'],
            'contact': '+91-11-4141-9090',
            'website': 'www.sanskritischool.org',
            'entrance_exam': 'Written Test + Interview',
            'rating': '4.7/5'
        }
    ],
    'mumbai': [
        {
            'name': 'Cathedral School, Fort',
            'city': 'Mumbai',
            'location': 'Fort, South Mumbai',
            'coordinates': '18.9676°N, 72.8220°E',
            'board': 'ICSE',
            'type': 'Boys',
            'classes': 'Nursery to 12',
            'fees_annual': '₹2,00,000 - ₹4,00,000',
            'facilities': ['Labs', 'Playground', 'Library', 'Cafeteria', 'Sports Complex'],
            'contact': '+91-22-2265-4242',
            'website': 'www.cathedralschool.com',
            'entrance_exam': 'Entrance Test',
            'rating': '4.8/5'
        },
        {
            'name': 'SVKM\'s Mithibai College School',
            'city': 'Mumbai',
            'location': 'Vile Parle, Mumbai',
            'coordinates': '19.1136°N, 72.8223°E',
            'board': 'CBSE',
            'type': 'Co-ed',
            'classes': 'Nursery to 12',
            'fees_annual': '₹1,80,000 - ₹3,50,000',
            'facilities': ['Labs', 'Sports', 'Art Rooms', 'Library', 'Auditorium'],
            'contact': '+91-22-6193-6666',
            'website': 'www.mithibaischool.org',
            'entrance_exam': 'Entrance Test',
            'rating': '4.7/5'
        }
    ],
    'bangalore': [
        {
            'name': 'Bangalore International School',
            'city': 'Bangalore',
            'location': 'Yeshwanthpur, Bangalore',
            'coordinates': '13.3506°N, 77.5703°E',
            'board': 'IB (International Baccalaureate)',
            'type': 'Co-ed',
            'classes': 'Nursery to 12',
            'fees_annual': '₹5,00,000 - ₹8,00,000',
            'facilities': ['Advanced Labs', 'Sports Complex', 'Art Studio', 'Pool', 'Auditorium'],
            'contact': '+91-80-4141-4141',
            'website': 'www.bisbangalore.com',
            'entrance_exam': 'Entrance Assessment',
            'rating': '4.9/5'
        },
        {
            'name': 'Whitefield Global School',
            'city': 'Bangalore',
            'location': 'Whitefield, Bangalore',
            'coordinates': '13.0357°N, 77.7413°E',
            'board': 'CBSE',
            'type': 'Co-ed',
            'classes': 'Nursery to 12',
            'fees_annual': '₹3,50,000 - ₹6,00,000',
            'facilities': ['Science Labs', 'Sports Field', 'Library', 'Computer Labs', 'Cafeteria'],
            'contact': '+91-80-6799-6799',
            'website': 'www.wgs.edu.in',
            'entrance_exam': 'Entrance Test',
            'rating': '4.6/5'
        }
    ],
    'prayagraj': [
        {
            'name': 'St. Mary\'s Convent School, Civil Lines',
            'city': 'Prayagraj',
            'location': 'Civil Lines, Prayagraj',
            'coordinates': '25.4358°N, 81.8463°E',
            'board': 'CBSE',
            'type': 'Girls',
            'classes': 'Nursery to 12',
            'fees_annual': '₹80,000 - ₹2,00,000',
            'facilities': ['Labs', 'Sports Ground', 'Library', 'Auditorium', 'Computer Center'],
            'contact': '+91-532-2411-911',
            'website': 'www.smcsallahabad.edu.in',
            'entrance_exam': 'Interview + Assessment',
            'rating': '4.5/5'
        },
        {
            'name': 'Montfort School, Kanpur Road',
            'city': 'Prayagraj',
            'location': 'Kanpur Road, Prayagraj',
            'coordinates': '25.4520°N, 81.8880°E',
            'board': 'ICSE',
            'type': 'Co-ed',
            'classes': 'Nursery to 12',
            'fees_annual': '₹1,00,000 - ₹2,50,000',
            'facilities': ['Labs', 'Playground', 'Library', 'Sports Field', 'Cafeteria'],
            'contact': '+91-532-2220-077',
            'website': 'www.montfortprayagraj.com',
            'entrance_exam': 'Written Test',
            'rating': '4.4/5'
        },
        {
            'name': 'The Pinnacle School',
            'city': 'Prayagraj',
            'location': 'Naini, Prayagraj',
            'coordinates': '25.3890°N, 81.9050°E',
            'board': 'CBSE',
            'type': 'Co-ed',
            'classes': 'Nursery to 12',
            'fees_annual': '₹70,000 - ₹1,80,000',
            'facilities': ['Labs', 'Smart Classrooms', 'Sports Complex', 'Library', 'Art Studio'],
            'contact': '+91-532-2567-890',
            'website': 'www.pinnacle.edu.in',
            'entrance_exam': 'Written Test',
            'rating': '4.3/5'
        },
        {
            'name': 'Delhi Public School, Prayagraj',
            'city': 'Prayagraj',
            'location': 'Ashok Nagar, Prayagraj',
            'coordinates': '25.4250°N, 81.8550°E',
            'board': 'CBSE',
            'type': 'Co-ed',
            'classes': 'Nursery to 12',
            'fees_annual': '₹90,000 - ₹2,20,000',
            'facilities': ['Advanced Labs', 'Sports Ground', 'Library', 'Computer Lab', 'Auditorium'],
            'contact': '+91-532-2345-678',
            'website': 'www.dpsprayagraj.edu.in',
            'entrance_exam': 'Entrance Test',
            'rating': '4.6/5'
        },
        {
            'name': 'St. Augustine\'s College School',
            'city': 'Prayagraj',
            'location': 'College Road, Prayagraj',
            'coordinates': '25.4180°N, 81.8420°E',
            'board': 'ICSE',
            'type': 'Co-ed',
            'classes': 'Nursery to 12',
            'fees_annual': '₹85,000 - ₹2,10,000',
            'facilities': ['Labs', 'Playground', 'Library', 'Science Museum', 'Auditorium'],
            'contact': '+91-532-2198-765',
            'website': 'www.staugustines.edu.in',
            'entrance_exam': 'Written Test + Interview',
            'rating': '4.5/5'
        },
        {
            'name': 'Ewing Christian College School',
            'city': 'Prayagraj',
            'location': 'Katra, Prayagraj',
            'coordinates': '25.4320°N, 81.8480°E',
            'board': 'CBSE',
            'type': 'Co-ed',
            'classes': 'Class 1 to 12',
            'fees_annual': '₹75,000 - ₹1,90,000',
            'facilities': ['Labs', 'Sports Field', 'Library', 'Computer Center', 'Auditorium'],
            'contact': '+91-532-2567-123',
            'website': 'www.ewingchristian.edu.in',
            'entrance_exam': 'Entrance Test',
            'rating': '4.4/5'
        },
        {
            'name': 'Sunrise Public School',
            'city': 'Prayagraj',
            'location': 'Rambagh, Prayagraj',
            'coordinates': '25.4400°N, 81.8600°E',
            'board': 'CBSE',
            'type': 'Co-ed',
            'classes': 'Nursery to 12',
            'fees_annual': '₹60,000 - ₹1,60,000',
            'facilities': ['Labs', 'Playground', 'Library', 'Art Room', 'Music Studio'],
            'contact': '+91-532-2456-789',
            'website': 'www.sunriseprayagraj.edu.in',
            'entrance_exam': 'Written Test',
            'rating': '4.2/5'
        },
        {
            'name': 'Prism Academy',
            'city': 'Prayagraj',
            'location': 'Colonelganj, Prayagraj',
            'coordinates': '25.4100°N, 81.8300°E',
            'board': 'CBSE',
            'type': 'Co-ed',
            'classes': 'Nursery to 10',
            'fees_annual': '₹65,000 - ₹1,70,000',
            'facilities': ['Labs', 'Sports Ground', 'Library', 'Computer Lab', 'Play Area'],
            'contact': '+91-532-2234-567',
            'website': 'www.prismacademy.edu.in',
            'entrance_exam': 'Interview',
            'rating': '4.3/5'
        },
        {
            'name': 'Banaras Hindu University School',
            'city': 'Prayagraj',
            'location': 'Rambagh, Prayagraj',
            'coordinates': '25.4380°N, 81.8620°E',
            'board': 'CBSE',
            'type': 'Co-ed',
            'classes': 'Class 1 to 12',
            'fees_annual': '₹55,000 - ₹1,50,000',
            'facilities': ['Advanced Labs', 'Sports Complex', 'Library', 'Auditorium', 'Science Park'],
            'contact': '+91-532-2111-222',
            'website': 'www.bhuschool.edu.in',
            'entrance_exam': 'Entrance Assessment',
            'rating': '4.7/5'
        }
    ]
}

# Base system prompt for the agent
BASE_SYSTEM_PROMPT = """🎓 SCHOOLOO AI ASSISTANT - ADVANCED SCHOOL DISCOVERY SYSTEM 🎓

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
✓ MAINTAIN professional, consultative tone
✓ PROVIDE complete school information (not summaries)
✓ ASK clarifying questions about preferences
✓ SUGGEST best matches based on requirements
✓ INCLUDE follow-up options for further assistance

═══════════════════════════════════════════════════════════════════════════════
🌟 SAMPLE CITIES COVERED:
═══════════════════════════════════════════════════════════════════════════════

Delhi, Mumbai, Bangalore, Prayagraj, Pune, Kolkata, Chennai, Hyderabad,
Ahmedabad, Jaipur, Indore, Lucknow, Patna, Chandigarh, and 100+ Indian cities."""

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
⚠️  CRITICAL - RESPOND ENTIRELY IN {lang_name.upper()}:
• You MUST respond ENTIRELY in {lang_name} for ALL messages
• Do NOT use English or any other language in your response
• Translate all school information, recommendations, and guidance to {lang_name}
• Maintain professional formatting while using {lang_name}
• Use appropriate script for {lang_name} (e.g., Devanagari for Hindi)
• If user asks in English, still respond in {lang_name}
• Every single word, emoji description, and instruction must be in {lang_name}
═══════════════════════════════════════════════════════════════════════════════
"""
    
    return language_instruction + BASE_SYSTEM_PROMPT


# ═══════════════════════════════════════════════════════════════════════════════
# REAL-TIME SCHOOL DATA RETRIEVAL FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def search_schools_in_database(city_name, filters=None):
    """
    Search schools from the real-time database
    Returns: List of matching schools with real data
    """
    city_name_lower = city_name.lower().strip()
    
    # Normalize city names
    city_mapping = {
        'delhi': 'delhi',
        'new delhi': 'delhi',
        'bombay': 'mumbai',
        'mumbai': 'mumbai',
        'bangalore': 'bangalore',
        'bengaluru': 'bangalore',
        'prayagraj': 'prayagraj',
        'allahabad': 'prayagraj'
    }
    
    mapped_city = city_mapping.get(city_name_lower, city_name_lower)
    
    if mapped_city not in SCHOOL_DATABASE:
        return []
    
    schools = SCHOOL_DATABASE[mapped_city]
    
    # Apply filters if provided
    if filters:
        if 'board' in filters:
            schools = [s for s in schools if filters['board'].upper() in s['board'].upper()]
        if 'type' in filters:
            schools = [s for s in schools if filters['type'].lower() in s['type'].lower()]
        if 'max_fees' in filters:
            # This is a simple filter - in production, would parse fee range
            pass
    
    return schools


def format_schools_for_response(schools, language='en'):
    """
    Format school data for API response with real information
    """
    if not schools:
        if language == 'hi':
            return "दुर्भाग्यवश, इस शहर में स्कूलों के बारे में कोई जानकारी नहीं मिली।"
        else:
            return "No schools found in this city. Please try another city."
    
    formatted = ""
    for idx, school in enumerate(schools, 1):
        if language == 'hi':
            formatted += f"""
🏫 **{idx}. {school['name']}**
📍 स्थान: {school['location']}
🎯 बोर्ड: {school['board']}
👥 प्रकार: {school['type']}
📚 कक्षाएं: {school['classes']}
💰 वार्षिक शुल्क: {school['fees_annual']}
🏢 सुविधाएं: {', '.join(school['facilities'])}
📞 संपर्क: {school['contact']}
⭐ रेटिंग: {school['rating']}
🌐 वेबसाइट: {school['website']}
📝 प्रवेश परीक्षा: {school['entrance_exam']}
────────────────────────────────────────────────────────────
"""
        else:
            formatted += f"""
🏫 **{idx}. {school['name']}**
📍 Location: {school['location']}
🎯 Board: {school['board']}
👥 Type: {school['type']}
📚 Classes: {school['classes']}
💰 Annual Fees: {school['fees_annual']}
🏢 Facilities: {', '.join(school['facilities'])}
📞 Contact: {school['contact']}
⭐ Rating: {school['rating']}
🌐 Website: {school['website']}
📝 Entrance Exam: {school['entrance_exam']}
────────────────────────────────────────────────────────────
"""
    
    return formatted


def answer_school_question_with_real_data(user_message, language='en'):
    """
    Intelligently extract city and filters from user message,
    fetch real school data, and format response
    Returns: Formatted school information or advice
    """
    message_lower = user_message.lower()
    
    # City detection
    detected_city = None
    city_keywords = {
        'delhi': ['delhi', 'new delhi', 'delhit'],
        'mumbai': ['mumbai', 'bombay'],
        'bangalore': ['bangalore', 'bengaluru'],
        'prayagraj': ['prayagraj', 'allahabad']
    }
    
    for city, keywords in city_keywords.items():
        if any(kw in message_lower for kw in keywords):
            detected_city = city
            break
    
    if not detected_city:
        if language == 'hi':
            return "कृपया अपने शहर का नाम बताएं (दिल्ली, मुंबई, बेंगलुरु, या प्रयागराज)।"
        else:
            return "Please mention your city (Delhi, Mumbai, Bangalore, or Prayagraj) to get school information."
    
    # Filter detection
    filters = {}
    if 'cbse' in message_lower:
        filters['board'] = 'CBSE'
    elif 'icse' in message_lower:
        filters['board'] = 'ICSE'
    elif 'ib' in message_lower or 'international' in message_lower:
        filters['board'] = 'IB'
    
    if "girls" in message_lower or "girls'" in message_lower:
        filters['type'] = 'Girls'
    elif "boys" in message_lower:
        filters['type'] = 'Boys'
    elif "co-ed" in message_lower or "coed" in message_lower:
        filters['type'] = 'Co-ed'
    
    # Search schools
    schools = search_schools_in_database(detected_city, filters)
    
    # Format response
    if language == 'hi':
        city_display = detected_city.upper()
        header = f"🎓 **{city_display} के स्कूलों की जानकारी:**\n\n"
    else:
        city_display = detected_city.upper()
        header = f"🎓 **Schools Information for {city_display}:**\n\n"
    
    formatted_schools = format_schools_for_response(schools, language)
    
    return header + formatted_schools


def handle_follow_up_question(user_message, session_id, language='en'):
    """
    Handle follow-up questions like "show me more", "next", "more details", etc.
    Uses session context to maintain conversation state
    Returns: Response or None if not a follow-up question
    """
    global session_context
    
    message_lower = user_message.lower().strip()
    
    # Check if this is a follow-up question
    follow_up_keywords = [
        'show me more', 'show more', 'more schools', 'more details', 'next', 'tell me more',
        'what else', 'और दिखाएं', 'अधिक', 'अगला', 'और स्कूल', 'और जानकारी',
        'more', 'additional', 'extra', 'further', 'continue', '10 more', 'list more',
        'see more', 'show all', 'all schools', 'complete list', 'full list',
        'और', 'भी', 'अन्य', 'दिखाओ', 'बताओ'
    ]
    
    is_follow_up = any(kw in message_lower for kw in follow_up_keywords)
    
    logger.info(f"🔍 Follow-up check: message='{user_message}' is_follow_up={is_follow_up}")
    logger.info(f"📌 Current session_context: {session_context}")
    
    # If not a follow-up keyword match, return None
    if not is_follow_up:
        logger.info("ℹ️  Not a follow-up keyword")
        return None
    
    # Get last city context
    context = session_context.get(session_id)
    logger.info(f"📍 Checking context for {session_id}: {context}")
    
    if not context:
        logger.warning(f"⚠️  No context found for session {session_id}")
        return None
    
    city = context.get('city')
    if not city:
        logger.warning(f"⚠️  No city found in context for session {session_id}")
        return None
    
    logger.info(f"🎯 Follow-up detected! Using context: {city}")
    
    # Fetch all schools for that city
    all_schools = search_schools_in_database(city, {})
    
    if not all_schools:
        if language == 'hi':
            return f"दुर्भाग्यवश, {city} में कोई स्कूल नहीं मिले।"
        else:
            return f"No schools found in {city}."
    
    if language == 'hi':
        response = f"🎓 **{city.upper()} में सभी उपलब्ध स्कूल:**\n\n"
    else:
        response = f"🎓 **All Available Schools in {city.upper()}:**\n\n"
    
    response += format_schools_for_response(all_schools, language)
    
    return response


def answer_school_question_with_real_data(user_message, language='en'):
    """
    Intelligently extract city and filters from user message,
    fetch real school data, and format response
    Returns: Formatted school information or advice
    """
    message_lower = user_message.lower()
    
    # City detection
    detected_city = None
    city_keywords = {
        'delhi': ['delhi', 'new delhi', 'delhit'],
        'mumbai': ['mumbai', 'bombay'],
        'bangalore': ['bangalore', 'bengaluru'],
        'prayagraj': ['prayagraj', 'allahabad']
    }
    
    for city, keywords in city_keywords.items():
        if any(kw in message_lower for kw in keywords):
            detected_city = city
            break
    
    if not detected_city:
        if language == 'hi':
            return "कृपया अपने शहर का नाम बताएं (दिल्ली, मुंबई, बेंगलुरु, या प्रयागराज)।"
        else:
            return "Please mention your city (Delhi, Mumbai, Bangalore, or Prayagraj) to get school information."
    
    # Filter detection
    filters = {}
    if 'cbse' in message_lower:
        filters['board'] = 'CBSE'
    elif 'icse' in message_lower:
        filters['board'] = 'ICSE'
    elif 'ib' in message_lower or 'international' in message_lower:
        filters['board'] = 'IB'
    
    if "girls" in message_lower or "girls'" in message_lower:
        filters['type'] = 'Girls'
    elif "boys" in message_lower:
        filters['type'] = 'Boys'
    elif "co-ed" in message_lower or "coed" in message_lower:
        filters['type'] = 'Co-ed'
    
    # Search schools
    schools = search_schools_in_database(detected_city, filters)
    
    # Format response
    if language == 'hi':
        city_display = detected_city.upper()
        header = f"🎓 **{city_display} के स्कूलों की जानकारी:**\n\n"
    else:
        city_display = detected_city.upper()
        header = f"🎓 **Schools Information for {city_display}:**\n\n"
    
    formatted_schools = format_schools_for_response(schools, language)
    
    return header + formatted_schools


# Store conversation history (in-memory)
conversation_history = []

# Session tracking for login popup (after 5 responses)
session_responses = {}  # {session_id: response_count}
session_languages = {}  # {session_id: language}
sessions_with_accounts = set()  # Set of session_ids that have created accounts (NEVER show popup again)

# Session context tracking for "show me more" feature
session_context = {}  # {session_id: {'city': 'delhi', 'filters': {}, 'last_query': '...'}}

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

def get_demo_response(message: str, language: str = 'en') -> str:
    """Generate demo responses for testing - multilingual support"""
    message_lower = message.lower()
    
    # Extract city from query
    city = None
    for city_name in DEMO_SCHOOLS.keys():
        if city_name in message_lower:
            city = city_name
            break
    
    if city:
        schools = DEMO_SCHOOLS[city]
        
        if language == 'hi':
            # Hindi response
            response = f"📚 **{city.capitalize()} के सर्वश्रेष्ठ स्कूल** 📚\n\n"
            response += "यहाँ इस क्षेत्र के शीर्ष रेटेड स्कूल हैं:\n\n"
            for school in schools:
                # Keep school names in English but add Hindi context
                response += f"{school}\n\n"
            response += "✨ **आप और क्या जानना चाहते हैं?**\n"
            response += "• प्रवेश प्रक्रिया और समय सारणी\n"
            response += "• शुल्क और छात्रवृत्ति\n"
            response += "• प्रवेश परीक्षाएं\n"
            response += "• खेल और अतिरिक्त गतिविधियाँ"
        else:
            # English response (default)
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
    
    # Generic responses based on language
    if "hello" in message_lower or "hi" in message_lower or "नमस्ते" in message or "हेलो" in message:
        if language == 'hi':
            return """👋 **Schooloo AI असिस्टेंट में आपका स्वागत है!** 👋

मैं आपको आपके बच्चे के लिए सही स्कूल खोजने में मदद करने के लिए यहाँ हूँ। मैं आपकी मदद कर सकता हूँ:

✨ **मैं किस में मदद कर सकता हूँ:**
• आपके शहर में सर्वश्रेष्ठ स्कूल खोजें
• स्कूल की फीस और सुविधाओं की तुलना करें
• प्रवेश प्रक्रिया के बारे में जानकारी
• प्रवेश परीक्षाओं का विवरण
• पाठ्येतर गतिविधियाँ
• स्कूल का स्थान और परिवहन

📍 **बस मुझे बताएँ:**
• आपका शहर (जैसे दिल्ली, मुंबई, बेंगलुरु, प्रयागराज, पुणे)
• आपकी प्राथमिकताएं (शुल्क, बोर्ड, स्कूल का प्रकार)
• कोई विशेष आवश्यकता

चलिए शुरुआत करें! 🚀 आप किस शहर में स्कूल खोज रहे हैं?"""
        else:
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
    
    if "fee" in message_lower or "cost" in message_lower or "price" in message_lower or "शुल्क" in message or "फीस" in message:
        if language == 'hi':
            return """💰 **स्कूल फीस की जानकारी** 💰

भारत में विशिष्ट शुल्क सीमाएं:

**प्रीमियम स्कूल (शीर्ष स्तर):**
• वार्षिक शुल्क: ₹4 लाख - ₹6.5 लाख+
• सर्वोत्तम: अंतर्राष्ट्रीय पाठ्यक्रम, विश्व-स्तरीय सुविधाएं
• उदाहरण: बॉम्बे स्कॉटिश, डीपीएस, बैंगलोर इंटरनेशनल

**मध्य-स्तरीय स्कूल (गुणवत्ता शिक्षा):**
• वार्षिक शुल्क: ₹2 लाख - ₹4 लाख
• सर्वोत्तम: अच्छे अकादमिक्स, आधुनिक सुविधाएं
• उदाहरण: ग्रीनफील्ड, सिम्बायोसिस, नेशनल पब्लिक स्कूल

**सस्ते स्कूल (पैसे के लिए मूल्य):**
• वार्षिक शुल्क: ₹1 लाख - ₹2 लाख
• सर्वोत्तम: उचित लागत पर गुणवत्ता शिक्षा
• उदाहरण: सेंट जोसेफ, आदर्श पब्लिक स्कूल

**अतिरिक्त लागत:**
• परिवहन: ₹20,000 - ₹60,000/वर्ष
• यूनिफॉर्म और किताबें: ₹10,000 - ₹30,000/वर्ष
• अतिरिक्त गतिविधियाँ: ₹5,000 - ₹20,000/वर्ष

आप कौन सी फीस सीमा के लिए सहज हैं?"""
        else:
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
    
    if "admission" in message_lower or "enroll" in message_lower or "प्रवेश" in message or "दाखिला" in message:
        if language == 'hi':
            return """📝 **प्रवेश प्रक्रिया** 📝

विशिष्ट प्रवेश समय सारणी और चरण:

**समय सारणी:**
• मार्च-अप्रैल: प्रवेश फॉर्म जारी
• अप्रैल-मई: प्रवेश परीक्षाएं (यदि लागू हो)
• मई-जून: परिणाम घोषित
• जून-जुलाई: प्रवेश अंतिम रूप
• जुलाई-अगस्त: स्कूल वर्ष शुरू

**आवश्यक दस्तावेज:**
✓ जन्म प्रमाण पत्र
✓ स्थानांतरण प्रमाण पत्र (पिछले स्कूल से)
✓ चरित्र प्रमाण पत्र
✓ चिकित्सा रिकॉर्ड/टीकाकरण विवरण
✓ हाल की पासपोर्ट आकार की फोटो (6-8)
✓ माता-पिता के आईडी प्रमाण और पता प्रमाण
✓ बैंक स्टेटमेंट (छात्रवृत्ति के लिए)

**प्रवेश परीक्षाएं:**
अधिकांश स्कूल कक्षा 6, 9 और 11 के लिए प्रवेश परीक्षा लेते हैं
परीक्षा में शामिल: गणित, अंग्रेजी, तर्क, सामान्य ज्ञान

**अगले कदम:**
1. स्कूल की वेबसाइट से विवरणिका देखें
2. ऑनलाइन आवेदन पूरा करें
3. प्रवेश परीक्षा में शामिल हों
4. साक्षात्कार में भाग लें (यदि चयनित हों)
5. प्रवेश शुल्क का भुगतान करें

क्या आप किसी विशेष स्कूल के बारे में जानकारी चाहते हैं?"""
        else:
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
    
    if language == 'hi':
        return """🎓 **Schooloo AI असिस्टेंट** 🎓

मैं स्कूल से संबंधित प्रश्नों में आपकी मदद कर सकता हूँ। सर्वोत्तम सिफारिशों के लिए:

**कृपया उल्लेख करें:**
1. 📍 आपका शहर (जैसे दिल्ली, मुंबई, बेंगलुरु, प्रयागराज)
2. 💰 बजट/शुल्क सीमा (वैकल्पिक)
3. 📋 प्राथमिकताएं (CBSE/ICSE/ISC, सह-शिक्षा/एकल लिंग, आदि)

**उदाहरण प्रश्न:**
• "दिल्ली में सर्वश्रेष्ठ CBSE स्कूल खोजें"
• "प्रयागराज में ₹2 लाख से कम सस्ते स्कूल"
• "बेंगलुरु में खेल सुविधाओं वाले शीर्ष स्कूल"
• "मुंबई में लड़कियों के स्कूल"

मैं आज आपको क्या खोजने में मदद कर सकता हूँ? 🌟"""
    else:
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


@app.route('/api/debug/context', methods=['GET'])
def debug_context():
    """DEBUG: View current session context"""
    global session_context
    return jsonify({
        'session_context': session_context,
        'context_size': len(session_context)
    }), 200


@app.route('/api/schools/search', methods=['POST'])
def search_schools():
    """Real-time school search endpoint with actual data"""
    try:
        data = request.get_json()
        city = data.get('city', '').strip()
        language = data.get('language', 'en')
        filters = data.get('filters', {})
        
        if not city:
            return jsonify({
                'error': 'City required',
                'message': 'Please provide a city name'
            }), 400
        
        logger.info(f"🔍 School search: {city} (Language: {language})")
        
        # Search in real database
        schools = search_schools_in_database(city, filters)
        
        if not schools:
            return jsonify({
                'success': False,
                'city': city,
                'schools': [],
                'message': f'No schools found in {city}',
                'total': 0
            }), 404
        
        return jsonify({
            'success': True,
            'city': city,
            'schools': schools,
            'total': len(schools),
            'formatted': format_schools_for_response(schools, language)
        }), 200
    
    except Exception as e:
        logger.error(f"School search error: {str(e)}")
        return jsonify({
            'error': 'Search Error',
            'message': str(e)
        }), 500


@app.route('/api/schools/available-cities', methods=['GET'])
def get_available_cities():
    """Get list of cities with available school data"""
    try:
        cities = list(SCHOOL_DATABASE.keys())
        language = request.args.get('language', 'en')
        
        if language == 'hi':
            city_names = {
                'delhi': '🏛️ दिल्ली',
                'mumbai': '🌊 मुंबई',
                'bangalore': '🏙️ बेंगलुरु',
                'prayagraj': '🙏 प्रयागराज'
            }
        else:
            city_names = {
                'delhi': '🏛️ Delhi',
                'mumbai': '🌊 Mumbai',
                'bangalore': '🏙️ Bangalore',
                'prayagraj': '🙏 Prayagraj'
            }
        
        return jsonify({
            'success': True,
            'available_cities': cities,
            'city_names': city_names,
            'total': len(cities)
        }), 200
    
    except Exception as e:
        logger.error(f"Cities list error: {str(e)}")
        return jsonify({
            'error': 'Error',
            'message': str(e)
        }), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint - receives user message and returns AI response"""
    global session_context, session_responses, session_languages
    
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
        
        # FIRST: Check if this is a follow-up question (show me more, next, etc.)
        # This should be checked BEFORE anything else
        follow_up_response = handle_follow_up_question(user_message, session_id, user_language)
        if follow_up_response:
            logger.info("📝 Handling follow-up question - returning all schools")
            response_dict = {
                'success': True,
                'message': follow_up_response,
                'response': follow_up_response,
                'model': 'Schooloo AI (Real Data)',
                'mode': 'direct',
                'session_id': session_id,
                'is_follow_up': True
            }
            return jsonify(response_dict), 200
        
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
            demo_response = get_demo_response(user_message, language=user_language)
            
            # IMPORTANT: Save session context for follow-up questions even in DEMO_MODE
            message_lower = user_message.lower()
            # Include both English and Hindi city variations
            city_keywords = {
                'delhi': ['delhi', 'new delhi', 'दिल्ली', 'नई दिल्ली'],
                'mumbai': ['mumbai', 'bombay', 'मुंबई', 'बॉम्बे'],
                'bangalore': ['bangalore', 'bengaluru', 'बेंगलुरु', 'बैंगलोर'],
                'prayagraj': ['prayagraj', 'allahabad', 'प्रयागराज', 'इलाहाबाद']
            }
            for city, keywords in city_keywords.items():
                if any(kw in message_lower for kw in keywords):
                    session_context[session_id] = {
                        'city': city,
                        'filters': {},
                        'last_query': user_message
                    }
                    logger.info(f"📌 Saved session context for {session_id}: city={city}")
                    break
            
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
            
            # Save session context for follow-up questions
            message_lower = user_message.lower()
            city_keywords = {
                'delhi': ['delhi', 'new delhi'],
                'mumbai': ['mumbai', 'bombay'],
                'bangalore': ['bangalore', 'bengaluru'],
                'prayagraj': ['prayagraj', 'allahabad']
            }
            for city, keywords in city_keywords.items():
                if any(kw in message_lower for kw in keywords):
                    session_context[session_id] = {
                        'city': city,
                        'filters': {},
                        'last_query': user_message
                    }
                    break
            
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
            
            # IMPORTANT: Save session context even on API errors
            message_lower = user_message.lower()
            # Include both English and Hindi city variations
            city_keywords = {
                'delhi': ['delhi', 'new delhi', 'दिल्ली', 'नई दिल्ली'],
                'mumbai': ['mumbai', 'bombay', 'मुंबई', 'बॉम्बे'],
                'bangalore': ['bangalore', 'bengaluru', 'बेंगलुरु', 'बैंगलोर'],
                'prayagraj': ['prayagraj', 'allahabad', 'प्रयागराज', 'इलाहाबाद']
            }
            for city, keywords in city_keywords.items():
                if any(kw in message_lower for kw in keywords):
                    session_context[session_id] = {
                        'city': city,
                        'filters': {},
                        'last_query': user_message
                    }
                    logger.info(f"📌 Saved session context during API error for {session_id}: city={city}")
                    break
            
            # Always use demo mode on any API error for better UX
            logger.warning("⚠️ API error occurred, using DEMO MODE for response")
            demo_response = get_demo_response(user_message, language=user_language)
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
        user_language = data.get('language', 'en')
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        def generate():
            try:
                language_aware_prompt = get_language_aware_system_prompt(user_language)
                response = model.generate_content(
                    [language_aware_prompt, user_message],
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
 