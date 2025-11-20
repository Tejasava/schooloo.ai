"""Schooloo AI Agent using Google Agent Development Kit"""
import os
import json
import requests
from typing import Any, Optional
from datetime import datetime

# Try to import Google Agent Development Kit components
try:
    import google.generativeai as genai
    from google.generativeai import types
except ImportError:
    print("Note: google-generativeai not installed. Install with: pip install google-generativeai")

# Backend API base URL
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000/api')

class SchoolooAgentTools:
    """Tool definitions for Schooloo AI Agent"""
    
    @staticmethod
    def search_schools(location: str, radius_km: float = 5.0) -> dict:
        """Search schools by location"""
        try:
            response = requests.post(
                f"{BACKEND_URL}/schools/search",
                json={"location": location}
            )
            return response.json()
        except Exception as e:
            return {"error": f"Failed to search schools: {str(e)}"}
    
    @staticmethod
    def get_nearby_schools(latitude: float, longitude: float, radius_km: float = 5.0) -> dict:
        """Get schools nearby based on GPS coordinates"""
        try:
            response = requests.post(
                f"{BACKEND_URL}/schools/nearby",
                json={
                    "latitude": latitude,
                    "longitude": longitude,
                    "radius_km": radius_km
                }
            )
            return response.json()
        except Exception as e:
            return {"error": f"Failed to get nearby schools: {str(e)}"}
    
    @staticmethod
    def get_school_details(school_id: str) -> dict:
        """Get detailed information about a school"""
        try:
            response = requests.get(f"{BACKEND_URL}/schools/{school_id}")
            return response.json()
        except Exception as e:
            return {"error": f"Failed to get school details: {str(e)}"}
    
    @staticmethod
    def get_fee_structure(school_id: str) -> dict:
        """Get fee structure of a school"""
        try:
            response = requests.get(f"{BACKEND_URL}/schools/{school_id}")
            if response.status_code == 200:
                school = response.json()
                return {
                    "success": True,
                    "school_name": school['data']['name'],
                    "fees": school['data']['fee_structure']
                }
            return {"error": "School not found"}
        except Exception as e:
            return {"error": f"Failed to get fee structure: {str(e)}"}
    
    @staticmethod
    def compare_schools(school_ids: list) -> dict:
        """Compare multiple schools"""
        try:
            response = requests.post(
                f"{BACKEND_URL}/schools/compare",
                json={"school_ids": school_ids}
            )
            return response.json()
        except Exception as e:
            return {"error": f"Failed to compare schools: {str(e)}"}
    
    @staticmethod
    def get_admission_info(school_id: str) -> dict:
        """Get admission information for a school"""
        try:
            response = requests.get(f"{BACKEND_URL}/admissions/{school_id}")
            return response.json()
        except Exception as e:
            return {"error": f"Failed to get admission info: {str(e)}"}
    
    @staticmethod
    def get_required_documents(school_id: str) -> dict:
        """Get required documents for admission"""
        try:
            response = requests.get(f"{BACKEND_URL}/admissions/documents/{school_id}")
            return response.json()
        except Exception as e:
            return {"error": f"Failed to get required documents: {str(e)}"}
    
    @staticmethod
    def get_exam_pattern(school_id: str) -> dict:
        """Get entrance exam pattern"""
        try:
            response = requests.get(f"{BACKEND_URL}/admissions/exam-pattern/{school_id}")
            return response.json()
        except Exception as e:
            return {"error": f"Failed to get exam pattern: {str(e)}"}
    
    @staticmethod
    def get_eligibility_criteria(school_id: str) -> dict:
        """Get eligibility criteria for a school"""
        try:
            response = requests.get(f"{BACKEND_URL}/admissions/eligibility/{school_id}")
            return response.json()
        except Exception as e:
            return {"error": f"Failed to get eligibility criteria: {str(e)}"}
    
    @staticmethod
    def get_faqs(category: Optional[str] = None) -> dict:
        """Get FAQs, optionally filtered by category"""
        try:
            params = {"category": category} if category else {}
            response = requests.get(f"{BACKEND_URL}/faqs", params=params)
            return response.json()
        except Exception as e:
            return {"error": f"Failed to get FAQs: {str(e)}"}
    
    @staticmethod
    def add_faq(question: str, answer: str, category: str, school_id: Optional[str] = None) -> dict:
        """Add a new FAQ"""
        try:
            response = requests.post(
                f"{BACKEND_URL}/faqs",
                json={
                    "question": question,
                    "answer": answer,
                    "category": category,
                    "school_id": school_id
                }
            )
            return response.json()
        except Exception as e:
            return {"error": f"Failed to add FAQ: {str(e)}"}
    
    @staticmethod
    def capture_lead(name: str, email: str, phone: str, school_interested: str, 
                     query_type: str, query_text: str) -> dict:
        """Capture a new lead"""
        try:
            response = requests.post(
                f"{BACKEND_URL}/leads",
                json={
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "school_interested": school_interested,
                    "query_type": query_type,
                    "query_text": query_text
                }
            )
            return response.json()
        except Exception as e:
            return {"error": f"Failed to capture lead: {str(e)}"}
    
    @staticmethod
    def get_all_leads() -> dict:
        """Get all leads (admin endpoint)"""
        try:
            response = requests.get(f"{BACKEND_URL}/leads")
            return response.json()
        except Exception as e:
            return {"error": f"Failed to get leads: {str(e)}"}
    
    @staticmethod
    def update_lead_status(lead_id: str, status: str) -> dict:
        """Update lead status"""
        try:
            response = requests.patch(
                f"{BACKEND_URL}/leads/{lead_id}",
                json={"status": status}
            )
            return response.json()
        except Exception as e:
            return {"error": f"Failed to update lead: {str(e)}"}


class SchoolooAgent:
    """Main Schooloo AI Agent class"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the agent"""
        self.tools = SchoolooAgentTools()
        self.api_key = api_key or os.getenv('API_KEY') or os.getenv('GOOGLE_API_KEY')
        self.model_name = os.getenv('AGENT_MODEL', 'gemini-1.5-pro')
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            print(f"✅ API Key configured for Gemini model: {self.model_name}")
        else:
            print("⚠️ Warning: No API key found. Set API_KEY or GOOGLE_API_KEY environment variable")
    
    def get_tools_schema(self) -> list:
        """Get the schema of available tools"""
        return [
            {
                "name": "search_schools",
                "description": "Search schools by location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "Location to search schools in"
                        },
                        "radius_km": {
                            "type": "number",
                            "description": "Radius in kilometers (optional)"
                        }
                    },
                    "required": ["location"]
                }
            },
            {
                "name": "get_nearby_schools",
                "description": "Find schools near a GPS location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "latitude": {"type": "number"},
                        "longitude": {"type": "number"},
                        "radius_km": {"type": "number"}
                    },
                    "required": ["latitude", "longitude"]
                }
            },
            {
                "name": "get_school_details",
                "description": "Get detailed information about a specific school",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "school_id": {"type": "string"}
                    },
                    "required": ["school_id"]
                }
            },
            {
                "name": "get_fee_structure",
                "description": "Get fee structure of a school",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "school_id": {"type": "string"}
                    },
                    "required": ["school_id"]
                }
            },
            {
                "name": "compare_schools",
                "description": "Compare multiple schools",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "school_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of school IDs to compare"
                        }
                    },
                    "required": ["school_ids"]
                }
            },
            {
                "name": "get_admission_info",
                "description": "Get admission information for a school",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "school_id": {"type": "string"}
                    },
                    "required": ["school_id"]
                }
            },
            {
                "name": "get_required_documents",
                "description": "Get required documents for admission to a school",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "school_id": {"type": "string"}
                    },
                    "required": ["school_id"]
                }
            },
            {
                "name": "get_exam_pattern",
                "description": "Get entrance exam pattern for a school",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "school_id": {"type": "string"}
                    },
                    "required": ["school_id"]
                }
            },
            {
                "name": "get_eligibility_criteria",
                "description": "Get eligibility criteria for admission",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "school_id": {"type": "string"}
                    },
                    "required": ["school_id"]
                }
            },
            {
                "name": "get_faqs",
                "description": "Get frequently asked questions",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": "Category: parent, student, or general"
                        }
                    }
                }
            },
            {
                "name": "add_faq",
                "description": "Add a new FAQ",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string"},
                        "answer": {"type": "string"},
                        "category": {"type": "string"},
                        "school_id": {"type": "string"}
                    },
                    "required": ["question", "answer", "category"]
                }
            },
            {
                "name": "capture_lead",
                "description": "Capture a new lead/inquiry",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                        "phone": {"type": "string"},
                        "school_interested": {"type": "string"},
                        "query_type": {"type": "string"},
                        "query_text": {"type": "string"}
                    },
                    "required": ["name", "email", "phone", "school_interested", "query_type", "query_text"]
                }
            },
            {
                "name": "get_all_leads",
                "description": "Get all captured leads (admin)",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "update_lead_status",
                "description": "Update lead status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "lead_id": {"type": "string"},
                        "status": {"type": "string"}
                    },
                    "required": ["lead_id", "status"]
                }
            }
        ]
    
    def process_tool_call(self, tool_name: str, tool_input: dict) -> str:
        """Process a tool call and return the result"""
        tool_method = getattr(self.tools, tool_name, None)
        
        if not tool_method:
            return json.dumps({"error": f"Tool {tool_name} not found"})
        
        try:
            result = tool_method(**tool_input)
            return json.dumps(result)
        except Exception as e:
            return json.dumps({"error": f"Error executing {tool_name}: {str(e)}"})
    
    def chat(self, user_message: str) -> str:
        """Chat with the agent"""
        try:
            model = genai.GenerativeModel(
                model_name=self.model_name,
                tools=self.get_tools_schema()
            )
            
            response = model.generate_content(
                user_message,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "max_output_tokens": 2048,
                }
            )
            
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"


# Example usage and testing
def run_demo():
    """Run a demo of the agent"""
    print("\n" + "="*60)
    print("SCHOOLOO AI AGENT DEMO")
    print("="*60 + "\n")
    
    agent = SchoolooAgent()
    
    # Test queries
    test_queries = [
        "What are the best schools near Delhi?",
        "Tell me about DPS Delhi - location, fees, and facilities",
        "What documents do I need for admission to DPS?",
        "Does Greenfield school have an entrance exam?",
        "Compare Delhi Public School and Greenfield Public School",
        "What FAQs are available for parents?"
    ]
    
    print("Available Tools:")
    print("-" * 60)
    for tool in agent.get_tools_schema():
        print(f"  • {tool['name']}: {tool['description']}")
    print("-" * 60 + "\n")
    
    for query in test_queries[:2]:  # Show first 2 examples
        print(f"User: {query}")
        print(f"Agent: {agent.chat(query)[:200]}...")
        print("-" * 60 + "\n")


if __name__ == "__main__":
    run_demo()
