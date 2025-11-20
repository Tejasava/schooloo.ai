# 🎓 Schooloo AI - School Discovery Agent

> An intelligent AI-powered school discovery platform for India, powered by Google's Gemini 2.0 Flash

[![Deploy on Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FYOUR_USERNAME%2Fschooloo-agent&env=API_KEY&envDescription=Google%20Gemini%20API%20Key&envLink=https%3A%2F%2Fai.google.dev%2F)

## ✨ Live Demo

🌐 **[View Live](https://schooloo-agent.vercel.app)** (if deployed)

## 🎯 About Schooloo

Schooloo is an AI chatbot that helps students and parents discover the perfect school across India. Using advanced natural language processing and comprehensive school data, Schooloo provides:

- **Personalized Recommendations**: Get schools matched to your preferences
- **Real School Data**: Actual fees, curriculum, facilities, and reviews
- **City-Specific Results**: Find schools in any Indian city
- **Smart Filtering**: Filter by budget, board, specialization, and more
- **Instant Answers**: Get responses in seconds, not hours

### Sample Questions

- "Find best CBSE schools in Prayagraj under ₹50,000"
- "What are the top boarding schools in India?"
- "Science schools in Mumbai with good infrastructure"
- "ICSE schools in Delhi with sports facilities"

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Google Gemini API Key ([get one free](https://ai.google.dev/))
- (Optional) Vercel account for deployment

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/schooloo-agent.git
cd schooloo-agent

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your API_KEY
nano .env

# Run locally
python3 app.py
# Visit http://localhost:5000
```

## 📦 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Flask 3.0+ |
| **AI Model** | Google Gemini 2.0 Flash |
| **Frontend** | Vanilla HTML5/CSS3/JS |
| **Deployment** | Vercel Serverless |
| **Database** | Optional (In-Memory) |

## 🌐 Deployment

### Deploy on Vercel (Recommended)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FYOUR_USERNAME%2Fschooloo-agent&env=API_KEY&envDescription=Google%20Gemini%20API%20Key&envLink=https%3A%2F%2Fai.google.dev%2F)

Or manually:

1. Push code to GitHub
2. Sign in to [Vercel](https://vercel.com/dashboard)
3. Click "New Project" → "Import Git Repository"
4. Select your GitHub repo
5. Add environment variable: `API_KEY=your_api_key`
6. Click "Deploy" 🎉

**[Detailed Deployment Guide](./VERCEL_DEPLOYMENT_GUIDE.md)**

## 📚 API Documentation

### POST `/api/chat`
Send a message and get a response.

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Best schools in Delhi"}'
```

**Response:**
```json
{
  "success": true,
  "message": "Here are the best schools in Delhi...",
  "model": "gemini-2.0-flash"
}
```

### GET `/api/health`
Check if the backend is running.

```bash
curl http://localhost:5000/api/health
```

**Response:**
```json
{
  "status": "online",
  "message": "Schooloo AI Backend is running",
  "model": "gemini-2.0-flash"
}
```

### GET `/api/models`
Get available AI models.

```bash
curl http://localhost:5000/api/models
```

[Full API Documentation](./docs/API_EXAMPLES.md)

## 🛠 Development

### Project Structure

```
schooloo-agent/
├── app.py                    # Main Flask app
├── index.html                # Frontend (single-page app)
├── requirements.txt          # Python dependencies
├── .env.example              # Example config
├── vercel.json              # Vercel configuration
├── api/
│   └── index.py             # Serverless handler
├── agent/                    # AI agent modules
├── backend/                  # Additional backend modules
└── docs/                     # Documentation
```

### Run Locally

```bash
# Development mode
FLASK_ENV=development python3 app.py

# Production mode
FLASK_ENV=production python3 app.py
```

### Testing

```bash
# Run tests
python3 -m pytest

# Test specific endpoint
curl http://localhost:5000/api/health
```

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```env
# Required
API_KEY=your_google_gemini_api_key

# Optional
AGENT_MODEL=gemini-2.0-flash
FLASK_ENV=development
FLASK_PORT=5000
```

**Get your API key:**
1. Go to [Google AI Studio](https://ai.google.dev/)
2. Click "Get API Key"
3. Create new API key or select existing one
4. Copy and paste into `.env`

## 📊 Features

- ✅ AI-powered school recommendations
- ✅ Real school data and pricing
- ✅ Multi-city support (all major Indian cities)
- ✅ Smart filtering and search
- ✅ Responsive mobile design
- ✅ Zero external JS dependencies (lightweight)
- ✅ CORS-enabled API
- ✅ Rate limiting support
- ✅ Error handling and logging

## 🎨 Customization

### Change the AI Personality

Edit the `system_prompt` in `app.py`:

```python
system_prompt = """You are Schooloo AI Assistant - an expert school discovery assistant...
[Customize the prompt here]
"""
```

### Style the Frontend

Edit the CSS in `index.html` `<style>` section. The design uses:
- CSS Grid and Flexbox
- CSS Custom Properties (variables)
- Gradient backgrounds
- CSS animations

### Add More Quick Actions

Edit `index.html` around line 530:

```html
<button class="quick-btn" data-question="Your custom question">🔍 Custom</button>
```

## 🐛 Troubleshooting

### "Could not reach the server"
- Check backend is running: `curl http://localhost:5000/api/health`
- Verify port 5000 is not in use: `lsof -i :5000`
- Check CORS headers in browser DevTools

### "API key not found"
- Verify `.env` file exists and has `API_KEY=...`
- Check file is not in `.gitignore`
- On Vercel, check Settings → Environment Variables

### Rate limit exceeded (429)
- Wait a moment and retry
- Google Gemini has usage limits
- Consider implementing request queuing

## 📈 Performance

- **Page Load**: < 1s (pure HTML/CSS/JS, no frameworks)
- **API Response**: 1-3s (Gemini processing)
- **Serverless Cold Start**: < 2s (Vercel optimized)

## 🔒 Security

- 🔒 No user data stored (stateless)
- 🔒 API key never exposed to frontend
- 🔒 HTTPS enforced on Vercel
- 🔒 CORS configured for specific origins
- 🔒 Input sanitization on backend

## 📝 License

MIT License - See [LICENSE](./LICENSE) for details

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Commit: `git commit -m 'Add amazing feature'`
5. Push: `git push origin feature/amazing-feature`
6. Open a Pull Request

## 💬 Support

- **Documentation**: Check `/docs` folder
- **Issues**: [Open an issue](https://github.com/YOUR_USERNAME/schooloo-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/schooloo-agent/discussions)
- **Email**: support@schooloo.ai

## 🙏 Acknowledgments

- [Google Generative AI](https://ai.google.dev/) - Powering the intelligence
- [Flask](https://flask.palletsprojects.com/) - Backend framework
- [Vercel](https://vercel.com/) - Hosting platform

## 📊 Status

- ✅ Production Ready
- ✅ Vercel Deployable
- ✅ Fully Documented
- 🚀 Ready to Scale

## 🚀 What's Next?

- [ ] Add school rating system
- [ ] Integrate school comparison
- [ ] Add parent reviews
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard

## 📌 Changelog

### v1.0 (Current)
- Initial release
- Gemini 2.0 Flash integration
- Full API implementation
- Responsive frontend
- Vercel deployment support

---

**Made with ❤️ by the Schooloo Team**

**Questions? Need help? [Contact us](mailto:support@schooloo.ai)**

**Happy School Hunting! 🎓**
