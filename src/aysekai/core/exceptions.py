"""Custom exception classes for the Aysekai application"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class AsmaBaseException(Exception):
    """Base exception class for all Aysekai-specific exceptions"""
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.context = context or {}
        self.timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize exception for logging"""
        return {
            "message": self.message,
            "error_code": self.error_code,
            "context": self.context,
            "timestamp": self.timestamp,
            "exception_type": self.__class__.__name__
        }
    
    def is_similar_to(self, other: 'AsmaBaseException') -> bool:
        """Check if this exception is similar to another"""
        return (
            self.__class__ == other.__class__ and
            self.message == other.message and
            getattr(self, 'field', None) == getattr(other, 'field', None)
        )
    
    def is_user_recoverable(self) -> bool:
        """Check if this error can be recovered by user action"""
        return isinstance(self, ValidationError)
    
    def requires_admin_intervention(self) -> bool:
        """Check if this error requires admin intervention"""
        return isinstance(self, SystemError) and getattr(self, 'severity', '') == 'critical'
    
    def format_for_logging(self) -> str:
        """Format exception for detailed logging"""
        details = [f"{self.__class__.__name__}: {self.message}"]
        if self.error_code:
            details.append(f"Error Code: {self.error_code}")
        
        # Add subclass-specific details
        if hasattr(self, 'field') and self.field:
            details.append(f"Field: {self.field}")
        if hasattr(self, 'value') and self.value is not None:
            details.append(f"Value: {self.value}")
        if hasattr(self, 'file_path') and self.file_path:
            details.append(f"File: {self.file_path}")
        if hasattr(self, 'system_error_code') and self.system_error_code:
            details.append(f"System Code: {self.system_error_code}")
        if hasattr(self, 'setting') and self.setting:
            details.append(f"Setting: {self.setting}")
            
        if self.context:
            details.append(f"Context: {self.context}")
        return " | ".join(details)
    
    def format_for_user(self) -> str:
        """Format exception for user-friendly display"""
        # Base implementation - subclasses should override for specific formatting
        return self.message


class ValidationError(AsmaBaseException):
    """Exception for user input validation errors"""
    
    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        value: Optional[Any] = None,
        expected_format: Optional[str] = None,
        suggested_action: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        self.field = field
        self.value = value
        self.expected_format = expected_format
        self.suggested_action = suggested_action
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize validation error with field information"""
        data = super().to_dict()
        data.update({
            "field": self.field,
            "value": self.value,
            "expected_format": self.expected_format,
            "suggested_action": self.suggested_action
        })
        return data
    
    def is_user_actionable(self) -> bool:
        """Check if user can take action to resolve this error"""
        return self.suggested_action is not None
    
    def format_for_user(self) -> str:
        """Format validation error for user display (excludes technical details)"""
        message = self.message
        if self.suggested_action:
            message += f"\n\n{self.suggested_action}"
        return message


class DataError(AsmaBaseException):
    """Exception for data loading and processing errors"""
    
    def __init__(
        self,
        message: str,
        file_path: Optional[Path] = None,
        line_number: Optional[int] = None,
        data_type: Optional[str] = None,
        expected_format: Optional[str] = None,
        recovery_suggestion: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        self.file_path = file_path
        self.line_number = line_number
        self.data_type = data_type
        self.expected_format = expected_format
        self.recovery_suggestion = recovery_suggestion
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize data error with file information"""
        data = super().to_dict()
        data.update({
            "file_path": str(self.file_path) if self.file_path else None,
            "line_number": self.line_number,
            "data_type": self.data_type,
            "expected_format": self.expected_format,
            "recovery_suggestion": self.recovery_suggestion
        })
        return data


class SystemError(AsmaBaseException):
    """Exception for system and environment errors"""
    
    def __init__(
        self,
        message: str,
        system_error_code: Optional[int] = None,
        component: Optional[str] = None,
        severity: str = "error",
        environment_info: Optional[Dict[str, Any]] = None,
        recovery_actions: Optional[List[str]] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        self.system_error_code = system_error_code
        self.component = component
        self.severity = severity
        self.environment_info = environment_info or {}
        self.recovery_actions = recovery_actions or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize system error with system information"""
        data = super().to_dict()
        data.update({
            "system_error_code": self.system_error_code,
            "component": self.component,
            "severity": self.severity,
            "environment_info": self.environment_info,
            "recovery_actions": self.recovery_actions
        })
        return data
    
    def is_critical(self) -> bool:
        """Check if this is a critical system error"""
        return self.severity == "critical"


class ConfigError(AsmaBaseException):
    """Exception for configuration and settings errors"""
    
    def __init__(
        self,
        message: str,
        setting: Optional[str] = None,
        config_file: Optional[Path] = None,
        current_value: Optional[Any] = None,
        expected_type: Optional[str] = None,
        validation_rules: Optional[List[str]] = None,
        default_fallback: Optional[Any] = None,
        using_default: bool = False,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        self.setting = setting
        self.config_file = config_file
        self.current_value = current_value
        self.expected_type = expected_type
        self.validation_rules = validation_rules or []
        self.default_fallback = default_fallback
        self.using_default = using_default
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize config error with configuration information"""
        data = super().to_dict()
        data.update({
            "setting": self.setting,
            "config_file": str(self.config_file) if self.config_file else None,
            "current_value": self.current_value,
            "expected_type": self.expected_type,
            "validation_rules": self.validation_rules,
            "default_fallback": self.default_fallback,
            "using_default": self.using_default
        })
        return data


# Keep old aliases for backward compatibility during transition
AysekaiError = AsmaBaseException
ConfigurationError = ConfigError
