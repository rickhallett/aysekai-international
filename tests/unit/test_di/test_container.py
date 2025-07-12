"""Tests for DI container functionality"""

import pytest
from typing import Protocol, runtime_checkable
from unittest.mock import Mock

from src.aysekai.di.container import DIContainer
from src.aysekai.di.interfaces import DataReader, RandomSelector, PathResolver


@runtime_checkable  
class ITestService(Protocol):
    """Test service interface"""
    def do_something(self) -> str: ...


class ConcreteTestService:
    """Concrete implementation for testing"""
    def __init__(self, message: str = "default"):
        self.message = message
    
    def do_something(self) -> str:
        return f"Service says: {self.message}"


class TestDIContainer:
    """Test DI container functionality"""
    
    def test_container_creation(self):
        """Test that DI container can be created"""
        container = DIContainer()
        assert container is not None
    
    def test_register_singleton_service(self):
        """Test registering singleton services"""
        container = DIContainer()
        container.register_singleton(ITestService, ConcreteTestService)
        
        # Should return same instance each time
        service1 = container.get(ITestService)
        service2 = container.get(ITestService)
        
        assert service1 is service2
        assert isinstance(service1, ConcreteTestService)
        assert service1.do_something() == "Service says: default"
    
    def test_register_factory_service(self):
        """Test registering factory-created services"""
        container = DIContainer()
        
        def test_factory() -> ITestService:
            return ConcreteTestService("from factory")
        
        container.register_factory(ITestService, test_factory)
        
        # Should create new instance each time
        service1 = container.get(ITestService)
        service2 = container.get(ITestService)
        
        assert service1 is not service2
        assert isinstance(service1, ConcreteTestService)
        assert service1.do_something() == "Service says: from factory"
    
    def test_register_instance(self):
        """Test registering pre-created instances"""
        container = DIContainer()
        instance = ConcreteTestService("pre-created")
        
        container.register_instance(ITestService, instance)
        
        service = container.get(ITestService)
        assert service is instance
        assert service.do_something() == "Service says: pre-created"
    
    def test_dependency_injection_with_constructor_args(self):
        """Test that constructor dependencies are injected"""
        container = DIContainer()
        
        class ServiceWithDependency:
            def __init__(self, dependency: ITestService):
                self.dependency = dependency
        
        container.register_singleton(ITestService, ConcreteTestService)
        container.register_singleton(ServiceWithDependency, ServiceWithDependency)
        
        service = container.get(ServiceWithDependency)
        assert isinstance(service.dependency, ConcreteTestService)
    
    def test_unregistered_service_raises_error(self):
        """Test that requesting unregistered service raises error"""
        container = DIContainer()
        
        with pytest.raises(KeyError, match="Service.*not registered"):
            container.get(ITestService)
    
    def test_container_scope_isolation(self):
        """Test that scoped containers can override registrations"""
        parent = DIContainer()
        parent.register_singleton(ITestService, ConcreteTestService)
        
        child = parent.create_scope()
        child.register_instance(ITestService, ConcreteTestService("scoped"))
        
        # Parent should have original registration
        parent_service = parent.get(ITestService)
        assert parent_service.do_something() == "Service says: default"
        
        # Child should have scoped registration
        child_service = child.get(ITestService)
        assert child_service.do_something() == "Service says: scoped"
    
    def test_dispose_releases_resources(self):
        """Test that dispose cleans up container resources"""
        container = DIContainer()
        container.register_singleton(ITestService, ConcreteTestService)
        
        # Get service to ensure it's created
        service = container.get(ITestService)
        assert service is not None
        
        # Dispose container
        container.dispose()
        
        # Should raise error after disposal
        with pytest.raises(RuntimeError, match="Container has been disposed"):
            container.get(ITestService)


class TestServiceRegistration:
    """Test service registration utilities"""
    
    def test_register_core_services(self):
        """Test that core application services can be registered"""
        container = DIContainer()
        
        # Should be able to register our main service types
        container.register_singleton(DataReader, Mock)
        container.register_singleton(RandomSelector, Mock)
        container.register_singleton(PathResolver, Mock)
        
        # Should be able to retrieve them
        data_reader = container.get(DataReader)
        random_selector = container.get(RandomSelector) 
        path_resolver = container.get(PathResolver)
        
        assert data_reader is not None
        assert random_selector is not None
        assert path_resolver is not None
    
    def test_service_factory_with_dependencies(self):
        """Test factory that creates services with their own dependencies"""
        container = DIContainer()
        
        class AnotherService:
            def __init__(self, dependency: ITestService):
                self.dependency = dependency
            
            def get_message(self):
                return f"with {self.dependency.message}"
        
        # Register dependency first
        container.register_singleton(ITestService, ConcreteTestService)
        
        # Register service that needs dependency using constructor injection
        container.register_singleton(AnotherService, AnotherService)
        
        service = container.get(AnotherService)
        assert "with default" in service.get_message()


class TestDIIntegration:
    """Test DI integration scenarios"""
    
    def test_can_create_test_container_with_mocks(self):
        """Test creating container with mocked services for testing"""
        container = DIContainer()
        
        # Register mocks for testing
        mock_reader = Mock(spec=DataReader)
        mock_selector = Mock(spec=RandomSelector)
        
        container.register_instance(DataReader, mock_reader)
        container.register_instance(RandomSelector, mock_selector)
        
        # Verify mocks are returned
        reader = container.get(DataReader)
        selector = container.get(RandomSelector)
        
        assert reader is mock_reader
        assert selector is mock_selector
    
    def test_container_can_be_configured_for_production(self):
        """Test that container can be configured with real services"""
        container = DIContainer()
        
        # This should work once we implement the real services
        # For now, just test the registration pattern
        def data_reader_factory():
            # Would create real CSVDataReader
            return Mock(spec=DataReader)
        
        def random_selector_factory():
            # Would create real UltraRandomSelector  
            return Mock(spec=RandomSelector)
        
        container.register_factory(DataReader, data_reader_factory)
        container.register_factory(RandomSelector, random_selector_factory)
        
        # Should be able to get configured services
        reader = container.get(DataReader)
        selector = container.get(RandomSelector)
        
        assert reader is not None
        assert selector is not None