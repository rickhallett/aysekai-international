"""Global error handling and user-friendly error messages"""

import sys
import functools
import traceback
from pathlib import Path
from datetime import datetime
from typing import Callable, Optional, Type, Any, List
import time

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from ..core.exceptions import (
    ValidationError,
    DataError,
    ConfigurationError,
)


# Default console for error output
_console = Console(stderr=True)


def format_user_error(error: Exception) -> str:
    """
    Format error message for user display.
    
    Args:
        error: Exception to format
        
    Returns:
        User-friendly error message
    """
    error_messages = {
        ValidationError: {
            "prefix": "Input validation failed",
            "suffix": "Please check your input and try again.",
        },
        DataError: {
            "prefix": "Data access problem",
            "suffix": "Please ensure the CSV files are properly installed.",
        },
        ConfigurationError: {
            "prefix": "Configuration issue",
            "suffix": "Please check your settings and environment variables.",
        },
    }
    
    # Check if this is one of our specific error types
    for exc_type in error_messages:
        if isinstance(error, exc_type):
            config = error_messages[exc_type]
            return f"{config['prefix']}: {str(error)}\n\n{config['suffix']}"
    
    # Generic error
    return (
        f"An error occurred: {str(error)}\n\n"
        "Please try again or report this issue if it persists."
    )


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


def error_boundary(
    console: Optional[Console] = None,
    error_log: Optional[Path] = None
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
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
                
            except ValidationError as e:
                console.print(Panel(
                    format_user_error(e),
                    title="⚠️  Invalid Input",
                    border_style="red",
                    padding=(1, 2),
                ))
                sys.exit(1)
                
            except DataError as e:
                console.print(Panel(
                    format_user_error(e),
                    title="📁 Data Problem",
                    border_style="red",
                    padding=(1, 2),
                ))
                sys.exit(2)
                
            except ConfigurationError as e:
                console.print(Panel(
                    format_user_error(e),
                    title="⚙️  Configuration Problem",
                    border_style="red",
                    padding=(1, 2),
                ))
                sys.exit(3)
                
            except KeyboardInterrupt:
                console.print(
                    "\n[yellow]Meditation interrupted. Ma'a salama! 🌙[/yellow]"
                )
                sys.exit(0)
                
            except Exception as e:
                # Log the full error for debugging
                log_path = log_error(e, error_log)
                
                # Show user-friendly message
                console.print(Panel(
                    Text.from_markup(
                        "[red]An unexpected error occurred.[/red]\n\n"
                        f"Error details have been saved to:\n{log_path}\n\n"
                        "Please report this issue if it continues.",
                        justify="center",
                    ),
                    title="❌ Unexpected Error",
                    border_style="red",
                    padding=(1, 2),
                ))
                sys.exit(99)
        
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
    if console is None:
        console = _console
    
    def exception_handler(
        exc_type: Type[BaseException],
        exc_value: BaseException,
        exc_traceback: Any
    ) -> None:
        """Handle uncaught exceptions"""
        if issubclass(exc_type, KeyboardInterrupt):
            # Handle Ctrl+C gracefully
            console.print(
                "\n[yellow]Interrupted. Ma'a salama! 🌙[/yellow]"
            )
            sys.exit(0)
        
        # Log the error
        if exc_value and isinstance(exc_value, Exception):
            log_path = log_error(exc_value, error_log)
        else:
            log_path = error_log or Path.home() / ".aysekai" / "error.log"
        
        # Show user-friendly message
        console.print(Panel(
            Text.from_markup(
                "[red]An unexpected error occurred.[/red]\n\n"
                f"Error details have been saved to:\n{log_path}\n\n"
                "Please report this issue.",
                justify="center",
            ),
            title="❌ Unexpected Error",
            border_style="red",
            padding=(1, 2),
        ))
        
        sys.exit(99)
    
    sys.excepthook = exception_handler


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