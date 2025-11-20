"""Flask backend for Schooloo"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid
import math
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import db, School, Lead
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# ============ HEALTH CHECK ============

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Schooloo Backend"})

# ============ SCHOOL ENDPOINTS ============

@app.route('/api/schools', methods=['GET'])
def get_schools():
    """Get all schools"""
    schools = db.get_all_schools()
    return jsonify({
        "success": True,
        "data": [s.to_dict() for s in schools],
        "count": len(schools)
    })

@app.route('/api/schools/<school_id>', methods=['GET'])
def get_school(school_id):
    """Get school by ID"""
    school = db.get_school_by_id(school_id)
    if not school:
        return jsonify({"success": False, "error": "School not found"}), 404
    return jsonify({"success": True, "data": school.to_dict()})

@app.route('/api/schools/search', methods=['POST'])
def search_schools():
    """Search schools by location and criteria"""
    data = request.get_json()
    location = data.get('location', '')
    
    schools = db.get_schools_by_location(location) if location else db.get_all_schools()
    
    return jsonify({
        "success": True,
        "data": [s.to_dict() for s in schools],
        "count": len(schools)
    })

@app.route('/api/schools/nearby', methods=['POST'])
def get_nearby_schools():
    """Get schools nearby based on latitude and longitude"""
    data = request.get_json()
    lat = data.get('latitude')
    lon = data.get('longitude')
    radius_km = data.get('radius_km', 5)
    
    if not lat or not lon:
        return jsonify({"success": False, "error": "Latitude and longitude required"}), 400
    
    def haversine(lat1, lon1, lat2, lon2):
        """Calculate distance between two points"""
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return R * c
    
    nearby = []
    for school in db.get_all_schools():
        distance = haversine(lat, lon, school.latitude, school.longitude)
        if distance <= radius_km:
            school_dict = school.to_dict()
            school_dict['distance_km'] = round(distance, 2)
            nearby.append(school_dict)
    
    nearby.sort(key=lambda x: x['distance_km'])
    
    return jsonify({
        "success": True,
        "data": nearby,
        "count": len(nearby)
    })

# ============ ADMISSION ENDPOINTS ============

@app.route('/api/admissions/<school_id>', methods=['GET'])
def get_admission_info(school_id):
    """Get admission info for a school"""
    admission = db.get_admission_info(school_id)
    if not admission:
        return jsonify({"success": False, "error": "Admission info not found"}), 404
    return jsonify({"success": True, "data": admission.to_dict()})

@app.route('/api/admissions/documents/<school_id>', methods=['GET'])
def get_required_documents(school_id):
    """Get required documents for admission"""
    admission = db.get_admission_info(school_id)
    if not admission:
        return jsonify({"success": False, "error": "School not found"}), 404
    return jsonify({
        "success": True,
        "school_id": school_id,
        "documents": admission.required_documents
    })

@app.route('/api/admissions/exam-pattern/<school_id>', methods=['GET'])
def get_exam_pattern(school_id):
    """Get entrance exam pattern"""
    admission = db.get_admission_info(school_id)
    if not admission:
        return jsonify({"success": False, "error": "School not found"}), 404
    
    if not admission.entrance_exam_required:
        return jsonify({
            "success": True,
            "exam_required": False,
            "message": "No entrance exam required"
        })
    
    return jsonify({
        "success": True,
        "exam_required": True,
        "exam_name": admission.exam_name,
        "exam_pattern": admission.exam_pattern,
        "syllabus": "Available on school website"
    })

@app.route('/api/admissions/eligibility/<school_id>', methods=['GET'])
def get_eligibility(school_id):
    """Get eligibility criteria"""
    admission = db.get_admission_info(school_id)
    if not admission:
        return jsonify({"success": False, "error": "School not found"}), 404
    return jsonify({
        "success": True,
        "school_id": school_id,
        "eligibility": admission.eligibility_criteria
    })

# ============ FAQ ENDPOINTS ============

@app.route('/api/faqs', methods=['GET'])
def get_faqs():
    """Get all FAQs"""
    category = request.args.get('category', None)
    
    if category:
        faqs = db.get_faqs_by_category(category)
    else:
        faqs = list(db.faqs.values())
    
    return jsonify({
        "success": True,
        "data": [f.to_dict() for f in faqs],
        "count": len(faqs)
    })

@app.route('/api/faqs', methods=['POST'])
def create_faq():
    """Create a new FAQ"""
    data = request.get_json()
    faq_id = str(uuid.uuid4())
    
    from database import FAQ
    faq = FAQ(
        id=faq_id,
        question=data.get('question'),
        answer=data.get('answer'),
        category=data.get('category', 'general'),
        school_id=data.get('school_id'),
        updated_at=datetime.now().isoformat()
    )
    
    db.faqs[faq.id] = faq
    return jsonify({"success": True, "data": faq.to_dict()}), 201

# ============ LEAD ENDPOINTS ============

@app.route('/api/leads', methods=['POST'])
def create_lead():
    """Create a new lead"""
    data = request.get_json()
    lead_id = str(uuid.uuid4())
    
    lead = Lead(
        id=lead_id,
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone'),
        school_interested=data.get('school_interested'),
        query_type=data.get('query_type', 'general'),  # parent, student, admin
        query_text=data.get('query_text'),
        status="new",
        created_at=datetime.now().isoformat()
    )
    
    db.create_lead(lead)
    return jsonify({"success": True, "data": lead.to_dict()}), 201

@app.route('/api/leads', methods=['GET'])
def get_leads():
    """Get all leads (admin endpoint)"""
    leads = db.get_all_leads()
    return jsonify({
        "success": True,
        "data": [l.to_dict() for l in leads],
        "count": len(leads)
    })

@app.route('/api/leads/<lead_id>', methods=['PATCH'])
def update_lead(lead_id):
    """Update lead status"""
    data = request.get_json()
    lead = db.leads.get(lead_id)
    
    if not lead:
        return jsonify({"success": False, "error": "Lead not found"}), 404
    
    if 'status' in data:
        lead.status = data['status']
    
    return jsonify({"success": True, "data": lead.to_dict()})

# ============ COMPARISON ENDPOINT ============

@app.route('/api/schools/compare', methods=['POST'])
def compare_schools():
    """Compare multiple schools"""
    data = request.get_json()
    school_ids = data.get('school_ids', [])
    
    schools_data = []
    for school_id in school_ids:
        school = db.get_school_by_id(school_id)
        if school:
            schools_data.append(school.to_dict())
    
    if not schools_data:
        return jsonify({"success": False, "error": "No schools found"}), 404
    
    return jsonify({
        "success": True,
        "data": schools_data,
        "comparison": {
            "count": len(schools_data),
            "schools": [s['name'] for s in schools_data]
        }
    })

# ============ ERROR HANDLERS ============

@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(__import__('os').getenv('FLASK_PORT', 5000))
    app.run(debug=True, port=port)
