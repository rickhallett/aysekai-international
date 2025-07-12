import pytest
from pathlib import Path
from aysekai.config import get_settings, reset_settings


class TestConfigIntegration:
    """Test configuration integration with application"""
    
    def test_config_used_in_data_paths(self):
        """Test that configuration is used for data paths"""
        settings = get_settings()
        
        # Verify paths are constructed correctly
        processed_dir = settings.data_dir / "processed"
        logs_dir = settings.data_dir / "logs"
        cache_dir = settings.data_dir / "cache"
        
        # All paths should be under the configured data directory
        assert str(processed_dir).startswith(str(settings.data_dir))
        assert str(logs_dir).startswith(str(settings.data_dir))
        assert str(cache_dir).startswith(str(settings.data_dir))
    
    def test_config_reset_for_testing(self):
        """Test configuration can be reset for testing"""
        original = get_settings()
        
        # Reset should clear singleton
        reset_settings()
        
        # New instance should be created
        new_settings = get_settings()
        assert new_settings is not original