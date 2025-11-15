"""Query processors for different user types"""
from typing import Dict, List, Any
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tools import ToolHandler

class QueryProcessor:
    """Process and route queries based on user type"""
    
    @staticmethod
    def process_parent_query(query: str) -> Dict[str, Any]:
        """Process queries from parents"""
        response = {
            "user_type": "parent",
            "query": query,
            "suggested_tools": [],
            "response": ""
        }
        
        # Detect query intent
        query_lower = query.lower()
        
        if "best schools" in query_lower or "top schools" in query_lower:
            response["suggested_tools"].append("search_schools")
        
        if "fee" in query_lower or "cost" in query_lower:
            response["suggested_tools"].append("get_fee_structure")
        
        if "admission" in query_lower:
            response["suggested_tools"].append("get_admission_info")
        
        if "compare" in query_lower:
            response["suggested_tools"].append("compare_schools")
        
        if "nearby" in query_lower or "near me" in query_lower:
            response["suggested_tools"].append("get_nearby_schools")
        
        if "facilities" in query_lower or "hostel" in query_lower or "transport" in query_lower:
            response["suggested_tools"].append("get_school_details")
        
        if not response["suggested_tools"]:
            response["suggested_tools"].append("get_faqs")
        
        return response
    
    @staticmethod
    def process_student_query(query: str) -> Dict[str, Any]:
        """Process queries from students"""
        response = {
            "user_type": "student",
            "query": query,
            "suggested_tools": [],
            "response": ""
        }
        
        query_lower = query.lower()
        
        if "document" in query_lower or "requirement" in query_lower:
            response["suggested_tools"].append("get_required_documents")
        
        if "exam" in query_lower or "entrance" in query_lower:
            response["suggested_tools"].append("get_exam_pattern")
        
        if "eligible" in query_lower or "eligibility" in query_lower:
            response["suggested_tools"].append("get_eligibility_criteria")
        
        if "dress" in query_lower or "transport" in query_lower or "hostel" in query_lower or "location" in query_lower:
            response["suggested_tools"].append("get_faqs")
        
        if "school" in query_lower and "details" in query_lower:
            response["suggested_tools"].append("get_school_details")
        
        if not response["suggested_tools"]:
            response["suggested_tools"].append("get_faqs")
        
        return response
    
    @staticmethod
    def process_admin_query(query: str, action: str = None) -> Dict[str, Any]:
        """Process admin queries"""
        response = {
            "user_type": "admin",
            "query": query,
            "action": action,
            "suggested_tools": [],
            "response": ""
        }
        
        query_lower = query.lower()
        
        if "lead" in query_lower:
            if "new" in query_lower or "capture" in query_lower:
                response["suggested_tools"].append("capture_lead")
            elif "all" in query_lower or "view" in query_lower or "get" in query_lower:
                response["suggested_tools"].append("get_all_leads")
            elif "update" in query_lower or "status" in query_lower:
                response["suggested_tools"].append("update_lead_status")
        
        if "faq" in query_lower:
            if "add" in query_lower or "new" in query_lower:
                response["suggested_tools"].append("add_faq")
            elif "view" in query_lower or "get" in query_lower:
                response["suggested_tools"].append("get_faqs")
        
        if not response["suggested_tools"]:
            response["suggested_tools"].append("get_all_leads")
        
        return response

class ResponseFormatter:
    """Format responses for different user types"""
    
    @staticmethod
    def format_parent_response(tool_result: str, tool_name: str) -> str:
        """Format response for parents"""
        try:
            data = json.loads(tool_result)
            
            if tool_name == "search_schools" and data.get('success'):
                schools = data.get('data', [])
                response = f"Found {len(schools)} schools:\n\n"
                for school in schools[:3]:  # Show top 3
                    response += f"📍 {school['name']}\n"
                    response += f"   Location: {school['location']}\n"
                    response += f"   Contact: {school['contact_phone']}\n\n"
                return response
            
            elif tool_name == "get_fee_structure" and data.get('success'):
                response = f"Fee Structure for {data['school_name']}:\n\n"
                for class_type, fee in data.get('fees', {}).items():
                    response += f"  • {class_type}: {fee}\n"
                return response
            
            elif tool_name == "compare_schools":
                schools = data.get('data', [])
                response = f"Comparison of {len(schools)} Schools:\n\n"
                for school in schools:
                    response += f"🏫 {school['name']}\n"
                    response += f"   Fees: {list(school['fee_structure'].values())}\n"
                    response += f"   Facilities: {', '.join(school['facilities'][:3])}\n\n"
                return response
            
            return str(data)
        except:
            return tool_result
    
    @staticmethod
    def format_student_response(tool_result: str, tool_name: str) -> str:
        """Format response for students"""
        try:
            data = json.loads(tool_result)
            
            if tool_name == "get_required_documents" and data.get('success'):
                response = "Required Documents for Admission:\n\n"
                for i, doc in enumerate(data.get('documents', []), 1):
                    response += f"{i}. {doc}\n"
                return response
            
            elif tool_name == "get_exam_pattern":
                if data.get('exam_required'):
                    response = f"Entrance Exam Details:\n\n"
                    response += f"Exam Name: {data['exam_name']}\n"
                    response += f"Pattern: {data['exam_pattern']}\n"
                    return response
                else:
                    return "No entrance exam is required for this school."
            
            elif tool_name == "get_eligibility_criteria":
                response = "Eligibility Criteria:\n\n"
                for key, value in data.get('eligibility', {}).items():
                    response += f"• {key.replace('_', ' ').title()}: {value}\n"
                return response
            
            return str(data)
        except:
            return tool_result
    
    @staticmethod
    def format_admin_response(tool_result: str, tool_name: str) -> str:
        """Format response for admins"""
        try:
            data = json.loads(tool_result)
            
            if tool_name == "get_all_leads" and data.get('success'):
                leads = data.get('data', [])
                response = f"Total Leads: {len(leads)}\n\n"
                
                by_status = {}
                for lead in leads:
                    status = lead.get('status', 'unknown')
                    if status not in by_status:
                        by_status[status] = []
                    by_status[status].append(lead)
                
                for status, status_leads in by_status.items():
                    response += f"{status.upper()}: {len(status_leads)}\n"
                
                return response
            
            elif tool_name == "capture_lead" and data.get('success'):
                lead = data.get('data', {})
                response = f"✅ Lead Captured Successfully!\n\n"
                response += f"Name: {lead.get('name')}\n"
                response += f"Email: {lead.get('email')}\n"
                response += f"Phone: {lead.get('phone')}\n"
                response += f"School: {lead.get('school_interested')}\n"
                return response
            
            return str(data)
        except:
            return tool_result
