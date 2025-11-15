#!/usr/bin/env python3
"""
Interactive Schooloo AI Agent - Demo Mode (Offline)
Works without consuming API quota by using local responses
"""
import os
import sys
import json
import time
from typing import Optional
from datetime import datetime

# Add agent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agent'))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

class DemoSchoolooAgent:
    """Demo Schooloo AI Agent with Offline Mode"""
    
    def __init__(self):
        """Initialize the demo agent"""
        # Sample data from database
        self.schools = {
            "dps": {
                "id": "dps-001",
                "name": "Delhi Public School",
                "location": "New Delhi",
                "latitude": 28.5244,
                "longitude": 77.1855,
                "classes": ["KG", "1-5", "6-10", "11-12"],
                "fee_structure": "₹2.5L - ₹4.5L/year",
                "facilities": ["Library", "Lab", "Sports", "Auditorium"],
                "entrance_exam": True,
                "contact": "+91-11-4653-0000",
                "website": "www.delhipublicschool.edu.in"
            },
            "greenfield": {
                "id": "greenfield-001",
                "name": "Greenfield Public School",
                "location": "Bangalore",
                "latitude": 13.0827,
                "longitude": 77.6104,
                "classes": ["Nursery", "KG", "1-5", "6-10", "11-12"],
                "fee_structure": "₹2L - ₹3.8L/year",
                "facilities": ["Library", "Pool", "Lab", "Gym"],
                "entrance_exam": False,
                "contact": "+91-80-4161-0000",
                "website": "www.greenfieldpublic.edu.in"
            }
        }
        
        self.faqs = {
            "admission_fee": {
                "question": "What is the admission fee?",
                "answer": "Admission fees vary by school and class. Usually ₹10,000 - ₹50,000.",
                "category": "parent"
            },
            "transport": {
                "question": "Do you provide transportation?",
                "answer": "Yes, most schools provide transportation with additional charges.",
                "category": "parent"
            },
            "documents": {
                "question": "What documents are needed?",
                "answer": "Birth certificate, previous school records, address proof, passport photos",
                "category": "student"
            },
            "exam_pattern": {
                "question": "What is the entrance exam pattern?",
                "answer": "Entrance exams typically cover Math, English, and General Knowledge.",
                "category": "student"
            }
        }
        
        self.leads_db = []
        self.conversation_count = 0
    
    def search_schools(self, location: str) -> dict:
        """Search schools by location"""
        results = []
        for school_id, school in self.schools.items():
            if location.lower() in school['location'].lower():
                results.append({
                    "id": school["id"],
                    "name": school["name"],
                    "location": school["location"],
                    "fee_structure": school["fee_structure"]
                })
        
        return {
            "success": True,
            "total": len(results),
            "schools": results
        }
    
    def get_school_details(self, location: str) -> dict:
        """Get detailed school information"""
        for school_id, school in self.schools.items():
            if location.lower() in school['location'].lower() or location.lower() in school['name'].lower():
                return {
                    "success": True,
                    "school": school
                }
        return {"success": False, "error": "School not found"}
    
    def compare_schools(self) -> dict:
        """Compare available schools"""
        comparison = []
        for school_id, school in self.schools.items():
            comparison.append({
                "name": school["name"],
                "location": school["location"],
                "fee_structure": school["fee_structure"],
                "entrance_exam": school["entrance_exam"],
                "facilities": school["facilities"]
            })
        return {"success": True, "schools": comparison}
    
    def get_admission_info(self, school_name: str) -> dict:
        """Get admission information"""
        for school_id, school in self.schools.items():
            if school_name.lower() in school['name'].lower():
                return {
                    "success": True,
                    "school": school['name'],
                    "entrance_exam": school['entrance_exam'],
                    "documents_required": ["Birth Certificate", "Previous School Records", "Address Proof", "Passport Photos"],
                    "eligibility": "Must have passed previous class with minimum 40% marks",
                    "contact": school['contact']
                }
        return {"success": False, "error": "School not found"}
    
    def get_faqs(self, category: str = "general") -> dict:
        """Get FAQs by category"""
        faqs = []
        for faq_id, faq in self.faqs.items():
            if category == "general" or faq['category'] == category:
                faqs.append(faq)
        return {"success": True, "faqs": faqs}
    
    def capture_lead(self, name: str, email: str, phone: str) -> dict:
        """Capture a lead"""
        lead = {
            "id": f"lead-{len(self.leads_db) + 1}",
            "name": name,
            "email": email,
            "phone": phone,
            "timestamp": datetime.now().isoformat(),
            "status": "new"
        }
        self.leads_db.append(lead)
        return {"success": True, "message": f"Lead captured for {name}", "lead_id": lead["id"]}
    
    def process_query(self, user_input: str) -> str:
        """Process user query and return response"""
        self.conversation_count += 1
        user_input_lower = user_input.lower()
        
        # Search schools
        if any(keyword in user_input_lower for keyword in ['school', 'search', 'find', 'best school', 'near']):
            if 'delhi' in user_input_lower:
                result = self.search_schools("Delhi")
                if result['schools']:
                    response = f"🎓 Found {result['total']} school(s) in Delhi:\n\n"
                    for school in result['schools']:
                        response += f"📍 **{school['name']}**\n"
                        response += f"   Location: {school['location']}\n"
                        response += f"   Fees: {school['fee_structure']}\n\n"
                    return response
            elif 'bangalore' in user_input_lower or 'bengaluru' in user_input_lower:
                result = self.search_schools("Bangalore")
                if result['schools']:
                    response = f"🎓 Found {result['total']} school(s) in Bangalore:\n\n"
                    for school in result['schools']:
                        response += f"📍 **{school['name']}**\n"
                        response += f"   Location: {school['location']}\n"
                        response += f"   Fees: {school['fee_structure']}\n\n"
                    return response
            else:
                comparison = self.compare_schools()
                response = "🎓 Here are all available schools:\n\n"
                for school in comparison['schools']:
                    response += f"📍 **{school['name']}**\n"
                    response += f"   Location: {school['location']}\n"
                    response += f"   Fees: {school['fee_structure']}\n"
                    response += f"   Entrance Exam: {'Yes' if school['entrance_exam'] else 'No'}\n\n"
                return response
        
        # Fee structure
        if any(keyword in user_input_lower for keyword in ['fee', 'cost', 'price', 'charge']):
            comparison = self.compare_schools()
            response = "💰 Fee Structure:\n\n"
            for school in comparison['schools']:
                response += f"📍 **{school['name']}**: {school['fee_structure']}\n"
            return response
        
        # Compare schools
        if 'compare' in user_input_lower:
            comparison = self.compare_schools()
            response = "📊 School Comparison:\n\n"
            for school in comparison['schools']:
                response += f"**{school['name']}** ({school['location']})\n"
                response += f"  • Fees: {school['fee_structure']}\n"
                response += f"  • Entrance Exam: {'Yes' if school['entrance_exam'] else 'No'}\n"
                response += f"  • Facilities: {', '.join(school['facilities'])}\n\n"
            return response
        
        # Admission info
        if any(keyword in user_input_lower for keyword in ['admission', 'document', 'requirement', 'eligibility']):
            if 'dps' in user_input_lower or 'delhi' in user_input_lower:
                info = self.get_admission_info("Delhi Public School")
                if info['success']:
                    response = f"📋 Admission Info for {info['school']}:\n\n"
                    response += f"  • Entrance Exam: {'Required' if info['entrance_exam'] else 'Not Required'}\n"
                    response += f"  • Required Documents:\n"
                    for doc in info['documents_required']:
                        response += f"    - {doc}\n"
                    response += f"  • Eligibility: {info['eligibility']}\n"
                    response += f"  • Contact: {info['contact']}\n"
                    return response
            elif 'greenfield' in user_input_lower or 'bangalore' in user_input_lower:
                info = self.get_admission_info("Greenfield Public School")
                if info['success']:
                    response = f"📋 Admission Info for {info['school']}:\n\n"
                    response += f"  • Entrance Exam: {'Required' if info['entrance_exam'] else 'Not Required'}\n"
                    response += f"  • Required Documents:\n"
                    for doc in info['documents_required']:
                        response += f"    - {doc}\n"
                    response += f"  • Eligibility: {info['eligibility']}\n"
                    response += f"  • Contact: {info['contact']}\n"
                    return response
            else:
                response = "Please specify which school you're interested in (DPS Delhi or Greenfield Bangalore)"
                return response
        
        # FAQs
        if any(keyword in user_input_lower for keyword in ['faq', 'question', 'help', 'how']):
            faqs = self.get_faqs()
            response = "❓ Frequently Asked Questions:\n\n"
            for faq in faqs['faqs']:
                response += f"**Q:** {faq['question']}\n"
                response += f"**A:** {faq['answer']}\n\n"
            return response
        
        # Lead capture
        if any(keyword in user_input_lower for keyword in ['inquire', 'contact', 'interested', 'apply', 'admit']):
            response = "Great! I'd like to capture your contact information.\n\n"
            response += "To help you better, could you please provide:\n"
            response += "1. Your full name\n"
            response += "2. Email address\n"
            response += "3. Phone number\n"
            response += "4. Which school are you interested in?\n\n"
            return response
        
        # Default responses
        default_responses = [
            "I'm Schooloo AI Assistant! 🎓 I can help you with:\n"
            "  • Search for schools in different locations\n"
            "  • Get fee structures and facilities\n"
            "  • Compare schools\n"
            "  • Learn about admission requirements\n"
            "  • Access FAQs\n"
            "  • Capture your inquiry\n\n"
            "What would you like to know?",
            
            "Hi there! 👋 I'm here to help you find the right school.\n"
            "Ask me about:\n"
            "  • Schools in Delhi, Bangalore, or other cities\n"
            "  • Fees and facilities\n"
            "  • Admission process and documents\n"
            "  • Entrance exams\n\n"
            "How can I assist you?",
            
            "Welcome to Schooloo! 📚 I can help you with school-related queries.\n"
            "Try asking:\n"
            "  • 'What schools are in Delhi?'\n"
            "  • 'What are the fees?'\n"
            "  • 'Tell me about admission'\n"
            "  • 'Compare DPS and Greenfield'\n\n"
            "What's your question?"
        ]
        
        return default_responses[self.conversation_count % len(default_responses)]
    
    def run_interactive(self):
        """Run interactive chat loop"""
        print("\n" + "="*70)
        print("🎓 SCHOOLOO AI ASSISTANT - INTERACTIVE MODE (DEMO)")
        print("="*70)
        print("\n✨ Chat with the Schooloo AI Agent")
        print("📚 Ask questions about schools, admissions, fees, documents, etc.")
        print("⚡ Demo Mode: Running offline (no API quota used)")
        print("✋ Type 'quit' or 'exit' to end the conversation\n")
        print("-"*70 + "\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit']:
                    print("\n" + "="*70)
                    print("Thank you for using Schooloo AI Assistant!")
                    print("="*70 + "\n")
                    break
                
                print("\n🤖 Processing...\n")
                response = self.process_query(user_input)
                
                print(f"Agent: {response}\n")
                print("-"*70 + "\n")
                
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"❌ Error: {e}\n")


def main():
    """Main entry point"""
    agent = DemoSchoolooAgent()
    agent.run_interactive()


if __name__ == "__main__":
    main()
