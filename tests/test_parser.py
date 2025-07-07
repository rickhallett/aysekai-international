"""Tests for asma_core.parser module"""
import pytest
from asma_core import parser


class TestParseNameWithArabic:
    """Test parse_name_with_arabic function"""
    
    def test_function_exists(self):
        """Test that parse_name_with_arabic function exists"""
        assert hasattr(parser, 'parse_name_with_arabic')
    
    def test_parse_standard_format(self):
        """Test parsing standard name format"""
        text = "Al-Rahman (الرحمن)"
        transliteration, arabic = parser.parse_name_with_arabic(text)
        assert transliteration == "Al-Rahman"
        assert arabic == "الرحمن"
    
    def test_parse_with_extra_spaces(self):
        """Test parsing with extra spaces"""
        text = " Al-Rahman  ( الرحمن ) "
        transliteration, arabic = parser.parse_name_with_arabic(text)
        assert transliteration == "Al-Rahman"
        assert arabic == "الرحمن"
    
    def test_parse_without_parentheses(self):
        """Test parsing name without parentheses"""
        text = "Al-Rahman الرحمن"
        transliteration, arabic = parser.parse_name_with_arabic(text)
        assert transliteration == "Al-Rahman"
        assert arabic == "الرحمن"
    
    def test_parse_arabic_only(self):
        """Test parsing Arabic only"""
        text = "الرحمن"
        transliteration, arabic = parser.parse_name_with_arabic(text)
        assert transliteration == ""
        assert arabic == "الرحمن"
    
    def test_parse_english_only(self):
        """Test parsing English only"""
        text = "Al-Rahman"
        transliteration, arabic = parser.parse_name_with_arabic(text)
        assert transliteration == "Al-Rahman"
        assert arabic == ""
    
    def test_empty_input(self):
        """Test with empty input"""
        transliteration, arabic = parser.parse_name_with_arabic("")
        assert transliteration == ""
        assert arabic == ""
    
    def test_none_input(self):
        """Test with None input"""
        transliteration, arabic = parser.parse_name_with_arabic(None)
        assert transliteration == ""
        assert arabic == ""


class TestExtractNameNumber:
    """Test extract_name_number function"""
    
    def test_function_exists(self):
        """Test that extract_name_number function exists"""
        assert hasattr(parser, 'extract_name_number')
    
    def test_extract_simple_number(self):
        """Test extracting simple number"""
        text = "1. Al-Rahman"
        number = parser.extract_name_number(text)
        assert number == 1
    
    def test_extract_number_with_parentheses(self):
        """Test extracting number with parentheses"""
        text = "(42) Al-Kabir"
        number = parser.extract_name_number(text)
        assert number == 42
    
    def test_extract_number_from_middle(self):
        """Test extracting number from middle of text"""
        text = "Name number 99 is Al-Sabur"
        number = parser.extract_name_number(text)
        assert number == 99
    
    def test_no_number_returns_none(self):
        """Test that no number returns None"""
        text = "Al-Rahman"
        number = parser.extract_name_number(text)
        assert number is None
    
    def test_multiple_numbers_returns_first(self):
        """Test that multiple numbers returns first"""
        text = "5. Name 10"
        number = parser.extract_name_number(text)
        assert number == 5
    
    def test_empty_input(self):
        """Test with empty input"""
        number = parser.extract_name_number("")
        assert number is None


class TestIsExistingName:
    """Test is_existing_name function"""
    
    def test_function_exists(self):
        """Test that is_existing_name function exists"""
        assert hasattr(parser, 'is_existing_name')
    
    def test_existing_name_exact_match(self):
        """Test exact match of existing name"""
        assert parser.is_existing_name("Al-Bāqī (الباقي)") is True
    
    def test_existing_name_partial_match(self):
        """Test partial match of existing name"""
        assert parser.is_existing_name("Al-Bāqī") is True
        assert parser.is_existing_name("الباقي") is True
    
    def test_non_existing_name(self):
        """Test non-existing name"""
        assert parser.is_existing_name("Al-Rahman") is False
    
    def test_case_sensitivity(self):
        """Test case sensitivity"""
        assert parser.is_existing_name("al-bāqī") is True  # Should be case-insensitive
    
    def test_empty_input(self):
        """Test with empty input"""
        assert parser.is_existing_name("") is False
    
    def test_all_existing_names(self):
        """Test all known existing names"""
        existing_names = [
            "Al-Bāqī (الباقي)",
            "Al-Khabīr (الخبير)",
            "Ar-Raqīb (الرقيب)",
            "Al-Matīn (المتين)",
            "Al-Mu'īd (المعيد)",
        ]
        for name in existing_names:
            assert parser.is_existing_name(name) is True


class TestParseQuranicReference:
    """Test parse_quranic_reference function"""
    
    def test_function_exists(self):
        """Test that parse_quranic_reference function exists"""
        assert hasattr(parser, 'parse_quranic_reference')
    
    def test_parse_standard_reference(self):
        """Test parsing standard Quranic reference"""
        text = "Surah Al-Baqarah (2:255)"
        result = parser.parse_quranic_reference(text)
        assert result['surah'] == "Al-Baqarah"
        assert result['surah_number'] == 2
        assert result['verse'] == 255
    
    def test_parse_multiple_verses(self):
        """Test parsing reference with verse range"""
        text = "Surah Al-Fatiha (1:1-7)"
        result = parser.parse_quranic_reference(text)
        assert result['surah'] == "Al-Fatiha"
        assert result['surah_number'] == 1
        assert result['verse_start'] == 1
        assert result['verse_end'] == 7
    
    def test_parse_arabic_surah_name(self):
        """Test parsing with Arabic surah name"""
        text = "سورة البقرة (2:255)"
        result = parser.parse_quranic_reference(text)
        assert result['surah_number'] == 2
        assert result['verse'] == 255
    
    def test_parse_invalid_reference(self):
        """Test parsing invalid reference"""
        text = "Not a reference"
        result = parser.parse_quranic_reference(text)
        assert result == {}
    
    def test_empty_input(self):
        """Test with empty input"""
        result = parser.parse_quranic_reference("")
        assert result == {}


class TestExtractNameFromLine:
    """Test extract_name_from_line function"""
    
    def test_function_exists(self):
        """Test that extract_name_from_line function exists"""
        assert hasattr(parser, 'extract_name_from_line')
    
    def test_extract_numbered_name(self):
        """Test extracting name from numbered line"""
        line = "1. Al-Rahman (الرحمن) - The Compassionate"
        name, number = parser.extract_name_from_line(line)
        assert name == "Al-Rahman (الرحمن)"
        assert number == 1
    
    def test_extract_name_without_number(self):
        """Test extracting name without number"""
        line = "Al-Rahman (الرحمن) - The Compassionate"
        name, number = parser.extract_name_from_line(line)
        assert name == "Al-Rahman (الرحمن)"
        assert number is None
    
    def test_extract_name_with_complex_format(self):
        """Test extracting name with complex format"""
        line = "99 | Al-Sabur (الصبور) | The Patient One"
        name, number = parser.extract_name_from_line(line)
        assert name == "Al-Sabur (الصبور)"
        assert number == 99
    
    def test_empty_line(self):
        """Test with empty line"""
        name, number = parser.extract_name_from_line("")
        assert name == ""
        assert number is None