"""Input validation and sanitization utilities"""

import re
import bleach
from typing import Optional, List, Union
from pathlib import Path
from ..core.exceptions import ValidationError


class InputValidator:
    """Validate and sanitize all user inputs"""

    # Constants
    MAX_PROMPT_LENGTH = 500
    SAFE_TEXT_PATTERN = re.compile(
        r"^[\w\s\-.,!?؛،؟\u0600-\u06FF\u0020-\u007E\u00A0-\u00FF]+$"
    )

    # Dangerous command patterns
    DANGEROUS_PATTERNS = [
        r"\brm\s+-rf",
        r"\beval\b",
        r"\bcurl\b.*\|\s*bash",
        r";\s*cat\s+/etc",
        r"\|\|",
        r"`[^`]+`",
        r"\$\([^)]+\)",
        r"DROP\s+TABLE",
        r"DELETE\s+FROM",
    ]

    @staticmethod
    def sanitize_prompt(prompt: Optional[str]) -> str:
        """
        Sanitize user prompt for safe logging and storage.

        Args:
            prompt: User input prompt

        Returns:
            Sanitized prompt safe for CSV storage
        """
        if not prompt:
            return ""

        # Convert to string if needed
        prompt = str(prompt).strip()

        # Limit length first
        if len(prompt) > InputValidator.MAX_PROMPT_LENGTH:
            prompt = prompt[: InputValidator.MAX_PROMPT_LENGTH]

        # Remove control characters first (keep printable + common Unicode)
        cleaned_chars = []
        for char in prompt:
            # Keep regular printable ASCII, extended ASCII, and Unicode (above 32)
            # Filter out control characters (0-31) except tab, newlines, carriage returns
            if ord(char) >= 32:
                cleaned_chars.append(char)
            elif char in "\t\n\r":
                cleaned_chars.append(" ")  # Convert tab/newline/CR to space

        prompt = "".join(cleaned_chars)

        # Remove HTML/script tags using bleach (after control char removal)
        prompt = bleach.clean(prompt, tags=[], strip=True)

        # Replace newlines and carriage returns with spaces
        prompt = prompt.replace("\n", " ").replace("\r", " ")

        # Remove multiple spaces
        prompt = re.sub(r"\s+", " ", prompt)

        # Remove SQL injection patterns
        sql_patterns = [
            r"DROP\s+TABLE",
            r"DELETE\s+FROM",
            r"INSERT\s+INTO",
            r"UPDATE\s+SET",
            r"UNION\s+SELECT",
            r";\s*--",
            r"'\s*OR\s+'",
        ]

        for pattern in sql_patterns:
            prompt = re.sub(pattern, "", prompt, flags=re.IGNORECASE)

        # Escape quotes for CSV
        prompt = prompt.replace('"', '""')

        return prompt.strip()

    @staticmethod
    def validate_number_input(value: Optional[Union[str, int]]) -> Optional[int]:
        """
        Validate and parse number input (1-99).

        Args:
            value: Input value to validate

        Returns:
            Validated integer or None if invalid
        """
        if value is None:
            return None

        try:
            # Handle string input
            if isinstance(value, str):
                value = value.strip()

            num = int(value)

            # Check range
            if 1 <= num <= 99:
                return num

        except (ValueError, TypeError):
            pass

        return None

    @staticmethod
    def validate_file_path(path: Path, allowed_dirs: List[str]) -> bool:
        """
        Validate file path is within allowed directories.

        Args:
            path: Path to validate
            allowed_dirs: List of allowed base directories

        Returns:
            True if path is allowed, False otherwise
        """
        try:
            # Check for traversal patterns in original path
            path_str = str(path)

            # Check for directory traversal patterns (including URL encoded)
            dangerous_patterns = [
                "..",
                "%2e%2e",  # URL encoded ..
                "%2E%2E",  # URL encoded .. (uppercase)
                "..%2f",  # Mixed encoding
                "%2f..",  # Mixed encoding
            ]

            for pattern in dangerous_patterns:
                if pattern in path_str.lower():
                    return False

            # Resolve to absolute path
            resolved = path.resolve()
            resolved_str = str(resolved)

            # Check against each allowed directory
            for allowed in allowed_dirs:
                allowed_path = Path(allowed).resolve()
                allowed_str = str(allowed_path)

                # Check if resolved path is under allowed directory
                if resolved_str.startswith(allowed_str):
                    return True

        except Exception:
            # Any error in path resolution means it's invalid
            pass

        return False

    @staticmethod
    def validate_command(command: str) -> bool:
        """
        Validate command for dangerous patterns.

        Args:
            command: Command string to validate

        Returns:
            True if command appears safe, False otherwise
        """
        if not command:
            return False

        # Check against dangerous patterns
        for pattern in InputValidator.DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return False

        # Check for common injection attempts
        dangerous_chars = [";", "||", "&&", "`", "$", ">", "<", "|"]
        for char in dangerous_chars:
            if char in command:
                # Some chars are OK in certain contexts
                if char == ">" and command.count(char) == 1:
                    continue  # Single redirect might be OK
                return False

        return True

    @staticmethod
    def validate_required_field(value: Optional[str], field_name: str = "field") -> str:
        """
        Validate that a required field is not empty.

        Args:
            value: Field value
            field_name: Name of field for error message

        Returns:
            Validated non-empty string

        Raises:
            ValidationError: If field is empty
        """
        if not value or not value.strip():
            raise ValidationError(f"Required field '{field_name}' cannot be empty")

        return value.strip()

    @staticmethod
    def validate_arabic_text(text: str) -> bool:
        """
        Check if text contains Arabic characters.

        Args:
            text: Text to check

        Returns:
            True if text contains Arabic
        """
        arabic_pattern = re.compile(r"[\u0600-\u06FF]")
        return bool(arabic_pattern.search(text))
