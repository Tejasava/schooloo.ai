"""
Test suite for Schooloo backend and agent
Run: python -m pytest test_schooloo.py -v
"""
import json
import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agent'))

from database import DatabaseManager, School
from tools import ToolHandler

class TestSchoolooBackend:
    """Test backend functionality"""
    
    @staticmethod
    def test_database_initialization():
        """Test database setup"""
        db = DatabaseManager()
        assert len(db.schools) >= 2, "Should have sample schools"
        assert len(db.admissions) >= 2, "Should have sample admissions"
        print("✅ Database initialization test passed")
    
    @staticmethod
    def test_school_search():
        """Test school search"""
        db = DatabaseManager()
        delhi_schools = db.get_schools_by_location("Delhi")
        assert len(delhi_schools) > 0, "Should find schools in Delhi"
        print(f"✅ School search test passed ({len(delhi_schools)} schools found)")
    
    @staticmethod
    def test_admission_info():
        """Test admission info retrieval"""
        db = DatabaseManager()
        school_id = "school_001"
        admission = db.get_admission_info(school_id)
        assert admission is not None, "Should get admission info"
        assert admission.required_documents, "Should have required documents"
        print(f"✅ Admission info test passed ({len(admission.required_documents)} documents)")
    
    @staticmethod
    def test_faq_by_category():
        """Test FAQ retrieval by category"""
        db = DatabaseManager()
        parent_faqs = db.get_faqs_by_category("parent")
        student_faqs = db.get_faqs_by_category("student")
        assert len(parent_faqs) > 0, "Should have parent FAQs"
        assert len(student_faqs) > 0, "Should have student FAQs"
        print(f"✅ FAQ test passed (Parent: {len(parent_faqs)}, Student: {len(student_faqs)})")
    
    @staticmethod
    def test_lead_capture():
        """Test lead capture"""
        from database import Lead
        db = DatabaseManager()
        
        lead = Lead(
            id="test_lead_001",
            name="Test Parent",
            email="test@example.com",
            phone="+91-9876543210",
            school_interested="school_001",
            query_type="parent",
            query_text="Test query",
            status="new",
            created_at="2024-01-01"
        )
        
        captured_lead = db.create_lead(lead)
        assert captured_lead.id in db.leads, "Lead should be captured"
        print("✅ Lead capture test passed")


class TestToolHandler:
    """Test tool handler"""
    
    @staticmethod
    def test_tool_execution():
        """Test basic tool execution"""
        handler = ToolHandler()
        
        # Test search_schools
        result = handler.execute_tool("search_schools", {"location": "Delhi"})
        data = json.loads(result)
        assert data.get('success'), "Search should succeed"
        print(f"✅ Tool execution test passed")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("SCHOOLOO TEST SUITE")
    print("="*60 + "\n")
    
    tests = [
        ("Database Initialization", TestSchoolooBackend.test_database_initialization),
        ("School Search", TestSchoolooBackend.test_school_search),
        ("Admission Info", TestSchoolooBackend.test_admission_info),
        ("FAQ Retrieval", TestSchoolooBackend.test_faq_by_category),
        ("Lead Capture", TestSchoolooBackend.test_lead_capture),
        ("Tool Execution", TestToolHandler.test_tool_execution),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test_name}: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test_name}: Unexpected error - {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
