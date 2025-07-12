"""Integration tests for CLI error handling with real commands"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock
from typer.testing import CliRunner

from src.aysekai.cli.main import app
from src.aysekai.core.exceptions import ValidationError, DataError, SystemError
from src.aysekai.cli.dependencies import set_container, setup_test_container


class TestCLIErrorIntegration:
    """Test error handling integration with actual CLI commands"""
    
    def setup_method(self):
        """Set up test environment with test container"""
        self.runner = CliRunner()
        self.test_container = setup_test_container()
        set_container(self.test_container)
    
    def teardown_method(self):
        """Clean up test environment"""
        # Reset to default container
        set_container(None)
    
    def test_meditate_command_handles_validation_error(self):
        """Test meditate command handles validation errors gracefully"""
        # Configure mock to raise validation error
        mock_reader = self.test_container.get(DataReader)
        mock_reader.read_all_names.side_effect = ValidationError(
            "Invalid data format",
            field="csv_data"
        )
        
        result = self.runner.invoke(app, ['meditate'])
        
        assert result.exit_code == 1
        assert "Input Error" in result.stdout
        assert "Invalid data format" in result.stdout
        # Technical details should not be in output
        assert "csv_data" not in result.stdout
    
    def test_meditate_command_handles_data_error(self):
        """Test meditate command handles data errors gracefully"""
        # Configure mock to raise data error
        mock_reader = self.test_container.get(DataReader)
        mock_reader.read_all_names.side_effect = DataError(
            "CSV file corrupted",
            file_path=Path("/data/names.csv"),
            line_number=42
        )
        
        result = self.runner.invoke(app, ['meditate'])
        
        assert result.exit_code == 1
        assert "Data Error" in result.stdout
        assert "meditation data" in result.stdout
        # File paths should not be in user output
        assert "/data/names.csv" not in result.stdout
        assert "42" not in result.stdout
    
    def test_meditate_command_handles_system_error(self):
        """Test meditate command handles system errors gracefully"""
        # Configure mock to raise system error
        mock_reader = self.test_container.get(DataReader)
        mock_reader.read_all_names.side_effect = SystemError(
            "Permission denied accessing file",
            system_error_code=13,
            component="file_reader"
        )
        
        result = self.runner.invoke(app, ['meditate'])
        
        assert result.exit_code == 1
        assert "System Error" in result.stdout
        assert "permissions" in result.stdout
        # Technical details should not be in output
        assert "13" not in result.stdout
        assert "file_reader" not in result.stdout
    
    def test_meditate_command_handles_unexpected_error(self):
        """Test meditate command handles unexpected errors gracefully"""
        # Configure mock to raise unexpected error
        mock_reader = self.test_container.get(DataReader)
        mock_reader.read_all_names.side_effect = RuntimeError(
            "Unexpected internal error with sensitive data"
        )
        
        result = self.runner.invoke(app, ['meditate'])
        
        assert result.exit_code == 1
        assert "Application Error" in result.stdout
        assert "unexpected error" in result.stdout
        # Sensitive information should not be in output
        assert "sensitive data" not in result.stdout
        assert "internal error" not in result.stdout
    
    def test_list_names_command_handles_validation_error(self):
        """Test list-names command handles validation errors gracefully"""
        # Test with invalid range
        result = self.runner.invoke(app, ['list-names', '100', '200'])
        
        assert result.exit_code == 1
        assert "Input Error" in result.stdout
        assert "range" in result.stdout.lower()
    
    def test_list_names_command_handles_data_error(self):
        """Test list-names command handles data errors gracefully"""
        # Configure mock to raise data error
        mock_reader = self.test_container.get(DataReader)
        mock_reader.read_all_names.side_effect = DataError("No data available")
        
        result = self.runner.invoke(app, ['list-names'])
        
        assert result.exit_code == 1
        assert "Data Error" in result.stdout
    
    def test_about_command_remains_functional_after_errors(self):
        """Test about command works even when other commands have errors"""
        # Configure data reader to fail
        mock_reader = self.test_container.get(DataReader)
        mock_reader.read_all_names.side_effect = DataError("Data unavailable")
        
        # About command should still work
        result = self.runner.invoke(app, ['about'])
        
        assert result.exit_code == 0
        assert "Aysekai" in result.stdout
        assert "Islamic Meditation CLI" in result.stdout
    
    def test_error_logging_integration(self):
        """Test errors are properly logged during CLI execution"""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "error.log"
            
            # Configure error with logging
            mock_reader = self.test_container.get(DataReader)
            mock_reader.read_all_names.side_effect = DataError(
                "Test error for logging",
                file_path=Path("/test.csv")
            )
            
            with patch('src.aysekai.cli.error_handler.get_log_file', return_value=log_file):
                result = self.runner.invoke(app, ['meditate'])
            
            assert result.exit_code == 1
            
            # Check log file was created and contains error details
            assert log_file.exists()
            log_content = log_file.read_text()
            assert "DataError" in log_content
            assert "Test error for logging" in log_content
            assert "/test.csv" in log_content  # Technical details in logs
    
    def test_multiple_error_scenarios_in_session(self):
        """Test handling multiple different errors in same session"""
        # First command with validation error
        result1 = self.runner.invoke(app, ['list-names', '0', '200'])
        assert result1.exit_code == 1
        assert "Input Error" in result1.stdout
        
        # Second command with data error
        mock_reader = self.test_container.get(DataReader)
        mock_reader.read_all_names.side_effect = DataError("Data error")
        
        result2 = self.runner.invoke(app, ['meditate'])
        assert result2.exit_code == 1
        assert "Data Error" in result2.stdout
        
        # Third command should still work if no errors
        mock_reader.read_all_names.side_effect = None
        mock_reader.read_all_names.return_value = []
        
        result3 = self.runner.invoke(app, ['about'])
        assert result3.exit_code == 0


class TestErrorRecoveryIntegration:
    """Test error recovery and graceful degradation in CLI commands"""
    
    def setup_method(self):
        """Set up test environment"""
        self.runner = CliRunner()
        self.test_container = setup_test_container()
        set_container(self.test_container)
    
    def teardown_method(self):
        """Clean up test environment"""
        set_container(None)
    
    def test_graceful_degradation_with_partial_data(self):
        """Test commands can work with partial data when available"""
        # Configure reader to return partial data instead of failing
        from src.aysekai.core.models import DivineName
        partial_data = [
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
        
        mock_reader = self.test_container.get(DataReader)
        mock_reader.read_all_names.return_value = partial_data
        
        result = self.runner.invoke(app, ['list-names'])
        
        assert result.exit_code == 0
        assert "Ar-Rahman" in result.stdout
        assert "The Compassionate" in result.stdout
    
    def test_fallback_to_defaults_on_config_errors(self):
        """Test commands use sensible defaults when configuration fails"""
        # This test will verify fallback behavior once implemented
        pass
    
    def test_alternative_data_source_fallback(self):
        """Test commands try alternative data sources when primary fails"""
        # This test will verify alternative data source logic once implemented
        pass


class TestUserExperienceIntegration:
    """Test user experience aspects of error handling"""
    
    def setup_method(self):
        """Set up test environment"""
        self.runner = CliRunner()
    
    def test_error_messages_are_respectful_for_sacred_content(self):
        """Test error messages maintain respectful tone for sacred content"""
        # Configure a data error related to sacred content
        with patch('src.aysekai.cli.dependencies.setup_production_container') as mock_setup:
            mock_container = Mock()
            mock_reader = Mock()
            mock_reader.read_all_names.side_effect = DataError(
                "Sacred content validation failed"
            )
            mock_container.get.return_value = mock_reader
            mock_setup.return_value = mock_container
            
            result = self.runner.invoke(app, ['meditate'])
            
            assert result.exit_code == 1
            # Check that error message is respectful
            assert "meditation data" in result.stdout
            # Should not expose technical validation details
            assert "validation failed" not in result.stdout
    
    def test_error_messages_provide_helpful_guidance(self):
        """Test error messages provide actionable guidance to users"""
        # Test validation error guidance
        result = self.runner.invoke(app, ['list-names', '0'])
        
        assert result.exit_code == 1
        output = result.stdout.lower()
        # Should provide helpful guidance
        assert any(word in output for word in ["please", "try", "should", "between"])
    
    def test_error_output_formatting_consistency(self):
        """Test error output formatting is consistent across commands"""
        # This test will verify consistent error formatting once implemented
        pass


class TestSecurityIntegration:
    """Test security aspects of CLI error handling"""
    
    def setup_method(self):
        """Set up test environment"""
        self.runner = CliRunner()
    
    def test_no_sensitive_paths_exposed_in_errors(self):
        """Test internal file paths are not exposed in CLI errors"""
        with patch('src.aysekai.cli.dependencies.setup_production_container') as mock_setup:
            mock_container = Mock()
            mock_reader = Mock()
            mock_reader.read_all_names.side_effect = DataError(
                "File access error",
                file_path=Path("/internal/sensitive/path/data.csv")
            )
            mock_container.get.return_value = mock_reader
            mock_setup.return_value = mock_container
            
            result = self.runner.invoke(app, ['meditate'])
            
            assert result.exit_code == 1
            assert "/internal/sensitive/path" not in result.stdout
    
    def test_no_stack_traces_in_cli_output(self):
        """Test stack traces are never shown in CLI output"""
        with patch('src.aysekai.cli.dependencies.setup_production_container') as mock_setup:
            mock_container = Mock()
            mock_reader = Mock()
            mock_reader.read_all_names.side_effect = RuntimeError(
                "Internal error with stack trace"
            )
            mock_container.get.return_value = mock_reader
            mock_setup.return_value = mock_container
            
            result = self.runner.invoke(app, ['meditate'])
            
            assert result.exit_code == 1
            # Should not contain stack trace elements
            assert "Traceback" not in result.stdout
            assert "File \"" not in result.stdout
            assert "line " not in result.stdout
    
    def test_no_environment_variables_exposed_in_errors(self):
        """Test environment variables are not exposed in error messages"""
        # This test will verify environment variable protection once implemented
        pass


class TestPerformanceIntegration:
    """Test performance aspects of error handling"""
    
    def test_error_handling_minimal_overhead(self):
        """Test error handling adds minimal performance overhead"""
        # This test will measure error handling performance once implemented
        pass
    
    def test_error_recovery_performance(self):
        """Test error recovery doesn't significantly impact performance"""
        # This test will measure recovery performance once implemented
        pass