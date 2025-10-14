from app.services.google_translator import translate_text_google, translate_batch
from app.services.glossary import async_load_glossary, apply_glossary
from app.services.adaptations import adapt_region
import re
import asyncio
import logging
from typing import List, Tuple
from pathlib import Path
import uuid

TMP_SUB_DIR = Path("./temp_subtitles")
TMP_SUB_DIR.mkdir(parents=True, exist_ok=True)

async def translate_subtitle_file(request) -> str:
    """
    Translate SRT subtitle file while preserving timing and formatting
    
    Uses deep-translator for high-quality translation
    Applies glossary and regional adaptation
    Supports chunking for large subtitle files
    """
    try:
        # Read original SRT file
        with open(request.subtitle_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        logging.info(f"Parsing SRT file: {request.subtitle_file_path}")

        # Parse SRT format (index, timestamp, text)
        # Allow optional blank lines/whitespace between components and capture multi-line subtitle text
        pattern = r"(\d+)\s*\r?\n\s*(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})\s*\r?\n([\s\S]*?)(?=\r?\n\s*\r?\n|\Z)"
        matches = re.findall(pattern, content, re.MULTILINE)

        if not matches:
            raise ValueError("No valid SRT entries found in file")
        
        logging.info(f"Found {len(matches)} subtitle entries")
        
        # Load glossary
        glossary = await async_load_glossary(request.domain)
        
        # Translate each subtitle entry (use batch translation when available)
        translated_entries = []
        batch_size = 20  # larger batches for batch API

        for i in range(0, len(matches), batch_size):
            batch = matches[i:i + batch_size]

            # Prepare texts for batch translation (apply glossary/adaptations first)
            texts_to_translate = []
            index_timestamp = []
            for index, timestamp, text in batch:
                text_clean = text.strip().replace('\n', ' ')
                text_glossary = apply_glossary(text_clean, glossary)
                text_adapted = adapt_region(text_glossary, request.region)
                texts_to_translate.append(text_adapted)
                index_timestamp.append((index, timestamp))

            # Use batch translator if available
            try:
                translated_texts = await translate_batch(texts_to_translate, request.target_language, request.source_language)
            except Exception:
                # Fallback to individual translations
                translated_texts = []
                for t in texts_to_translate:
                    translated_texts.append(await translate_text_google(t, request.target_language, request.source_language))

            # Reconstruct entries
            for (index, timestamp), translated in zip(index_timestamp, translated_texts):
                translated_entries.append(f"{index}\n{timestamp}\n{translated}\n")

            logging.info(f"Translated batch {i//batch_size + 1}/{(len(matches)-1)//batch_size + 1}")
        
        # Write translated SRT file
        # Write translated SRT file into temp dir with unique name
        unique_name = f"translated_{request.target_language}_{uuid.uuid4().hex}.srt"
        output_path = str(TMP_SUB_DIR / unique_name)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(translated_entries))
        
        logging.info(f"Translated subtitle saved: {output_path}")
        return output_path
    
    except Exception as e:
        logging.error(f"Subtitle translation failed: {e}")
        raise Exception(f"Failed to translate subtitles: {e}")

async def translate_subtitle_with_context(request, context_window: int = 2) -> str:
    """
    Translate subtitles with context awareness
    
    Uses surrounding subtitle lines for better translation context
    Improves accuracy for dialogue and narrative continuity
    """
    try:
        with open(request.subtitle_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Accept both LF and CRLF endings and capture multi-line text
        pattern = r"(\d+)\s*\r?\n\s*(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})\s*\r?\n([\s\S]*?)(?=\r?\n\s*\r?\n|\Z)"
        matches = re.findall(pattern, content, re.MULTILINE)

        glossary = await async_load_glossary(request.domain)
        translated_entries = []
        
        for i, (index, timestamp, text) in enumerate(matches):
            # Build context from surrounding subtitles
            context_before = []
            context_after = []
            
            # Get previous subtitles for context
            for j in range(max(0, i - context_window), i):
                context_before.append(matches[j][2].strip())
            
            # Get following subtitles for context
            for j in range(i + 1, min(len(matches), i + context_window + 1)):
                context_after.append(matches[j][2].strip())
            
            # Combine context
            full_context = " ".join(context_before + [text.strip()] + context_after)
            
            # Apply glossary and adaptation
            text_glossary = apply_glossary(full_context, glossary)
            text_adapted = adapt_region(text_glossary, request.region)
            
            # Translate with context
            translated = await translate_text_google(
                text_adapted,
                request.target_language,
                request.source_language
            )
            
            # Extract just the current subtitle from translated context
            # (This is a simplified approach; production would use more sophisticated extraction)
            translated_parts = translated.split()
            current_translation = " ".join(translated_parts[len(" ".join(context_before).split()):
                                                          len(" ".join(context_before).split()) + len(text.strip().split())])
            
            translated_entries.append(f"{index}\n{timestamp}\n{current_translation}\n")
        
        unique_name = f"translated_context_{request.target_language}_{uuid.uuid4().hex}.srt"
        output_path = str(TMP_SUB_DIR / unique_name)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(translated_entries))
        
        return output_path
    
    except Exception as e:
        logging.error(f"Context-aware subtitle translation failed: {e}")
        raise

def parse_srt(content: str) -> List[Tuple[str, str, str]]:
    """
    Parse SRT content into structured format
    
    Returns:
        List of tuples (index, timestamp, text)
    """
    # Accept both LF and CRLF endings and capture multi-line text
    pattern = r"(\d+)\s*\r?\n\s*(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})\s*\r?\n([\s\S]*?)(?=\r?\n\s*\r?\n|\Z)"
    matches = re.findall(pattern, content, re.MULTILINE)
    return matches

def format_srt_entry(index: str, timestamp: str, text: str) -> str:
    """Format a single SRT entry"""
    return f"{index}\n{timestamp}\n{text}\n"

async def merge_subtitle_files(file_paths: List[str], output_path: str) -> str:
    """
    Merge multiple subtitle files into one
    Useful for combining different language tracks
    """
    try:
        all_entries = []
        
        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                entries = parse_srt(content)
                all_entries.extend(entries)
        
        # Sort by index
        all_entries.sort(key=lambda x: int(x[0]))
        
        # Write merged file
        with open(output_path, 'w', encoding='utf-8') as f:
            for index, timestamp, text in all_entries:
                f.write(format_srt_entry(index, timestamp, text))
                f.write("\n")
        
        return output_path
    
    except Exception as e:
        logging.error(f"Subtitle merge failed: {e}")
        raise
