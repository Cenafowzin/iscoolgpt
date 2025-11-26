import sys
import os
from pathlib import Path

# Adiciona o diretório pai ao Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from app.main import app
import pytest

# Set a mock API key for testing if not present
if not os.getenv("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = "test-key-for-testing"

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "IsCoolGPT" in response.json()["message"]

@pytest.mark.api_required
def test_generate_basic():
    """Teste que requer API real - pular em CI/CD"""
    if not os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") == "test-key-for-testing":
        pytest.skip("API key real necessária para este teste")
    
    response = client.post("/generate", json={"content": "Hello"})
    assert response.status_code == 200
    assert "response" in response.json()

def test_generate_structure_only():
    """Teste apenas a estrutura sem consumir API"""
    response = client.post("/generate", json={"content": "Hello"})
    # Verifica apenas que o endpoint existe e valida dados
    assert response.status_code in [200, 422, 500]  # Estrutura válida

@pytest.mark.api_required
def test_explain_concept():
    """Teste que requer API real - pular em CI/CD"""
    if not os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") == "test-key-for-testing":
        pytest.skip("API key real necessária para este teste")
        
    response = client.post("/explain", json={
        "concept": "Photosynthesis",
        "level": "beginner",
        "subject": "Biology"
    })
    assert response.status_code == 200
    assert "explanation" in response.json()

def test_explain_validation():
    """Testa apenas validação sem consumir API"""
    # Teste com dados válidos - estrutura OK
    response = client.post("/explain", json={
        "concept": "Test",
        "level": "beginner",
        "subject": "Math"
    })
    assert response.status_code in [200, 500]  # Estrutura válida
    
    # Teste com dados inválidos - deve dar erro de validação
    response = client.post("/explain", json={"concept": "Test", "level": "invalid_level"})
    assert response.status_code == 422  # Erro de validação

@pytest.mark.api_required  
def test_generate_question():
    """Teste que requer API real - pular em CI/CD"""
    if not os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") == "test-key-for-testing":
        pytest.skip("API key real necessária para este teste")
        
    response = client.post("/generate-question", json={
        "subject": "Mathematics",
        "topic": "Algebra", 
        "difficulty": "medium",
        "question_type": "multiple_choice"
    })
    assert response.status_code == 200
    assert "question" in response.json()

@pytest.mark.api_required
def test_study_plan():
    """Teste que requer API real - pular em CI/CD"""
    if not os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") == "test-key-for-testing":
        pytest.skip("API key real necessária para este teste")
        
    response = client.post("/study-plan", json={
        "subject": "Python Programming",
        "duration_weeks": 4,
        "daily_hours": 2,
        "current_level": "beginner"
    })
    assert response.status_code == 200
    assert "study_plan" in response.json()

@pytest.mark.api_required
def test_summarize():
    """Teste que requer API real - pular em CI/CD"""
    if not os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") == "test-key-for-testing":
        pytest.skip("API key real necessária para este teste")
        
    response = client.post("/summarize", json={
        "content": "This is a test content to summarize for studying purposes."
    })
    assert response.status_code == 200
    assert "summary" in response.json()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "service" in data
    assert data["service"] == "IsCoolGPT"

@pytest.mark.api_required
def test_models_endpoint():
    """Test the models listing endpoint - CONSOME TOKENS!"""
    if not os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") == "test-key-for-testing":
        pytest.skip("API key real necessária - endpoint consome tokens!")
        
    response = client.get("/models")
    assert response.status_code == 200
    data = response.json()
    assert "available_models" in data
    assert "recommendations" in data
    assert "note" in data  # Aviso sobre consumo de tokens

@pytest.mark.api_required
def test_full_health_check():
    """Test the full health check endpoint - CONSOME TOKENS!"""
    if not os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") == "test-key-for-testing":
        pytest.skip("API key real necessária - health check completo consome tokens!")
        
    response = client.get("/health/full")
    assert response.status_code == 200  
    data = response.json()
    assert "status" in data
    assert "gemini_connection" in data

def test_invalid_endpoints():
    """Test invalid endpoints return 404"""
    response = client.get("/invalid-endpoint")
    assert response.status_code == 404

def test_malformed_requests():
    """Test malformed requests return proper errors"""
    # Test missing required fields
    response = client.post("/explain", json={})
    assert response.status_code == 422  # Validation error
    
    response = client.post("/generate-question", json={"subject": "Math"})
    assert response.status_code == 422  # Missing required fields
    
    response = client.post("/study-plan", json={"subject": "Python"})
    assert response.status_code == 422  # Missing required fields
