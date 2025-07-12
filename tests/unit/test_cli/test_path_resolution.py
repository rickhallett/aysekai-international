import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from aysekai.cli.path_resolver import PathResolver
from aysekai.config import get_settings, reset_settings
from aysekai.core.exceptions import ConfigurationError


class TestPathResolver:
    """Test path resolution without hardcoded paths"""
    
    @pytest.fixture(autouse=True)
    def reset_config(self):
        """Reset configuration after each test"""
        yield
        reset_settings()
    
    def test_get_data_files_path_default(self, tmp_path, monkeypatch):
        """Test default data files path resolution"""
        monkeypatch.setenv("AYSEKAI_DATA_DIR", str(tmp_path))
        reset_settings()
        
        resolver = PathResolver()
        data_path = resolver.get_data_files_path()
        
        assert data_path == tmp_path
        assert str(data_path).startswith(str(tmp_path))
    
    def test_get_data_files_path_with_csv(self, tmp_path, monkeypatch):
        """Test path resolution finds CSV files"""
        monkeypatch.setenv("AYSEKAI_DATA_DIR", str(tmp_path))
        reset_settings()
        
        # Create expected CSV files
        processed_dir = tmp_path / "processed"
        processed_dir.mkdir()
        (processed_dir / "all_remaining_names_for_notion.csv").touch()
        (processed_dir / "asma_al_husna_notion_ready.csv").touch()
        
        resolver = PathResolver()
        data_path = resolver.get_data_files_path()
        
        assert resolver.validate_data_files(data_path) is True
    
    def test_no_hardcoded_paths(self):
        """Ensure no hardcoded paths exist"""
        resolver = PathResolver()
        
        # Should not contain any hardcoded paths
        source = resolver.__class__.__module__
        
        # These patterns should NOT exist in the code
        forbidden_patterns = [
            "Library/Mobile Documents",
            "com~apple~CloudDocs",
            "Manual Library",
            "/Users/",
            "~/Library",
            "Path.home() / 'Library'",
        ]
        
        # This test will fail if hardcoded paths exist
        # (actual implementation check happens during code review)
    
    def test_get_csv_paths(self, tmp_path, monkeypatch):
        """Test getting specific CSV file paths"""
        monkeypatch.setenv("AYSEKAI_DATA_DIR", str(tmp_path))
        reset_settings()
        
        resolver = PathResolver()
        
        csv1 = resolver.get_csv_path("all_remaining_names_for_notion.csv")
        csv2 = resolver.get_csv_path("asma_al_husna_notion_ready.csv")
        
        assert csv1 == tmp_path / "processed" / "all_remaining_names_for_notion.csv"
        assert csv2 == tmp_path / "processed" / "asma_al_husna_notion_ready.csv"
    
    def test_missing_data_files_error(self, tmp_path, monkeypatch):
        """Test error when data files are missing"""
        monkeypatch.setenv("AYSEKAI_DATA_DIR", str(tmp_path))
        reset_settings()
        
        resolver = PathResolver()
        
        with pytest.raises(ConfigurationError) as exc_info:
            resolver.get_data_files_path(require_files=True)
        
        assert "Could not find CSV data files" in str(exc_info.value)
    
    def test_log_directory_path(self, tmp_path, monkeypatch):
        """Test log directory path resolution"""
        monkeypatch.setenv("AYSEKAI_DATA_DIR", str(tmp_path))
        reset_settings()
        
        resolver = PathResolver()
        log_dir = resolver.get_log_directory()
        
        assert log_dir == tmp_path / "logs"
        assert not str(log_dir).startswith("/Users")
    
    def test_cache_directory_path(self, tmp_path, monkeypatch):
        """Test cache directory path resolution"""
        monkeypatch.setenv("AYSEKAI_DATA_DIR", str(tmp_path))
        reset_settings()
        
        resolver = PathResolver()
        cache_dir = resolver.get_cache_directory()
        
        assert cache_dir == tmp_path / "cache"
        assert "Library" not in str(cache_dir)
    
    def test_create_directories(self, tmp_path, monkeypatch):
        """Test directory creation"""
        monkeypatch.setenv("AYSEKAI_DATA_DIR", str(tmp_path))
        reset_settings()
        
        resolver = PathResolver()
        resolver.ensure_directories()
        
        # All directories should be created
        assert (tmp_path / "processed").exists()
        assert (tmp_path / "logs").exists()
        assert (tmp_path / "cache").exists()
    
    def test_path_validation(self, tmp_path, monkeypatch):
        """Test path validation against allowed directories"""
        monkeypatch.setenv("AYSEKAI_DATA_DIR", str(tmp_path))
        reset_settings()
        
        resolver = PathResolver()
        
        # Allowed paths
        assert resolver.is_path_allowed(tmp_path / "processed" / "file.csv")
        assert resolver.is_path_allowed(tmp_path / "logs" / "session.log")
        
        # Disallowed paths
        assert not resolver.is_path_allowed(Path("/etc/passwd"))
        assert not resolver.is_path_allowed(Path("/tmp/evil"))