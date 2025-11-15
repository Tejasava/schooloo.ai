"""Tool implementations for Schooloo Agent"""
import json
import requests
import os
from typing import Dict, Any, List, Optional

BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000/api')

class ToolHandler:
    """Handle all tool executions for the agent"""
    
    @staticmethod
    def execute_tool(tool_name: str, tool_input: Dict[str, Any]) -> str:
        """Execute a tool and return JSON result"""
        handlers = {
            "search_schools": ToolHandler.search_schools,
            "get_school_details": ToolHandler.get_school_details,
            "get_fee_structure": ToolHandler.get_fee_structure,
            "compare_schools": ToolHandler.compare_schools,
            "get_admission_info": ToolHandler.get_admission_info,
            "get_required_documents": ToolHandler.get_required_documents,
            "get_exam_pattern": ToolHandler.get_exam_pattern,
            "get_eligibility_criteria": ToolHandler.get_eligibility_criteria,
            "get_faqs": ToolHandler.get_faqs,
            "capture_lead": ToolHandler.capture_lead,
            "get_all_leads": ToolHandler.get_all_leads,
            "update_lead_status": ToolHandler.update_lead_status,
        }
        
        handler = handlers.get(tool_name)
        if not handler:
            return json.dumps({"error": f"Unknown tool: {tool_name}"})
        
        try:
            result = handler(**tool_input)
            return json.dumps(result)
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    @staticmethod
    def search_schools(location: str, **kwargs) -> Dict[str, Any]:
        """Search schools by location"""
        response = requests.post(
            f"{BACKEND_URL}/schools/search",
            json={"location": location}
        )
        return response.json()
    
    @staticmethod
    def get_school_details(school_id: str, **kwargs) -> Dict[str, Any]:
        """Get school details"""
        response = requests.get(f"{BACKEND_URL}/schools/{school_id}")
        return response.json()
    
    @staticmethod
    def get_fee_structure(school_id: str, **kwargs) -> Dict[str, Any]:
        """Get fee structure"""
        response = requests.get(f"{BACKEND_URL}/schools/{school_id}")
        if response.status_code == 200:
            school = response.json()['data']
            return {
                "success": True,
                "school_name": school['name'],
                "fees": school['fee_structure']
            }
        return {"error": "School not found"}
    
    @staticmethod
    def compare_schools(school_ids: List[str], **kwargs) -> Dict[str, Any]:
        """Compare schools"""
        response = requests.post(
            f"{BACKEND_URL}/schools/compare",
            json={"school_ids": school_ids}
        )
        return response.json()
    
    @staticmethod
    def get_admission_info(school_id: str, **kwargs) -> Dict[str, Any]:
        """Get admission info"""
        response = requests.get(f"{BACKEND_URL}/admissions/{school_id}")
        return response.json()
    
    @staticmethod
    def get_required_documents(school_id: str, **kwargs) -> Dict[str, Any]:
        """Get required documents"""
        response = requests.get(f"{BACKEND_URL}/admissions/documents/{school_id}")
        return response.json()
    
    @staticmethod
    def get_exam_pattern(school_id: str, **kwargs) -> Dict[str, Any]:
        """Get exam pattern"""
        response = requests.get(f"{BACKEND_URL}/admissions/exam-pattern/{school_id}")
        return response.json()
    
    @staticmethod
    def get_eligibility_criteria(school_id: str, **kwargs) -> Dict[str, Any]:
        """Get eligibility criteria"""
        response = requests.get(f"{BACKEND_URL}/admissions/eligibility/{school_id}")
        return response.json()
    
    @staticmethod
    def get_faqs(category: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Get FAQs"""
        params = {"category": category} if category else {}
        response = requests.get(f"{BACKEND_URL}/faqs", params=params)
        return response.json()
    
    @staticmethod
    def capture_lead(name: str, email: str, phone: str, school_interested: str,
                     query_type: str, query_text: str, **kwargs) -> Dict[str, Any]:
        """Capture a lead"""
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
    
    @staticmethod
    def get_all_leads(**kwargs) -> Dict[str, Any]:
        """Get all leads"""
        response = requests.get(f"{BACKEND_URL}/leads")
        return response.json()
    
    @staticmethod
    def update_lead_status(lead_id: str, status: str, **kwargs) -> Dict[str, Any]:
        """Update lead status"""
        response = requests.patch(
            f"{BACKEND_URL}/leads/{lead_id}",
            json={"status": status}
        )
        return response.json()
