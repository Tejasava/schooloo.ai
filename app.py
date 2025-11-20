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
if not api_key:
    logger.error("API_KEY not found in .env file")
    sys.exit(1)

genai.configure(api_key=api_key)
model_name = os.getenv('AGENT_MODEL', 'gemini-2.0-flash')
model = genai.GenerativeModel(model_name)

# System prompt for the agent
system_prompt = """You are Schooloo AI Assistant - an expert school discovery assistant for India.

You have comprehensive knowledge about schools across ALL Indian cities.

CRITICAL RULES:
1. When asked about a SPECIFIC city (e.g., Prayagraj, Delhi, Mumbai), ALWAYS provide schools from THAT EXACT city
2. Provide REAL school names, fees (in ₹), boards (CBSE/ICSE/ISC), and facilities
3. Include follow-up questions to help refine recommendations
4. Be helpful, accurate, and personalized
5. Format responses with clear sections and bullet points
6. Include emojis for better visual appeal
7. the response should be in point wise clean and professional and proper space should be in different pints. 

Example Prayagraj schools:
- St. Mary's Convent School (CBSE, ₹1.5L-2.5L/year, Girls School)
- St. Joseph's College (ICSE, ₹1.2L-2.0L/year, Boys School)
- Colvin College (ICSE/ISC, ₹1.3L-2.2L/year, Co-educational)

Always provide real school information with details."""

# Store conversation history (in-memory)
conversation_history = []


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
        
        if not user_message:
            return jsonify({
                'error': 'Empty message',
                'message': 'Please provide a non-empty message'
            }), 400
        
        logger.info(f"Received message: {user_message}")
        
        try:
            # Call Gemini API
            response = model.generate_content(
                [system_prompt, user_message],
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
                'model': model_name
            }), 200
        
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Gemini API error: {error_msg}")
            
            # Check for quota exceeded
            if "429" in error_msg or "quota" in error_msg.lower():
                return jsonify({
                    'error': 'API Quota Exceeded',
                    'message': 'Daily API quota exceeded. Please try again tomorrow or upgrade your plan.',
                    'details': error_msg
                }), 429
            
            return jsonify({
                'error': 'API Error',
                'message': f'Error from AI model: {error_msg}'
            }), 500
    
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
