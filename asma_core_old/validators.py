"""Data validation functions for Asma al-Husna"""

from typing import List, Dict, Any
from .constants import TOTAL_NAMES, CSV_COLUMN_COUNT, COLUMN_HEADERS


def validate_name_number(number: Any) -> bool:
    """
    Validate that a name number is within valid range.

    Args:
        number: Number to validate

    Returns:
        True if valid (1-99)
    """
    try:
        num = int(number)
        return 1 <= num <= TOTAL_NAMES
    except (ValueError, TypeError):
        return False


def validate_row_length(row: List[str]) -> bool:
    """
    Validate that a CSV row has the correct number of columns.

    Args:
        row: CSV row to validate

    Returns:
        True if correct length
    """
    return len(row) == CSV_COLUMN_COUNT


def validate_name_data(data: Dict[str, str]) -> List[str]:
    """
    Validate a complete name data dictionary.

    Args:
        data: Dictionary with name data

    Returns:
        List of validation errors (empty if valid)
    """
    errors = []

    # Check required fields
    if not data.get("name"):
        errors.append("Missing required field: name")

    if not data.get("number"):
        errors.append("Missing required field: number")
    elif not validate_name_number(data["number"]):
        errors.append(f"Invalid number: {data['number']} (must be 1-99)")

    if not data.get("meaning"):
        errors.append("Missing required field: meaning")

    # Check for suspicious content
    if data.get("tawil"):
        tawil = data["tawil"]
        if not any(emoji in tawil for emoji in ["📿", "🚶", "💎", "🌟"]):
            errors.append("Ta'wil content missing expected emoji markers")

    return errors


def validate_csv_headers(headers: List[str]) -> bool:
    """
    Validate that CSV headers match expected format.

    Args:
        headers: List of header strings

    Returns:
        True if headers match expected format
    """
    if len(headers) != len(COLUMN_HEADERS):
        return False

    # Could do exact match or fuzzy match
    # For now, just check length
    return True
