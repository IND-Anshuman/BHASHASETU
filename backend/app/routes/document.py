from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.models import DocumentTranslateResult
from app.services.universal_translator import translate_document, translate_and_save
from app.services.google_translator import get_supported_languages
import shutil
import os
import logging

router = APIRouter()

@router.post("/translate", response_model=DocumentTranslateResult)
async def translate_document_endpoint(
    file: UploadFile = File(...),
    target_language: str = Form(...),
    source_language: str = Form('auto'),
    domain: str = Form('general'),
    region: str = Form('default')
):
    """
    Universal Document Translation
    
    Supports: PDF, DOCX, TXT, SRT files
    Translates to any of 22+ Indian languages using deep-translator
    Auto-detects source language if not specified
    """
    try:
        file_location = f"temp_{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logging.info(f"Translating document: {file.filename} -> {target_language}")
        
        result = await translate_document(
            file_path=file_location,
            target_language=target_language,
            source_language=source_language,
            domain=domain,
            region=region
        )
        
        os.remove(file_location)
        
        return DocumentTranslateResult(**result)
    except Exception as e:
        logging.error(f"Document translation failed: {e}")
        if os.path.exists(file_location):
            os.remove(file_location)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/translate-and-save")
async def translate_and_save_endpoint(
    file: UploadFile = File(...),
    target_language: str = Form(...),
    source_language: str = Form('auto'),
    domain: str = Form('general'),
    region: str = Form('default'),
    output_filename: str = Form(None)
):
    """
    Translate document and save translated text to file
    Returns both translation result and output file path
    """
    try:
        input_file = f"temp_input_{file.filename}"
        with open(input_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Generate output filename
        if not output_filename:
            base_name = os.path.splitext(file.filename)[0]
            output_filename = f"translated_{target_language}_{base_name}.txt"
        
        logging.info(f"Translating and saving: {file.filename} -> {output_filename}")
        
        result = await translate_and_save(
            input_file=input_file,
            output_file=output_filename,
            target_language=target_language,
            source_language=source_language,
            domain=domain,
            region=region
        )
        
        os.remove(input_file)
        
        return result
    except Exception as e:
        logging.error(f"Translate and save failed: {e}")
        if os.path.exists(input_file):
            os.remove(input_file)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/supported-formats")
async def get_supported_formats():
    """Get list of supported document formats"""
    return {
        "formats": ["PDF", "DOCX", "TXT", "SRT"],
        "extensions": [".pdf", ".docx", ".txt", ".srt"],
        "description": "All formats support text extraction and translation"
    }

@router.get("/languages")
async def get_document_languages():
    """Get supported languages for document translation"""
    try:
        languages = get_supported_languages()
        return {
            "total": len(languages),
            "languages": languages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
