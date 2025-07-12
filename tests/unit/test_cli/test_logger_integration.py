import pytest
from pathlib import Path
from aysekai.cli.secure_logger import SecureSessionLogger
from aysekai.config import get_settings


class TestLoggerIntegration:
    """Test logger integration with application"""
    
    def test_logger_uses_config_settings(self, tmp_path, monkeypatch):
        """Test logger respects configuration settings"""
        # Set config to use encryption
        monkeypatch.setenv("AYSEKAI_SESSION_LOG_ENCRYPTION", "true")
        monkeypatch.setenv("AYSEKAI_DATA_DIR", str(tmp_path))
        
        from aysekai.config import reset_settings
        reset_settings()  # Force reload
        
        settings = get_settings()
        log_dir = settings.data_dir / "logs"
        log_dir.mkdir(parents=True)
        
        # Create logger - should use encryption from config
        logger = SecureSessionLogger(log_dir, encrypt=settings.session_log_encryption)
        
        assert logger.encrypt is True
    
    def test_logger_in_meditation_flow(self, tmp_path):
        """Test logger in actual meditation workflow"""
        log_dir = tmp_path / "logs"
        log_dir.mkdir()
        
        logger = SecureSessionLogger(log_dir)
        
        # Simulate meditation session
        from aysekai.utils.validators import InputValidator
        
        user_prompt = "I seek guidance for patience"
        sanitized = InputValidator.sanitize_prompt(user_prompt)
        
        logger.log_session(
            user="cli_user",
            prompt=sanitized,
            name_number=26,
            name_transliteration="As-Sabur"
        )
        
        # Verify session was logged correctly
        assert logger.log_file.exists()