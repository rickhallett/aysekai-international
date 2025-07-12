"""Simple dependency injection container implementation"""

from typing import Type, TypeVar, Dict, Any, Callable, Optional
import inspect
from contextlib import contextmanager

T = TypeVar('T')


class DIContainer:
    """Simple dependency injection container"""
    
    def __init__(self, parent: Optional['DIContainer'] = None):
        self._services: Dict[Type, Any] = {}
        self._factories: Dict[Type, Callable] = {}
        self._singletons: Dict[Type, Any] = {}
        self._parent = parent
        self._disposed = False
    
    def register_singleton(self, interface: Type[T], implementation: Type[T]) -> None:
        """Register a service as singleton (one instance for container lifetime)"""
        self._check_not_disposed()
        
        def factory():
            return self._create_instance(implementation)
        
        self._factories[interface] = factory
        # Mark as singleton
        if interface not in self._singletons:
            self._singletons[interface] = None
    
    def register_factory(self, interface: Type[T], factory: Callable[[], T]) -> None:
        """Register a factory function that creates new instances each time"""
        self._check_not_disposed()
        self._factories[interface] = factory
    
    def register_factory_with_container(self, interface: Type[T], factory: Callable[['DIContainer'], T]) -> None:
        """Register a factory that receives the container as parameter"""
        self._check_not_disposed()
        
        def wrapper():
            return factory(self)
        
        self._factories[interface] = wrapper
    
    def register_instance(self, interface: Type[T], instance: T) -> None:
        """Register a pre-created instance"""
        self._check_not_disposed()
        self._services[interface] = instance
    
    def get(self, interface: Type[T]) -> T:
        """Get service instance for the given interface"""
        self._check_not_disposed()
        
        # Check if we have a direct instance
        if interface in self._services:
            return self._services[interface]
        
        # Check if we have a singleton that's already created
        if interface in self._singletons and self._singletons[interface] is not None:
            return self._singletons[interface]
        
        # Check if we have a factory
        if interface in self._factories:
            instance = self._factories[interface]()
            
            # If this is a singleton, store it
            if interface in self._singletons:
                self._singletons[interface] = instance
            
            return instance
        
        # Check parent container
        if self._parent:
            return self._parent.get(interface)
        
        # Service not found
        raise KeyError(f"Service {interface} is not registered in the container")
    
    def create_scope(self) -> 'DIContainer':
        """Create a child container that can override parent registrations"""
        return DIContainer(parent=self)
    
    @contextmanager
    def scope(self):
        """Context manager for scoped container usage"""
        scoped_container = self.create_scope()
        try:
            yield scoped_container
        finally:
            scoped_container.dispose()
    
    def dispose(self) -> None:
        """Clean up container resources"""
        self._services.clear()
        self._factories.clear()
        self._singletons.clear()
        self._disposed = True
    
    def _check_not_disposed(self):
        """Check if container has been disposed"""
        if self._disposed:
            raise RuntimeError("Container has been disposed")
    
    def _create_instance(self, implementation: Type[T]) -> T:
        """Create instance with dependency injection"""
        # Get constructor signature
        sig = inspect.signature(implementation.__init__)
        
        # Build arguments for constructor
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            
            # Try to inject dependency
            if param.annotation != inspect.Parameter.empty:
                try:
                    kwargs[param_name] = self.get(param.annotation)
                except KeyError:
                    # If dependency not found and parameter has default, skip
                    if param.default == inspect.Parameter.empty:
                        raise
        
        return implementation(**kwargs)