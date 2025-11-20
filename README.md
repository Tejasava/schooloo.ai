# Schooloo AI Agent - Complete Documentation

## 📋 Overview

Schooloo is an AI-powered school discovery and admission platform with an intelligent agent built using Google's Agent Development Kit (ADK). The system helps parents, students, and administrators with school information, admissions, and lead management.

## 🚀 Features

### Parent Features
- ✅ Find best schools nearby
- ✅ Compare fee structures
- ✅ Check admission deadlines
- ✅ Get school comparisons
- ✅ View eligibility criteria
- ✅ Access FAQs

### Student Features
- ✅ Get required documents for admission
- ✅ Learn entrance exam patterns
- ✅ Find information about transport/hostel/location
- ✅ Understand eligibility requirements
- ✅ Access student-specific FAQs

### Admin Features
- ✅ Capture new leads
- ✅ View all leads
- ✅ Update lead status
- ✅ Manage FAQs
- ✅ View school listings

## 📂 Project Structure

```
schooloo-agent/
├── backend/
│   ├── app.py              # Flask API endpoints
│   ├── config.py           # Configuration
│   └── database.py         # Data models and management
├── agent/
│   ├── schooloo_agent.py   # Main agent with Google ADK
│   ├── tools.py            # Tool implementations
│   └── query_processor.py  # Query routing and formatting
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
└── README.md              # This file
```

## 🔧 Setup Instructions

### 1. Install Dependencies

```bash
cd schooloo-agent
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
cp .env.example .env
# Edit .env with your values:
# - GOOGLE_CLOUD_PROJECT_ID
# - GOOGLE_APPLICATION_CREDENTIALS
# - GOOGLE_API_KEY (for Gemini)
# - FLASK_PORT (default: 5000)
```

### 3. Start the Backend

```bash
cd backend
python app.py
```

The API will be available at `http://localhost:5000/api`

### 4. Run the Agent

In a new terminal:

```bash
# Run all examples
python main.py

# Or run specific mode
python main.py --mode parent
python main.py --mode student
python main.py --mode admin
python main.py --mode interactive
python main.py --mode api
```

## 🛠️ API Endpoints

### Schools
- `GET /api/schools` - Get all schools
- `GET /api/schools/<id>` - Get school details
- `POST /api/schools/search` - Search schools by location
- `POST /api/schools/nearby` - Get nearby schools (GPS)
- `POST /api/schools/compare` - Compare multiple schools

### Admissions
- `GET /api/admissions/<school_id>` - Get admission info
- `GET /api/admissions/documents/<school_id>` - Get required documents
- `GET /api/admissions/exam-pattern/<school_id>` - Get exam pattern
- `GET /api/admissions/eligibility/<school_id>` - Get eligibility

### FAQs
- `GET /api/faqs` - Get FAQs (optional: ?category=parent|student)
- `POST /api/faqs` - Create new FAQ

### Leads
- `POST /api/leads` - Create new lead
- `GET /api/leads` - Get all leads (admin)
- `PATCH /api/leads/<lead_id>` - Update lead status

## 🤖 Agent Tools

The AI agent has access to the following tools:

1. **search_schools** - Search schools by location
2. **get_nearby_schools** - Find schools near GPS coordinates
3. **get_school_details** - Get full school information
4. **get_fee_structure** - View fees by class
5. **compare_schools** - Compare multiple schools
6. **get_admission_info** - Get admission requirements
7. **get_required_documents** - List required admission docs
8. **get_exam_pattern** - Get entrance exam details
9. **get_eligibility_criteria** - View eligibility requirements
10. **get_faqs** - Access frequently asked questions
11. **capture_lead** - Create new lead inquiry
12. **get_all_leads** - View all leads (admin)
13. **update_lead_status** - Change lead status (admin)

## 📝 Example Usage

### As a Parent
```python
system = SchoolooAISystem()
result = system.handle_query("What are the best schools in Delhi?", "parent")
```

### As a Student
```python
system = SchoolooAISystem()
result = system.handle_query("What documents do I need for admission?", "student")
```

### As an Admin
```python
system = SchoolooAISystem()
result = system.handle_query("Show me all new leads", "admin")
```

### Using Tools Directly
```python
system = SchoolooAISystem()
result = system.execute_tool("search_schools", {"location": "Delhi"})
```

## 🔌 Integration with Google ADK

The agent uses Google's Generative AI API (Gemini) with the following capabilities:

- **Multi-turn Conversations** - Maintains context across queries
- **Tool Calling** - Automatically invokes appropriate tools
- **Intent Recognition** - Understands user intent and routes to correct tools
- **Natural Language** - Provides conversational, natural responses

### Configuration

```python
from agent.schooloo_agent import SchoolooAgent

# Initialize with API key
agent = SchoolooAgent(api_key="your-google-api-key")

# Chat with the agent
response = agent.chat("What schools are near me?")
```

## 📊 Sample Data

The system comes with sample data including:

**Schools:**
- Delhi Public School (DPS) - Delhi
- Greenfield Public School - Bangalore

**Admissions:**
- Entrance exams, documents, deadlines, eligibility criteria

**FAQs:**
- Parent and student categories
- Questions about fees, dress code, hostels, etc.

## 🔐 Security Notes

- Store API keys in `.env` file (never commit)
- Use environment variables for sensitive data
- Validate all user inputs
- Implement authentication for admin endpoints

## 📈 Scalability

To scale this system:

1. **Database** - Replace in-memory storage with MongoDB/PostgreSQL
2. **Caching** - Add Redis for frequently accessed data
3. **Load Balancing** - Use load balancer for multiple API instances
4. **Queue System** - Implement Celery for async tasks (lead processing)
5. **Search** - Integrate Elasticsearch for advanced search

## 🚀 Deployment

### Using Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py", "--mode", "interactive"]
```

### Using Google Cloud

```bash
gcloud app deploy
```

### Using Heroku

```bash
git push heroku main
```

## 📞 Support

For issues or questions:
1. Check the FAQ section in the app
2. Review API documentation
3. Check backend logs for errors

## 📄 License

MIT License - Feel free to use and modify

## 🎯 Future Enhancements

- [ ] Video tours of schools
- [ ] Student testimonials
- [ ] Real-time admission tracking
- [ ] Payment integration
- [ ] SMS/Email notifications
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Mobile app
- [ ] Integration with WhatsApp Business API
- [ ] School virtual events

---

**Built with ❤️ using Google Agent Development Kit**
