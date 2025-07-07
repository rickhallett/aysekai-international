"""Content processing utilities for Asma al-Husna data"""
import re
from typing import Optional
from .constants import TAWIL_PATTERNS, TAWIL_LEVELS


def clean_multiline_content(content: Optional[str], preserve_structure: bool = True) -> str:
    """
    Clean and format multiline content.
    
    Args:
        content: The content to clean
        preserve_structure: Whether to preserve pipe separators
        
    Returns:
        Cleaned content string
    """
    if not content:
        return ''
    
    # Remove duplicate quotes
    cleaned = content.replace('""', '"')
    
    # Clean whitespace
    if preserve_structure and '|' in content:
        # Handle pipe-separated content specially
        parts = cleaned.split('|')
        parts = [' '.join(part.split()) for part in parts]
        result = ' | '.join(parts)
    else:
        # Standard whitespace cleaning - collapse all whitespace to single spaces
        # and replace pipes with spaces if preserve_structure is False
        if not preserve_structure:
            cleaned = cleaned.replace('|', ' ')
        result = ' '.join(cleaned.split())
    
    return result.strip()


def process_tawil_sections(content: str) -> str:
    """
    Process Ta'wil content with proper emoji sections.
    
    Args:
        content: Raw Ta'wil content
        
    Returns:
        Formatted Ta'wil content with proper sections
    """
    if not content:
        return ''
    
    # Extract sections using patterns
    sections = {}
    
    for pattern, label in TAWIL_PATTERNS:
        match = re.search(pattern, content, re.DOTALL | re.UNICODE)
        if match:
            section_content = match.group(0)
            # Clean the section content
            section_content = ' '.join(section_content.split())
            sections[label] = section_content
    
    # Build result in standard order
    result_parts = []
    ordered_labels = ['📿 SHARĪ\'A', '🚶 ṬARĪQA', '💎 ḤAQĪQA', '🌟 MA\'RIFA']
    
    for label in ordered_labels:
        if label in sections:
            result_parts.append(sections[label])
    
    return '\n'.join(result_parts)


def format_dhikr_content(content: str) -> str:
    """
    Format Dhikr formulas for display.
    
    Args:
        content: Raw Dhikr formula content
        
    Returns:
        Formatted Dhikr content
    """
    if not content:
        return ''
    
    # Handle pipe-separated formulas
    if '|' in content:
        formulas = content.split('|')
        formulas = [' '.join(f.strip().split()) for f in formulas]
        return '\n'.join(formulas)
    
    # Clean single formula
    return ' '.join(content.strip().split())


def normalize_arabic_text(text: str) -> str:
    """
    Normalize Arabic text for consistent display.
    
    Args:
        text: Text containing Arabic
        
    Returns:
        Normalized text
    """
    if not text:
        return ''
    
    # Basic normalization - remove extra spaces
    normalized = ' '.join(text.split())
    
    # Could add more Arabic-specific normalization here
    # For now, just return cleaned text
    return normalized


def remove_empty_lines(text: str) -> str:
    """
    Remove empty lines from text.
    
    Args:
        text: Text with potential empty lines
        
    Returns:
        Text without empty lines
    """
    if not text:
        return ''
    
    lines = text.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)


def clean_quotes(text: str) -> str:
    """
    Convert smart quotes to regular quotes.
    
    Args:
        text: Text with potential smart quotes
        
    Returns:
        Text with regular quotes
    """
    if not text:
        return ''
    
    # Replace smart quotes with regular quotes
    replacements = {
        '\u201C': '"',  # Left double quotation mark
        '\u201D': '"',  # Right double quotation mark
        '\u2018': "'",  # Left single quotation mark
        '\u2019': "'",  # Right single quotation mark
        '"': '"',       # Another left double quote variant
        '"': '"',       # Another right double quote variant
        ''': "'",       # Another left single quote variant
        ''': "'",       # Another right single quote variant
    }
    
    result = text
    for smart, regular in replacements.items():
        result = result.replace(smart, regular)
    
    return result