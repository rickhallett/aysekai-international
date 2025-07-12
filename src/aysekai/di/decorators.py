"""Dependency injection decorators and utilities"""

from typing import Callable, TypeVar, Dict, Type, Any, get_type_hints, Optional
import inspect
import functools

from .container import DIContainer

F = TypeVar('F', bound=Callable[..., Any])


class Depends:
    """Marker class to indicate a parameter should be injected"""
    
    def __init__(self, service_type: Optional[Type] = None):
        self.service_type = service_type


def inject_dependencies(container: DIContainer) -> Callable[[F], F]:
    """Decorator to inject dependencies into function parameters"""
    
    def decorator(func: F) -> F:
        # Get type hints and signature
        type_hints = get_type_hints(func)
        sig = inspect.signature(func)
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Inject dependencies for parameters marked with Depends()
            injected_kwargs = kwargs.copy()
            
            for param_name, param in sig.parameters.items():
                # Skip if already provided in kwargs
                if param_name in kwargs:
                    continue
                
                # Check if parameter has Depends() as default
                if isinstance(param.default, Depends):
                    # Get service type from type hint
                    service_type = type_hints.get(param_name)
                    if service_type:
                        injected_kwargs[param_name] = container.get(service_type)
            
            return func(*args, **injected_kwargs)
        
        return wrapper  # type: ignore
    
    return decorator


def get_dependencies(func: Callable) -> Dict[Type, str]:
    """Extract dependency types from function signature"""
    dependencies = {}
    type_hints = get_type_hints(func)
    sig = inspect.signature(func)
    
    for param_name, param in sig.parameters.items():
        if isinstance(param.default, Depends):
            service_type = type_hints.get(param_name)
            if service_type:
                dependencies[service_type] = param_name
    
    return dependencies