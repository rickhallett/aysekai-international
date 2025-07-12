"""Tests for CLI dependency injection integration"""

import pytest
from unittest.mock import Mock, patch
from typer.testing import CliRunner

from src.aysekai.core.models import DivineName
from src.aysekai.di.interfaces import DataReader, RandomSelector, PathResolver, SessionLogger
from src.aysekai.di.container import DIContainer
from src.aysekai.cli.main import app


class TestCLIDependencyInjection:
    """Test CLI commands use dependency injection properly"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.runner = CliRunner()
        self.container = DIContainer()
        
        # Create test data
        self.test_name = DivineName(
            number=1,
            arabic="الرحمن",
            transliteration="Ar-Rahman",
            brief_meaning="The Compassionate",
            level_1_sharia="The divine quality of mercy in Islamic law",
            level_2_tariqa="The path of compassion in spiritual practice", 
            level_3_haqiqa="The reality of divine mercy as experienced truth",
            level_4_marifa="The gnosis of mercy as the essence of existence",
            quranic_references="Mentioned 169 times in the Quran",
            dhikr_formulas="Ya Rahman (O Compassionate One) - 99 times daily",
            pronunciation_guide="ar-rah-MAHN"
        )
    
    def test_meditate_command_uses_injected_dependencies(self):
        """Test that meditate command gets dependencies from DI container"""
        # Arrange - Set up mocks
        mock_reader = Mock(spec=DataReader)
        mock_selector = Mock(spec=RandomSelector) 
        mock_logger = Mock(spec=SessionLogger)
        mock_resolver = Mock(spec=PathResolver)
        
        mock_reader.read_all_names.return_value = [self.test_name]
        mock_selector.select_random_name.return_value = self.test_name
        
        # Register mocks in container
        self.container.register_instance(DataReader, mock_reader)
        self.container.register_instance(RandomSelector, mock_selector)
        self.container.register_instance(SessionLogger, mock_logger)
        self.container.register_instance(PathResolver, mock_resolver)
        
        # Act - Run command with DI container
        with patch('src.aysekai.cli.main.get_container', return_value=self.container):
            result = self.runner.invoke(app, ['meditate'])
        
        # Assert - Verify dependencies were used
        assert result.exit_code == 0
        mock_reader.read_all_names.assert_called_once()
        mock_selector.select_random_name.assert_called_once()
        mock_logger.log_session.assert_called_once()
    
    def test_meditate_command_handles_dependency_errors(self):
        """Test meditate command gracefully handles dependency errors"""
        # Arrange - Set up failing mock
        mock_reader = Mock(spec=DataReader)
        mock_reader.read_all_names.side_effect = FileNotFoundError("CSV file not found")
        
        self.container.register_instance(DataReader, mock_reader)
        
        # Act - Run command that should fail gracefully
        with patch('src.aysekai.cli.main.get_container', return_value=self.container):
            result = self.runner.invoke(app, ['meditate'])
        
        # Assert - Should exit with error but show user-friendly message  
        assert result.exit_code != 0  # Accept any non-zero exit code
        assert "CSV file" in result.output or "data" in result.output.lower() or "error" in result.output.lower()
    
    def test_list_names_command_uses_injected_dependencies(self):
        """Test that list-names command uses dependency injection"""
        # Arrange
        mock_reader = Mock(spec=DataReader)
        names = [self.test_name]
        mock_reader.read_all_names.return_value = names
        
        self.container.register_instance(DataReader, mock_reader)
        
        # Act
        with patch('src.aysekai.cli.main.get_container', return_value=self.container):
            result = self.runner.invoke(app, ['list-names'])
        
        # Assert
        assert result.exit_code == 0
        mock_reader.read_all_names.assert_called_once()
        assert "Ar-Rahman" in result.output
    
    def test_list_names_with_range_uses_injected_dependencies(self):
        """Test list-names with range parameter uses DI"""
        # Arrange
        mock_reader = Mock(spec=DataReader)
        names = [self.test_name]
        mock_reader.read_all_names.return_value = names
        
        self.container.register_instance(DataReader, mock_reader)
        
        # Act
        with patch('src.aysekai.cli.main.get_container', return_value=self.container):
            result = self.runner.invoke(app, ['list-names', '1', '10'])
        
        # Assert
        assert result.exit_code == 0
        mock_reader.read_all_names.assert_called_once()
    
    def test_cli_commands_dont_create_services_directly(self):
        """Test that CLI commands don't instantiate services directly"""
        # This test ensures we've removed hard dependencies
        
        # Check that imports don't include direct service instantiation
        import src.aysekai.cli.main as main_module
        import inspect
        
        # Get source code of main module
        source = inspect.getsource(main_module)
        
        # Should not have direct instantiation of these classes
        forbidden_instantiations = [
            'AsmaCSVReader(',
            'UltraRandomizer(',
            'SessionLogger(',
            'DataLoader(',
        ]
        
        for instantiation in forbidden_instantiations:
            assert instantiation not in source, f"Found forbidden instantiation: {instantiation}"
    
    def test_container_setup_for_production(self):
        """Test that production container can be set up properly"""
        from src.aysekai.cli.dependencies import setup_production_container
        
        # Should be able to create production container
        container = setup_production_container()
        
        # Should have all required services registered
        data_reader = container.get(DataReader)
        random_selector = container.get(RandomSelector)
        path_resolver = container.get(PathResolver)
        session_logger = container.get(SessionLogger)
        
        assert data_reader is not None
        assert random_selector is not None
        assert path_resolver is not None
        assert session_logger is not None
    
    def test_container_setup_for_testing(self):
        """Test that test container can be set up with mocks"""
        from src.aysekai.cli.dependencies import setup_test_container
        
        # Should be able to create test container with mocks
        container = setup_test_container()
        
        # All services should be mocks
        data_reader = container.get(DataReader)
        random_selector = container.get(RandomSelector)
        
        # Should be mock objects (can check by looking for mock attributes)
        assert hasattr(data_reader, 'assert_called_once') or hasattr(data_reader, '_mock_name')
        assert hasattr(random_selector, 'assert_called_once') or hasattr(random_selector, '_mock_name')


class TestDependencyDecorator:
    """Test the dependency injection decorator functionality"""
    
    def test_inject_dependencies_decorator_works(self):
        """Test that @inject_dependencies decorator properly injects services"""
        from src.aysekai.di.decorators import inject_dependencies, Depends
        
        # Set up container with test service
        container = DIContainer()
        mock_reader = Mock(spec=DataReader)
        container.register_instance(DataReader, mock_reader)
        
        # Define function that uses dependency injection
        @inject_dependencies(container)
        def test_function(reader: DataReader = Depends()):
            return reader
        
        # Call function - should get injected dependency
        result = test_function()
        assert result is mock_reader
    
    def test_depends_marker_identifies_dependencies(self):
        """Test that Depends() properly marks parameters for injection"""
        from src.aysekai.di.decorators import Depends, get_dependencies
        
        def example_function(
            reader: DataReader = Depends(),
            selector: RandomSelector = Depends(),
            normal_param: str = "default"
        ):
            pass
        
        # Should be able to identify which parameters need injection
        dependencies = get_dependencies(example_function)
        
        assert DataReader in dependencies
        assert RandomSelector in dependencies
        assert len(dependencies) == 2  # Only the Depends() parameters
    
    def test_decorator_preserves_function_metadata(self):
        """Test that decorator preserves original function information"""
        from src.aysekai.di.decorators import inject_dependencies
        
        container = DIContainer()
        
        @inject_dependencies(container)
        def example_function(reader: DataReader = None):
            """Example function docstring"""
            return "result"
        
        # Should preserve function name and docstring
        assert example_function.__name__ == "example_function"
        assert "Example function docstring" in example_function.__doc__
    
    def test_decorator_handles_mixed_parameters(self):
        """Test decorator with both injected and regular parameters"""
        from src.aysekai.di.decorators import inject_dependencies, Depends
        
        container = DIContainer()
        mock_reader = Mock(spec=DataReader)
        container.register_instance(DataReader, mock_reader)
        
        @inject_dependencies(container)
        def mixed_function(
            regular_param: str,
            reader: DataReader = Depends(),
            optional_param: str = "default"
        ):
            return f"{regular_param}, {reader}, {optional_param}"
        
        # Should inject reader but keep other parameters normal
        result = mixed_function("test")
        assert "test" in result
        assert str(mock_reader) in result
        assert "default" in result