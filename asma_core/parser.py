"""Name parsing and extraction utilities"""
import re
from typing import Optional, Tuple, Dict
from .constants import EXISTING_NOTION_NAMES


def parse_name_with_arabic(text: Optional[str]) -> Tuple[str, str]:
    """
    Parse a name to extract transliteration and Arabic parts.
    
    Args:
        text: Text containing name with possible Arabic
        
    Returns:
        Tuple of (transliteration, arabic)
    """
    if not text:
        return "", ""
    
    text = text.strip()
    
    # Check for parentheses format: "Al-Rahman (الرحمن)"
    match = re.match(r'^([^(]+)\s*\(([^)]+)\)', text)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    
    # Check for Arabic characters without parentheses
    arabic_chars = re.findall(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+', text)
    if arabic_chars:
        arabic_text = ' '.join(arabic_chars)
        # Remove Arabic from text to get transliteration
        transliteration = re.sub(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+', '', text).strip()
        return transliteration, arabic_text
    
    # No Arabic found, assume it's all transliteration
    return text, ""


def extract_name_number(text: Optional[str]) -> Optional[int]:
    """
    Extract name number from text.
    
    Args:
        text: Text possibly containing a number
        
    Returns:
        The first number found, or None
    """
    if not text:
        return None
    
    # Look for numbers in various formats
    # 1. At start with period: "1. Name"
    # 2. In parentheses: "(42) Name"
    # 3. Anywhere as digits: "Name 99"
    
    # Try to find first number in the text
    numbers = re.findall(r'\d+', text)
    if numbers:
        return int(numbers[0])
    
    return None


def is_existing_name(name: Optional[str]) -> bool:
    """
    Check if a name is in the existing Notion names set.
    
    Args:
        name: Name to check
        
    Returns:
        True if name exists in Notion set
    """
    if not name:
        return False
    
    name_lower = name.lower()
    
    # Check exact match or partial match
    for existing in EXISTING_NOTION_NAMES:
        existing_lower = existing.lower()
        # Check if input is contained in existing name or vice versa
        if name_lower in existing_lower or existing_lower in name_lower:
            return True
        
        # Also check just the transliteration part
        transliteration, _ = parse_name_with_arabic(existing)
        if transliteration and name_lower in transliteration.lower():
            return True
        
        # Check Arabic part
        _, arabic = parse_name_with_arabic(existing)
        if arabic and arabic in name:
            return True
    
    return False


def parse_quranic_reference(text: Optional[str]) -> Dict[str, any]:
    """
    Parse Quranic reference to extract surah and verse information.
    
    Args:
        text: Text containing Quranic reference
        
    Returns:
        Dictionary with parsed information
    """
    if not text:
        return {}
    
    result = {}
    
    # Pattern for references like "Surah Al-Baqarah (2:255)" or "(2:255-257)"
    # Match surah name (optional), number:verse or number:verse-verse
    pattern = r'(?:(?:Surah|سورة)\s+([^(]+)\s*)?\((\d+):(\d+)(?:-(\d+))?\)'
    
    match = re.search(pattern, text)
    if match:
        if match.group(1):
            result['surah'] = match.group(1).strip()
        
        result['surah_number'] = int(match.group(2))
        
        if match.group(4):
            # Range of verses
            result['verse_start'] = int(match.group(3))
            result['verse_end'] = int(match.group(4))
        else:
            # Single verse
            result['verse'] = int(match.group(3))
    
    return result


def extract_name_from_line(line: Optional[str]) -> Tuple[str, Optional[int]]:
    """
    Extract divine name and number from a line of text.
    
    Args:
        line: Line containing a divine name
        
    Returns:
        Tuple of (name with Arabic, number or None)
    """
    if not line:
        return "", None
    
    line = line.strip()
    
    # Extract number first
    number = extract_name_number(line)
    
    # Common patterns:
    # "1. Al-Rahman (الرحمن) - The Compassionate"
    # "99 | Al-Sabur (الصبور) | The Patient One"
    # "Al-Rahman (الرحمن) - The Compassionate"
    
    # Remove number prefix if found
    if number:
        # Remove patterns like "1. " or "99 | " from the start
        line = re.sub(r'^\d+\.?\s*\|?\s*', '', line)
    
    # Look for name with Arabic in parentheses pattern first
    # This handles "Al-Rahman (الرحمن)" even if followed by " - description"
    match = re.search(r'([A-Za-z\-]+\s*\([^)]+\))', line)
    if match:
        return match.group(1).strip(), number
    
    # If no parentheses, extract up to common delimiters (but not hyphens in names)
    # Look for " - " or " | " as delimiters
    match = re.match(r'^([^|]+?)(?:\s*\|\s*|\s+-\s+|$)', line)
    if match:
        name = match.group(1).strip()
        return name, number
    
    return line, number