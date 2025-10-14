from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.models import SubtitleExtractRequest, SubtitleExtractResult, SubtitleTranslateRequest, SubtitleTranslateResult
from app.services.subtitle_extractor import extract_subtitles
from app.services.subtitle_translator import translate_subtitle_file
import shutil
import os
import logging

router = APIRouter()

@router.post("/extract", response_model=SubtitleExtractResult)
async def extract_subtitle_endpoint(
    video_file: UploadFile = File(...),
    subtitle_index: int = Form(0)
):
    """
    Extract embedded subtitles from video files
    
    Supports: MP4, MKV, AVI and other video formats with embedded SRT subtitles
    """
    try:
        video_path = f"temp_video_{video_file.filename}"
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(video_file.file, buffer)
        
        logging.info(f"Extracting subtitles from: {video_file.filename}")
        
        request = SubtitleExtractRequest(
            video_file_path=video_path,
            subtitle_index=subtitle_index
        )
        result = await extract_subtitles(request)
        
        os.remove(video_path)
        
        return SubtitleExtractResult(**result)
    except Exception as e:
        logging.error(f"Subtitle extraction failed: {e}")
        if os.path.exists(video_path):
            os.remove(video_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/translate", response_model=SubtitleTranslateResult)
async def translate_subtitle_endpoint(
    subtitle_file: UploadFile = File(...),
    source_language: str = Form(...),
    target_language: str = Form(...),
    domain: str = Form("general"),
    region: str = Form("default")
):
    """
    Translate SRT subtitle files
    
    Preserves SRT timestamp format while translating text
    Applies glossary and regional adaptation
    Uses deep-translator for high-quality translation
    """
    try:
        srt_path = f"temp_{subtitle_file.filename}"
        with open(srt_path, "wb") as buffer:
            shutil.copyfileobj(subtitle_file.file, buffer)
        
        logging.info(f"Translating subtitles: {subtitle_file.filename} -> {target_language}")
        
        request = SubtitleTranslateRequest(
            subtitle_file_path=srt_path,
            source_language=source_language,
            target_language=target_language,
            domain=domain,
            region=region
        )
        
        translated_path = await translate_subtitle_file(request)
        
        os.remove(srt_path)
        
        return SubtitleTranslateResult(
            translated_subtitle_path=translated_path,
            language=target_language
        )
    except Exception as e:
        logging.error(f"Subtitle translation failed: {e}")
        if os.path.exists(srt_path):
            os.remove(srt_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/extract-and-translate")
async def extract_and_translate_subtitles(
    video_file: UploadFile = File(...),
    target_language: str = Form(...),
    source_language: str = Form('auto'),
    subtitle_index: int = Form(0),
    domain: str = Form("general"),
    region: str = Form("default")
):
    """
    Complete pipeline: Extract subtitles from video and translate
    
    Steps:
    1. Extract embedded subtitles from video
    2. Translate SRT file to target language
    3. Return translated subtitle file
    """
    try:
        video_path = f"temp_video_{video_file.filename}"
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(video_file.file, buffer)
        
        logging.info(f"Extract + Translate pipeline for: {video_file.filename}")
        
        # Step 1: Extract
        extract_request = SubtitleExtractRequest(
            video_file_path=video_path,
            subtitle_index=subtitle_index
        )
        extract_result = await extract_subtitles(extract_request)
        
        # Step 2: Translate
        translate_request = SubtitleTranslateRequest(
            subtitle_file_path=extract_result['subtitle_file_path'],
            source_language=source_language,
            target_language=target_language,
            domain=domain,
            region=region
        )
        translated_path = await translate_subtitle_file(translate_request)
        
        # Cleanup
        os.remove(video_path)
        os.remove(extract_result['subtitle_file_path'])
        
        return {
            "original_subtitle": extract_result['subtitle_file_path'],
            "translated_subtitle": translated_path,
            "target_language": target_language
        }
    except Exception as e:
        logging.error(f"Extract + translate pipeline failed: {e}")
        if os.path.exists(video_path):
            os.remove(video_path)
        raise HTTPException(status_code=500, detail=str(e))
