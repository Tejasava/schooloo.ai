# 🌐 Schooloo AI - Multilingual Language Support Guide

## ✨ Overview

The Schooloo AI application now fully supports **22 official Indian languages** with automatic language detection and language-specific responses.

---

## 📋 Supported Languages

| Code | Language | Script | Native Name |
|------|----------|--------|-------------|
| en | English | Latin | English |
| hi | Hindi | Devanagari | हिंदी |
| bn | Bengali | Bengali | বাংলা |
| te | Telugu | Telugu | తెలుగు |
| mr | Marathi | Devanagari | मराठी |
| ta | Tamil | Tamil | தமிழ் |
| gu | Gujarati | Gujarati | ગુજરાતી |
| kn | Kannada | Kannada | ಕನ್ನಡ |
| ml | Malayalam | Malayalam | മലയാളം |
| or | Odia | Odia | ଓଡ଼ିଆ |
| pa | Punjabi | Gurmukhi | ਪੰਜਾਬੀ |
| as | Assamese | Assamese | অসমীয়া |
| ks | Kashmiri | Perso-Arabic | کشمیری |
| ne | Nepali | Devanagari | नेपाली |
| sd | Sindhi | Perso-Arabic | سندھی |
| sa | Sanskrit | Devanagari | संस्कृतम् |
| ur | Urdu | Perso-Arabic | اردو |
| bo | Tibetan | Tibetan | བོད་སྐད། |
| mni | Manipuri | Meitei | ꯃꯤꯇꯩꯁꯨꯡ |
| mai | Maithili | Devanagari | मैथिली |
| si | Sinhala | Sinhala | සිංහල |
| doi | Dogri | Devanagari | डोगरी |

---

## 🎯 How It Works

### Frontend Flow

1. **First Load**: Language selector modal appears with all 22 languages
2. **User Selection**: User chooses their preferred language
3. **Persistence**: Language selection is saved to `localStorage`
4. **Every Request**: Selected language is sent to backend with each message

### Backend Flow

1. **Receive Request**: Backend receives `message`, `session_id`, and `language` code
2. **Generate Prompt**: `get_language_aware_system_prompt()` creates language-specific system prompt
3. **Add Instructions**: System prompt includes critical instruction to respond ONLY in selected language
4. **Send to AI**: Language-aware prompt + user message sent to Gemini AI
5. **Response**: AI responds entirely in the user's selected language

---

## 🔧 Technical Implementation

### Language-Aware System Prompt

The system prompt now includes dynamic language instructions:

```python
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
```

### Backend Code Changes

```python
# In chat endpoint:
language_aware_prompt = get_language_aware_system_prompt(user_language)
response = model.generate_content(
    [language_aware_prompt, user_message],
    generation_config=genai.types.GenerationConfig(...)
)
```

### Frontend Language Selection

```javascript
// Language selector modal appears on first load
function showLanguageModal() {
    languageModal.classList.remove('hidden');
    languageButtons.forEach(btn => {
        btn.addEventListener('click', selectLanguage);
    });
}

// Language selection handler
function selectLanguage(e) {
    const lang = e.target.dataset.lang;
    selectedLanguage = lang;
    localStorage.setItem('selectedLanguage', lang);
    
    // Close modal and continue
    languageModal.classList.add('hidden');
}
```

---

## 📝 System Prompt Structure

### Base Prompt (Language-Agnostic)
- Core responsibilities
- School details requirements
- Professional tone guidelines
- Response format standards

### Language-Specific Addition
- **CRITICAL instruction** to respond ONLY in selected language
- Do NOT mix languages
- Translate all content
- Use appropriate script

---

## 🧪 Testing

### Test 1: Language Selection
```bash
curl -X POST http://localhost:5002/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me about schools",
    "session_id": "test_001",
    "language": "hi"
  }'
```

### Test 2: Multilingual Response
```python
import requests

languages = ["en", "hi", "ta", "gu", "mr"]

for lang in languages:
    response = requests.post(
        'http://localhost:5002/api/chat',
        json={
            "message": "Schools in your city",
            "session_id": f"test_{lang}",
            "language": lang
        }
    )
    print(f"Language {lang}: Status {response.status_code}")
```

---

## 🔐 Key Features

### ✅ Complete Language Support
- All 22 official Indian languages
- Proper script support (Devanagari, Tamil, Telugu, etc.)
- Language persistence across sessions

### ✅ Language-Specific Responses
- AI responds ONLY in user's selected language
- No language mixing
- Professional formatting maintained

### ✅ User Experience
- Beautiful 4-column language grid on first load
- 2-column responsive layout on mobile
- Smooth language selection
- One-time selection (persistent in localStorage)

### ✅ Fallback Handling
- If language not specified, defaults to English
- Invalid language codes handled gracefully
- Session-based language tracking

---

## 🚀 Deployment Considerations

### For Production
1. **Language Persistence**: Uses `localStorage` - works across sessions on same device
2. **Multi-User**: Each user session gets unique `sessionId` - language per user session
3. **Scalability**: Language routing happens at backend - stateless design
4. **API Cost**: Each language generates unique prompt - no significant overhead

### For Internet Deployment
- Language selection modal appears first
- User language preference drives all responses
- No language mixing in responses
- Professional multilingual interface

---

## 📊 API Response Example

```json
{
  "success": true,
  "message": "...response in selected language...",
  "response": "...response in selected language...",
  "session_id": "session_123",
  "response_count": 1,
  "show_login_popup": false,
  "language": "hi",
  "model": "Schooloo AI",
  "mode": "demo"
}
```

---

## 🎓 Example Interactions

### English (en)
```
User: "Tell me about schools in Delhi"
AI: "Here are the best schools in Delhi..."
```

### Hindi (hi)
```
User: "दिल्ली में स्कूलों के बारे में बताएं"
AI: "दिल्ली के सर्वश्रेष्ठ स्कूलों की जानकारी यहां दी गई है..."
```

### Tamil (ta)
```
User: "சென்னையில் உள்ள பள்ளிகளைப் பற்றி சொல்லுங்கள்"
AI: "சென்னையில் உள்ள சிறந்த பள்ளிகள் இங்கே உள்ளன..."
```

---

## 🔧 Configuration

### To Add More Languages
1. Add language code and name to `LANGUAGE_NAMES` dictionary
2. Add button to language grid in `index.html`
3. Restart backend - automatic support!

### To Change Language Grid Layout
- Desktop: 4 columns (edit line 576 in CSS)
- Mobile: 2 columns (edit line 750 in CSS)

---

## ✅ Verification Checklist

- [ ] 22 languages appear in language selector modal
- [ ] Language selection saves to localStorage
- [ ] Language preference persists on page reload
- [ ] Backend receives language code in requests
- [ ] System prompt includes language-specific instructions
- [ ] Responses are in selected language (when using real API)
- [ ] Multilingual modal is beautiful and responsive

---

## 📞 Support

For language-related issues:
1. Check language code is valid (must be in `LANGUAGE_NAMES`)
2. Verify browser's localStorage is enabled
3. Clear browser cache if language selection not persisting
4. Check backend logs: `grep "LANGUAGE REQUIREMENT" backend.log`

---

**Last Updated**: January 30, 2026
**Version**: 1.0.0 - Complete Multilingual Support
