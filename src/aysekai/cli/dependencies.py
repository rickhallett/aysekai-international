"""CLI dependency injection setup and configuration"""

from unittest.mock import Mock
from pathlib import Path
from typing import cast

from ..di.container import DIContainer
from ..di.interfaces import DataReader, RandomSelector, PathResolver, SessionLogger


def setup_production_container() -> DIContainer:
    """Set up DI container with production services"""
    container = DIContainer()
    
    # For now, register mock implementations
    # These will be replaced with real implementations in future iterations
    
    # Data reading service
    def data_reader_factory():
        # TODO: Replace with real CSVDataReader implementation
        from ..core.models import DivineName
        
        mock = Mock(spec=DataReader)
        # Provide test data for production container
        test_names = [
            DivineName(
                number=1,
                arabic="الرحمن",
                transliteration="Ar-Rahman",
                brief_meaning="The Compassionate",
                level_1_sharia="",
                level_2_tariqa="",
                level_3_haqiqa="",
                level_4_marifa="",
                quranic_references="",
                dhikr_formulas="",
                pronunciation_guide=""
            )
        ]
        mock.read_all_names.return_value = test_names
        mock.get_name_by_number.return_value = test_names[0]
        return mock
    
    # Random selection service  
    def random_selector_factory():
        # TODO: Replace with real UltraRandomSelector implementation
        from ..core.models import DivineName
        
        mock = Mock(spec=RandomSelector)
        test_name = DivineName(
            number=33,
            arabic="الكبير", 
            transliteration="Al-Kabir",
            brief_meaning="The Greatest",
            level_1_sharia="",
            level_2_tariqa="",
            level_3_haqiqa="",
            level_4_marifa="",
            quranic_references="",
            dhikr_formulas="",
            pronunciation_guide=""
        )
        mock.select_random_name.return_value = test_name
        mock.get_entropy_report.return_value = {"sources": ["crypto", "time", "hardware"]}
        return mock
    
    # Path resolution service
    def path_resolver_factory():
        # TODO: Replace with real ConfigurablePathResolver implementation
        mock = Mock(spec=PathResolver)
        mock.get_data_path.return_value = Path("/tmp")
        mock.list_csv_files.return_value = []
        mock.resolve_path.return_value = Path("/tmp")
        return mock
    
    # Session logging service
    def session_logger_factory():
        # TODO: Replace with real SessionLogger implementation
        mock = Mock(spec=SessionLogger)
        return mock
    
    # Register services with cast to handle Protocol types
    container.register_factory(cast(type, DataReader), data_reader_factory)
    container.register_factory(cast(type, RandomSelector), random_selector_factory)
    container.register_factory(cast(type, PathResolver), path_resolver_factory)
    container.register_factory(cast(type, SessionLogger), session_logger_factory)
    
    return container


def setup_test_container() -> DIContainer:
    """Set up DI container with test/mock services"""
    container = DIContainer()
    
    # Register mocks for all services
    mock_reader = Mock(spec=DataReader)
    mock_selector = Mock(spec=RandomSelector)
    mock_resolver = Mock(spec=PathResolver)
    mock_logger = Mock(spec=SessionLogger)
    
    # Configure mocks with sensible defaults for testing
    mock_reader.read_all_names.return_value = []
    mock_selector.select_random_name.return_value = None
    mock_selector.get_entropy_report.return_value = {"sources": ["test"]}
    mock_resolver.get_data_path.return_value = Path("/test")
    mock_resolver.list_csv_files.return_value = []
    
    container.register_instance(cast(type, DataReader), mock_reader)
    container.register_instance(cast(type, RandomSelector), mock_selector)
    container.register_instance(cast(type, PathResolver), mock_resolver)
    container.register_instance(cast(type, SessionLogger), mock_logger)
    
    return container


# Global container instance
_container = None


def get_container() -> DIContainer:
    """Get the global DI container instance"""
    global _container
    if _container is None:
        _container = setup_production_container()
    return _container


def set_container(container: DIContainer) -> None:
    """Set the global DI container (useful for testing)"""
    global _container
    _container = container