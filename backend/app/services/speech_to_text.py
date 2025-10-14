import whisper
import asyncio
import logging
from typing import Optional, Dict
from app.services.google_translator import translate_text_google

# Whisper language codes mapping for Indian languages
WHISPER_INDIAN_LANGUAGES = {
    "hi": "hindi",
    "bn": "bengali",
    "te": "telugu",
    "mr": "marathi",
    "ta": "tamil",
    "ur": "urdu",
    "gu": "gujarati",
    "kn": "kannada",
    "ml": "malayalam",
    "or": "odia",
    "pa": "punjabi",
    "as": "assamese",
    "ne": "nepali",
    "sa": "sanskrit",
    "sd": "sindhi",
    # Note: Whisper doesn't have explicit support for all 22 languages
    # For unsupported languages, it will auto-detect or use closest match
}

# Google Translate language code mapping
GOOGLE_TRANSLATE_CODES = {
    "hi": "hi",      # Hindi
    "bn": "bn",      # Bengali
    "te": "te",      # Telugu
    "mr": "mr",      # Marathi
    "ta": "ta",      # Tamil
    "ur": "ur",      # Urdu
    "gu": "gu",      # Gujarati
    "kn": "kn",      # Kannada
    "ml": "ml",      # Malayalam
    "or": "or",      # Odia
    "pa": "pa",      # Punjabi
    "as": "as",      # Assamese
    "ne": "ne",      # Nepali
    "sa": "sa",      # Sanskrit
    "sd": "sd",      # Sindhi
    "ks": "ks",      # Kashmiri
    "mai": "mai",    # Maithili
    "brx": "brx",    # Bodo
    "doi": "doi",    # Dogri
    "mni": "mni",    # Manipuri
    "sat": "sat",    # Santali
    "kok": "kok",    # Konkani
    "en": "en",      # English
}

# Load Whisper model globally (can be changed to 'small', 'medium', 'large' for better accuracy)
whisper_model = None

def get_whisper_model(model_size: str = "base"):
    """
    Load and cache Whisper model
    Model sizes: tiny, base, small, medium, large
    - tiny/base: Fast, lower accuracy
    - small/medium: Balanced
    - large: Best accuracy, slower
    """
    global whisper_model
    if whisper_model is None:
        logging.info(f"Loading Whisper {model_size} model...")
        whisper_model = whisper.load_model(model_size)
        logging.info("Whisper model loaded successfully")
    return whisper_model

async def transcribe_audio(
    audio_file_path: str,
    source_language: Optional[str] = None,
    model_size: str = "base"
) -> dict:
    """
    Convert speech to text using Whisper with Indian language support
    
    Args:
        audio_file_path: Path to audio file
        source_language: Expected language code (hi, ta, etc.) or None for auto-detect
        model_size: Whisper model size (tiny, base, small, medium, large)
    
    Returns:
        {
            'text': str,              # Transcribed text
            'language': str,          # Detected language code
            'language_name': str,     # Full language name
            'confidence': float,      # Confidence score
            'segments': list          # Time-stamped segments
        }
    """
    try:
        model = get_whisper_model(model_size)
        
        # Map language code to Whisper format
        whisper_lang = None
        if source_language:
            whisper_lang = WHISPER_INDIAN_LANGUAGES.get(source_language.lower())
        
        logging.info(f"Transcribing audio: {audio_file_path} (expected lang: {source_language})")
        
        # Run Whisper transcription
        result = await asyncio.to_thread(
            model.transcribe,
            audio_file_path,
            language=whisper_lang,  # None = auto-detect
            fp16=False,  # Set True if using GPU
            verbose=False,
            task="transcribe"  # 'transcribe' keeps original language, 'translate' converts to English
        )
        
        detected_language = result.get('language', 'unknown')
        transcribed_text = result['text'].strip()
        
        logging.info(f"Transcription complete. Detected language: {detected_language}")
        logging.info(f"Transcribed text: {transcribed_text[:100]}...")
        
        return {
            'text': transcribed_text,
            'language': detected_language,
            'language_name': WHISPER_INDIAN_LANGUAGES.get(detected_language, detected_language),
            'confidence': 0.95,  # Whisper doesn't provide confidence, approximate
            'segments': result.get('segments', [])
        }
    
    except Exception as e:
        logging.error(f"Transcription failed: {e}")
        raise Exception(f"Speech-to-text transcription error: {e}")

async def transcribe_and_translate(
    audio_file_path: str,
    target_language: str,
    source_language: Optional[str] = None,
    model_size: str = "base"
) -> dict:
    """
    Complete pipeline: Speech → Text (same language) → Translated Text (target language)
    
    This is the recommended approach for Indian languages:
    1. Whisper transcribes audio to text in original language
    2. Google Translate converts text to target language
    
    Args:
        audio_file_path: Path to audio file
        target_language: Desired output language code
        source_language: Expected source language (optional, auto-detect if None)
        model_size: Whisper model size
    
    Returns:
        {
            'original_text': str,           # Transcribed text in original language
            'translated_text': str,         # Translated text in target language
            'source_language': str,         # Detected source language
            'target_language': str,         # Target language
            'segments': list                # Time-stamped segments
        }
    """
    try:
        # Step 1: Transcribe audio to text (in original language)
        logging.info("Step 1: Transcribing audio to text...")
        transcription = await transcribe_audio(
            audio_file_path,
            source_language=source_language,
            model_size=model_size
        )
        
        original_text = transcription['text']
        detected_language = transcription['language']
        
        # Check if translation is needed
        if detected_language == target_language:
            logging.info("Source and target languages are the same, skipping translation")
            return {
                'original_text': original_text,
                'translated_text': original_text,
                'source_language': detected_language,
                'target_language': target_language,
                'segments': transcription['segments']
            }
        
        # Step 2: Translate text to target language using Google Translate
        logging.info(f"Step 2: Translating from {detected_language} to {target_language}...")
        
        # Map Whisper language code to Google Translate code
        google_source_lang = detected_language if detected_language in GOOGLE_TRANSLATE_CODES.values() else 'auto'
        google_target_lang = GOOGLE_TRANSLATE_CODES.get(target_language, target_language)
        
        translated_text = await translate_text_google(
            text=original_text,
            target_language=google_target_lang,
            source_language=google_source_lang
        )
        
        logging.info(f"Translation complete: {translated_text[:100]}...")
        
        return {
            'original_text': original_text,
            'translated_text': translated_text,
            'source_language': detected_language,
            'target_language': target_language,
            'segments': transcription['segments']
        }
    
    except Exception as e:
        logging.error(f"Transcribe and translate failed: {e}")
        raise Exception(f"Speech transcription and translation error: {e}")

async def transcribe_with_timestamps(
    audio_file_path: str,
    source_language: Optional[str] = None
) -> list:
    """
    Transcribe audio with detailed word-level or segment-level timestamps
    Useful for subtitle generation and alignment
    
    Returns:
        List of segments with structure:
        [
            {
                'id': int,
                'start': float,    # Start time in seconds
                'end': float,      # End time in seconds
                'text': str,       # Segment text
                'tokens': list,    # Token IDs
                'temperature': float,
                'avg_logprob': float,
                'compression_ratio': float,
                'no_speech_prob': float
            },
            ...
        ]
    """
    try:
        model = get_whisper_model()
        
        whisper_lang = None
        if source_language:
            whisper_lang = WHISPER_INDIAN_LANGUAGES.get(source_language.lower())
        
        logging.info(f"Transcribing with timestamps: {audio_file_path}")
        
        result = await asyncio.to_thread(
            model.transcribe,
            audio_file_path,
            language=whisper_lang,
            word_timestamps=True,  # Enable word-level timestamps
            fp16=False
        )
        
        return result['segments']
    
    except Exception as e:
        logging.error(f"Timestamp transcription failed: {e}")
        raise Exception(f"Timestamp transcription error: {e}")

async def batch_transcribe(
    audio_files: list,
    target_language: Optional[str] = None,
    source_language: Optional[str] = None
) -> list:
    """
    Batch transcribe multiple audio files
    Optionally translate all to target language
    
    Returns list of transcription results
    """
    results = []
    for audio_file in audio_files:
        if target_language:
            result = await transcribe_and_translate(
                audio_file,
                target_language=target_language,
                source_language=source_language
            )
        else:
            result = await transcribe_audio(
                audio_file,
                source_language=source_language
            )
        results.append(result)
    return results

def get_supported_languages() -> Dict[str, str]:
    """Return dictionary of supported Indian languages"""
    return WHISPER_INDIAN_LANGUAGES

