import pytest
import sys
from unittest.mock import patch, MagicMock
from rich.console import Console
from io import StringIO

from aysekai.cli.error_handler import (
    error_boundary,
    setup_exception_handler,
    format_user_error,
    log_error,
)
from aysekai.core.exceptions import (
    ValidationError,
    DataError,
    ConfigurationError,
    AysekaiError,
)


class TestErrorHandler:
    """Test error handling functionality"""
    
    @pytest.fixture
    def mock_console(self):
        """Create mock console for testing output"""
        return Console(file=StringIO(), force_terminal=True)
    
    def test_error_boundary_validation_error(self, mock_console):
        """Test error boundary handles ValidationError"""
        @error_boundary(console=mock_console)
        def failing_function():
            raise ValidationError("Invalid input: test")
        
        with pytest.raises(SystemExit) as exc_info:
            failing_function()
        
        assert exc_info.value.code == 1
        output = mock_console.file.getvalue()
        assert "Invalid Input" in output
        assert "Invalid input: test" in output
    
    def test_error_boundary_data_error(self, mock_console):
        """Test error boundary handles DataError"""
        @error_boundary(console=mock_console)
        def failing_function():
            raise DataError("CSV file not found")
        
        with pytest.raises(SystemExit) as exc_info:
            failing_function()
        
        assert exc_info.value.code == 2
        output = mock_console.file.getvalue()
        assert "Data Problem" in output
        assert "CSV file not found" in output
        assert "ensure the CSV files" in output
    
    def test_error_boundary_configuration_error(self, mock_console):
        """Test error boundary handles ConfigurationError"""
        @error_boundary(console=mock_console)
        def failing_function():
            raise ConfigurationError("Missing API_KEY")
        
        with pytest.raises(SystemExit) as exc_info:
            failing_function()
        
        assert exc_info.value.code == 3
        output = mock_console.file.getvalue()
        assert "Configuration Problem" in output
        assert "Missing API_KEY" in output
        assert "environment variables" in output
    
    def test_error_boundary_keyboard_interrupt(self, mock_console):
        """Test error boundary handles KeyboardInterrupt gracefully"""
        @error_boundary(console=mock_console)
        def interrupted_function():
            raise KeyboardInterrupt()
        
        with pytest.raises(SystemExit) as exc_info:
            interrupted_function()
        
        assert exc_info.value.code == 0
        output = mock_console.file.getvalue()
        assert "interrupted" in output.lower()
        assert "Ma'a salama" in output
    
    def test_error_boundary_unexpected_error(self, mock_console, tmp_path):
        """Test error boundary handles unexpected errors"""
        # Set up temporary error log
        error_log = tmp_path / "error.log"
        
        @error_boundary(console=mock_console, error_log=error_log)
        def failing_function():
            raise RuntimeError("Unexpected error occurred")
        
        with pytest.raises(SystemExit) as exc_info:
            failing_function()
        
        assert exc_info.value.code == 99
        output = mock_console.file.getvalue()
        assert "Unexpected Error" in output
        # Check for the filename since the path might be wrapped by Rich
        assert error_log.name in output
        
        # Verify error was logged
        assert error_log.exists()
        log_content = error_log.read_text()
        assert "RuntimeError: Unexpected error occurred" in log_content
        assert "Traceback" in log_content
    
    def test_error_boundary_preserves_return_value(self, mock_console):
        """Test error boundary preserves function return value"""
        @error_boundary(console=mock_console)
        def successful_function():
            return "success"
        
        result = successful_function()
        assert result == "success"
    
    def test_format_user_error_messages(self):
        """Test user-friendly error message formatting"""
        # Validation error
        msg = format_user_error(ValidationError("Number must be 1-99"))
        assert "input" in msg.lower()
        assert "1-99" in msg
        
        # Data error
        msg = format_user_error(DataError("names.csv missing"))
        assert "data" in msg.lower()
        assert "names.csv" in msg
        
        # Generic error
        msg = format_user_error(Exception("Something went wrong"))
        assert "error occurred" in msg.lower()
    
    def test_log_error_creates_file(self, tmp_path):
        """Test error logging creates log file"""
        error_log = tmp_path / "errors.log"
        
        try:
            raise ValueError("Test error")
        except ValueError as e:
            log_error(e, error_log)
        
        assert error_log.exists()
        content = error_log.read_text()
        assert "ValueError: Test error" in content
        assert "Traceback" in content
        assert "test_log_error_creates_file" in content
    
    def test_log_error_appends(self, tmp_path):
        """Test error logging appends to existing file"""
        error_log = tmp_path / "errors.log"
        
        # Log first error
        try:
            raise ValueError("Error 1")
        except ValueError as e:
            log_error(e, error_log)
        
        # Log second error
        try:
            raise TypeError("Error 2")
        except TypeError as e:
            log_error(e, error_log)
        
        content = error_log.read_text()
        assert "Error Message: Error 1" in content
        assert "Error Message: Error 2" in content
        assert content.count("=" * 60) == 2
    
    def test_setup_exception_handler(self, mock_console):
        """Test global exception handler setup"""
        original_hook = sys.excepthook
        try:
            setup_exception_handler(console=mock_console)
            
            # Verify excepthook was set
            assert sys.excepthook is not original_hook
            
            # Test the hook with pytest.raises to catch SystemExit
            with pytest.raises(SystemExit):
                try:
                    raise ValueError("Test error")
                except ValueError:
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    sys.excepthook(exc_type, exc_value, exc_tb)
            
            output = mock_console.file.getvalue()
            assert "Unexpected Error" in output
        finally:
            # Restore original hook
            sys.excepthook = original_hook
    
    def test_error_messages_no_technical_details(self, mock_console):
        """Test error messages hide technical details from user"""
        @error_boundary(console=mock_console)
        def failing_function():
            # Simulate a technical error
            null_object = None
            return null_object.some_method()  # AttributeError
        
        with pytest.raises(SystemExit):
            failing_function()
        
        output = mock_console.file.getvalue()
        # Should not expose technical details
        assert "AttributeError" not in output
        assert "NoneType" not in output
        assert "some_method" not in output
        # Should show user-friendly message
        assert "unexpected error occurred" in output.lower()