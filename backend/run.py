#!/usr/bin/env python3
"""
BhashaSetu Backend Server Runner
Run this file to start the development server
"""
import uvicorn
from app.config import settings, logger

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("🚀 Starting BhashaSetu Backend Server")
    logger.info("=" * 60)
    logger.info(f"📍 Server URL: http://{settings.HOST}:{settings.PORT}")
    logger.info(f"📖 API Docs: http://{settings.HOST}:{settings.PORT}/docs")
    logger.info(f"📘 ReDoc: http://{settings.HOST}:{settings.PORT}/redoc")
    logger.info("=" * 60)
    logger.info("Press CTRL+C to stop the server")
    logger.info("=" * 60)
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=False  # Disable access log (we have custom logging)
    )
