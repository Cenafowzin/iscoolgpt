from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import google.generativeai as genai
import os
from typing import List, Optional
import logging
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
# Get the directory where this script is located
current_dir = Path(__file__).parent.parent  # Go up to backend directory
env_path = current_dir / '.env'
load_dotenv(dotenv_path=env_path)

# Debug: Print if .env file was found
if env_path.exists():
    print(f"✅ Arquivo .env encontrado em: {env_path}")
else:
    print(f"❌ Arquivo .env NÃO encontrado em: {env_path}")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="IsCoolGPT - Assistente Virtual de Estudos",
    description="Um assistente inteligente para ajudar nos seus estudos usando Google Gemini",
    version="1.0.0"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure according to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
is_ci = os.getenv("CI", "false").lower() == "true"
skip_api_validation = os.getenv("SKIP_API_VALIDATION", "false").lower() == "true"

if not api_key and not (is_ci or skip_api_validation):
    logger.error("GEMINI_API_KEY not found in environment variables")
    raise ValueError("GEMINI_API_KEY environment variable is required")

if is_ci or skip_api_validation:
    print(f"🧪 Modo CI/Teste - API Key validation pulada")
else:
    print(f"🔑 API Key: OK")
    genai.configure(api_key=api_key)

# Configure generation settings optimized for Gemini 2.0 Flash-Lite
generation_config = {
    "temperature": 0.7,        # Criatividade balanceada
    "top_p": 0.8,             # Diversidade controlada  
    "top_k": 40,              # Limitação de escolhas
    "max_output_tokens": 2048, # Máximo de tokens por resposta
}

# Usar modelo otimizado para free tier
model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite")
print(f"🤖 Modelo: {model_name}")

# Inicializar modelo apenas se não estiver no CI
if not (is_ci or skip_api_validation):
    model = genai.GenerativeModel(
        model_name,
        generation_config=generation_config
    )
else:
    model = None  # No CI, não precisamos do modelo real

# Helper function
def check_model_available():
    """Verifica se o modelo está disponível (não estamos no CI)"""
    if is_ci or skip_api_validation:
        raise HTTPException(
            status_code=503, 
            detail="API não disponível em modo CI/Teste. Use apenas endpoints básicos."
        )
    if model is None:
        raise HTTPException(
            status_code=500,
            detail="Modelo Gemini não inicializado"
        )

# Pydantic models
class Prompt(BaseModel):
    content: str = Field(..., description="The prompt content to send to Gemini")
    context: Optional[str] = Field(None, description="Additional context for the prompt")

class StudyQuestion(BaseModel):
    subject: str = Field(..., description="Subject area (e.g., Mathematics, History, Science)")
    topic: str = Field(..., description="Specific topic within the subject")
    difficulty: str = Field("medium", description="Difficulty level: easy, medium, hard")
    question_type: str = Field("multiple_choice", description="Type: multiple_choice, open_ended, true_false")

class ExplanationRequest(BaseModel):
    concept: str = Field(..., description="Concept to be explained")
    level: str = Field("intermediate", description="Explanation level: beginner, intermediate, advanced")
    subject: Optional[str] = Field(None, description="Subject context")

class StudyPlanRequest(BaseModel):
    subject: str = Field(..., description="Subject to study")
    duration_weeks: int = Field(..., description="Study duration in weeks")
    daily_hours: int = Field(..., description="Available daily study hours")
    current_level: str = Field("beginner", description="Current knowledge level")

@app.get("/")
async def root():
    return {"message": "IsCoolGPT - Assistente Virtual de Estudos", "status": "online"}

@app.get("/health")
async def health_check():
    """Basic health check without testing Gemini API"""
    return {
        "status": "healthy", 
        "service": "IsCoolGPT", 
        "api_configured": bool(os.getenv("GEMINI_API_KEY"))
    }

@app.get("/health/full")
async def full_health_check():
    """Complete health check including Gemini API test"""
    if is_ci or skip_api_validation:
        return {"status": "healthy", "mode": "CI/Test", "gemini_connection": "skipped"}
    
    try:
        # Test Gemini connection with timeout
        test_response = model.generate_content("Test", request_options={"timeout": 10})
        return {"status": "healthy", "gemini_connection": "ok", "test_response": bool(test_response.text)}
    except Exception as e:
        logger.error(f"Full health check failed: {e}")
        return {"status": "degraded", "gemini_connection": "error", "error": str(e)}

@app.get("/models")
async def list_available_models():
    """Lista modelos disponíveis (use apenas quando necessário para economizar requests)"""
    try:
        models = genai.list_models()
        available_models = []
        
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                available_models.append({
                    "name": model.name,
                    "display_name": model.display_name,
                    "description": getattr(model, 'description', 'No description available')
                })
        
        # Adiciona informações sobre modelos recomendados para free tier
        recommendations = {
            "current_model": model_name,
            "recommended_free_tier": [
                {
                    "name": "gemini-2.0-flash-lite",
                    "limits": "30 RPM, 1M TPM, 200 RPD",
                    "description": "Melhor custo-benefício"
                },
                {
                    "name": "gemini-2.0-flash", 
                    "limits": "15 RPM, 1M TPM, 200 RPD",
                    "description": "Maior capacidade"
                },
                {
                    "name": "gemini-2.5-flash-lite",
                    "limits": "15 RPM, 250k TPM, 1000 RPD", 
                    "description": "Mais requisições por dia"
                }
            ]
        }
        
        return {
            "available_models": available_models,
            "recommendations": recommendations,
            "note": "⚠️ Este endpoint consome uma request da sua cota. Use apenas quando necessário."
        }
        
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        raise HTTPException(status_code=500, detail=f"Error listing models: {str(e)}")

@app.post("/generate")
async def generate(data: Prompt):
    """Generate a response using Gemini AI"""
    check_model_available()  # Verifica se não estamos no CI
    
    try:
        prompt_text = data.content
        if data.context:
            prompt_text = f"Contexto: {data.context}\n\nPergunta: {data.content}"
        
        # Add timeout to prevent infinite loading
        result = model.generate_content(
            prompt_text,
            request_options={"timeout": 30}  # 30 second timeout
        )
        
        if not result or not result.text:
            raise HTTPException(status_code=500, detail="Failed to generate response")
            
        return {"response": result.text, "status": "success"}
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@app.post("/explain")
async def explain_concept(request: ExplanationRequest):
    """Explain a concept in detail for studying"""
    check_model_available()  # Verifica se não estamos no CI
    
    try:
        prompt = f"""
        Explique o conceito "{request.concept}" de forma didática e clara.
        
        Nível de explicação: {request.level}
        {f"Área de conhecimento: {request.subject}" if request.subject else ""}
        
        Por favor, organize a explicação com:
        1. Definição simples
        2. Explicação detalhada
        3. Exemplos práticos
        4. Aplicações no dia a dia (se aplicável)
        5. Dicas para memorização
        
        Use linguagem adequada ao nível solicitado.
        """
        
        result = model.generate_content(prompt)
        return {"explanation": result.text, "concept": request.concept, "level": request.level}
    except Exception as e:
        logger.error(f"Error explaining concept: {e}")
        raise HTTPException(status_code=500, detail=f"Error explaining concept: {str(e)}")

@app.post("/generate-question")
async def generate_study_question(request: StudyQuestion):
    """Generate study questions for practice"""
    check_model_available()  # Verifica se não estamos no CI
    
    try:
        prompt = f"""
        Gere uma questão de estudo sobre {request.subject}, especificamente sobre {request.topic}.
        
        Configurações:
        - Dificuldade: {request.difficulty}
        - Tipo de questão: {request.question_type}
        
        Para questões de múltipla escolha, inclua 4 alternativas (A, B, C, D).
        Para questões verdadeiro/falso, inclua a justificativa.
        Para questões abertas, forneça critérios de avaliação.
        
        Sempre inclua a resposta correta e uma explicação detalhada.
        """
        
        result = model.generate_content(prompt)
        return {
            "question": result.text,
            "subject": request.subject,
            "topic": request.topic,
            "difficulty": request.difficulty,
            "type": request.question_type
        }
    except Exception as e:
        logger.error(f"Error generating question: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating question: {str(e)}")

@app.post("/study-plan")
async def create_study_plan(request: StudyPlanRequest):
    """Create a personalized study plan"""
    check_model_available()  # Verifica se não estamos no CI
    
    try:
        prompt = f"""
        Crie um plano de estudos personalizado com as seguintes especificações:
        
        - Matéria: {request.subject}
        - Duração: {request.duration_weeks} semanas
        - Tempo diário disponível: {request.daily_hours} horas
        - Nível atual: {request.current_level}
        
        O plano deve incluir:
        1. Divisão semanal dos tópicos
        2. Objetivos de aprendizagem para cada semana
        3. Distribuição do tempo de estudo por dia
        4. Métodos de estudo recomendados
        5. Marcos de avaliação
        6. Recursos de estudo sugeridos
        7. Dicas de organização e produtividade
        
        Organize em formato claro e executável.
        """
        
        result = model.generate_content(prompt)
        return {
            "study_plan": result.text,
            "subject": request.subject,
            "duration_weeks": request.duration_weeks,
            "daily_hours": request.daily_hours,
            "level": request.current_level
        }
    except Exception as e:
        logger.error(f"Error creating study plan: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating study plan: {str(e)}")

@app.post("/summarize")
async def summarize_content(content: Prompt):
    """Summarize study content for review"""
    check_model_available()  # Verifica se não estamos no CI
    
    try:
        prompt = f"""
        Faça um resumo didático e estruturado do seguinte conteúdo de estudo:
        
        {content.content}
        
        O resumo deve incluir:
        1. Pontos principais
        2. Conceitos-chave
        3. Fatos importantes para memorizar
        4. Conexões entre ideias
        5. Possíveis perguntas de prova
        
        Use bullets e organize de forma clara para revisão.
        """
        
        result = model.generate_content(prompt)
        return {"summary": result.text, "status": "success"}
    except Exception as e:
        logger.error(f"Error summarizing content: {e}")
        raise HTTPException(status_code=500, detail=f"Error summarizing content: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
