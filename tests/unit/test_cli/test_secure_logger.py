import pytest
import threading
import time
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
from cryptography.fernet import Fernet

from aysekai.cli.secure_logger import SecureSessionLogger
from aysekai.core.exceptions import ValidationError


class TestSecureSessionLogger:
    """Test secure session logging"""
    
    @pytest.fixture
    def temp_log_dir(self, tmp_path):
        """Create temporary log directory"""
        log_dir = tmp_path / "logs"
        log_dir.mkdir()
        return log_dir
    
    def test_initialization(self, temp_log_dir):
        """Test logger initialization"""
        logger = SecureSessionLogger(temp_log_dir)
        
        assert logger.log_dir == temp_log_dir
        assert logger.log_file == temp_log_dir / "sessions.log"
        assert logger.encrypt is False
        assert logger._lock is not None
    
    def test_initialization_with_encryption(self, temp_log_dir):
        """Test logger initialization with encryption"""
        logger = SecureSessionLogger(temp_log_dir, encrypt=True)
        
        assert logger.encrypt is True
        assert hasattr(logger, 'cipher')
        assert (temp_log_dir / ".key").exists()
        
        # Key file should have restricted permissions
        key_file = temp_log_dir / ".key"
        assert oct(key_file.stat().st_mode)[-3:] == '600'
    
    def test_log_session_basic(self, temp_log_dir):
        """Test basic session logging"""
        logger = SecureSessionLogger(temp_log_dir)
        
        logger.log_session(
            user="test_user",
            prompt="Test meditation",
            name_number=42,
            name_transliteration="Al-Hakeem"
        )
        
        # Verify log file exists and contains data
        assert logger.log_file.exists()
        
        with open(logger.log_file, 'r') as f:
            content = f.read()
            assert "test_user" in content
            assert "Test meditation" in content
            assert "42" in content
            assert "Al-Hakeem" in content
    
    def test_log_session_sanitization(self, temp_log_dir):
        """Test input sanitization in logging"""
        logger = SecureSessionLogger(temp_log_dir)
        
        # Dangerous input
        logger.log_session(
            user="test",
            prompt="<script>alert('xss')</script>Meditation",
            name_number=1,
            name_transliteration="Ar-Rahman"
        )
        
        with open(logger.log_file, 'r') as f:
            content = f.read()
            # Script tags should be removed
            assert "<script>" not in content
            assert "</script>" not in content
            # But sanitized content should remain
            assert "alert('xss')Meditation" in content
            assert "Meditation" in content
    
    def test_log_session_with_encryption(self, temp_log_dir):
        """Test encrypted session logging"""
        logger = SecureSessionLogger(temp_log_dir, encrypt=True)
        
        logger.log_session(
            user="test_user",
            prompt="Secret meditation",
            name_number=99,
            name_transliteration="Al-Ahad"
        )
        
        # Read raw file content
        with open(logger.log_file, 'r') as f:
            encrypted_content = f.read().strip()
        
        # Content should be hex-encoded encrypted data
        assert all(c in '0123456789abcdef' for c in encrypted_content)
        
        # Decrypt and verify
        decrypted = logger.cipher.decrypt(bytes.fromhex(encrypted_content))
        data = json.loads(decrypted)
        
        assert data["user"] == "test_user"
        assert data["prompt"] == "Secret meditation"
        assert data["name_number"] == 99
    
    def test_thread_safety(self, temp_log_dir):
        """Test concurrent logging is thread-safe"""
        logger = SecureSessionLogger(temp_log_dir)
        errors = []
        entries = []
        
        def log_entry(thread_id):
            try:
                for i in range(10):
                    logger.log_session(
                        user=f"user_{thread_id}",
                        prompt=f"Prompt {thread_id}-{i}",
                        name_number=i + 1,
                        name_transliteration=f"Name-{i}"
                    )
                    entries.append(f"{thread_id}-{i}")
                    time.sleep(0.001)  # Small delay to increase contention
            except Exception as e:
                errors.append(e)
        
        # Launch multiple threads
        threads = []
        for i in range(5):
            t = threading.Thread(target=log_entry, args=(i,))
            threads.append(t)
            t.start()
        
        # Wait for completion
        for t in threads:
            t.join()
        
        # No errors should occur
        assert len(errors) == 0
        
        # All entries should be logged
        assert len(entries) == 50
        
        # Verify file integrity (no corruption)
        with open(logger.log_file, 'r') as f:
            lines = f.readlines()
            # Should have header + 50 entries
            assert len(lines) == 51
    
    def test_file_locking(self, temp_log_dir, monkeypatch):
        """Test file locking prevents corruption"""
        logger = SecureSessionLogger(temp_log_dir)
        
        # Mock fcntl to track lock/unlock calls
        lock_calls = []
        unlock_calls = []
        
        def mock_flock(fd, operation):
            if operation == 2:  # LOCK_EX
                lock_calls.append(fd)
            elif operation == 8:  # LOCK_UN
                unlock_calls.append(fd)
        
        monkeypatch.setattr("fcntl.flock", mock_flock)
        
        logger.log_session("user", "prompt", 1, "name")
        
        # Should have acquired and released lock
        assert len(lock_calls) == 1
        assert len(unlock_calls) == 1
        assert lock_calls[0] == unlock_calls[0]
    
    def test_session_id_generation(self, temp_log_dir):
        """Test unique session ID generation"""
        logger = SecureSessionLogger(temp_log_dir)
        
        # Generate multiple session IDs
        ids = set()
        for _ in range(100):
            session_id = logger._generate_session_id()
            ids.add(session_id)
        
        # All should be unique
        assert len(ids) == 100
        
        # Should be valid UUIDs
        import uuid
        for session_id in ids:
            uuid.UUID(session_id)  # Should not raise
    
    def test_log_rotation_preparation(self, temp_log_dir):
        """Test logger handles log rotation scenarios"""
        logger = SecureSessionLogger(temp_log_dir)
        
        # Log some entries
        for i in range(5):
            logger.log_session(f"user{i}", f"prompt{i}", i+1, f"name{i}")
        
        # Simulate external rotation (rename file)
        import shutil
        shutil.move(logger.log_file, logger.log_file.with_suffix('.log.1'))
        
        # Logger should create new file
        logger.log_session("new_user", "new_prompt", 1, "new_name")
        
        # Both files should exist
        assert logger.log_file.exists()
        assert logger.log_file.with_suffix('.log.1').exists()
    
    def test_encryption_key_persistence(self, temp_log_dir):
        """Test encryption key is persisted correctly"""
        # Create logger with encryption
        logger1 = SecureSessionLogger(temp_log_dir, encrypt=True)
        logger1.log_session("user1", "prompt1", 1, "name1")
        
        # Create new logger instance
        logger2 = SecureSessionLogger(temp_log_dir, encrypt=True)
        
        # Should use same key
        assert logger1.cipher._signing_key == logger2.cipher._signing_key
        
        # Should be able to decrypt old entries
        with open(logger2.log_file, 'r') as f:
            encrypted = f.read().strip()
            decrypted = logger2.cipher.decrypt(bytes.fromhex(encrypted))
            data = json.loads(decrypted)
            assert data["user"] == "user1"
    
    def test_csv_header_creation(self, temp_log_dir):
        """Test CSV header is created for new files"""
        logger = SecureSessionLogger(temp_log_dir, encrypt=False)
        
        # Log entry to create file
        logger.log_session("user", "prompt", 1, "name")
        
        with open(logger.log_file, 'r') as f:
            lines = f.readlines()
            # First line should be header
            assert "timestamp" in lines[0]
            assert "user" in lines[0]
            assert "prompt" in lines[0]
            assert "session_id" in lines[0]
    
    def test_max_user_length(self, temp_log_dir):
        """Test user field length limit"""
        logger = SecureSessionLogger(temp_log_dir)
        
        long_user = "x" * 200
        logger.log_session(long_user, "prompt", 1, "name")
        
        with open(logger.log_file, 'r') as f:
            content = f.read()
            # User should be truncated to 100 chars
            assert "x" * 100 in content
            assert "x" * 101 not in content