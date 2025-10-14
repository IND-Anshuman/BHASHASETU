from fastapi import APIRouter, HTTPException, Body
from app.models import TranslateRequest, TranslationResult
from app.services.google_translator import translate_text_google, detect_language, get_supported_languages
from app.services.glossary import async_load_glossary, apply_glossary
from app.services.adaptations import adapt_region
import logging

router = APIRouter()

@router.post("/", response_model=TranslationResult)
async def translate_text_endpoint(request: TranslateRequest):
    """
    Text-to-Text Translation
    
    Supports all 22+ Indian languages using deep-translator
    Auto-detects source language if not specified
    Applies domain glossary and regional adaptation
    """
    try:
        logging.info(f"Translation request: {request.source_language} -> {request.target_language}")
        
        # Detect language if auto
        detected_lang = request.source_language
        if request.source_language == 'auto':
            detection = await detect_language(request.text)
            detected_lang = detection['language']
            logging.info(f"Auto-detected language: {detected_lang}")
        
        # Apply glossary
        glossary = await async_load_glossary(request.domain)
        text_with_glossary = apply_glossary(request.text, glossary)
        
        # Apply regional adaptation
        text_adapted = adapt_region(text_with_glossary, request.region)
        
        # Translate
        translated = await translate_text_google(
            text=text_adapted,
            target_language=request.target_language,
            source_language=detected_lang
        )
        
        return TranslationResult(
            original=request.text,
            translated=translated,
            glossary_applied=bool(glossary),
            confidence_score=0.95
        )
    except Exception as e:
        logging.error(f"Translation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/languages")
async def get_languages():
    """Get all supported languages for translation"""
    try:
        languages = get_supported_languages()
        return {
            "total": len(languages),
            "languages": languages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/detect")
async def detect_language_endpoint(text: str = Body(..., embed=True)):
    """Detect the language of input text (expects JSON body: {"text": "..."})"""
    try:
        result = await detect_language(text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch")
async def batch_translate_endpoint(
    texts: list[str],
    target_language: str,
    source_language: str = 'auto',
    domain: str = 'general'
):
    """
    Batch translate multiple texts
    Useful for translating lists or arrays
    """
    try:
        from app.services.google_translator import translate_batch
        
        results = await translate_batch(
            texts=texts,
            target_language=target_language,
            source_language=source_language
        )
        
        return {
            "total": len(results),
            "translations": results,
            "target_language": target_language
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
