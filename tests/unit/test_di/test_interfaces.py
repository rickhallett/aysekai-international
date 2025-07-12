"""Tests for service interfaces and protocols"""

import pytest
from typing import List
from pathlib import Path
from unittest.mock import Mock

from src.aysekai.core.models import DivineName
from src.aysekai.di.interfaces import DataReader, RandomSelector, PathResolver, SessionLogger


class TestDataReaderInterface:
    """Test DataReader protocol compliance"""
    
    def test_data_reader_protocol_methods(self):
        """Test that DataReader protocol has required methods"""
        # Create a mock that implements the protocol
        mock_reader = Mock(spec=DataReader)
        
        # Configure mock return values
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
        
        mock_reader.read_all_names.return_value = test_names
        mock_reader.get_name_by_number.return_value = test_names[0]
        
        # Test protocol methods exist and work
        names = mock_reader.read_all_names()
        assert len(names) == 1
        assert isinstance(names[0], DivineName)
        
        name = mock_reader.get_name_by_number(1)
        assert isinstance(name, DivineName)
        assert name.number == 1
    
    def test_data_reader_handles_errors(self):
        """Test DataReader error handling"""
        mock_reader = Mock(spec=DataReader)
        
        # Test that it can raise appropriate errors
        mock_reader.get_name_by_number.side_effect = ValueError("Name not found")
        
        with pytest.raises(ValueError, match="Name not found"):
            mock_reader.get_name_by_number(999)


class TestRandomSelectorInterface:
    """Test RandomSelector protocol compliance"""
    
    def test_random_selector_protocol_methods(self):
        """Test that RandomSelector protocol has required methods"""
        mock_selector = Mock(spec=RandomSelector)
        
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
        
        mock_selector.select_random_name.return_value = test_name
        mock_selector.get_entropy_report.return_value = {"sources": ["crypto", "time"]}
        
        # Test selection method
        names = [test_name]
        selected = mock_selector.select_random_name(names, "test intention")
        assert isinstance(selected, DivineName)
        
        # Test entropy reporting
        report = mock_selector.get_entropy_report()
        assert "sources" in report
    
    def test_random_selector_validates_input(self):
        """Test RandomSelector input validation"""
        mock_selector = Mock(spec=RandomSelector)
        
        # Test empty list handling
        mock_selector.select_random_name.side_effect = ValueError("Empty names list")
        
        with pytest.raises(ValueError, match="Empty names list"):
            mock_selector.select_random_name([], "intention")


class TestPathResolverInterface:
    """Test PathResolver protocol compliance"""
    
    def test_path_resolver_protocol_methods(self):
        """Test that PathResolver protocol has required methods"""
        mock_resolver = Mock(spec=PathResolver)
        
        test_path = Path("/test/data")
        test_files = [Path("/test/data/file1.csv"), Path("/test/data/file2.csv")]
        
        mock_resolver.get_data_path.return_value = test_path
        mock_resolver.list_csv_files.return_value = test_files
        mock_resolver.resolve_path.return_value = test_path / "resolved"
        
        # Test path methods
        data_path = mock_resolver.get_data_path()
        assert isinstance(data_path, Path)
        
        csv_files = mock_resolver.list_csv_files()
        assert isinstance(csv_files, list)
        assert all(isinstance(f, Path) for f in csv_files)
        
        resolved = mock_resolver.resolve_path("some/path")
        assert isinstance(resolved, Path)
    
    def test_path_resolver_handles_missing_paths(self):
        """Test PathResolver handles missing paths gracefully"""
        mock_resolver = Mock(spec=PathResolver)
        
        mock_resolver.get_data_path.side_effect = FileNotFoundError("Data path not found")
        
        with pytest.raises(FileNotFoundError, match="Data path not found"):
            mock_resolver.get_data_path()


class TestSessionLoggerInterface:
    """Test SessionLogger protocol compliance"""
    
    def test_session_logger_protocol_methods(self):
        """Test that SessionLogger protocol has required methods"""
        mock_logger = Mock(spec=SessionLogger)
        
        # Test logging methods
        mock_logger.log_session("test intention", 1, "Ar-Rahman")
        mock_logger.get_session_history.return_value = []
        
        # Call get_session_history to test the method
        history = mock_logger.get_session_history()
        
        # Verify methods were called
        mock_logger.log_session.assert_called_once_with("test intention", 1, "Ar-Rahman")
        mock_logger.get_session_history.assert_called_once()
        assert history == []
    
    def test_session_logger_error_handling(self):
        """Test SessionLogger error handling"""
        mock_logger = Mock(spec=SessionLogger)
        
        # Test that logging errors are handled gracefully
        mock_logger.log_session.side_effect = IOError("Cannot write to log file")
        
        with pytest.raises(IOError, match="Cannot write to log file"):
            mock_logger.log_session("intention", 1, "name")


class TestInterfaceUsage:
    """Test how interfaces work together"""
    
    def test_services_can_be_composed(self):
        """Test that services can use each other via interfaces"""
        # Create mocks for all services
        mock_reader = Mock(spec=DataReader)
        mock_selector = Mock(spec=RandomSelector)
        mock_resolver = Mock(spec=PathResolver)
        mock_logger = Mock(spec=SessionLogger)
        
        test_name = DivineName(
            number=1,
            arabic="الله",
            transliteration="Allah",
            brief_meaning="The One",
            level_1_sharia="",
            level_2_tariqa="",
            level_3_haqiqa="",
            level_4_marifa="",
            quranic_references="",
            dhikr_formulas="",
            pronunciation_guide=""
        )
        
        # Configure mocks to work together
        mock_reader.read_all_names.return_value = [test_name]
        mock_selector.select_random_name.return_value = test_name
        
        # Simulate a meditation session workflow
        names = mock_reader.read_all_names()
        selected = mock_selector.select_random_name(names, "seeking guidance")
        mock_logger.log_session("seeking guidance", selected.number, selected.transliteration)
        
        # Verify the workflow
        mock_reader.read_all_names.assert_called_once()
        mock_selector.select_random_name.assert_called_once_with(names, "seeking guidance")
        mock_logger.log_session.assert_called_once_with("seeking guidance", 1, "Allah")
    
    def test_interface_implementations_are_interchangeable(self):
        """Test that different implementations of same interface are interchangeable"""
        # Create two different mock readers
        csv_reader = Mock(spec=DataReader, name="CSVReader")
        json_reader = Mock(spec=DataReader, name="JSONReader")
        
        test_name = DivineName(
            number=1,
            arabic="الله",
            transliteration="Allah", 
            brief_meaning="The One",
            level_1_sharia="",
            level_2_tariqa="",
            level_3_haqiqa="",
            level_4_marifa="",
            quranic_references="",
            dhikr_formulas="",
            pronunciation_guide=""
        )
        
        # Both should implement the same interface
        csv_reader.read_all_names.return_value = [test_name]
        json_reader.read_all_names.return_value = [test_name]
        
        # Client code should work with either implementation
        def use_reader(reader: DataReader):
            return reader.read_all_names()
        
        csv_result = use_reader(csv_reader)
        json_result = use_reader(json_reader)
        
        assert len(csv_result) == 1
        assert len(json_result) == 1
        assert csv_result[0].transliteration == json_result[0].transliteration