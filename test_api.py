import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API base URL
API_PORT = os.environ.get('API_PORT', '8531')
BASE_URL = f"http://localhost:{API_PORT}/api/v1"

# Test data
test_user = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}

test_template = {
    "name": "Test Invoice Template",
    "description": "Template for creating test invoices",
    "content": "<html><body><h1>INVOICE</h1><p>Customer: {{customer_name}}</p><p>Amount: {{amount}}</p></body></html>",
    "editable_fields": {
        "fields": [
            {"name": "customer_name", "type": "text", "required": True},
            {"name": "amount", "type": "number", "required": True}
        ]
    },
    "status": "active"
}

test_station = {
    "name": "Approval Station",
    "description": "Station for document approval",
    "type": "approval",
    "responsible_role": "admin"
}

# Store tokens and IDs
access_token = None
template_id = None
station_id = None

def print_response(response):
    """Print formatted response"""
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print("-" * 50)

def register_user():
    """Register test user"""
    global access_token
    
    print("\n=== Registering User ===")
    response = requests.post(f"{BASE_URL}/auth/register", json=test_user)
    print_response(response)
    
    if response.status_code == 201:
        print("User registered successfully")
    elif response.status_code == 400 and "Username already exists" in response.text:
        print("User already exists, proceeding to login")
    else:
        print("Failed to register user")
        return False
    
    # Login to get access token
    print("\n=== Logging In ===")
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response(response)
    
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print(f"Login successful, token received")
        return True
    else:
        print("Login failed")
        return False

def create_template():
    """Create test template"""
    global template_id
    
    print("\n=== Creating Template ===")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(f"{BASE_URL}/templates", headers=headers, json=test_template)
    print_response(response)
    
    if response.status_code == 201:
        template_id = response.json().get("public_id")
        print(f"Template created successfully with ID: {template_id}")
        return True
    else:
        print("Failed to create template")
        return False

def create_station():
    """Create test station"""
    global station_id
    
    print("\n=== Creating Station ===")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(f"{BASE_URL}/stations", headers=headers, json=test_station)
    print_response(response)
    
    if response.status_code == 201:
        station_id = response.json().get("public_id")
        print(f"Station created successfully with ID: {station_id}")
        return True
    else:
        print("Failed to create station")
        return False

def create_document():
    """Create test document"""
    global template_id, station_id
    
    print("\n=== Creating Document ===")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Get template by ID
    template_response = requests.get(f"{BASE_URL}/templates/{template_id}", headers=headers)
    template = template_response.json()
    
    document_data = {
        "name": "Test Invoice #12345",
        "content": template["content"].replace("{{customer_name}}", "John Doe").replace("{{amount}}", "100.00"),
        "template_id": template["id"],
        "status": "draft",
        "current_station_id": station_id
    }
    
    response = requests.post(f"{BASE_URL}/documents", headers=headers, json=document_data)
    print_response(response)
    
    if response.status_code == 201:
        document_id = response.json().get("public_id")
        print(f"Document created successfully with ID: {document_id}")
        return True
    else:
        print("Failed to create document")
        return False

def run_tests():
    """Run all tests"""
    if not register_user():
        return
    
    if not create_template():
        return
    
    if not create_station():
        return
    
    create_document()

if __name__ == "__main__":
    print("=== Document Template API Test ===")
    run_tests()
