import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf
import asyncio
import logging
from typing import Optional

# Language codes supported by Indic Parler TTS (21 languages)
SUPPORTED_LANGUAGES = {
    "as": "Assamese",
    "bn": "Bengali",
    "brx": "Bodo",
    "doi": "Dogri",
    "en": "English",
    "gu": "Gujarati",
    "hi": "Hindi",
    "kn": "Kannada",
    "kok": "Konkani",
    "mai": "Maithili",
    "ml": "Malayalam",
    "mni": "Manipuri",
    "mr": "Marathi",
    "ne": "Nepali",
    "or": "Odia",
    "sa": "Sanskrit",
    "sat": "Santali",
    "sd": "Sindhi",
    "ta": "Tamil",
    "te": "Telugu",
    "ur": "Urdu"
}

# Pre-defined speaker names for consistent voice generation
MALE_SPEAKERS = {
    "hi": ["Rohit", "Karan", "Aditya", "Arjun"],
    "ta": ["Kumar", "Raja", "Selvan"],
    "te": ["Ravi", "Krishna", "Prakash"],
    "bn": ["Amit", "Rajesh", "Subhas"],
    "mr": ["Suresh", "Ganesh", "Prakash"],
    "gu": ["Dhruv", "Kishan", "Mohan"],
    "kn": ["Sunil", "Karthik", "Vivek"],
    "ml": ["Anand", "Arun", "Gopal"],
    "pa": ["Harpreet", "Jaspal", "Mandeep"],
    "or": ["Biswajit", "Debashish", "Santosh"],
    "as": ["Bhaskar", "Jatin", "Ranjit"],
    "ur": ["Hamid", "Karim", "Zahir"],
    "default": ["Rohit", "Karan"]  # Default male voices
}

FEMALE_SPEAKERS = {
    "hi": ["Divya", "Priya", "Anjali", "Kavya"],
    "ta": ["Lakshmi", "Meena", "Kamala"],
    "te": ["Lakshmi", "Sailaja", "Madhavi"],
    "bn": ["Riya", "Ananya", "Diya"],
    "mr": ["Aarti", "Sneha", "Varsha"],
    "gu": ["Diya", "Khushi", "Riya"],
    "kn": ["Shreya", "Pooja", "Nandini"],
    "ml": ["Sreelakshmi", "Nisha", "Meera"],
    "pa": ["Simran", "Jasleen", "Harleen"],
    "or": ["Sujata", "Priyanka", "Swati"],
    "as": ["Jyoti", "Puja", "Ritu"],
    "ur": ["Ayesha", "Fatima", "Zainab"],
    "default": ["Divya", "Priya"]  # Default female voices
}

# Voice description templates for male and female
VOICE_DESCRIPTIONS = {
    "male": {
        "default": "{speaker}'s voice is clear and slightly expressive with a moderate speed and pitch. The recording is of very high quality, with the speaker's voice sounding close up.",
        "formal": "{speaker} speaks in a formal, clear manner with a moderate pace. The voice is deep and authoritative with minimal background noise.",
        "casual": "{speaker} delivers a casual, friendly speech with natural expressivity and a comfortable pace.",
        "energetic": "{speaker}'s voice is energetic and animated, speaking at a slightly faster pace with high expressivity."
    },
    "female": {
        "default": "{speaker}'s voice is clear and slightly expressive with a moderate speed and pitch. The recording is of very high quality, with the speaker's voice sounding close up.",
        "formal": "{speaker} speaks in a formal, clear manner with a moderate pace. The voice is professional and articulate with minimal background noise.",
        "casual": "{speaker} delivers a casual, friendly speech with natural expressivity and a comfortable pace.",
        "energetic": "{speaker}'s voice is energetic and animated, speaking at a slightly faster pace with high expressivity."
    }
}

# Global model cache
_model_cache = None
_tokenizer_cache = None
_description_tokenizer_cache = None

def get_indic_parler_model():
    """Load and cache Indic Parler TTS model"""
    global _model_cache, _tokenizer_cache, _description_tokenizer_cache
    
    if _model_cache is None:
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        logging.info(f"Loading Indic Parler TTS model on {device}...")
        
        _model_cache = ParlerTTSForConditionalGeneration.from_pretrained(
            "ai4bharat/indic-parler-tts"
        ).to(device)
        
        _tokenizer_cache = AutoTokenizer.from_pretrained("ai4bharat/indic-parler-tts")
        _description_tokenizer_cache = AutoTokenizer.from_pretrained(
            _model_cache.config.text_encoder._name_or_path
        )
        
        logging.info("Indic Parler TTS model loaded successfully")
    
    return _model_cache, _tokenizer_cache, _description_tokenizer_cache

async def text_to_speech(
    request,
    style: str = "default",
    speaker_name: Optional[str] = None
) -> str:
    """
    Generate speech using Indic Parler TTS
    
    Args:
        request: TTSRequest containing text, language, voice_type
        style: Voice style (default, formal, casual, energetic)
        speaker_name: Specific speaker name (optional)
    
    Returns:
        Path to generated audio file
    """
    try:
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        model, tokenizer, description_tokenizer = get_indic_parler_model()
        
        # Validate language
        if request.language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {request.language}. Supported: {list(SUPPORTED_LANGUAGES.keys())}")
        
        # Select speaker based on voice type
        if speaker_name is None:
            if request.voice_type == "male":
                speakers = MALE_SPEAKERS.get(request.language, MALE_SPEAKERS["default"])
            else:
                speakers = FEMALE_SPEAKERS.get(request.language, FEMALE_SPEAKERS["default"])
            speaker_name = speakers[0]  # Use first speaker as default
        
        # Get voice description template
        voice_template = VOICE_DESCRIPTIONS.get(request.voice_type, VOICE_DESCRIPTIONS["female"])
        description = voice_template.get(style, voice_template["default"]).format(speaker=speaker_name)
        
        logging.info(f"Generating TTS: Language={request.language}, Voice={request.voice_type}, Speaker={speaker_name}")
        
        # Tokenize inputs
        description_input_ids = await asyncio.to_thread(
            lambda: description_tokenizer(description, return_tensors="pt").to(device)
        )
        prompt_input_ids = await asyncio.to_thread(
            lambda: tokenizer(request.text, return_tensors="pt").to(device)
        )
        
        # Generate audio
        generation = await asyncio.to_thread(
            lambda: model.generate(
                input_ids=description_input_ids.input_ids,
                attention_mask=description_input_ids.attention_mask,
                prompt_input_ids=prompt_input_ids.input_ids,
                prompt_attention_mask=prompt_input_ids.attention_mask
            )
        )
        
        # Convert to audio array
        audio_arr = generation.cpu().numpy().squeeze()
        
        # Save audio file
        output_path = f"output_tts_{request.language}_{request.voice_type}_{speaker_name}.wav"
        await asyncio.to_thread(
            lambda: sf.write(output_path, audio_arr, model.config.sampling_rate)
        )
        
        logging.info(f"TTS audio generated: {output_path}")
        return output_path
    
    except Exception as e:
        logging.error(f"TTS generation failed: {e}")
        raise Exception(f"TTS generation error: {e}")

async def text_to_speech_with_emotion(
    text: str,
    language: str,
    voice_type: str = "female",
    emotion: str = "neutral",
    speaker_name: Optional[str] = None
) -> str:
    """
    Generate speech with specific emotion
    
    Supported emotions: Command, Anger, Narration, Conversation, Disgust, 
                       Fear, Happy, Neutral, Sad, Surprise
    
    Emotion support varies by language. Best support for:
    Assamese, Bengali, Bodo, Dogri, Kannada, Malayalam, Marathi, 
    Sanskrit, Nepali, Tamil
    """
    try:
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        model, tokenizer, description_tokenizer = get_indic_parler_model()
        
        # Select speaker
        if speaker_name is None:
            if voice_type == "male":
                speakers = MALE_SPEAKERS.get(language, MALE_SPEAKERS["default"])
            else:
                speakers = FEMALE_SPEAKERS.get(language, FEMALE_SPEAKERS["default"])
            speaker_name = speakers[0]
        
        # Emotion-aware description
        emotion_descriptions = {
            "happy": f"{speaker_name} speaks with a happy and cheerful tone, with clear expressivity and moderate pace.",
            "sad": f"{speaker_name}'s voice conveys sadness with a slower pace and subdued tone.",
            "angry": f"{speaker_name} speaks with an angry tone, slightly faster with increased intensity.",
            "neutral": f"{speaker_name} delivers speech in a neutral, balanced tone with moderate pace.",
            "narration": f"{speaker_name} narrates in a storytelling manner with clear articulation and engaging tone.",
            "conversation": f"{speaker_name} speaks conversationally with natural flow and friendly tone.",
            "command": f"{speaker_name} gives commands in an authoritative, clear voice with firm tone."
        }
        
        description = emotion_descriptions.get(emotion.lower(), emotion_descriptions["neutral"])
        
        logging.info(f"Generating emotional TTS: Language={language}, Emotion={emotion}, Speaker={speaker_name}")
        
        # Tokenize
        description_input_ids = await asyncio.to_thread(
            lambda: description_tokenizer(description, return_tensors="pt").to(device)
        )
        prompt_input_ids = await asyncio.to_thread(
            lambda: tokenizer(text, return_tensors="pt").to(device)
        )
        
        # Generate
        generation = await asyncio.to_thread(
            lambda: model.generate(
                input_ids=description_input_ids.input_ids,
                attention_mask=description_input_ids.attention_mask,
                prompt_input_ids=prompt_input_ids.input_ids,
                prompt_attention_mask=prompt_input_ids.attention_mask
            )
        )
        
        audio_arr = generation.cpu().numpy().squeeze()
        output_path = f"output_tts_{language}_{voice_type}_{emotion}_{speaker_name}.wav"
        await asyncio.to_thread(
            lambda: sf.write(output_path, audio_arr, model.config.sampling_rate)
        )
        
        return output_path
    
    except Exception as e:
        logging.error(f"Emotional TTS failed: {e}")
        raise

def get_available_speakers(language: str, voice_type: str) -> list:
    """Get list of available speakers for a language and voice type"""
    if voice_type == "male":
        return MALE_SPEAKERS.get(language, MALE_SPEAKERS["default"])
    else:
        return FEMALE_SPEAKERS.get(language, FEMALE_SPEAKERS["default"])

def get_supported_languages() -> dict:
    """Return dictionary of supported languages"""
    return SUPPORTED_LANGUAGES
