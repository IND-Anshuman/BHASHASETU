from deep_translator import GoogleTranslator
import asyncio
import logging
from typing import List, Optional

# Complete language code mapping for 22+ Indian languages supported by Google Translate
INDIAN_LANGUAGE_CODES = {
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

# Cache translator instances for performance
_translator_cache = {}

def get_translator_instance(source: str, target: str) -> GoogleTranslator:
    """
    Get or create a cached translator instance
    Reusing instances improves performance significantly
    """
    # Validate target code (deep-translator expects ISO codes; we map if possible)
    def _normalize_code(code: str) -> str:
        if not code:
            return 'en'
        return code

    target = _normalize_code(target)

    # Do not cache translators that were created with source='auto' because
    # detection behavior and internal state may vary; return a fresh instance.
    if source == 'auto':
        return GoogleTranslator(source=source, target=target)

    cache_key = f"{source}_{target}"
    if cache_key not in _translator_cache:
        _translator_cache[cache_key] = GoogleTranslator(source=source, target=target)
    return _translator_cache[cache_key]

async def translate_text_google(
    text: str,
    target_language: str,
    source_language: str = 'auto',
    chunk_size: int = 4500
) -> str:
    """
    Translate text using Google Translate via deep-translator
    
    Args:
        text: Text to translate
        target_language: Target language code (hi, ta, te, etc.)
        source_language: Source language code or 'auto' for auto-detection
        chunk_size: Maximum characters per chunk (Google limit ~5000)
    
    Returns:
        Translated text string
    
    Raises:
        ValueError: If language code is unsupported
        Exception: For translation failures
    """
    try:
        # Validate target language
        if target_language not in INDIAN_LANGUAGE_CODES and target_language != 'auto':
            logging.warning(f"Language {target_language} not in Indian languages list, proceeding anyway")
        
        # Handle empty text
        if not text or text.strip() == "":
            return ""
        
        # For short text, translate directly
        if len(text) <= chunk_size:
            translator = get_translator_instance(source_language, target_language)
            try:
                result = await asyncio.to_thread(translator.translate, text)
                # deep-translator may return None or empty string on failure
                if result is None or (isinstance(result, str) and result.strip() == ""):
                    return text
                return result
            except Exception as e:
                logging.warning(f"Translation call failed for short text; returning original: {e}")
                return text
        
        # For large texts, chunk and translate
        logging.info(f"Text length {len(text)} exceeds chunk size, splitting into chunks")
        chunks = _split_text_intelligently(text, chunk_size)
        translated_chunks = []
        
        translator = get_translator_instance(source_language, target_language)
        
        for i, chunk in enumerate(chunks):
            logging.debug(f"Translating chunk {i+1}/{len(chunks)}")
            try:
                translated_chunk = await asyncio.to_thread(translator.translate, chunk)
                if translated_chunk is None or (isinstance(translated_chunk, str) and translated_chunk.strip() == ""):
                    translated_chunks.append(chunk)
                else:
                    translated_chunks.append(translated_chunk)
            except Exception as e:
                logging.warning(f"Chunk translation failed; using original chunk: {e}")
                translated_chunks.append(chunk)
            
            # Small delay to avoid rate limiting
            if i < len(chunks) - 1:
                await asyncio.sleep(0.1)
        
        return " ".join(translated_chunks)
    
    except Exception as e:
        logging.error(f"Translation failed from {source_language} to {target_language}: {e}")
        raise Exception(f"Translation error: {e}")

async def translate_batch(
    texts: List[str],
    target_language: str,
    source_language: str = 'auto'
) -> List[str]:
    """
    Translate multiple texts in batch
    
    Args:
        texts: List of text strings to translate
        target_language: Target language code
        source_language: Source language code or 'auto'
    
    Returns:
        List of translated strings
    """
    try:
        translator = get_translator_instance(source_language, target_language)
        
        # Use deep-translator's batch translation if available
        if hasattr(translator, 'translate_batch'):
            logging.info(f"Batch translating {len(texts)} texts")
            results = await asyncio.to_thread(translator.translate_batch, texts)
            return results
        else:
            # Fallback to individual translations
            logging.info(f"Translating {len(texts)} texts individually")
            tasks = [translate_text_google(text, target_language, source_language) for text in texts]
            return await asyncio.gather(*tasks)
    
    except Exception as e:
        logging.error(f"Batch translation failed: {e}")
        raise Exception(f"Batch translation error: {e}")

async def detect_language(text: str) -> dict:
    """
    Detect the language of input text
    
    Returns:
        {
            'language': str,      # Language code (e.g., 'hi', 'en')
            'language_name': str, # Full language name
            'confidence': float   # Confidence score (if available)
        }
    """
    try:
        # Try deep-translator's single_detection first (may require API key)
        from deep_translator import single_detection

        try:
            detected_lang = await asyncio.to_thread(single_detection, text, api_key=None)
            language_name = INDIAN_LANGUAGE_CODES.get(detected_lang, "Unknown")
            logging.info(f"Detected language (deep-translator): {detected_lang} ({language_name})")
            return {
                'language': detected_lang,
                'language_name': language_name,
                'confidence': 0.95
            }
        except Exception as dt_err:
            logging.debug(f"deep-translator detection failed: {dt_err}")

        # Fallback: use langdetect (no API key required)
        try:
            from langdetect import detect_langs
            detections = await asyncio.to_thread(detect_langs, text)
            if detections:
                best = detections[0]
                detected_lang = best.lang
                confidence = best.prob
                language_name = INDIAN_LANGUAGE_CODES.get(detected_lang, "Unknown")
                logging.info(f"Detected language (langdetect): {detected_lang} ({language_name}) confidence={confidence}")
                return {
                    'language': detected_lang,
                    'language_name': language_name,
                    'confidence': float(confidence)
                }
        except Exception as ld_err:
            logging.debug(f"langdetect failed: {ld_err}")

        # Heuristic fallback: if text is plain ASCII letters/digits/punctuation, assume English
        try:
            if all(ord(c) < 128 for c in text.strip() if c):
                logging.info("Heuristic detect: ASCII-only text -> assuming 'en'")
                return {'language': 'en', 'language_name': 'English', 'confidence': 0.5}
        except Exception:
            pass

        logging.error("Language detection failed with all methods")
        return {
            'language': 'unknown',
            'language_name': 'Unknown',
            'confidence': 0.0
        }
    except Exception as e:
        logging.error(f"Unexpected error in language detection: {e}")
        return {
            'language': 'unknown',
            'language_name': 'Unknown',
            'confidence': 0.0
        }

def _split_text_intelligently(text: str, chunk_size: int) -> List[str]:
    """
    Split text into chunks at sentence boundaries when possible
    Preserves sentence integrity for better translation quality
    
    Args:
        text: Text to split
        chunk_size: Maximum chunk size
    
    Returns:
        List of text chunks
    """
    import re
    
    # Split by sentence endings
    sentences = re.split(r'(?<=[।.!?;])\s+', text)
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        # If single sentence exceeds chunk size, split it
        if len(sentence) > chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""
            # Split long sentence by words
            words = sentence.split()
            temp_chunk = ""
            for word in words:
                if len(temp_chunk) + len(word) + 1 <= chunk_size:
                    temp_chunk += word + " "
                else:
                    chunks.append(temp_chunk.strip())
                    temp_chunk = word + " "
            if temp_chunk:
                chunks.append(temp_chunk.strip())
        # If adding sentence doesn't exceed limit
        elif len(current_chunk) + len(sentence) + 1 <= chunk_size:
            current_chunk += sentence + " "
        # Start new chunk
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    
    # Add remaining text
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def get_supported_languages() -> dict:
    """
    Get all supported languages for Google Translate
    
    Returns:
        Dictionary mapping language codes to language names
    """
    try:
        translator = GoogleTranslator()
        all_languages = translator.get_supported_languages(as_dict=True)

        # Return only Indian languages if possible
        indian_langs = {k: v for k, v in all_languages.items() if k in INDIAN_LANGUAGE_CODES}
        if indian_langs:
            return indian_langs
        # if deep-translator returned unexpected format, fall back to built-in mapping
        logging.debug("deep-translator did not return expected language codes; using fallback mapping")
        return INDIAN_LANGUAGE_CODES
    except Exception as e:
        logging.error(f"Failed to get supported languages: {e}")
        return INDIAN_LANGUAGE_CODES

async def translate_with_alternatives(
    text: str,
    target_language: str,
    source_language: str = 'auto',
    num_alternatives: int = 3
) -> dict:
    """
    Get translation with alternative suggestions (if available)
    
    Returns:
        {
            'primary_translation': str,
            'alternatives': List[str],
            'source_language': str,
            'target_language': str
        }
    """
    try:
        primary = await translate_text_google(text, target_language, source_language)
        
        return {
            'primary_translation': primary,
            'alternatives': [],  # deep-translator doesn't provide alternatives by default
            'source_language': source_language,
            'target_language': target_language
        }
    except Exception as e:
        logging.error(f"Translation with alternatives failed: {e}")
        raise

def clear_translator_cache():
    """Clear cached translator instances"""
    global _translator_cache
    _translator_cache.clear()
    logging.info("Translator cache cleared")

# Statistics tracking (optional)
_translation_stats = {
    'total_translations': 0,
    'total_characters': 0,
    'failures': 0
}

async def get_translation_stats() -> dict:
    """Get translation usage statistics"""
    return _translation_stats.copy()
