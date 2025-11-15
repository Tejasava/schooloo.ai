"""Database models for Schooloo"""
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

@dataclass
class School:
    """School model"""
    id: str
    name: str
    location: str
    latitude: float
    longitude: float
    fee_structure: Dict[str, Any]
    classes_offered: List[str]
    facilities: List[str]
    contact_email: str
    contact_phone: str
    website: str
    established_year: int
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class SchoolAdmission:
    """School admission requirements"""
    school_id: str
    entrance_exam_required: bool
    exam_name: Optional[str]
    exam_pattern: Optional[str]
    admission_deadline: str
    required_documents: List[str]
    eligibility_criteria: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class Lead:
    """Lead capture model"""
    id: str
    name: str
    email: str
    phone: str
    school_interested: str
    query_type: str  # parent, student, admin
    query_text: str
    status: str  # new, contacted, converted
    created_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class FAQ:
    """FAQ model"""
    id: str
    question: str
    answer: str
    category: str  # parent, student, general
    school_id: Optional[str]
    updated_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class DatabaseManager:
    """In-memory database manager"""
    
    def __init__(self):
        self.schools: Dict[str, School] = {}
        self.admissions: Dict[str, SchoolAdmission] = {}
        self.leads: Dict[str, Lead] = {}
        self.faqs: Dict[str, FAQ] = {}
        self._load_sample_data()
    
    def _load_sample_data(self):
        """Load sample data"""
        # Sample Schools
        school1 = School(
            id="school_001",
            name="Delhi Public School",
            location="New Delhi, India",
            latitude=28.5355,
            longitude=77.2030,
            fee_structure={
                "kindergarten": "₹2,50,000/year",
                "primary": "₹3,50,000/year",
                "secondary": "₹4,50,000/year"
            },
            classes_offered=["KG", "1-5", "6-10", "11-12"],
            facilities=["Swimming Pool", "Computer Lab", "Sports Ground", "Library"],
            contact_email="admin@dps-delhi.edu",
            contact_phone="+91-11-4152-7000",
            website="https://www.dpsdelhi.edu.in",
            established_year=1949
        )
        
        school2 = School(
            id="school_002",
            name="Greenfield Public School",
            location="Bangalore, India",
            latitude=13.0827,
            longitude=77.6054,
            fee_structure={
                "kindergarten": "₹2,00,000/year",
                "primary": "₹2,80,000/year",
                "secondary": "₹3,80,000/year"
            },
            classes_offered=["Nursery", "KG", "1-5", "6-10", "11-12"],
            facilities=["Sports Complex", "STEM Lab", "Auditorium", "Cafeteria"],
            contact_email="info@greenfield.edu",
            contact_phone="+91-80-4141-2020",
            website="https://www.greenfieldschool.in",
            established_year=2005
        )
        
        self.schools[school1.id] = school1
        self.schools[school2.id] = school2
        
        # Sample Admissions
        admission1 = SchoolAdmission(
            school_id="school_001",
            entrance_exam_required=True,
            exam_name="DPS Entrance Exam",
            exam_pattern="Multiple Choice + Verbal + Math + Reasoning",
            admission_deadline="March 31, 2024",
            required_documents=["Birth Certificate", "Marks Sheet", "Address Proof", "Transfer Certificate"],
            eligibility_criteria={
                "age_limit": "4-5 years for KG",
                "academic_requirement": "No prior experience required for KG",
                "nationality": "Indian or International"
            }
        )
        
        admission2 = SchoolAdmission(
            school_id="school_002",
            entrance_exam_required=False,
            exam_name=None,
            exam_pattern=None,
            admission_deadline="April 30, 2024",
            required_documents=["Birth Certificate", "Previous School Report", "Medical Fitness Certificate"],
            eligibility_criteria={
                "age_limit": "3+ years",
                "academic_requirement": "Assessments only",
                "nationality": "Open for all"
            }
        )
        
        self.admissions[admission1.school_id] = admission1
        self.admissions[admission2.school_id] = admission2
        
        # Sample FAQs
        faqs = [
            FAQ(
                id="faq_001",
                question="What is the admission fee?",
                answer="Admission fee varies from ₹25,000 to ₹75,000 depending on the class.",
                category="parent",
                school_id="school_001",
                updated_at=datetime.now().isoformat()
            ),
            FAQ(
                id="faq_002",
                question="Do you provide transportation?",
                answer="Yes, school buses are available in multiple routes across the city.",
                category="parent",
                school_id="school_001",
                updated_at=datetime.now().isoformat()
            ),
            FAQ(
                id="faq_003",
                question="What is the dress code?",
                answer="Formal uniform is compulsory from KG onwards. Details are provided at admission.",
                category="student",
                school_id="school_001",
                updated_at=datetime.now().isoformat()
            ),
            FAQ(
                id="faq_004",
                question="Are hostels available?",
                answer="Yes, separate hostels for boys and girls with 24/7 supervision.",
                category="parent",
                school_id="school_002",
                updated_at=datetime.now().isoformat()
            ),
        ]
        
        for faq in faqs:
            self.faqs[faq.id] = faq
    
    def get_schools_by_location(self, location: str) -> List[School]:
        """Get schools by location"""
        return [s for s in self.schools.values() if location.lower() in s.location.lower()]
    
    def get_school_by_id(self, school_id: str) -> Optional[School]:
        """Get school by ID"""
        return self.schools.get(school_id)
    
    def get_admission_info(self, school_id: str) -> Optional[SchoolAdmission]:
        """Get admission info for a school"""
        return self.admissions.get(school_id)
    
    def get_faqs_by_category(self, category: str) -> List[FAQ]:
        """Get FAQs by category"""
        return [f for f in self.faqs.values() if f.category == category]
    
    def create_lead(self, lead: Lead) -> Lead:
        """Create a new lead"""
        self.leads[lead.id] = lead
        return lead
    
    def get_all_schools(self) -> List[School]:
        """Get all schools"""
        return list(self.schools.values())
    
    def get_all_leads(self) -> List[Lead]:
        """Get all leads"""
        return list(self.leads.values())

# Global database instance
db = DatabaseManager()
