from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_home():
    """Test the home endpoint returns correct status and message"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Python CI/CD Pipeline Running Successfully!"}

def test_home_response_type():
    """Test the home endpoint returns JSON"""
    response = client.get("/")
    assert response.headers["content-type"] == "application/json"

def test_invalid_route():
    """Test that invalid routes return 404"""
    response = client.get("/nonexistent")
    assert response.status_code == 404
