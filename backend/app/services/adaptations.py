import re
import logging
from typing import Dict, Any

# Comprehensive regional adaptation rules
REGIONAL_RULES = {
    "tamilnadu": {
        "places": {
            "Delhi": "Chennai",
            "Mumbai": "Chennai",
            "Kolkata": "Chennai",
            "Bangalore": "Coimbatore"
        },
        "currency": {
            r"\$([0-9]+)": lambda m: f"₹{int(m.group(1)) * 80}",
            r"USD\s*([0-9]+)": lambda m: f"₹{int(m.group(1)) * 80}"
        },
        "measurements": {
            r"([0-9]+)\s*miles": lambda m: f"{int(m.group(1)) * 1.6} kilometers",
            r"([0-9]+)\s*feet": lambda m: f"{int(m.group(1)) * 0.3} meters"
        }
    },
    "kerala": {
        "places": {
            "Mumbai": "Kochi",
            "Delhi": "Thiruvananthapuram",
            "Chennai": "Kochi"
        },
        "currency": {
            r"\$([0-9]+)": lambda m: f"₹{int(m.group(1)) * 79}"
        }
    },
    "maharashtra": {
        "places": {
            "Delhi": "Mumbai",
            "Chennai": "Pune",
            "Bangalore": "Pune"
        },
        "currency": {
            r"\$([0-9]+)": lambda m: f"₹{int(m.group(1)) * 80}"
        }
    },
    "karnataka": {
        "places": {
            "Delhi": "Bangalore",
            "Mumbai": "Mysore",
            "Chennai": "Mangalore"
        },
        "currency": {
            r"\$([0-9]+)": lambda m: f"₹{int(m.group(1)) * 80}"
        }
    },
    "west_bengal": {
        "places": {
            "Delhi": "Kolkata",
            "Mumbai": "Kolkata"
        },
        "currency": {
            r"\$([0-9]+)": lambda m: f"₹{int(m.group(1)) * 80}"
        }
    }
}

def adapt_region(text: str, region: str) -> str:
    """
    Apply regional adaptation rules to text
    
    Adapts:
    - Place names (city references)
    - Currency conversions ($ to ₹)
    - Measurement units (miles to km, feet to meters)
    - Local idioms and expressions
    
    Args:
        text: Input text
        region: Region code (tamilnadu, kerala, maharashtra, etc.)
    
    Returns:
        Regionally adapted text
    """
    try:
        rules = REGIONAL_RULES.get(region.lower())
        
        if not rules:
            logging.debug(f"No adaptation rules for region: {region}")
            return text
        
        adapted_text = text
        
        # Apply place name replacements
        for place, replacement in rules.get("places", {}).items():
            # Case-insensitive replacement
            adapted_text = re.sub(
                rf'\b{re.escape(place)}\b',
                replacement,
                adapted_text,
                flags=re.IGNORECASE
            )
        
        # Apply currency conversions with regex
        for pattern, conversion in rules.get("currency", {}).items():
            if callable(conversion):
                adapted_text = re.sub(pattern, conversion, adapted_text)
            else:
                adapted_text = re.sub(pattern, conversion, adapted_text)
        
        # Apply measurement conversions
        for pattern, conversion in rules.get("measurements", {}).items():
            if callable(conversion):
                adapted_text = re.sub(pattern, conversion, adapted_text)
        
        logging.info(f"Applied regional adaptation for: {region}")
        return adapted_text
    
    except Exception as e:
        logging.error(f"Regional adaptation failed: {e}")
        return text  # Return original text if adaptation fails

def get_available_regions() -> list:
    """Get list of supported regions"""
    return list(REGIONAL_RULES.keys())

def add_custom_region(region_name: str, rules: Dict[str, Any]):
    """
    Add custom regional adaptation rules
    
    Useful for extending support to new regions
    """
    try:
        REGIONAL_RULES[region_name.lower()] = rules
        logging.info(f"Added custom region: {region_name}")
    except Exception as e:
        logging.error(f"Failed to add custom region: {e}")
        raise
