"""Test suite for custom exception classes"""

import pytest
from pathlib import Path

from src.aysekai.core.exceptions import (
    ValidationError,
    DataError,
    SystemError,
    ConfigError,
    AsmaBaseException
)


class TestAsmaBaseException:
    """Test base exception class"""
    
    def test_base_exception_inheritance(self):
        """Test base exception inherits from Exception"""
        exception = AsmaBaseException("Test message")
        assert isinstance(exception, Exception)
        assert str(exception) == "Test message"
    
    def test_base_exception_with_error_code(self):
        """Test base exception with error code"""
        exception = AsmaBaseException("Test message", error_code="ASMA001")
        assert exception.error_code == "ASMA001"
        assert str(exception) == "Test message"
    
    def test_base_exception_with_context(self):
        """Test base exception with context data"""
        context = {"user_id": "123", "operation": "meditation"}
        exception = AsmaBaseException("Test message", context=context)
        assert exception.context == context
    
    def test_base_exception_serialization(self):
        """Test base exception can be serialized for logging"""
        exception = AsmaBaseException(
            "Test message", 
            error_code="ASMA001",
            context={"key": "value"}
        )
        
        serialized = exception.to_dict()
        assert serialized["message"] == "Test message"
        assert serialized["error_code"] == "ASMA001"
        assert serialized["context"] == {"key": "value"}
        assert "timestamp" in serialized


class TestValidationError:
    """Test validation error class"""
    
    def test_validation_error_basic(self):
        """Test basic validation error"""
        error = ValidationError("Invalid input")
        assert isinstance(error, AsmaBaseException)
        assert str(error) == "Invalid input"
    
    def test_validation_error_with_field(self):
        """Test validation error with field information"""
        error = ValidationError("Invalid value", field="name_number")
        assert error.field == "name_number"
        assert str(error) == "Invalid value"
    
    def test_validation_error_with_value(self):
        """Test validation error with invalid value"""
        error = ValidationError("Out of range", field="name_number", value=100)
        assert error.field == "name_number"
        assert error.value == 100
    
    def test_validation_error_with_expected_format(self):
        """Test validation error with expected format information"""
        error = ValidationError(
            "Invalid format",
            field="intention",
            value="",
            expected_format="non-empty string"
        )
        assert error.expected_format == "non-empty string"
    
    def test_validation_error_user_actionable(self):
        """Test validation error provides user-actionable information"""
        error = ValidationError(
            "Name number must be between 1 and 99",
            field="name_number",
            value=100,
            suggested_action="Please enter a number between 1 and 99"
        )
        assert error.suggested_action == "Please enter a number between 1 and 99"
        assert error.is_user_actionable() == True
    
    def test_validation_error_serialization(self):
        """Test validation error serialization includes all fields"""
        error = ValidationError(
            "Invalid input",
            field="test_field",
            value="test_value",
            expected_format="test_format"
        )
        
        serialized = error.to_dict()
        assert serialized["field"] == "test_field"
        assert serialized["value"] == "test_value"
        assert serialized["expected_format"] == "test_format"


class TestDataError:
    """Test data error class"""
    
    def test_data_error_basic(self):
        """Test basic data error"""
        error = DataError("File not found")
        assert isinstance(error, AsmaBaseException)
        assert str(error) == "File not found"
    
    def test_data_error_with_file_path(self):
        """Test data error with file path"""
        file_path = Path("/test/file.csv")
        error = DataError("Corrupted file", file_path=file_path)
        assert error.file_path == file_path
    
    def test_data_error_with_line_number(self):
        """Test data error with line number"""
        error = DataError("Invalid data", line_number=42)
        assert error.line_number == 42
    
    def test_data_error_with_data_type(self):
        """Test data error with data type information"""
        error = DataError("Invalid format", data_type="csv", expected_format="UTF-8")
        assert error.data_type == "csv"
        assert error.expected_format == "UTF-8"
    
    def test_data_error_recovery_suggestions(self):
        """Test data error provides recovery suggestions"""
        error = DataError(
            "File corrupted",
            file_path=Path("/test.csv"),
            recovery_suggestion="Please check file integrity and re-download if necessary"
        )
        assert "re-download" in error.recovery_suggestion
    
    def test_data_error_serialization(self):
        """Test data error serialization includes file information"""
        error = DataError(
            "Test error",
            file_path=Path("/test.csv"),
            line_number=10,
            data_type="csv"
        )
        
        serialized = error.to_dict()
        assert serialized["file_path"] == "/test.csv"
        assert serialized["line_number"] == 10
        assert serialized["data_type"] == "csv"


class TestSystemError:
    """Test system error class"""
    
    def test_system_error_basic(self):
        """Test basic system error"""
        error = SystemError("Permission denied")
        assert isinstance(error, AsmaBaseException)
        assert str(error) == "Permission denied"
    
    def test_system_error_with_error_code(self):
        """Test system error with system error code"""
        error = SystemError("File access error", system_error_code=13)
        assert error.system_error_code == 13
    
    def test_system_error_with_component(self):
        """Test system error with system component"""
        error = SystemError("Network error", component="file_downloader")
        assert error.component == "file_downloader"
    
    def test_system_error_with_environment_info(self):
        """Test system error with environment information"""
        env_info = {"os": "linux", "python_version": "3.11"}
        error = SystemError("System error", environment_info=env_info)
        assert error.environment_info == env_info
    
    def test_system_error_with_recovery_actions(self):
        """Test system error with recovery actions"""
        actions = ["Check file permissions", "Restart application"]
        error = SystemError("Permission error", recovery_actions=actions)
        assert error.recovery_actions == actions
    
    def test_system_error_severity_levels(self):
        """Test system error severity levels"""
        error = SystemError("Critical error", severity="critical")
        assert error.severity == "critical"
        assert error.is_critical() == True
        
        warning = SystemError("Minor issue", severity="warning")
        assert warning.is_critical() == False
    
    def test_system_error_serialization(self):
        """Test system error serialization includes system info"""
        error = SystemError(
            "Test error",
            system_error_code=13,
            component="test_component",
            severity="error"
        )
        
        serialized = error.to_dict()
        assert serialized["system_error_code"] == 13
        assert serialized["component"] == "test_component"
        assert serialized["severity"] == "error"


class TestConfigError:
    """Test configuration error class"""
    
    def test_config_error_basic(self):
        """Test basic configuration error"""
        error = ConfigError("Invalid setting")
        assert isinstance(error, AsmaBaseException)
        assert str(error) == "Invalid setting"
    
    def test_config_error_with_setting_name(self):
        """Test config error with setting name"""
        error = ConfigError("Invalid value", setting="data_path")
        assert error.setting == "data_path"
    
    def test_config_error_with_config_file(self):
        """Test config error with configuration file"""
        config_file = Path("/config/settings.json")
        error = ConfigError("Parse error", config_file=config_file)
        assert error.config_file == config_file
    
    def test_config_error_with_current_value(self):
        """Test config error with current invalid value"""
        error = ConfigError(
            "Invalid path",
            setting="data_path",
            current_value="/invalid/path",
            expected_type="existing directory path"
        )
        assert error.current_value == "/invalid/path"
        assert error.expected_type == "existing directory path"
    
    def test_config_error_with_validation_rules(self):
        """Test config error with validation rules"""
        rules = ["Must be absolute path", "Directory must exist", "Must be readable"]
        error = ConfigError("Path validation failed", validation_rules=rules)
        assert error.validation_rules == rules
    
    def test_config_error_with_default_fallback(self):
        """Test config error with default fallback information"""
        error = ConfigError(
            "Setting missing",
            setting="log_level",
            default_fallback="INFO",
            using_default=True
        )
        assert error.default_fallback == "INFO"
        assert error.using_default == True
    
    def test_config_error_serialization(self):
        """Test config error serialization includes config info"""
        error = ConfigError(
            "Test error",
            setting="test_setting",
            current_value="invalid",
            expected_type="string"
        )
        
        serialized = error.to_dict()
        assert serialized["setting"] == "test_setting"
        assert serialized["current_value"] == "invalid"
        assert serialized["expected_type"] == "string"


class TestExceptionHierarchy:
    """Test exception hierarchy and relationships"""
    
    def test_all_exceptions_inherit_from_base(self):
        """Test all custom exceptions inherit from AsmaBaseException"""
        exceptions = [
            ValidationError("test"),
            DataError("test"),
            SystemError("test"),
            ConfigError("test")
        ]
        
        for exception in exceptions:
            assert isinstance(exception, AsmaBaseException)
            assert isinstance(exception, Exception)
    
    def test_exception_type_checking(self):
        """Test exception type checking works correctly"""
        validation_error = ValidationError("test")
        data_error = DataError("test")
        
        assert isinstance(validation_error, ValidationError)
        assert not isinstance(validation_error, DataError)
        assert isinstance(data_error, DataError)
        assert not isinstance(data_error, ValidationError)
    
    def test_exception_catching_hierarchy(self):
        """Test exception catching follows inheritance hierarchy"""
        try:
            raise ValidationError("test")
        except AsmaBaseException as e:
            assert isinstance(e, ValidationError)
        
        try:
            raise DataError("test")
        except AsmaBaseException as e:
            assert isinstance(e, DataError)


class TestExceptionUtilities:
    """Test exception utility methods"""
    
    def test_exception_comparison(self):
        """Test exception comparison methods"""
        error1 = ValidationError("test", field="name")
        error2 = ValidationError("test", field="name")
        error3 = ValidationError("different", field="name")
        
        assert error1.is_similar_to(error2) == True
        assert error1.is_similar_to(error3) == False
    
    def test_exception_categorization(self):
        """Test exception categorization for handling"""
        validation_error = ValidationError("test")
        data_error = DataError("test")
        system_error = SystemError("test", severity="critical")
        
        assert validation_error.is_user_recoverable() == True
        assert data_error.is_user_recoverable() == False
        assert system_error.is_user_recoverable() == False
        assert system_error.requires_admin_intervention() == True
    
    def test_exception_logging_format(self):
        """Test exception formatting for logging"""
        error = ValidationError(
            "Invalid input",
            field="name_number",
            value=100,
            context={"user_session": "123"}
        )
        
        log_format = error.format_for_logging()
        assert "ValidationError" in log_format
        assert "name_number" in log_format
        assert "123" in log_format  # Context included
        assert "100" in log_format  # Value included
    
    def test_exception_user_message_format(self):
        """Test exception formatting for user messages"""
        error = ValidationError(
            "Invalid input",
            field="name_number",
            value=100,
            suggested_action="Please enter 1-99"
        )
        
        user_format = error.format_for_user()
        assert "Invalid input" in user_format
        assert "100" not in user_format  # Technical details excluded
        assert "Please enter 1-99" in user_format  # Guidance included