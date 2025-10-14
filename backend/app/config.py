import logging
import os
from typing import Dict, Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """
    Application settings and configuration
    Loads from .env file and environment variables
    """
    
    # ==================== API Keys ====================
    # Translation APIs (all optional for prototype)
    GOOGLE_TRANSLATE_API_KEY: Optional[str] = Field(default=None, description="Google Cloud Translation API key")
    GOOGLE_CLOUD_PROJECT_ID: Optional[str] = Field(default=None, description="Google Cloud Project ID")
    
    # Bhashini API (Indian government translation service)
    BHASHINI_API_KEY: Optional[str] = Field(default=None, description="Bhashini API key")
    BHASHINI_API_URL: str = Field(default="https://api.bhashini.gov.in/translate", description="Bhashini API endpoint")
    
    # Hugging Face (recommended for model downloads)
    HUGGING_FACE_TOKEN: Optional[str] = Field(default=None, description="Hugging Face API token")
    
    # ==================== Language Support ====================
    # All 22+ Indian languages supported
    SUPPORTED_LANGUAGES: Dict[str, str] = {
        "hi": "Hindi",
        "bn": "Bengali", 
        "te": "Telugu",
        "mr": "Marathi",
        "ta": "Tamil",
        "ur": "Urdu",
        "gu": "Gujarati",
        "kn": "Kannada",
        "ml": "Malayalam",
        "or": "Odia",
        "pa": "Punjabi",
        "as": "Assamese",
        "mai": "Maithili",
        "sa": "Sanskrit",
        "ks": "Kashmiri",
        "ne": "Nepali",
        "sd": "Sindhi",
        "kok": "Konkani",
        "doi": "Dogri",
        "mni": "Manipuri",
        "sat": "Santali",
        "brx": "Bodo",
        "en": "English"
    }
    
    # Voice options for TTS
    VOICE_OPTIONS: Dict[str, list] = {
        "male": ["male_voice_1", "male_voice_2"],
        "female": ["female_voice_1", "female_voice_2"]
    }
    
    # ==================== Database Configuration ====================
    DATABASE_URL: str = Field(
        default="sqlite:///./bhasha.db",
        description="Database connection URL"
    )
    
    # ==================== Server Configuration ====================
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    DEBUG: bool = Field(default=True, description="Debug mode")
    RELOAD: bool = Field(default=True, description="Auto-reload on code changes")
    
    # Application metadata
    APP_NAME: str = "BhashaSetu API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "AI-Powered Multilingual Translation Platform for 22+ Indian Languages"
    
    # ==================== CORS Configuration ====================
    # Allow these origins to access the API
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",  # Vite default
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
    ]
    
    # ==================== File Storage ====================
    UPLOAD_DIR: str = Field(default="uploads", description="Directory for uploaded files")
    OUTPUT_DIR: str = Field(default="outputs", description="Directory for generated files")
    MAX_UPLOAD_SIZE: int = Field(default=100 * 1024 * 1024, description="Max upload size in bytes (100MB)")
    
    # ==================== Model Configuration ====================
    WHISPER_MODEL_SIZE: str = Field(default="base", description="Whisper model size (tiny/base/small/medium/large)")
    TTS_MODEL_CACHE_DIR: str = Field(default=".cache/tts_models", description="TTS model cache directory")
    
    # ==================== Rate Limiting ====================
    RATE_LIMIT_ENABLED: bool = Field(default=False, description="Enable rate limiting")
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, description="Requests per minute")
    
    # ==================== Cloud Storage (Optional) ====================
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET: Optional[str] = None
    AWS_REGION: str = "ap-south-1"
    
    # ==================== Logging Configuration ====================
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] - %(message)s"
    LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Initialize settings
settings = Settings()

# ==================== Setup Logging ====================
def setup_logging():
    """Configure application logging"""
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    logging.basicConfig(
        level=log_level,
        format=settings.LOG_FORMAT,
        datefmt=settings.LOG_DATE_FORMAT,
        handlers=[
            logging.StreamHandler(),
            # Uncomment to enable file logging
            # logging.FileHandler("bhashasetu.log", encoding='utf-8')
        ]
    )
    
    # Set third-party loggers to WARNING to reduce noise
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# ==================== Create Required Directories ====================
def create_directories():
    """Create required directories if they don't exist"""
    directories = [
        settings.UPLOAD_DIR,
        settings.OUTPUT_DIR,
        settings.TTS_MODEL_CACHE_DIR,
        "data/glossaries",
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Directory ensured: {directory}")

create_directories()

# ==================== Log Configuration Status ====================
def log_configuration():
    """Log current configuration status"""
    logger.info("=" * 60)
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info("=" * 60)
    
    # API Keys status
    logger.info("📡 API Configuration:")
    logger.info(f"  - Hugging Face Token: {'✅ Configured' if settings.HUGGING_FACE_TOKEN else '⚠️  Not configured (optional)'}")
    logger.info(f"  - Google Translate API: {'✅ Configured' if settings.GOOGLE_TRANSLATE_API_KEY else '⚠️  Not configured (using free tier)'}")
    logger.info(f"  - Bhashini API: {'✅ Configured' if settings.BHASHINI_API_KEY else '⚠️  Not configured (optional)'}")
    
    # Model configuration
    logger.info("🤖 Model Configuration:")
    logger.info(f"  - Whisper Model Size: {settings.WHISPER_MODEL_SIZE}")
    logger.info(f"  - Supported Languages: {len(settings.SUPPORTED_LANGUAGES)}")
    
    # Server configuration
    logger.info("🌐 Server Configuration:")
    logger.info(f"  - Host: {settings.HOST}")
    logger.info(f"  - Port: {settings.PORT}")
    logger.info(f"  - Debug Mode: {settings.DEBUG}")
    logger.info(f"  - CORS Origins: {len(settings.ALLOWED_ORIGINS)} configured")
    
    logger.info("=" * 60)

log_configuration()

# ==================== Helper Functions ====================
def is_production() -> bool:
    """Check if running in production mode"""
    return not settings.DEBUG

def get_cors_origins() -> list:
    """Get CORS origins based on environment"""
    if is_production():
        # In production, only allow specific domains
        return [origin for origin in settings.ALLOWED_ORIGINS if not origin.startswith("http://localhost")]
    return settings.ALLOWED_ORIGINS

# ==================== Export ====================
__all__ = [
    "settings",
    "logger",
    "is_production",
    "get_cors_origins"
]

