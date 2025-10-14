from app.services.text_extractor import extract_text_universal
from app.services.google_translator import translate_text_google, detect_language
from app.services.glossary import async_load_glossary, apply_glossary
from app.services.adaptations import adapt_region
import logging
from typing import Optional

async def translate_document(
    file_path: str,
    target_language: str,
    source_language: str = 'auto',
    domain: str = 'general',
    region: str = 'default',
    file_type: Optional[str] = None
) -> dict:
    """
    Universal document translator with deep-translator backend
    
    Supports all 22+ Indian languages via Google Translate API
    
    Pipeline:
    1. Extract text from document (PDF/DOCX/TXT/SRT)
    2. Detect source language if 'auto'
    3. Apply domain-specific glossary
    4. Apply regional adaptation rules
    5. Translate using deep-translator Google Translate
    6. Return comprehensive result
    
    Args:
        file_path: Path to document file
        target_language: Target language code (hi, ta, te, etc.)
        source_language: Source language code or 'auto'
        domain: Domain for glossary (general, automotive, healthcare, etc.)
        region: Region for adaptation (default, tamilnadu, kerala, etc.)
        file_type: File type override (pdf, docx, txt, srt)
    
    Returns:
        {
            'original_text': str,
            'translated_text': str,
            'detected_language': str,
            'target_language': str,
            'file_type': str,
            'glossary_applied': bool,
            'region_adapted': bool,
            'character_count': int
        }
    """
    try:
        # Step 1: Extract text from document
        logging.info(f"Step 1: Extracting text from {file_path}")
        extracted_text = await extract_text_universal(file_path, file_type)
        
        if not extracted_text or extracted_text.strip() == "":
            raise ValueError("No text extracted from document")
        
        char_count = len(extracted_text)
        logging.info(f"Extracted {char_count} characters")
        
        # Step 2: Detect language if auto
        detected_lang = source_language
        if source_language == 'auto':
            logging.info("Step 2: Detecting source language...")
            detection_result = await detect_language(extracted_text[:500])  # Use first 500 chars
            detected_lang = detection_result['language']
            logging.info(f"Detected language: {detected_lang}")
        
        # Step 3: Apply domain glossary
        logging.info(f"Step 3: Applying glossary for domain '{domain}'...")
        glossary = await async_load_glossary(domain)
        text_with_glossary = apply_glossary(extracted_text, glossary)
        
        # Step 4: Apply regional adaptation
        logging.info(f"Step 4: Applying regional adaptation for '{region}'...")
        text_adapted = adapt_region(text_with_glossary, region)
        
        # Step 5: Translate using deep-translator
        logging.info(f"Step 5: Translating from {detected_lang} to {target_language}...")
        
        # Skip translation if source == target
        if detected_lang == target_language:
            logging.info("Source and target languages are same, skipping translation")
            translated_text = text_adapted
        else:
            translated_text = await translate_text_google(
                text_adapted,
                target_language=target_language,
                source_language=detected_lang
            )
        
        logging.info(f"Translation complete: {len(translated_text)} characters")
        
        # Return both `source_language` (expected by response model) and
        # `detected_language` for backward compatibility.
        return {
            'original_text': extracted_text,
            'translated_text': translated_text,
            'source_language': detected_lang,
            'detected_language': detected_lang,
            'target_language': target_language,
            'file_type': file_type or file_path.split('.')[-1],
            'glossary_applied': bool(glossary),
            'region_adapted': region != 'default',
            'character_count': char_count
        }
    
    except Exception as e:
        logging.error(f"Document translation failed: {e}")
        raise Exception(f"Universal document translation error: {e}")

async def translate_and_save(
    input_file: str,
    output_file: str,
    target_language: str,
    source_language: str = 'auto',
    domain: str = 'general',
    region: str = 'default'
) -> dict:
    """
    Translate document and save to output file
    
    Returns translation result with output file path
    """
    try:
        result = await translate_document(
            file_path=input_file,
            target_language=target_language,
            source_language=source_language,
            domain=domain,
            region=region
        )
        
        # Save translated text to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result['translated_text'])
        
        result['output_file'] = output_file
        logging.info(f"Translated document saved to {output_file}")
        
        return result
    
    except Exception as e:
        logging.error(f"Translate and save failed: {e}")
        raise
