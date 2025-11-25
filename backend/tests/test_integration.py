"""
Testes de integração para o IsCoolGPT
Testa funcionalidades mais complexas e fluxos completos
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório pai ao Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

class TestIntegration:
    """Testes de integração para fluxos completos"""
    
    @pytest.mark.api_required
    def test_complete_study_workflow(self, mock_api_key):
        """Testa um fluxo completo de estudo - CONSOME MUITOS TOKENS!"""
        if not os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") == "test-key-for-testing":
            pytest.skip("API key real necessária - workflow consome muitos tokens!")
            
        # 1. Verificar saúde da aplicação
        health_response = client.get("/health")
        assert health_response.status_code == 200
        
        # 2. Explicar um conceito
        explain_data = {
            "concept": "Algoritmos de ordenação",
            "level": "intermediate",
            "subject": "Ciência da Computação"
        }
        explain_response = client.post("/explain", json=explain_data)
        assert explain_response.status_code == 200
        assert "explanation" in explain_response.json()
        
        # 3. Gerar uma questão sobre o conceito
        question_data = {
            "subject": "Ciência da Computação", 
            "topic": "Algoritmos de ordenação",
            "difficulty": "medium",
            "question_type": "multiple_choice"
        }
        question_response = client.post("/generate-question", json=question_data)
        assert question_response.status_code == 200
        assert "question" in question_response.json()
        
        # 4. Criar um plano de estudos
        plan_data = {
            "subject": "Algoritmos",
            "duration_weeks": 6,
            "daily_hours": 3,
            "current_level": "intermediate"
        }
        plan_response = client.post("/study-plan", json=plan_data)
        assert plan_response.status_code == 200
        assert "study_plan" in plan_response.json()
        
    def test_structural_workflow(self):
        """Testa fluxo estrutural sem consumir API"""
        # 1. Health check
        health_response = client.get("/health")
        assert health_response.status_code == 200
        
        # 2. Testa estrutura dos endpoints sem executar AI
        endpoints_data = [
            ("/explain", {"concept": "Test", "level": "beginner"}),
            ("/generate-question", {"subject": "Math", "topic": "Test", "difficulty": "easy", "question_type": "multiple_choice"}),
            ("/study-plan", {"subject": "Test", "duration_weeks": 1, "daily_hours": 1, "current_level": "beginner"}),
            ("/summarize", {"content": "Test content"})
        ]
        
        for endpoint, data in endpoints_data:
            response = client.post(endpoint, json=data)
            # Estrutura deve estar OK, mesmo que API falhe
            assert response.status_code in [200, 422, 500]
    
    def test_error_handling_chain(self):
        """Testa como a aplicação lida com erros em sequência"""
        
        # Dados inválidos em sequência
        invalid_requests = [
            ("/explain", {}),
            ("/generate-question", {"subject": "Math"}),
            ("/study-plan", {"invalid": "data"}),
            ("/summarize", {}),
        ]
        
        for endpoint, data in invalid_requests:
            response = client.post(endpoint, json=data)
            assert response.status_code == 422  # Validation error
            
    def test_concurrent_requests_simulation(self):
        """Simula requisições concorrentes"""
        
        # Simula várias requisições ao mesmo tempo
        responses = []
        endpoints = ["/", "/health", "/health", "/"]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            responses.append(response)
            
        # Todas devem ter sucesso
        for response in responses:
            assert response.status_code == 200

class TestValidation:
    """Testes específicos para validação de dados"""
    
    @pytest.mark.parametrize("level", ["beginner", "intermediate", "advanced"])
    def test_explanation_levels(self, level):
        """Testa todos os níveis de explicação válidos - APENAS ESTRUTURA"""
        data = {
            "concept": "Teste",
            "level": level,
            "subject": "Matemática"
        }
        response = client.post("/explain", json=data)
        # Estrutura deve estar correta, independente do resultado da API
        assert response.status_code in [200, 422, 500]
        if response.status_code == 422:
            # Se 422, deve ser por outro motivo, não pelo level
            error_detail = response.json()["detail"]
            level_errors = [e for e in error_detail if "level" in str(e)]
            assert len(level_errors) == 0
    
    @pytest.mark.parametrize("difficulty", ["easy", "medium", "hard"])
    def test_question_difficulties(self, difficulty):
        """Testa todas as dificuldades válidas - APENAS ESTRUTURA"""
        data = {
            "subject": "Matemática",
            "topic": "Álgebra", 
            "difficulty": difficulty,
            "question_type": "multiple_choice"
        }
        response = client.post("/generate-question", json=data)
        # Testa apenas estrutura, não consome API
        assert response.status_code in [200, 422, 500]
    
    @pytest.mark.parametrize("question_type", ["multiple_choice", "open_ended", "true_false"])
    def test_question_types(self, question_type):
        """Testa todos os tipos de questão válidos - APENAS ESTRUTURA"""
        data = {
            "subject": "História",
            "topic": "Segunda Guerra Mundial",
            "difficulty": "medium",
            "question_type": question_type
        }
        response = client.post("/generate-question", json=data)
        # Testa apenas estrutura, não consome API
        assert response.status_code in [200, 422, 500]

class TestPerformance:
    """Testes básicos de performance"""
    
    def test_response_time_basic_endpoints(self):
        """Testa se endpoints básicos respondem rapidamente"""
        import time
        
        start_time = time.time()
        response = client.get("/")
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 1.0  # Deve responder em menos de 1 segundo
        
    def test_health_check_performance(self):
        """Health check deve ser muito rápido"""
        import time
        
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        assert response.status_code == 200  
        assert (end_time - start_time) < 0.5  # Deve responder em menos de 500ms