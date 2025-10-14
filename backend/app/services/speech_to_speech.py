from app.services.speech_to_text import transcribe_and_translate
from app.services.tts import text_to_speech
from app.services.glossary import async_load_glossary, apply_glossary
from app.services.adaptations import adapt_region
from app.models import TTSRequest
import logging

async def translate_speech_to_speech(
    input_audio_path: str,
    target_language: str,
    source_language: str = None,
    voice_type: str = "female",
    domain: str = "general",
    region: str = "default"
) -> dict:
    """
    Complete Speech-to-Speech Translation Pipeline with proper language handling
    
    Steps:
    1. Whisper transcribes audio to text in original language (auto-detect or specified)
    2. Apply domain glossary to transcribed text
    3. Apply regional adaptation
    4. Google Translate converts to target language
    5. Indic Parler TTS generates speech in target language
    """
    try:
        # Step 1: Transcribe and translate text
        logging.info("Step 1: Transcribing and translating audio...")
        result = await transcribe_and_translate(
            audio_file_path=input_audio_path,
            target_language=target_language,
            source_language=source_language
        )
        
        original_text = result['original_text']
        translated_text = result['translated_text']
        detected_language = result['source_language']
        
        # Step 2: Apply glossary to translated text
        logging.info("Step 2: Applying domain glossary...")
        glossary = await async_load_glossary(domain)
        text_with_glossary = apply_glossary(translated_text, glossary)
        
        # Step 3: Apply regional adaptation
        logging.info("Step 3: Applying regional adaptation...")
        text_adapted = adapt_region(text_with_glossary, region)
        
        # Step 4: Generate speech in target language
        logging.info(f"Step 4: Generating speech in {target_language}...")
        tts_request = TTSRequest(
            text=text_adapted,
            language=target_language,
            voice_type=voice_type
        )
        output_audio_path = await text_to_speech(tts_request)
        
        logging.info(f"Speech-to-speech translation complete")
        
        return {
            'original_audio': input_audio_path,
            'transcribed_text': original_text,
            'detected_language': detected_language,
            'translated_text': text_adapted,
            'target_language': target_language,
            'output_audio': output_audio_path,
            'voice_type': voice_type,
            'glossary_applied': bool(glossary),
            'region_adapted': region != 'default'
        }
    
    except Exception as e:
        logging.error(f"Speech-to-speech translation failed: {e}")
        raise Exception(f"Speech-to-speech translation error: {e}")
