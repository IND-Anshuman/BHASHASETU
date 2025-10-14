from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.models import SpeechToSpeechResult, AudioTranscriptionResult
from app.services.speech_to_speech import translate_speech_to_speech
from app.services.speech_to_text import (
    transcribe_audio, 
    transcribe_and_translate,
    transcribe_with_timestamps,
    get_supported_languages
)
import shutil
import os
from typing import Optional
import logging

router = APIRouter()

@router.post("/transcribe", response_model=AudioTranscriptionResult)
async def transcribe_audio_endpoint(
    audio_file: UploadFile = File(...),
    source_language: Optional[str] = Form(None),
    model_size: str = Form("base")
):
    """
    Speech-to-Text using Whisper
    
    Supports all 22+ Indian languages with auto-detection
    Model sizes: tiny, base (default), small, medium, large
    
    Returns transcribed text in the original language
    """
    try:
        audio_path = f"temp_audio_{audio_file.filename}"
        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)
        
        logging.info(f"Transcribing: {audio_file.filename}")
        
        result = await transcribe_audio(
            audio_path, 
            source_language=source_language,
            model_size=model_size
        )
        
        os.remove(audio_path)
        
        return AudioTranscriptionResult(
            text=result['text'],
            language=result['language']
        )
    except Exception as e:
        logging.error(f"Transcription failed: {e}")
        if os.path.exists(audio_path):
            os.remove(audio_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transcribe-translate")
async def transcribe_and_translate_endpoint(
    audio_file: UploadFile = File(...),
    target_language: str = Form(...),
    source_language: Optional[str] = Form(None),
    model_size: str = Form("base")
):
    """
    Transcribe audio and translate to target language
    
    RECOMMENDED Pipeline for Indian languages:
    1. Whisper transcribes audio to text (original language)
    2. Google Translate converts text to target language
    """
    try:
        audio_path = f"temp_audio_{audio_file.filename}"
        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)
        
        logging.info(f"Transcribe + Translate: {audio_file.filename} -> {target_language}")
        
        result = await transcribe_and_translate(
            audio_file_path=audio_path,
            target_language=target_language,
            source_language=source_language,
            model_size=model_size
        )
        
        os.remove(audio_path)
        
        return {
            "original_text": result['original_text'],
            "translated_text": result['translated_text'],
            "source_language": result['source_language'],
            "target_language": result['target_language']
        }
    except Exception as e:
        logging.error(f"Transcribe + translate failed: {e}")
        if os.path.exists(audio_path):
            os.remove(audio_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transcribe-with-timestamps")
async def transcribe_with_timestamps_endpoint(
    audio_file: UploadFile = File(...),
    source_language: Optional[str] = Form(None)
):
    """
    Transcribe audio with word/segment-level timestamps
    Useful for subtitle generation and video alignment
    """
    try:
        audio_path = f"temp_audio_{audio_file.filename}"
        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)
        
        segments = await transcribe_with_timestamps(
            audio_path,
            source_language=source_language
        )
        
        os.remove(audio_path)
        
        return {
            "segments": segments,
            "total_segments": len(segments)
        }
    except Exception as e:
        logging.error(f"Timestamp transcription failed: {e}")
        if os.path.exists(audio_path):
            os.remove(audio_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/translate", response_model=SpeechToSpeechResult)
async def speech_to_speech_endpoint(
    audio_file: UploadFile = File(...),
    target_language: str = Form(...),
    source_language: Optional[str] = Form(None),
    voice_type: str = Form("female"),
    domain: str = Form("general"),
    region: str = Form("default")
):
    """
    Complete Speech-to-Speech Translation
    
    Pipeline:
    1. Whisper: Speech → Text (original language)
    2. Deep-translator: Text → Translated Text (target language)
    3. Indic Parler TTS: Translated Text → Speech (target language)
    """
    try:
        audio_path = f"temp_input_{audio_file.filename}"
        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)
        
        logging.info(f"Speech-to-Speech: {audio_file.filename} -> {target_language}")
        
        result = await translate_speech_to_speech(
            input_audio_path=audio_path,
            target_language=target_language,
            source_language=source_language,
            voice_type=voice_type,
            domain=domain,
            region=region
        )
        
        os.remove(audio_path)
        return SpeechToSpeechResult(**result)
    except Exception as e:
        logging.error(f"Speech-to-speech failed: {e}")
        if os.path.exists(audio_path):
            os.remove(audio_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/supported-languages")
async def get_supported_asr_languages():
    """Get list of Indian languages supported by Whisper ASR"""
    try:
        languages = get_supported_languages()
        return {
            "total": len(languages),
            "languages": languages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
