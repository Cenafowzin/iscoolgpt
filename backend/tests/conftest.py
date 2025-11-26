# Configuração dos testes do IsCoolGPT

import sys
import os
from pathlib import Path

# Adiciona o diretório pai (backend) ao Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Cliente de teste FastAPI"""
    return TestClient(app)

@pytest.fixture
def mock_api_key():
    """Mock da API key para testes"""
    original_key = os.getenv("GEMINI_API_KEY")
    os.environ["GEMINI_API_KEY"] = "test-mock-key-for-testing-only"
    yield "test-mock-key-for-testing-only"
    # Restaura a chave original após o teste
    if original_key:
        os.environ["GEMINI_API_KEY"] = original_key
    else:
        os.environ.pop("GEMINI_API_KEY", None)

@pytest.fixture
def sample_explain_request():
    """Dados de exemplo para teste de explicação"""
    return {
        "concept": "Fotossíntese",
        "level": "intermediate",
        "subject": "Biologia"
    }

@pytest.fixture  
def sample_question_request():
    """Dados de exemplo para teste de geração de questões"""
    return {
        "subject": "Matemática",
        "topic": "Equações de segundo grau",
        "difficulty": "medium",
        "question_type": "multiple_choice"
    }

@pytest.fixture
def sample_study_plan_request():
    """Dados de exemplo para teste de plano de estudos"""
    return {
        "subject": "Python Programming",
        "duration_weeks": 8,
        "daily_hours": 2,
        "current_level": "beginner"
    }

# Constantes para testes
VALID_DIFFICULTY_LEVELS = ["easy", "medium", "hard"]
VALID_QUESTION_TYPES = ["multiple_choice", "open_ended", "true_false"]
VALID_EXPLANATION_LEVELS = ["beginner", "intermediate", "advanced"]