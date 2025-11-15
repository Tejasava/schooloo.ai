# API Request Examples for Schooloo

## 1. Search Schools by Location

```bash
curl -X POST http://localhost:5000/api/schools/search \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Delhi"
  }'
```

Response:
```json
{
  "success": true,
  "data": [
    {
      "id": "school_001",
      "name": "Delhi Public School",
      "location": "New Delhi, India",
      "fee_structure": {...},
      "facilities": [...]
    }
  ],
  "count": 1
}
```

## 2. Get Nearby Schools (GPS)

```bash
curl -X POST http://localhost:5000/api/schools/nearby \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 28.5355,
    "longitude": 77.2030,
    "radius_km": 5
  }'
```

## 3. Get School Details

```bash
curl -X GET http://localhost:5000/api/schools/school_001
```

## 4. Compare Schools

```bash
curl -X POST http://localhost:5000/api/schools/compare \
  -H "Content-Type: application/json" \
  -d '{
    "school_ids": ["school_001", "school_002"]
  }'
```

## 5. Get Admission Information

```bash
curl -X GET http://localhost:5000/api/admissions/school_001
```

## 6. Get Required Documents

```bash
curl -X GET http://localhost:5000/api/admissions/documents/school_001
```

## 7. Get Exam Pattern

```bash
curl -X GET http://localhost:5000/api/admissions/exam-pattern/school_001
```

## 8. Get Eligibility Criteria

```bash
curl -X GET http://localhost:5000/api/admissions/eligibility/school_001
```

## 9. Get FAQs

```bash
# All FAQs
curl -X GET http://localhost:5000/api/faqs

# Parent FAQs only
curl -X GET "http://localhost:5000/api/faqs?category=parent"

# Student FAQs only
curl -X GET "http://localhost:5000/api/faqs?category=student"
```

## 10. Create New FAQ

```bash
curl -X POST http://localhost:5000/api/faqs \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Do you provide scholarships?",
    "answer": "Yes, merit-based scholarships are available.",
    "category": "parent",
    "school_id": "school_001"
  }'
```

## 11. Capture Lead

```bash
curl -X POST http://localhost:5000/api/leads \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rajesh Kumar",
    "email": "rajesh@example.com",
    "phone": "+91-9876543210",
    "school_interested": "school_001",
    "query_type": "parent",
    "query_text": "Interested in admission for Class 5"
  }'
```

## 12. Get All Leads

```bash
curl -X GET http://localhost:5000/api/leads
```

## 13. Update Lead Status

```bash
curl -X PATCH http://localhost:5000/api/leads/lead_id \
  -H "Content-Type: application/json" \
  -d '{
    "status": "contacted"
  }'
```

## Using Python Requests Library

```python
import requests

# Search schools
response = requests.post(
    'http://localhost:5000/api/schools/search',
    json={'location': 'Delhi'}
)
schools = response.json()

# Get school details
response = requests.get('http://localhost:5000/api/schools/school_001')
school = response.json()

# Capture lead
response = requests.post(
    'http://localhost:5000/api/leads',
    json={
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '+91-9876543210',
        'school_interested': 'school_001',
        'query_type': 'parent',
        'query_text': 'Admission inquiry'
    }
)
lead = response.json()
```

## Using cURL Helper

Create a file `api_test.sh`:

```bash
#!/bin/bash

BASE_URL="http://localhost:5000/api"

echo "Testing Schooloo API..."

echo -e "\n1. Get all schools:"
curl -s $BASE_URL/schools | python -m json.tool

echo -e "\n2. Search schools:"
curl -s -X POST $BASE_URL/schools/search \
  -H "Content-Type: application/json" \
  -d '{"location":"Delhi"}' | python -m json.tool

echo -e "\n3. Get school details:"
curl -s $BASE_URL/schools/school_001 | python -m json.tool

echo -e "\n4. Get admission info:"
curl -s $BASE_URL/admissions/school_001 | python -m json.tool

echo -e "\n5. Get FAQs:"
curl -s "$BASE_URL/faqs?category=parent" | python -m json.tool
```

Run with: `bash api_test.sh`
