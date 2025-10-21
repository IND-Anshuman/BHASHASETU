from pydantic import BaseModel, Field, validator
from typing import List, Optional
from app.config import settings

class BaseResponse(BaseModel):
    success: bool = True
    message: Optional[str] = None

# Translation Models
class TranslateRequest(BaseModel):
    text: str
    source_language: str
    target_language: str
    domain: str = "general"
    region: str = "default"

    @validator('source_language', 'target_language')
    def validate_lang(cls, v):
        if v not in settings.SUPPORTED_LANGUAGES and v != 'auto':
            raise ValueError(f"Unsupported language: {v}")
        return v

class TranslationResult(BaseModel):
    original: str
    translated: str
    glossary_applied: bool
    confidence_score: float = Field(default=0.9, ge=0, le=1)

# TTS Models
class TTSRequest(BaseModel):
    text: str
    language: str
    voice_type: str = Field("female", pattern="^(male|female)$")
    
    @validator('language')
    def valid_language(cls, v):
        if v not in settings.SUPPORTED_LANGUAGES:
            raise ValueError(f"Language {v} not supported")
        return v

class TTSResult(BaseModel):
    audio_file_path: str
    language: str
    voice_type: str

# Speech Models
class AudioTranscriptionRequest(BaseModel):
    audio_file_path: str
    source_language: Optional[str] = None

class AudioTranscriptionResult(BaseModel):
    text: str
    language: str

class SpeechToSpeechRequest(BaseModel):
    audio_file_path: str
    target_language: str
    source_language: Optional[str] = None
    voice_type: str = Field("female", pattern="^(male|female)$")
    domain: str = "general"
    region: str = "default"

class SpeechToSpeechResult(BaseModel):
    original_audio: str
    transcribed_text: str
    detected_language: str
    translated_text: str
    target_language: str
    output_audio: str
    voice_type: str
    glossary_applied: bool
    region_adapted: bool

# Document Models
class DocumentTranslateRequest(BaseModel):
    file_path: str
    target_language: str
    source_language: str = 'auto'
    domain: str = 'general'
    region: str = 'default'
    file_type: Optional[str] = None

class DocumentTranslateResult(BaseModel):
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    file_type: str
    glossary_applied: bool
    region_adapted: bool
    output_path: Optional[str] = None

# Subtitle Models
class SubtitleExtractRequest(BaseModel):
    video_file_path: str
    subtitle_index: int = 0

class SubtitleExtractResult(BaseModel):
    subtitle_file_path: str
    subtitle_format: str

class SubtitleTranslateRequest(BaseModel):
    subtitle_file_path: str
    source_language: str
    target_language: str
    domain: str = "general"
    region: str = "default"

class SubtitleTranslateResult(BaseModel):
    translated_subtitle_path: str
    language: str

# Feedback Models
class FeedbackRequest(BaseModel):
    translation_id: int
    # Rating scale: 0 (worst) to 5 (best)
    rating: int = Field(..., ge=0, le=5)
    user_edit: Optional[str] = None

# Dashboard Models
class DashboardMetrics(BaseModel):
    total_translations: int
    languages_served: List[str]
    average_confidence: float
    feedback_positive_rate: float
    tts_requests: int = 0
    subtitle_translations: int = 0
