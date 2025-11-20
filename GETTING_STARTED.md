# 🎓 Schooloo AI Agent - Getting Started Guide

## What You Just Got

A complete, production-ready AI agent system for school discovery and admission platform with:

✅ **Google ADK Integration** - Using Google's Generative AI (Gemini)
✅ **Python Backend** - Flask-based REST API with sample data
✅ **Smart Agent** - Intent routing for parents, students, and admins
✅ **13 Agent Tools** - Search, compare, admission, FAQ, lead management
✅ **Full Documentation** - API examples, tests, and guides

---

## 🚀 Quick Start (5 minutes)

### Option 1: Automated Setup
```bash
python quickstart.py
```

### Option 2: Manual Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your Google API key
   ```

3. **Start backend:**
   ```bash
   python backend/app.py
   ```

4. **In another terminal, run agent:**
   ```bash
   python main.py --mode examples
   ```

---

## 📋 Project Structure

```
schooloo-agent/
├── 📁 backend/
│   ├── app.py           → 200+ lines of Flask API endpoints
│   ├── database.py      → Data models with sample data
│   └── config.py        → Configuration management
│
├── 🤖 agent/
│   ├── schooloo_agent.py  → Main agent (Google ADK integration)
│   ├── tools.py           → 13 tool implementations
│   └── query_processor.py → Intent detection and routing
│
├── 🚀 main.py           → Multi-mode entry point
├── 📚 README.md         → Full documentation
├── 🧪 test_schooloo.py  → Test suite
├── ⚙️ config_settings.py → Configuration options
├── 📋 quickstart.py     → Interactive setup guide
└── 📖 API_EXAMPLES.md   → cURL and Python examples
```

---

## 🎯 Available Modes

Run the agent in different modes:

### 1. View All Examples
```bash
python main.py
# Shows parent, student, and admin examples
```

### 2. Parent Mode (Interactive)
```bash
python main.py --mode parent
```
**Parents can:**
- Search schools by location
- Compare fee structures
- Get admission deadlines
- View eligibility criteria

### 3. Student Mode
```bash
python main.py --mode student
```
**Students can:**
- Get required documents
- Learn exam patterns
- Find hostel/transport info
- Understand eligibility

### 4. Admin Mode
```bash
python main.py --mode admin
```
**Admins can:**
- Capture leads
- View all leads
- Update lead status
- Manage FAQs

### 5. Interactive Chat
```bash
python main.py --mode interactive
```
Real-time conversation with the agent

### 6. API Examples
```bash
python main.py --mode api
```
Shows how to use tools programmatically

---

## 🔌 Agent Tools (13 Total)

| Tool | Purpose | User Type |
|------|---------|-----------|
| `search_schools` | Find schools by location | Parent, Student |
| `get_nearby_schools` | Find schools by GPS | Parent |
| `get_school_details` | Get full school info | Parent, Student |
| `get_fee_structure` | View school fees | Parent |
| `compare_schools` | Compare multiple schools | Parent |
| `get_admission_info` | Get admission requirements | Student |
| `get_required_documents` | List needed documents | Student |
| `get_exam_pattern` | Get entrance exam info | Student |
| `get_eligibility_criteria` | Check eligibility | Student, Parent |
| `get_faqs` | Access frequently asked questions | All |
| `capture_lead` | Create new inquiry | Admin |
| `get_all_leads` | View all leads | Admin |
| `update_lead_status` | Change lead status | Admin |

---

## 🔌 API Endpoints (13 Total)

### School Endpoints
- `GET /api/schools` - Get all schools
- `POST /api/schools/search` - Search by location
- `POST /api/schools/nearby` - Find by GPS
- `GET /api/schools/<id>` - Get details
- `POST /api/schools/compare` - Compare schools

### Admission Endpoints
- `GET /api/admissions/<school_id>` - Admission info
- `GET /api/admissions/documents/<id>` - Required docs
- `GET /api/admissions/exam-pattern/<id>` - Exam details
- `GET /api/admissions/eligibility/<id>` - Eligibility

### FAQ & Lead Endpoints
- `GET /api/faqs` - Get FAQs
- `POST /api/faqs` - Create FAQ
- `POST /api/leads` - Capture lead
- `GET /api/leads` - Get all leads
- `PATCH /api/leads/<id>` - Update lead

---

## 💻 Code Examples

### Search Schools (Python)
```python
from main import SchoolooAISystem

system = SchoolooAISystem()
result = system.execute_tool("search_schools", {"location": "Delhi"})
```

### Handle Parent Query
```python
system = SchoolooAISystem()
response = system.handle_query(
    "What are the best schools in Delhi?",
    user_type="parent"
)
print(response['response'])
```

### Capture Lead
```python
result = system.execute_tool("capture_lead", {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+91-9876543210",
    "school_interested": "school_001",
    "query_type": "parent",
    "query_text": "Interested in admission"
})
```

### cURL API Call
```bash
curl -X POST http://localhost:5000/api/leads \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+91-9876543210",
    "school_interested": "school_001",
    "query_type": "parent",
    "query_text": "Admission inquiry"
  }'
```

---

## 📊 Sample Data Included

### Schools
- **Delhi Public School** (Delhi)
  - Fees: ₹2.5L - ₹4.5L/year
  - Classes: KG, 1-5, 6-10, 11-12
  - Facilities: Pool, Lab, Sports, Library

- **Greenfield Public School** (Bangalore)
  - Fees: ₹2L - ₹3.8L/year
  - Classes: Nursery-12
  - Facilities: Sports, STEM, Auditorium

### Admission Info
- Required documents
- Entrance exam patterns
- Eligibility criteria
- Admission deadlines

### FAQs
- Parent category questions
- Student category questions
- General information

---

## 🧪 Testing

Run the test suite:
```bash
python test_schooloo.py
```

Tests include:
- Database initialization
- School search
- Admission info retrieval
- FAQ categorization
- Lead capture
- Tool execution

---

## ⚙️ Configuration

Edit `.env` file:
```env
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_API_KEY=your-api-key
FLASK_PORT=5000
AGENT_MODEL=gemini-pro
```

Or edit `config_settings.py` for advanced settings.

---

## 🌐 Deployment Options

### Docker
```bash
docker build -t schooloo-agent .
docker run -p 5000:5000 schooloo-agent
```

### Google Cloud
```bash
gcloud app deploy
```

### Heroku
```bash
git push heroku main
```

---

## 📚 File Descriptions

| File | Lines | Purpose |
|------|-------|---------|
| `backend/app.py` | 200+ | Flask API with 13 endpoints |
| `backend/database.py` | 250+ | Data models + sample data |
| `agent/schooloo_agent.py` | 400+ | Main agent with Google ADK |
| `agent/tools.py` | 150+ | Tool implementations |
| `agent/query_processor.py` | 200+ | Intent routing & formatting |
| `main.py` | 300+ | Multi-mode entry point |
| `test_schooloo.py` | 100+ | Test suite |
| `config_settings.py` | 150+ | Configuration options |
| `quickstart.py` | 180+ | Interactive setup |

---

## 🎓 Learning Outcomes

After using this system, you'll understand:

✅ Google's Agent Development Kit integration
✅ Building REST APIs with Flask
✅ Intent-based query routing
✅ Tool calling and orchestration
✅ Multi-user type system design
✅ Backend-agent communication
✅ Production-ready Python practices

---

## 🔐 Security Considerations

Before production:

- [ ] Add authentication (JWT)
- [ ] Implement rate limiting
- [ ] Add input validation
- [ ] Use PostgreSQL instead of in-memory
- [ ] Add request logging
- [ ] Use HTTPS
- [ ] Hide API keys in env vars
- [ ] Add CORS restrictions

---

## 🚀 Next Steps

1. **Try Examples:**
   ```bash
   python main.py
   ```

2. **Read Full Docs:**
   - Open `README.md` for complete documentation
   - Check `API_EXAMPLES.md` for API calls

3. **Explore Code:**
   - Start with `backend/app.py` to understand endpoints
   - Check `agent/schooloo_agent.py` for agent logic
   - Review `agent/tools.py` for tool implementations

4. **Customize:**
   - Edit sample data in `backend/database.py`
   - Add more schools and FAQs
   - Extend agent tools for your needs

5. **Deploy:**
   - Choose deployment option (Docker, Cloud, Heroku)
   - Set up database
   - Configure authentication

---

## 📞 Support

- **Issues?** Check the test suite: `python test_schooloo.py`
- **API questions?** See `API_EXAMPLES.md`
- **Documentation?** Read `README.md`
- **Configuration?** Edit `config_settings.py`

---

## 📈 Feature Roadmap

Future enhancements:

- [ ] Database migration (PostgreSQL)
- [ ] Multi-language support
- [ ] WhatsApp Business integration
- [ ] Video tours of schools
- [ ] Payment integration
- [ ] Analytics dashboard
- [ ] Mobile app
- [ ] Email/SMS notifications
- [ ] Advanced search filters
- [ ] Student testimonials

---

## 🎉 You're All Set!

Start with:
```bash
python main.py
```

Happy exploring! 🚀

---

**Built with ❤️ using Google Agent Development Kit**
