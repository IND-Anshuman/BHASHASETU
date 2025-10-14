"""Routes package - imports all route modules so callers can do `from app.routes import ...`"""
from . import translate
from . import tts
from . import speech
from . import document
from . import subtitle
from . import feedback
from . import dashboard

__all__ = [
    'translate', 'tts', 'speech', 'document', 'subtitle', 'feedback', 'dashboard'
]
