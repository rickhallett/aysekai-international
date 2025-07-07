"""Tests for asma_core.content module"""
import pytest
from asma_core import content


class TestCleanMultilineContent:
    """Test clean_multiline_content function"""
    
    def test_function_exists(self):
        """Test that clean_multiline_content function exists"""
        assert hasattr(content, 'clean_multiline_content')
    
    def test_remove_duplicate_quotes(self):
        """Test removal of duplicate quotes"""
        text = '""Hello World""'
        result = content.clean_multiline_content(text)
        assert result == '"Hello World"'
    
    def test_clean_whitespace(self):
        """Test whitespace cleaning"""
        text = '  Hello   World  \n\n  Test  '
        result = content.clean_multiline_content(text)
        assert result == 'Hello World Test'
    
    def test_handle_pipe_separators(self):
        """Test handling of pipe separators for multiline content"""
        text = 'Line 1|Line 2|Line 3'
        result = content.clean_multiline_content(text, preserve_structure=True)
        assert '|' in result
    
    def test_preserve_structure_false(self):
        """Test with preserve_structure=False"""
        text = 'Line 1|Line 2|Line 3'
        result = content.clean_multiline_content(text, preserve_structure=False)
        assert '|' not in result
        assert 'Line 1 Line 2 Line 3' in result
    
    def test_empty_string(self):
        """Test with empty string"""
        result = content.clean_multiline_content('')
        assert result == ''
    
    def test_none_input(self):
        """Test with None input"""
        result = content.clean_multiline_content(None)
        assert result == ''


class TestProcessTawilSections:
    """Test process_tawil_sections function"""
    
    def test_function_exists(self):
        """Test that process_tawil_sections function exists"""
        assert hasattr(content, 'process_tawil_sections')
    
    def test_extract_sharia_section(self):
        """Test extraction of SHARĪ'A section"""
        text = "📿 SHARĪ'A: This is the sharī'a content 🚶 ṬARĪQA: Other content"
        result = content.process_tawil_sections(text)
        assert "📿 SHARĪ'A" in result
        assert "sharī'a content" in result
    
    def test_extract_all_sections(self):
        """Test extraction of all four Ta'wil sections"""
        text = """
        📿 SHARĪ'A: Legal meaning
        🚶 ṬARĪQA: Path meaning  
        💎 ḤAQĪQA: Reality meaning
        🌟 MA'RIFA: Gnosis meaning
        """
        result = content.process_tawil_sections(text)
        assert all(emoji in result for emoji in ['📿', '🚶', '💎', '🌟'])
    
    def test_preserve_section_order(self):
        """Test that sections are preserved in order"""
        text = "🌟 MA'RIFA: Fourth 📿 SHARĪ'A: First 💎 ḤAQĪQA: Third 🚶 ṬARĪQA: Second"
        result = content.process_tawil_sections(text)
        # Should reorder to standard sequence
        sharia_pos = result.find('📿')
        tariqa_pos = result.find('🚶')
        haqiqa_pos = result.find('💎')
        marifa_pos = result.find('🌟')
        assert sharia_pos < tariqa_pos < haqiqa_pos < marifa_pos
    
    def test_missing_sections(self):
        """Test handling of missing sections"""
        text = "📿 SHARĪ'A: Only this section exists"
        result = content.process_tawil_sections(text)
        assert "📿 SHARĪ'A" in result
        assert "🚶" not in result  # Other sections should not be added
    
    def test_empty_input(self):
        """Test with empty input"""
        result = content.process_tawil_sections('')
        assert result == ''


class TestFormatDhikrContent:
    """Test format_dhikr_content function"""
    
    def test_function_exists(self):
        """Test that format_dhikr_content function exists"""
        assert hasattr(content, 'format_dhikr_content')
    
    def test_basic_formatting(self):
        """Test basic Dhikr formula formatting"""
        text = "Yā Raḥmān (يا رحمن) - 100 times"
        result = content.format_dhikr_content(text)
        assert "Yā Raḥmān" in result
        assert "يا رحمن" in result
    
    def test_multiple_formulas(self):
        """Test formatting multiple Dhikr formulas"""
        text = "Formula 1|Formula 2|Formula 3"
        result = content.format_dhikr_content(text)
        assert "Formula 1" in result
        assert "Formula 2" in result
        assert "Formula 3" in result
    
    def test_clean_extra_spaces(self):
        """Test cleaning of extra spaces"""
        text = "  Dhikr   Formula   "
        result = content.format_dhikr_content(text)
        assert result.strip() == "Dhikr Formula"


class TestNormalizeArabicText:
    """Test normalize_arabic_text function"""
    
    def test_function_exists(self):
        """Test that normalize_arabic_text function exists"""
        assert hasattr(content, 'normalize_arabic_text')
    
    def test_basic_arabic_text(self):
        """Test basic Arabic text normalization"""
        text = "الرحمن"
        result = content.normalize_arabic_text(text)
        assert result == "الرحمن"
    
    def test_mixed_arabic_english(self):
        """Test mixed Arabic and English text"""
        text = "Al-Rahman الرحمن The Compassionate"
        result = content.normalize_arabic_text(text)
        assert "Al-Rahman" in result
        assert "الرحمن" in result
    
    def test_remove_extra_spaces(self):
        """Test removal of extra spaces around Arabic"""
        text = "  الله  "
        result = content.normalize_arabic_text(text)
        assert result.strip() == "الله"


class TestRemoveEmptyLines:
    """Test remove_empty_lines function"""
    
    def test_function_exists(self):
        """Test that remove_empty_lines function exists"""
        assert hasattr(content, 'remove_empty_lines')
    
    def test_remove_empty_lines(self):
        """Test removal of empty lines"""
        text = "Line 1\n\n\nLine 2\n\n"
        result = content.remove_empty_lines(text)
        assert result == "Line 1\nLine 2"
    
    def test_preserve_single_newlines(self):
        """Test preservation of single newlines"""
        text = "Line 1\nLine 2\nLine 3"
        result = content.remove_empty_lines(text)
        assert result == text


class TestCleanQuotes:
    """Test clean_quotes function"""
    
    def test_function_exists(self):
        """Test that clean_quotes function exists"""
        assert hasattr(content, 'clean_quotes')
    
    def test_smart_quotes_conversion(self):
        """Test conversion of smart quotes to regular quotes"""
        # Using unicode escapes for smart quotes
        text = "\u201CHello\u201D and \u2018World\u2019"
        result = content.clean_quotes(text)
        assert result == '"Hello" and \'World\''
    
    def test_preserve_regular_quotes(self):
        """Test that regular quotes are preserved"""
        text = '"Hello" and \'World\''
        result = content.clean_quotes(text)
        assert result == text