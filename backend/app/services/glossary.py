import asyncio
import json
import time
from functools import lru_cache
from typing import Dict
import logging

GLOSSARY_CACHE = {}
CACHE_TTL = 300  # 5 minutes

async def async_load_glossary(domain: str) -> Dict[str, str]:
    """Load glossary JSON asynchronously with TTL caching"""
    current_time = time.time()
    if (domain in GLOSSARY_CACHE and 
        current_time - GLOSSARY_CACHE[domain]["timestamp"] < CACHE_TTL):
        return GLOSSARY_CACHE[domain]["data"]

    try:
        path = f"data/glossaries/{domain}.json"
        loop = asyncio.get_running_loop()
        with open(path, encoding="utf-8") as f:
            data = await loop.run_in_executor(None, json.load, f)
        GLOSSARY_CACHE[domain] = {"data": data, "timestamp": current_time}
        return data
    except FileNotFoundError:
        logging.warning(f"Glossary not found for domain: {domain}")
        return {}
    except Exception as e:
        logging.error(f"Glossary loading error for domain '{domain}': {e}")
        return {}

def apply_glossary(text: str, glossary: Dict[str, str]) -> str:
    """Apply glossary term replacement"""
    for term, translation in glossary.items():
        text = text.replace(term, translation)
    return text
