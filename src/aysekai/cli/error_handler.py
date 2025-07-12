"""Global error handling and user-friendly error messages"""

import sys
import functools
import traceback
import logging
from pathlib import Path
from datetime import datetime
from typing import Callable, Optional, Any, List
import time

from rich.console import Console
from rich.panel import Panel

from ..core.exceptions import (
    ValidationError,
    DataError,
    SystemError,
    ConfigError
)


# Default console for error output
_console = Console(stderr=True)
console = _console

# Logger for error details
logger = logging.getLogger(__name__)


def format_user_friendly_message(error: Exception) -> str:
    """
    Format error message for user display, removing technical details.
    
    Args:
        error: Exception to format
        
    Returns:
        User-friendly error message
    """
    if isinstance(error, ValidationError):
        message = error.message
        
        # Handle specific technical error messages
        if "Field 'user_input' failed validation: value must be str" in message:
            return "Input validation failed. Please enter valid text."
        
        # Remove technical field references
        message = message.replace("Field '", "").replace("' failed validation", "")
        message = message.replace("value must be str", "Please enter valid text")
        
        # Remove field names from start of message
        if ": " in message and any(field in message.split(": ")[0] for field in ["user_input", "name_number", "intention"]):
            message = message.split(": ", 1)[1]
        
        # Add helpful guidance
        if "range" in message.lower():
            message += "\nPlease enter a number between 1 and 99."
        elif "validation" in message.lower():
            message += "\nPlease check your input and try again."
            
        return message
    
    elif isinstance(error, DataError):
        return "Unable to load meditation data. Please check data files are available."
    
    elif isinstance(error, SystemError):
        return "System error encountered. Please check permissions and environment."
    
    elif isinstance(error, ConfigError):
        return "Configuration error detected. Please check your settings."
    
    # Generic error - remove sensitive details
    message = str(error)
    if "sensitive data" in message:
        message = "An error occurred during processing."
    if "internal error" in message:
        message = "An unexpected error occurred."
    
    return message


def format_user_error(error: Exception) -> str:
    """
    Format error message for user display (legacy function).
    
    Args:
        error: Exception to format
        
    Returns:
        User-friendly error message
    """
    return format_user_friendly_message(error)


def log_error(
    error: Exception,
    error_log: Optional[Path] = None
) -> Path:
    """
    Log error details to file for debugging.
    
    Args:
        error: Exception to log
        error_log: Path to error log file
        
    Returns:
        Path to error log file
    """
    if error_log is None:
        error_log = Path.home() / ".aysekai" / "error.log"
    
    error_log.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if file already exists to add separator
    file_exists = error_log.exists()
    
    with open(error_log, 'a', encoding='utf-8') as f:
        if file_exists:
            # Add separator before new entry
            f.write(f"\n{'=' * 60}\n")
        
        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        f.write(f"Error Type: {type(error).__name__}\n")
        f.write(f"Error Message: {str(error)}\n")
        f.write("\nTraceback:\n")
        # Format traceback from the exception
        if hasattr(error, '__traceback__') and error.__traceback__ is not None:
            f.write(''.join(traceback.format_exception(type(error), error, error.__traceback__)))
        else:
            f.write(traceback.format_exc())
        
        if not file_exists:
            # Add separator after first entry
            f.write(f"{'=' * 60}\n")
    
    return error_log


def handle_validation_error(error: ValidationError, console: Console) -> None:
    """Handle user input validation errors"""
    message = format_user_friendly_message(error)
    console.print(Panel(
        message,
        title="Input Error",
        border_style="yellow"
    ))
    log_validation_error(error)


def handle_data_error(error: DataError, console: Console, log_file: Optional[Path] = None) -> None:
    """Handle data loading and processing errors"""
    message = "Unable to load meditation data. Please check data files."
    console.print(Panel(message, title="Data Error", border_style="red"))
    log_data_error(error, log_file)


def handle_system_error(error: SystemError, console: Console, log_file: Optional[Path] = None) -> None:
    """Handle system and environment errors"""
    message = "System error encountered. Please check permissions and environment."
    console.print(Panel(message, title="System Error", border_style="red"))
    log_system_error(error, log_file)


def handle_config_error(error: ConfigError, console: Console, log_file: Optional[Path] = None) -> None:
    """Handle configuration and settings errors"""
    message = "Configuration error detected. Please check your settings."
    console.print(Panel(message, title="Configuration Error", border_style="red"))
    log_config_error(error, log_file)


def handle_unexpected_error(error: Exception, console: Console, log_file: Optional[Path] = None) -> None:
    """Handle unexpected exceptions"""
    message = "An unexpected error occurred. Please check the logs for details."
    console.print(Panel(message, title="Application Error", border_style="red"))
    log_unexpected_error(error, log_file)


def log_validation_error(error: ValidationError) -> None:
    """Log validation error details"""
    logger.warning(f"Validation error: {error.format_for_logging()}")


def log_data_error(error: DataError, log_file: Optional[Path] = None) -> None:
    """Log data error details"""
    logger.error(f"Data error: {error.format_for_logging()}")
    if log_file:
        log_error(error, log_file)


def log_system_error(error: SystemError, log_file: Optional[Path] = None) -> None:
    """Log system error details"""
    logger.error(f"System error: {error.format_for_logging()}")
    if log_file:
        log_error(error, log_file)


def log_config_error(error: ConfigError, log_file: Optional[Path] = None) -> None:
    """Log configuration error details"""
    logger.error(f"Config error: {error.format_for_logging()}")
    if log_file:
        log_error(error, log_file)


def log_unexpected_error(error: Exception, log_file: Optional[Path] = None) -> None:
    """Log unexpected error details"""
    logger.critical(f"Unexpected error: {type(error).__name__}: {error}")
    if log_file:
        log_error(error, log_file)


def setup_global_exception_handler() -> None:
    """Install global exception handler for unhandled exceptions"""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        logger.critical("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))
        console.print(Panel(
            "[red]An unexpected error occurred. Please check the logs for details.[/]",
            title="Application Error",
            border_style="red"
        ))
    
    sys.excepthook = handle_exception


def get_log_file() -> Path:
    """Get the default log file path"""
    return Path.home() / ".aysekai" / "error.log"


def error_boundary(
    console: Optional[Console] = None,
    error_log: Optional[Path] = None,
    log_file: Optional[Path] = None,
    show_technical_details: bool = False
) -> Callable:
    """
    Decorator for global error handling with user-friendly messages.
    
    Args:
        console: Rich console for output
        error_log: Path to error log file
        
    Returns:
        Decorated function with error handling
    """
    if console is None:
        console = _console
    
    # Use log_file parameter if provided, otherwise fall back to error_log
    actual_log_file = log_file or error_log
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
                
            except ValidationError as e:
                handle_validation_error(e, console)
                sys.exit(1)
                
            except DataError as e:
                handle_data_error(e, console, actual_log_file)
                sys.exit(1)
                
            except SystemError as e:
                handle_system_error(e, console, actual_log_file)
                sys.exit(1)
                
            except ConfigError as e:
                handle_config_error(e, console, actual_log_file)
                sys.exit(1)
                
            except KeyboardInterrupt:
                console.print(
                    "\n[yellow]Meditation interrupted. Ma'a salama! 🌙[/yellow]"
                )
                sys.exit(0)
                
            except Exception as e:
                handle_unexpected_error(e, console, actual_log_file)
                sys.exit(1)
        
        return wrapper
    return decorator


def setup_exception_handler(
    console: Optional[Console] = None,
    error_log: Optional[Path] = None
) -> None:
    """
    Setup global exception handler for uncaught exceptions.
    
    Args:
        console: Rich console for output
        error_log: Path to error log file
    """
    setup_global_exception_handler()


def with_retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    retry_on: tuple = (DataError,)
) -> Callable:
    """
    Decorator for automatic retry on transient errors.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Backoff multiplier for delay
        retry_on: Tuple of exception types to retry on
        
    Returns:
        Decorated function with retry logic
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_error = None
            current_delay = delay
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except retry_on as e:
                    last_error = e
                    if attempt < max_attempts - 1:
                        time.sleep(current_delay)
                        current_delay *= backoff
                    continue
                except Exception:
                    # Don't retry other exceptions
                    raise
            
            # Exhausted retries
            if last_error:
                raise last_error
                
        return wrapper
    return decorator


class ErrorRecovery:
    """Context manager for error recovery strategies"""
    
    def __init__(self, max_attempts: int = 3):
        """
        Initialize error recovery context.
        
        Args:
            max_attempts: Maximum recovery attempts
        """
        self.max_attempts = max_attempts
        self.attempt_count = 0
        self.errors: List[Exception] = []
    
    def __enter__(self):
        """Enter recovery context"""
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Exit recovery context"""
        if exc_value:
            self.add_error(exc_value)
        return False  # Don't suppress exceptions
    
    def add_error(self, error: Exception) -> None:
        """Add error to recovery context"""
        self.errors.append(error)
        self.attempt_count += 1
    
    def should_retry(self) -> bool:
        """Check if operation should be retried"""
        if self.attempt_count >= self.max_attempts:
            return False
        
        # Only retry certain error types
        if self.errors:
            last_error = self.errors[-1]
            return isinstance(last_error, (DataError, OSError, IOError))
        
        return True