import pytest
from aysekai.cli.error_handler import with_retry, ErrorRecovery
from aysekai.core.exceptions import DataError, ValidationError


class TestErrorRecovery:
    """Test error recovery mechanisms"""
    
    def test_retry_on_transient_error(self):
        """Test retry logic for transient errors"""
        attempt_count = 0
        
        @with_retry(max_attempts=3, delay=0.01)
        def flaky_function():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise DataError("Temporary failure")
            return "success"
        
        result = flaky_function()
        assert result == "success"
        assert attempt_count == 3
    
    def test_retry_exhaustion(self):
        """Test retry exhaustion raises error"""
        @with_retry(max_attempts=2, delay=0.01)
        def always_fails():
            raise DataError("Permanent failure")
        
        with pytest.raises(DataError):
            always_fails()
    
    def test_no_retry_on_validation_error(self):
        """Test that validation errors are not retried"""
        attempt_count = 0
        
        @with_retry(max_attempts=3)
        def validation_error():
            nonlocal attempt_count
            attempt_count += 1
            raise ValidationError("Invalid input")
        
        with pytest.raises(ValidationError):
            validation_error()
        
        # Should not retry validation errors
        assert attempt_count == 1
    
    def test_error_recovery_context(self):
        """Test error recovery context manager"""
        with ErrorRecovery() as recovery:
            # Simulate recoverable error
            recovery.add_error(DataError("CSV temporarily locked"))
            
            # Should suggest retry
            assert recovery.should_retry()
            assert recovery.attempt_count == 1
        
        # After max attempts
        with ErrorRecovery(max_attempts=1) as recovery:
            recovery.add_error(DataError("Still locked"))
            recovery.add_error(DataError("Still locked"))
            
            assert not recovery.should_retry()