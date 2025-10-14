import ffmpeg
import asyncio
import logging
import subprocess
import json
import os
import uuid
from typing import List, Optional
from pathlib import Path

# Directory to store temporary uploads/extracted subtitles
TMP_SUB_DIR = Path("./temp_subtitles")
TMP_SUB_DIR.mkdir(parents=True, exist_ok=True)

async def extract_subtitles(request) -> dict:
    """
    Extract embedded subtitles from video using FFmpeg
    
    Supports multiple subtitle tracks and formats (SRT, ASS, VTT)
    """
    try:
        # generate unique output file in temp dir
        unique_name = f"extracted_{uuid.uuid4().hex}_{request.subtitle_index}.srt"
        output_path = str(TMP_SUB_DIR / unique_name)

        logging.info(f"Extracting subtitle track {request.subtitle_index} from {request.video_file_path} -> {output_path}")

        # Use FFmpeg to extract subtitle stream. Map format: 0:s:{index}
        def _run_extract():
            (ffmpeg
                .input(request.video_file_path)
                .output(output_path, map=f"0:s:{request.subtitle_index}")
                .overwrite_output()
                .run(quiet=True, capture_stdout=True, capture_stderr=True)
            )

        await asyncio.to_thread(_run_extract)

        logging.info(f"Subtitle extracted successfully: {output_path}")

        return {
            'subtitle_file_path': output_path,
            'subtitle_format': 'srt'
        }
    except ffmpeg.Error as e:
        error_message = e.stderr.decode() if e.stderr else str(e)
        logging.error(f"FFmpeg subtitle extraction failed: {error_message}")
        raise Exception(f"Failed to extract subtitles: {error_message}")
    except Exception as e:
        logging.error(f"Subtitle extraction failed: {e}")
        raise Exception(f"Subtitle extraction error: {e}")

async def list_subtitle_streams(video_path: str) -> List[dict]:
    """
    List all available subtitle streams in a video file
    
    Returns:
        List of subtitle stream information including:
        - index: Stream index
        - language: Language code (if available)
        - codec: Subtitle codec (srt, ass, etc.)
        - title: Stream title (if available)
    """
    try:
        logging.info(f"Probing subtitle streams in: {video_path}")
        
        # Use ffprobe to get stream information
        probe = await asyncio.to_thread(lambda: ffmpeg.probe(video_path))
        
        subtitle_streams = []
        for stream in probe.get('streams', []):
            if stream.get('codec_type') == 'subtitle':
                subtitle_info = {
                    'index': stream.get('index'),
                    'codec': stream.get('codec_name'),
                    'language': stream.get('tags', {}).get('language', 'unknown'),
                    'title': stream.get('tags', {}).get('title', 'Untitled')
                }
                subtitle_streams.append(subtitle_info)
        
        logging.info(f"Found {len(subtitle_streams)} subtitle streams")
        return subtitle_streams
    
    except Exception as e:
        logging.error(f"Failed to probe subtitle streams: {e}")
        raise Exception(f"Subtitle stream detection error: {e}")

async def extract_all_subtitles(video_path: str) -> List[dict]:
    """
    Extract all available subtitle streams from video
    
    Returns list of extracted subtitle files with metadata
    """
    try:
        streams = await list_subtitle_streams(video_path)
        extracted_files = []
        
        for stream in streams:
            unique_name = f"extracted_{uuid.uuid4().hex}_{stream['index']}_{stream['language']}.srt"
            output_path = str(TMP_SUB_DIR / unique_name)

            def _run_extract_stream(idx=stream['index']):
                (ffmpeg
                    .input(video_path)
                    .output(output_path, map=f"0:s:{idx}")
                    .overwrite_output()
                    .run(quiet=True)
                )

            await asyncio.to_thread(_run_extract_stream)

            extracted_files.append({
                'file_path': output_path,
                'language': stream['language'],
                'codec': stream['codec'],
                'stream_index': stream['index']
            })
        
        return extracted_files
    
    except Exception as e:
        logging.error(f"Failed to extract all subtitles: {e}")
        raise

async def extract_hardcoded_subtitles(video_path: str, output_path: str = "extracted_hardcoded.srt") -> str:
    """
    Extract hardcoded (burned-in) subtitles using OCR
    Note: This is computationally expensive and requires tesseract-ocr
    
    For prototype, this is a placeholder - full implementation would use videocr or similar
    """
    try:
        logging.warning("Hardcoded subtitle extraction requires OCR - not fully implemented in prototype")
        raise NotImplementedError("Hardcoded subtitle extraction requires additional dependencies (videocr, tesseract)")
    except Exception as e:
        logging.error(f"Hardcoded subtitle extraction failed: {e}")
        raise

async def convert_subtitle_format(input_path: str, output_format: str = "srt") -> str:
    """
    Convert subtitle format (e.g., ASS to SRT, VTT to SRT)
    
    Args:
        input_path: Path to input subtitle file
        output_format: Desired output format (srt, vtt, ass)
    
    Returns:
        Path to converted subtitle file
    """
    try:
        output_path = input_path.rsplit('.', 1)[0] + f'.{output_format}'
        
        logging.info(f"Converting subtitle format to {output_format}")
        
        await asyncio.to_thread(
            lambda: (
                ffmpeg
                .input(input_path)
                .output(output_path, format=output_format)
                .overwrite_output()
                .run(quiet=True)
            )
        )
        
        return output_path
    
    except Exception as e:
        logging.error(f"Subtitle format conversion failed: {e}")
        raise Exception(f"Format conversion error: {e}")
