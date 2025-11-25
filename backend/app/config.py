import os
from typing import Optional

class Settings:
    """Application settings and configuration"""
    
    # API Configuration
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    
    # Application Configuration
    APP_NAME: str = "IsCoolGPT - Assistente Virtual de Estudos"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # CORS Configuration
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    
    # Gemini Model Configuration
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", 2048))
    
    # Study Assistant Configuration
    DEFAULT_DIFFICULTY: str = "medium"
    DEFAULT_QUESTION_TYPE: str = "multiple_choice"
    DEFAULT_EXPLANATION_LEVEL: str = "intermediate"
    MAX_STUDY_PLAN_WEEKS: int = 52  # 1 year max
    MAX_DAILY_HOURS: int = 12
    
    def validate(self) -> bool:
        """Validate required settings"""
        if not self.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        return True

settings = Settings()