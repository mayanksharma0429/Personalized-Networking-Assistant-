import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from requests.exceptions import RequestException

from app.main import app
from app.services.topic_generator import generate_topics
from app.services.fact_checker import fact_check

from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

client = TestClient(app)

# Override database dependency for tests
engine = create_engine(
    "sqlite:///:memory:", 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

HEADERS = {
    "access_token": "my_super_secret_api_key_123"
}

# --- 1. API Route & Validation Tests ---

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome!"}

def test_unauthorized_access():
    response = client.post("/analyze-event", json={"description": "test"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid API Key! Access Denied."}

def test_invalid_request_returns_422():
    """Verifies that FastAPI's automatic Pydantic validation catches missing fields."""
    # Sending an empty payload to an endpoint requiring 'description'
    response = client.post("/analyze-event", headers=HEADERS, json={})
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert data["detail"][0]["loc"] == ["body", "description"]
    assert data["detail"][0]["msg"] == "Field required"

# --- 2. Event Analyzer (Structural) Tests ---

def test_analyze_event():
    """Validates structural properties: is it a list? <= 3 items?"""
    payload = {"description": "A medical conference about AI in hospitals."}
    response = client.post("/analyze-event", headers=HEADERS, json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert "topics" in data
    assert type(data["topics"]) == list
    assert len(data["topics"]) <= 3
    assert len(data["topics"]) > 0

# --- 3. Topic Generator (Post-processing Logic) Tests ---

def test_generate_strings():
    """Verifies that the cleanup process produces actual string content."""
    themes = ["AI", "healthcare"]
    interests = ["startups"]
    
    # We call the service function directly for unit testing
    results = generate_topics(themes, interests)
    
    assert type(results) == list
    for item in results:
        assert type(item) == str

def test_generate_non_empty_strings():
    """Verifies that stripping bullet markers doesn't accidentally produce empty strings."""
    themes = ["blockchain"]
    interests = ["coding"]
    
    results = generate_topics(themes, interests)
    
    for item in results:
        assert len(item.strip()) > 0
        assert not item.startswith("-")
        assert not item.startswith("*")

# --- 4. Fact Checker (Mocked External Network Call) Tests ---

@patch('app.services.fact_checker.requests.get')
def test_fact_check_happy_path(mock_get):
    """Mocks the requests.get function to simulate a successful Wikipedia summary."""
    # Setup mock
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"extract": "This is a mock summary of AI."}
    mock_get.return_value = mock_response
    
    # Execute
    result = fact_check("AI")
    
    # Verify
    assert result == "This is a mock summary of AI."
    mock_get.assert_called_once()

@patch('app.services.fact_checker.requests.get')
def test_fact_check_missing_data(mock_get):
    """Simulates Wikipedia returning a 200 OK but no 'extract' key."""
    # Setup mock
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"other_key": "data"}
    mock_get.return_value = mock_response
    
    # Execute
    result = fact_check("UnknownTopic")
    
    # Verify
    assert result == "No summary found for this specific topic."

@patch('app.services.fact_checker.requests.get')
def test_fact_check_error_path(mock_get):
    """Simulates a network error when calling Wikipedia API."""
    # Setup mock to raise an exception
    mock_get.side_effect = RequestException("Network down")
    
    # Execute
    result = fact_check("AI")
    
    # Verify
    assert result == "Could not verify the fact at this moment due to a network issue."

@patch('app.services.fact_checker.requests.get')
def test_fact_check_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    
    result = fact_check("UnknownTopic123")
    assert result == "Fact not found on Wikipedia."

@patch('app.services.fact_checker.requests.get')
def test_fact_check_general_exception(mock_get):
    mock_get.side_effect = Exception("General error")
    
    result = fact_check("AI")
    assert result == "An unexpected error occurred while verifying the fact."

# --- 5. Additional API Routes Tests ---

@patch('app.services.fact_checker.requests.get')
def test_fact_check_endpoint(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"extract": "API fact"}
    mock_get.return_value = mock_response
    
    response = client.post("/fact-check", headers=HEADERS, json={"query": "AI"})
    assert response.status_code == 200
    assert response.json() == {"summary": "API fact"}

@patch('app.routers.conversation.extract_event_themes')
@patch('app.routers.conversation.generate_topics')
@patch('app.routers.conversation.log_conversation')
def test_generate_conversation_endpoint(mock_log, mock_gen, mock_extract):
    mock_extract.return_value = ["AI"]
    mock_gen.return_value = ["Suggestion 1"]
    
    response = client.post("/generate-conversation", headers=HEADERS, json={"description": "AI event", "interests": ["tech"]})
    assert response.status_code == 200
    assert response.json() == {"topics": ["AI"], "suggestions": ["Suggestion 1"]}
    mock_log.assert_called_once()

@patch('app.services.fact_checker.requests.get')
def test_fact_check_timeout(mock_get):
    from requests.exceptions import Timeout
    mock_get.side_effect = Timeout("Timeout")
    
    result = fact_check("AI")
    assert result == "Fact verification timed out. Please try again."

@patch('app.routers.conversation.log_feedback')
def test_submit_feedback_endpoint(mock_log):
    response = client.post("/submit-feedback", headers=HEADERS, json={"user_id": "user1", "rating": "5", "comments": "Good"})
    assert response.status_code == 200
    assert response.json() == {"message": "Feedback submitted successfully!"}
    mock_log.assert_called_once()

