from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import time
import logging

from app.config import settings, get_cors_origins, logger
from app.routes import (
    translate,
    tts,
    speech,
    document,
    subtitle,
    feedback,
    dashboard
)

# ==================== Application Lifespan ====================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Runs on startup and shutdown
    """
    # Startup
    logger.info("🚀 Application startup initiated")
    
    # Perform any startup tasks here
    # Example: Load ML models, connect to databases, etc.
    try:
        # You can pre-load models here for faster first request
        # from app.services.speech_to_text import get_whisper_model
        # get_whisper_model()  # Pre-load Whisper model
        
        logger.info("✅ Application startup completed successfully")
    except Exception as e:
        logger.error(f"❌ Error during startup: {e}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Application shutdown initiated")
    # Cleanup tasks here
    logger.info("✅ Application shutdown completed")

# ==================== Create FastAPI Application ====================
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# ==================== Middleware Configuration ====================

# 1. CORS Middleware - Must be first
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# 2. GZip Compression Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 3. Request Timing Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add response time header to all responses"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# 4. Request Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    logger.info(f"📥 {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"📤 {request.method} {request.url.path} - Status: {response.status_code}")
    return response

# ==================== Exception Handlers ====================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with detailed messages"""
    logger.warning(f"⚠️ Validation error on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "message": "Request validation failed. Please check your input."
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions"""
    logger.error(f"❌ Unhandled exception on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Internal server error occurred",
            "detail": str(exc) if settings.DEBUG else "An error occurred. Please try again later."
        }
    )

# ==================== Include Routers ====================

# Speech Processing
app.include_router(
    speech.router,
    prefix="/speech",
    tags=["Speech Translation"],
    responses={404: {"description": "Not found"}}
)

# Document Translation
app.include_router(
    document.router,
    prefix="/document",
    tags=["Document Translation"],
    responses={404: {"description": "Not found"}}
)

# Text Translation
app.include_router(
    translate.router,
    prefix="/translate",
    tags=["Text Translation"],
    responses={404: {"description": "Not found"}}
)

# Text-to-Speech
app.include_router(
    tts.router,
    prefix="/tts",
    tags=["Text-to-Speech"],
    responses={404: {"description": "Not found"}}
)

# Subtitle Processing
app.include_router(
    subtitle.router,
    prefix="/subtitle",
    tags=["Subtitles"],
    responses={404: {"description": "Not found"}}
)

# Feedback
app.include_router(
    feedback.router,
    prefix="/feedback",
    tags=["Feedback"],
    responses={404: {"description": "Not found"}}
)

# Analytics Dashboard
app.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"],
    responses={404: {"description": "Not found"}}
)

# ==================== Root Endpoints ====================

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API information
    """
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
        "supported_languages": len(settings.SUPPORTED_LANGUAGES),
        "features": [
            "Speech-to-Speech Translation",
            "Document Translation (PDF/DOCX/TXT/SRT)",
            "Subtitle Extraction & Translation",
            "Text-to-Speech (Male/Female voices)",
            "Domain Glossaries",
            "Regional Adaptation"
        ],
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json",
            "health": "/health",
            "languages": "/languages"
        }
    }

@app.get("/health", tags=["Root"])
async def health_check():
    """
    Health check endpoint
    Used by monitoring tools and load balancers
    """
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": "development" if settings.DEBUG else "production"
    }

@app.get("/languages", tags=["Root"])
async def get_supported_languages():
    """
    Get all supported languages
    """
    return {
        "total": len(settings.SUPPORTED_LANGUAGES),
        "languages": settings.SUPPORTED_LANGUAGES
    }

@app.get("/info", tags=["Root"])
async def get_api_info():
    """
    Get detailed API information and capabilities
    """
    return {
        "api_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
        "supported_languages": {
            "count": len(settings.SUPPORTED_LANGUAGES),
            "list": list(settings.SUPPORTED_LANGUAGES.keys())
        },
        "features": {
            "translation": {
                "text": True,
                "document": True,
                "speech": True,
                "subtitle": True,
                "batch": True
            },
            "tts": {
                "languages": len(settings.SUPPORTED_LANGUAGES),
                "voices": list(settings.VOICE_OPTIONS.keys()),
                "emotions": ["happy", "sad", "angry", "neutral", "narration"]
            },
            "asr": {
                "engine": "OpenAI Whisper",
                "model_size": settings.WHISPER_MODEL_SIZE,
                "auto_detect": True
            },
            "document_formats": ["PDF", "DOCX", "TXT", "SRT"],
            "video_formats": ["MP4", "MKV", "AVI"],
            "audio_formats": ["MP3", "WAV", "M4A", "FLAC"]
        },
        "endpoints": {
            "total": len(app.routes),
            "documented": "/docs"
        }
    }

@app.get("/stats", tags=["Root"])
async def get_system_stats():
    """
    Get system statistics and configuration status
    """
    return {
        "configuration": {
            "hugging_face_configured": settings.HUGGING_FACE_TOKEN is not None,
            "google_translate_configured": settings.GOOGLE_TRANSLATE_API_KEY is not None,
            "bhashini_configured": settings.BHASHINI_API_KEY is not None,
            "database_type": "SQLite" if "sqlite" in settings.DATABASE_URL.lower() else "PostgreSQL"
        },
        "models": {
            "whisper_size": settings.WHISPER_MODEL_SIZE,
            "tts_engine": "Indic Parler TTS",
            "translation_engine": "Google Translate (deep-translator)"
        },
        "server": {
            "host": settings.HOST,
            "port": settings.PORT,
            "debug_mode": settings.DEBUG
        }
    }

# ==================== Application Metadata ====================

@app.on_event("startup")
async def startup_event():
    """
    Additional startup event handler
    Use for tasks that need to run after lifespan startup
    """
    logger.info("📡 All routes registered successfully")
    logger.info(f"📚 Total endpoints: {len(app.routes)}")
    logger.info(f"🌍 CORS configured for: {len(get_cors_origins())} origins")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Additional shutdown event handler
    Use for cleanup tasks
    """
    logger.info("🧹 Cleaning up resources...")
    # Add cleanup code here if needed

# ==================== Run Configuration ====================
if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"🚀 Starting server at http://{settings.HOST}:{settings.PORT}")
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
