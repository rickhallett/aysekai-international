import pytest
import os
from pathlib import Path
from pydantic import ValidationError
from aysekai.config.settings import Settings, get_settings


class TestSettings:
    """Test configuration management"""
    
    def test_default_settings(self):
        """Test default settings initialization"""
        settings = Settings()
        
        # Should use safe default paths
        assert settings.data_dir == Path.home() / ".aysekai" / "data"
        assert settings.max_prompt_length == 500
        assert settings.allowed_csv_paths == ["data/processed"]
        assert settings.session_log_encryption is False
        assert settings.cache_enabled is True
        assert settings.cache_ttl == 3600
    
    def test_env_override(self, monkeypatch):
        """Test environment variable override"""
        test_dir = "/tmp/test_aysekai"
        monkeypatch.setenv("AYSEKAI_DATA_DIR", test_dir)
        monkeypatch.setenv("AYSEKAI_MAX_PROMPT_LENGTH", "1000")
        monkeypatch.setenv("AYSEKAI_SESSION_LOG_ENCRYPTION", "true")
        
        settings = Settings()
        
        # On macOS, /tmp resolves to /private/tmp
        expected_path = Path(test_dir).resolve()
        assert settings.data_dir == expected_path
        assert settings.max_prompt_length == 1000
        assert settings.session_log_encryption is True
    
    def test_directory_traversal_prevention(self):
        """Test that directory traversal is prevented"""
        with pytest.raises(ValidationError) as exc_info:
            Settings(data_dir="../../../etc/passwd")
        
        assert "Invalid data directory" in str(exc_info.value)
    
    def test_max_prompt_length_validation(self):
        """Test prompt length constraints"""
        # Too small
        with pytest.raises(ValidationError):
            Settings(max_prompt_length=0)
        
        # Too large
        with pytest.raises(ValidationError):
            Settings(max_prompt_length=1001)
        
        # Valid range
        settings = Settings(max_prompt_length=750)
        assert settings.max_prompt_length == 750
    
    def test_singleton_pattern(self):
        """Test get_settings returns singleton"""
        settings1 = get_settings()
        settings2 = get_settings()
        
        assert settings1 is settings2
    
    def test_env_file_loading(self, tmp_path, monkeypatch):
        """Test loading from .env file"""
        env_file = tmp_path / ".env"
        env_file.write_text(
            "AYSEKAI_DATA_DIR=/custom/data\n"
            "AYSEKAI_CACHE_TTL=7200\n"
        )
        
        monkeypatch.chdir(tmp_path)
        settings = Settings(_env_file=str(env_file))
        
        assert settings.data_dir == Path("/custom/data")
        assert settings.cache_ttl == 7200
    
    def test_case_insensitive_env_vars(self, monkeypatch):
        """Test environment variables are case insensitive"""
        monkeypatch.setenv("aysekai_cache_enabled", "false")
        
        settings = Settings()
        assert settings.cache_enabled is False
    
    def test_path_resolution(self):
        """Test path resolution and normalization"""
        settings = Settings(data_dir="~/aysekai/../.aysekai/data")
        
        # Should resolve to normalized path
        expected = Path.home() / ".aysekai" / "data"
        assert settings.data_dir == expected
    
    def test_immutable_after_creation(self):
        """Test settings are immutable after creation"""
        settings = Settings()
        
        with pytest.raises(ValidationError):
            settings.max_prompt_length = 999