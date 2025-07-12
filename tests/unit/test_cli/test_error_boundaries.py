"""Test suite for global error boundaries and error handling"""

import pytest
import sys
import tempfile
from unittest.mock import Mock, patch, call
from pathlib import Path
from io import StringIO

from rich.console import Console

from src.aysekai.cli.error_handler import (
    error_boundary,
    setup_global_exception_handler,
    handle_validation_error,
    handle_data_error,
    handle_system_error,
    handle_config_error,
    handle_unexpected_error,
    format_user_friendly_message
)
from src.aysekai.core.exceptions import (
    ValidationError,
    DataError,
    SystemError,
    ConfigError
)


class TestErrorBoundaryDecorator:
    """Test the error boundary decorator functionality"""
    
    def setup_method(self):
        """Set up test environment"""
        self.console = Console(file=StringIO(), force_terminal=True)
        self.log_file = Path(tempfile.mktemp())
    
    def test_error_boundary_catches_validation_error(self):
        """Test error boundary catches and handles ValidationError"""
        @error_boundary(console=self.console, log_file=self.log_file)
        def test_function():
            raise ValidationError("Invalid input", field="name_number", value=100)
        
        with pytest.raises(SystemExit) as exc_info:
            test_function()
        
        assert exc_info.value.code == 1
        
        # Check user message was displayed
        output = self.console.file.getvalue()
        assert "Input Error" in output
        assert "Invalid input" in output
        
    def test_error_boundary_catches_data_error(self):
        """Test error boundary catches and handles DataError"""
        @error_boundary(console=self.console, log_file=self.log_file)
        def test_function():
            raise DataError("File not found", file_path=Path("/test.csv"))
        
        with pytest.raises(SystemExit) as exc_info:
            test_function()
        
        assert exc_info.value.code == 1
        
        # Check user message was displayed
        output = self.console.file.getvalue()
        assert "Data Error" in output
        assert "meditation data" in output
    
    def test_error_boundary_catches_system_error(self):
        """Test error boundary catches and handles SystemError"""
        @error_boundary(console=self.console, log_file=self.log_file)
        def test_function():
            raise SystemError("Permission denied", error_code=13)
        
        with pytest.raises(SystemExit) as exc_info:
            test_function()
        
        assert exc_info.value.code == 1
        
        # Check user message was displayed
        output = self.console.file.getvalue()
        assert "System Error" in output
        assert "permissions" in output
    
    def test_error_boundary_catches_config_error(self):
        """Test error boundary catches and handles ConfigError"""
        @error_boundary(console=self.console, log_file=self.log_file)
        def test_function():
            raise ConfigError("Invalid setting", setting="data_path")
        
        with pytest.raises(SystemExit) as exc_info:
            test_function()
        
        assert exc_info.value.code == 1
        
        # Check user message was displayed
        output = self.console.file.getvalue()
        assert "Configuration Error" in output
        assert "settings" in output
    
    def test_error_boundary_catches_unexpected_error(self):
        """Test error boundary catches and handles unexpected exceptions"""
        @error_boundary(console=self.console, log_file=self.log_file)
        def test_function():
            raise RuntimeError("Unexpected error")
        
        with pytest.raises(SystemExit) as exc_info:
            test_function()
        
        assert exc_info.value.code == 1
        
        # Check user message was displayed
        output = self.console.file.getvalue()
        assert "Application Error" in output
        assert "unexpected error" in output
    
    def test_error_boundary_preserves_successful_execution(self):
        """Test error boundary doesn't interfere with successful execution"""
        @error_boundary(console=self.console)
        def test_function():
            return "success"
        
        result = test_function()
        assert result == "success"
    
    def test_error_boundary_logs_errors_to_file(self):
        """Test error boundary logs errors to specified file"""
        @error_boundary(console=self.console, log_file=self.log_file)
        def test_function():
            raise DataError("Test error", file_path=Path("/test.csv"))
        
        with pytest.raises(SystemExit):
            test_function()
        
        # Check error was logged to file
        assert self.log_file.exists()
        log_content = self.log_file.read_text()
        assert "DataError" in log_content
        assert "Test error" in log_content


class TestGlobalExceptionHandler:
    """Test global exception handler setup and functionality"""
    
    def test_setup_global_exception_handler_installs_handler(self):
        """Test global exception handler is properly installed"""
        original_hook = sys.excepthook
        
        try:
            setup_global_exception_handler()
            assert sys.excepthook != original_hook
        finally:
            sys.excepthook = original_hook
    
    @patch('src.aysekai.cli.error_handler.logger')
    @patch('src.aysekai.cli.error_handler.console')
    def test_global_handler_logs_unhandled_exceptions(self, mock_console, mock_logger):
        """Test global handler logs unhandled exceptions"""
        setup_global_exception_handler()
        
        try:
            # Simulate unhandled exception
            raise ValueError("Test unhandled exception")
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            sys.excepthook(exc_type, exc_value, exc_traceback)
        
        # Verify logging occurred
        mock_logger.critical.assert_called_once()
        call_args = mock_logger.critical.call_args
        assert "Unhandled exception" in call_args[0][0]
        
        # Verify user message displayed
        mock_console.print.assert_called_once()
    
    def test_global_handler_preserves_keyboard_interrupt(self):
        """Test global handler preserves KeyboardInterrupt behavior"""
        original_hook = sys.excepthook
        
        try:
            setup_global_exception_handler()
            
            # Simulate KeyboardInterrupt - should use original hook
            with patch.object(sys, '__excepthook__') as mock_original:
                try:
                    raise KeyboardInterrupt()
                except:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    sys.excepthook(exc_type, exc_value, exc_traceback)
                
                mock_original.assert_called_once()
        finally:
            sys.excepthook = original_hook


class TestSpecificErrorHandlers:
    """Test specific error handler functions"""
    
    def setup_method(self):
        """Set up test environment"""
        self.console = Console(file=StringIO(), force_terminal=True)
        self.log_file = Path(tempfile.mktemp())
    
    def test_handle_validation_error_formats_user_message(self):
        """Test validation error handler formats user-friendly message"""
        error = ValidationError("Name number must be 1-99", field="name_number", value=100)
        
        handle_validation_error(error, self.console)
        
        output = self.console.file.getvalue()
        assert "Input Error" in output
        assert "Name number must be 1-99" in output
        assert "100" not in output  # Technical details excluded
    
    def test_handle_data_error_provides_generic_message(self):
        """Test data error handler provides generic user message"""
        error = DataError("CSV file corrupted", file_path=Path("/path/to/file.csv"))
        
        handle_data_error(error, self.console, self.log_file)
        
        output = self.console.file.getvalue()
        assert "Data Error" in output
        assert "meditation data" in output
        assert "/path/to/file.csv" not in output  # No file paths in user message
    
    def test_handle_system_error_provides_system_guidance(self):
        """Test system error handler provides system-level guidance"""
        error = SystemError("Permission denied", error_code=13)
        
        handle_system_error(error, self.console, self.log_file)
        
        output = self.console.file.getvalue()
        assert "System Error" in output
        assert "permissions" in output
        assert "13" not in output  # No error codes in user message
    
    def test_handle_config_error_provides_configuration_guidance(self):
        """Test config error handler provides configuration guidance"""
        error = ConfigError("Invalid data path", setting="AYSEKAI_DATA_PATH")
        
        handle_config_error(error, self.console, self.log_file)
        
        output = self.console.file.getvalue()
        assert "Configuration Error" in output
        assert "settings" in output
        assert "AYSEKAI_DATA_PATH" not in output  # No setting names in user message
    
    def test_handle_unexpected_error_provides_generic_message(self):
        """Test unexpected error handler provides generic message"""
        error = RuntimeError("Internal error with sensitive data")
        
        handle_unexpected_error(error, self.console, self.log_file)
        
        output = self.console.file.getvalue()
        assert "Application Error" in output
        assert "unexpected error" in output
        assert "sensitive data" not in output  # No technical details


class TestErrorMessageFormatting:
    """Test error message formatting functions"""
    
    def test_format_user_friendly_message_validation_error(self):
        """Test user-friendly message formatting for validation errors"""
        error = ValidationError("Invalid name number", field="name_number", value=100)
        
        message = format_user_friendly_message(error)
        
        assert "Invalid name number" in message
        assert "name number" in message.lower()
        assert "100" not in message  # No technical values
    
    def test_format_user_friendly_message_removes_technical_details(self):
        """Test message formatter removes technical details"""
        error = ValidationError("Field 'user_input' failed validation: value must be str")
        
        message = format_user_friendly_message(error)
        
        assert "user_input" not in message
        assert "str" not in message
        assert "validation" in message
    
    def test_format_user_friendly_message_provides_guidance(self):
        """Test message formatter provides actionable guidance"""
        error = ValidationError("Name number out of range", field="name_number")
        
        message = format_user_friendly_message(error)
        
        assert "range" in message
        assert any(word in message.lower() for word in ["please", "try", "should", "must"])


class TestErrorLogging:
    """Test error logging functionality"""
    
    def setup_method(self):
        """Set up test environment"""
        self.log_file = Path(tempfile.mktemp())
    
    def test_error_logging_includes_technical_details(self):
        """Test error logging includes comprehensive technical details"""
        error = DataError("File not found", file_path=Path("/test.csv"), line_number=42)
        
        with patch('src.aysekai.cli.error_handler.log_data_error') as mock_log:
            handle_data_error(error, Mock(), self.log_file)
            
            mock_log.assert_called_once_with(error, self.log_file)
    
    def test_error_logging_structured_format(self):
        """Test error logging uses structured format"""
        # This test will verify the actual logging format once implemented
        pass
    
    def test_error_logging_excludes_sensitive_data(self):
        """Test error logging excludes sensitive data"""
        # This test will verify sensitive data exclusion once implemented
        pass


class TestErrorRecovery:
    """Test error recovery and graceful degradation"""
    
    def test_partial_functionality_after_data_error(self):
        """Test application can provide partial functionality after data errors"""
        # This test will verify graceful degradation once implemented
        pass
    
    def test_default_values_after_config_error(self):
        """Test application uses defaults after configuration errors"""
        # This test will verify default value fallbacks once implemented
        pass
    
    def test_alternative_data_sources_after_primary_failure(self):
        """Test application tries alternative data sources"""
        # This test will verify alternative data source logic once implemented
        pass


class TestErrorBoundaryIntegration:
    """Test error boundary integration with CLI commands"""
    
    def test_cli_command_validation_error_handling(self):
        """Test CLI commands handle validation errors through error boundary"""
        # This test will verify CLI integration once commands are updated
        pass
    
    def test_dependency_injection_error_handling(self):
        """Test DI errors are properly handled by error boundaries"""
        # This test will verify DI error handling once implemented
        pass
    
    def test_error_boundary_with_typer_commands(self):
        """Test error boundaries work correctly with Typer commands"""
        # This test will verify Typer integration once implemented
        pass


class TestSecurityAspects:
    """Test security aspects of error handling"""
    
    def test_no_stack_traces_in_user_messages(self):
        """Test stack traces are never shown to users"""
        @error_boundary(console=Console(file=StringIO()))
        def test_function():
            raise RuntimeError("Test error")
        
        with pytest.raises(SystemExit):
            test_function()
        
        # Verify no stack trace elements in output
        # This will be implemented with actual error boundary
        pass
    
    def test_no_file_paths_in_user_messages(self):
        """Test internal file paths are not exposed to users"""
        error = DataError("File error", file_path=Path("/internal/path/file.csv"))
        console = Console(file=StringIO())
        
        handle_data_error(error, console, None)
        
        output = console.file.getvalue()
        assert "/internal/path" not in output
    
    def test_no_sensitive_config_in_user_messages(self):
        """Test sensitive configuration values not exposed to users"""
        error = ConfigError("Invalid API key", setting="SECRET_API_KEY")
        console = Console(file=StringIO())
        
        handle_config_error(error, console, None)
        
        output = console.file.getvalue()
        assert "SECRET_API_KEY" not in output
        assert "API key" not in output  # Even generic references avoided