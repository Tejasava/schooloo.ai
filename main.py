"""
Main entry point for Schooloo AI Agent with Google ADK
Orchestrates the agent, backend, and tooling
"""
import os
import sys
import json
from typing import Optional, Dict, Any

# Add agent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agent'))
sys.path.insert(0, os.path.dirname(__file__))

from agent.schooloo_agent import SchoolooAgent
from agent.query_processor import QueryProcessor, ResponseFormatter
from agent.tools import ToolHandler

class SchoolooAISystem:
    """Complete Schooloo AI System"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Schooloo AI system"""
        self.agent = SchoolooAgent(api_key)
        self.query_processor = QueryProcessor()
        self.response_formatter = ResponseFormatter()
        self.tool_handler = ToolHandler()
    
    def handle_query(self, user_message: str, user_type: str = "parent") -> Dict[str, Any]:
        """
        Handle a user query
        
        Args:
            user_message: The user's query
            user_type: Type of user - 'parent', 'student', or 'admin'
        
        Returns:
            Dict with processed response and metadata
        """
        result = {
            "user_type": user_type,
            "query": user_message,
            "tools_used": [],
            "response": "",
            "success": True
        }
        
        # Process query based on user type
        if user_type == "parent":
            analysis = self.query_processor.process_parent_query(user_message)
        elif user_type == "student":
            analysis = self.query_processor.process_student_query(user_message)
        elif user_type == "admin":
            analysis = self.query_processor.process_admin_query(user_message)
        else:
            analysis = self.query_processor.process_parent_query(user_message)
        
        result["tools_used"] = analysis.get("suggested_tools", [])
        
        # For demo, show tool suggestions
        if result["tools_used"]:
            result["response"] = f"I'll help you with that! Using tools: {', '.join(result['tools_used'])}\n\n"
        
        return result
    
    def execute_tool(self, tool_name: str, tool_input: dict) -> str:
        """Execute a specific tool"""
        return self.tool_handler.execute_tool(tool_name, tool_input)
    
    def interactive_chat(self, user_type: str = "parent"):
        """Start interactive chat with the agent"""
        print(f"\n{'='*60}")
        print(f"SCHOOLOO AI AGENT - {user_type.upper()} MODE")
        print(f"{'='*60}")
        print("Type 'quit' to exit\n")
        
        while True:
            try:
                user_input = input(f"{user_type.capitalize()} > ").strip()
                
                if user_input.lower() == 'quit':
                    print("Thank you for using Schooloo AI Agent!")
                    break
                
                if not user_input:
                    continue
                
                # Handle the query
                result = self.handle_query(user_input, user_type)
                
                print(f"\n🤖 Agent: {result['response']}")
                if result['tools_used']:
                    print(f"Tools: {result['tools_used']}")
                print("-" * 60 + "\n")
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}\n")


# Example functions for different use cases
def parent_example():
    """Example: Parent querying about schools"""
    print("\n" + "="*60)
    print("PARENT QUERY EXAMPLE")
    print("="*60 + "\n")
    
    system = SchoolooAISystem()
    
    parent_queries = [
        "What are the best schools in Delhi?",
        "How much do schools cost?",
        "Can you compare DPS and Greenfield schools?",
        "What are the admission requirements?"
    ]
    
    for query in parent_queries:
        print(f"Parent: {query}")
        result = system.handle_query(query, "parent")
        print(f"Agent: {result['response']}")
        print(f"Tools: {', '.join(result['tools_used'])}")
        print("-" * 60 + "\n")


def student_example():
    """Example: Student querying about requirements"""
    print("\n" + "="*60)
    print("STUDENT QUERY EXAMPLE")
    print("="*60 + "\n")
    
    system = SchoolooAISystem()
    
    student_queries = [
        "What documents do I need for admission?",
        "Is there an entrance exam?",
        "What's the dress code?",
        "Are hostels available?",
        "What's the exam pattern?"
    ]
    
    for query in student_queries:
        print(f"Student: {query}")
        result = system.handle_query(query, "student")
        print(f"Agent: {result['response']}")
        print(f"Tools: {', '.join(result['tools_used'])}")
        print("-" * 60 + "\n")


def admin_example():
    """Example: Admin managing leads and FAQs"""
    print("\n" + "="*60)
    print("ADMIN EXAMPLE")
    print("="*60 + "\n")
    
    system = SchoolooAISystem()
    
    admin_tasks = [
        "Show me all new leads",
        "Capture a new lead from a parent",
        "Update lead status to contacted",
        "Add a new FAQ"
    ]
    
    for task in admin_tasks:
        print(f"Admin: {task}")
        result = system.handle_query(task, "admin")
        print(f"Agent: {result['response']}")
        print(f"Tools: {', '.join(result['tools_used'])}")
        print("-" * 60 + "\n")


def api_example():
    """Example: Using the system as an API"""
    print("\n" + "="*60)
    print("API USAGE EXAMPLE")
    print("="*60 + "\n")
    
    system = SchoolooAISystem()
    
    # Example 1: Search schools
    print("1. Searching for schools in Delhi...")
    result = system.execute_tool("search_schools", {"location": "Delhi"})
    data = json.loads(result)
    print(f"   Found {len(data.get('data', []))} schools")
    print()
    
    # Example 2: Get school details
    print("2. Getting details for DPS...")
    result = system.execute_tool("get_school_details", {"school_id": "school_001"})
    data = json.loads(result)
    if data.get('success'):
        school = data['data']
        print(f"   Name: {school['name']}")
        print(f"   Location: {school['location']}")
        print(f"   Facilities: {', '.join(school['facilities'][:3])}")
    print()
    
    # Example 3: Get fees
    print("3. Getting fee structure...")
    result = system.execute_tool("get_fee_structure", {"school_id": "school_001"})
    data = json.loads(result)
    if data.get('success'):
        print(f"   School: {data['school_name']}")
        for class_type, fee in data['fees'].items():
            print(f"   {class_type}: {fee}")
    print()
    
    # Example 4: Capture a lead
    print("4. Capturing a new lead...")
    lead_result = system.execute_tool("capture_lead", {
        "name": "Rajesh Kumar",
        "email": "rajesh@example.com",
        "phone": "+91-9876543210",
        "school_interested": "Delhi Public School",
        "query_type": "parent",
        "query_text": "Interested in admission for my child"
    })
    data = json.loads(lead_result)
    if data.get('success'):
        print(f"   ✅ Lead captured with ID: {data['data']['id']}")
    print()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Schooloo AI Agent")
    parser.add_argument(
        "--mode",
        choices=["parent", "student", "admin", "interactive", "examples", "api"],
        default="examples",
        help="Mode to run the agent in"
    )
    parser.add_argument("--api-key", help="Google API key")
    
    args = parser.parse_args()
    
    if args.mode == "parent":
        parent_example()
    elif args.mode == "student":
        student_example()
    elif args.mode == "admin":
        admin_example()
    elif args.mode == "interactive":
        system = SchoolooAISystem(args.api_key)
        system.interactive_chat("parent")
    elif args.mode == "api":
        api_example()
    else:
        # Run all examples
        parent_example()
        student_example()
        admin_example()
        api_example()
