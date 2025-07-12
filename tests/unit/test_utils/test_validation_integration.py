import pytest
from aysekai.utils.validators import InputValidator
from aysekai.core.exceptions import ValidationError


class TestValidationIntegration:
    """Test validation integration with application"""
    
    def test_validation_error_types(self):
        """Test validation errors are properly typed"""
        with pytest.raises(ValidationError) as exc_info:
            InputValidator.validate_required_field("")
        
        assert isinstance(exc_info.value, ValidationError)
        assert "cannot be empty" in str(exc_info.value)
    
    def test_validation_in_pipeline(self):
        """Test validation can be chained"""
        # Input pipeline with HTML around a number
        user_input = "<b>42</b>"
        
        # Sanitize first (removes HTML tags)
        cleaned = InputValidator.sanitize_prompt(user_input)
        
        # Then validate as number
        number = InputValidator.validate_number_input(cleaned)
        
        # Should extract the number
        assert number == 42
    
    def test_batch_validation(self):
        """Test validating multiple inputs"""
        inputs = ["1", "50", "99", "100", "abc"]
        
        results = [
            InputValidator.validate_number_input(i)
            for i in inputs
        ]
        
        assert results == [1, 50, 99, None, None]