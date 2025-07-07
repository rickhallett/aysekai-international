"""Tests for asma_core.csv_handler module"""
import pytest
import tempfile
import os
from pathlib import Path
from asma_core import csv_handler


class TestAsmaCSVReader:
    """Test AsmaCSVReader class"""
    
    def test_class_exists(self):
        """Test that AsmaCSVReader class exists"""
        assert hasattr(csv_handler, 'AsmaCSVReader')
    
    def test_instantiation(self):
        """Test that AsmaCSVReader can be instantiated"""
        reader = csv_handler.AsmaCSVReader()
        assert reader is not None
    
    def test_read_names_method_exists(self):
        """Test that read_names method exists"""
        reader = csv_handler.AsmaCSVReader()
        assert hasattr(reader, 'read_names')
    
    def test_read_raw_method_exists(self):
        """Test that read_raw method exists"""
        reader = csv_handler.AsmaCSVReader()
        assert hasattr(reader, 'read_raw')
    
    def test_read_names_with_valid_csv(self):
        """Test reading names from valid CSV"""
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write('"The Beautiful Name / الاسم الحسن","Number / الرقم","Brief Meaning / المعنى المختصر","Ta\'wil / التأويل","Quranic Reference / المرجع القرآني","Verse → Ayah / الآية","Dhikr Formula / صيغة الذكر","Pronunciation","Phonetics"\n')
            f.write('"Al-Rahman (الرحمن)","1","The Compassionate","📿 SHARĪ\'A: Legal meaning","Surah Al-Fatiha (1:1)","بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ","Yā Raḥmān","ar-rah-maan","ar-raḥ-mān"\n')
            temp_path = f.name
        
        try:
            reader = csv_handler.AsmaCSVReader()
            names = reader.read_names(Path(temp_path))
            
            assert len(names) == 1
            assert names[0]['name'] == 'Al-Rahman (الرحمن)'
            assert names[0]['number'] == '1'
            assert names[0]['meaning'] == 'The Compassionate'
        finally:
            os.unlink(temp_path)
    
    def test_read_raw_returns_list(self):
        """Test that read_raw returns list of lists"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write('col1,col2,col3\n')
            f.write('val1,val2,val3\n')
            temp_path = f.name
        
        try:
            reader = csv_handler.AsmaCSVReader()
            data = reader.read_raw(Path(temp_path))
            
            assert isinstance(data, list)
            assert len(data) == 2
            assert data[0] == ['col1', 'col2', 'col3']
            assert data[1] == ['val1', 'val2', 'val3']
        finally:
            os.unlink(temp_path)
    
    def test_read_nonexistent_file_raises_error(self):
        """Test that reading nonexistent file raises appropriate error"""
        reader = csv_handler.AsmaCSVReader()
        with pytest.raises(FileNotFoundError):
            reader.read_names(Path('/nonexistent/file.csv'))


class TestAsmaCSVWriter:
    """Test AsmaCSVWriter class"""
    
    def test_class_exists(self):
        """Test that AsmaCSVWriter class exists"""
        assert hasattr(csv_handler, 'AsmaCSVWriter')
    
    def test_instantiation(self):
        """Test that AsmaCSVWriter can be instantiated"""
        writer = csv_handler.AsmaCSVWriter()
        assert writer is not None
    
    def test_write_notion_format_method_exists(self):
        """Test that write_notion_format method exists"""
        writer = csv_handler.AsmaCSVWriter()
        assert hasattr(writer, 'write_notion_format')
    
    def test_write_raw_method_exists(self):
        """Test that write_raw method exists"""
        writer = csv_handler.AsmaCSVWriter()
        assert hasattr(writer, 'write_raw')
    
    def test_write_notion_format(self):
        """Test writing data in Notion format"""
        data = [{
            'name': 'Al-Rahman (الرحمن)',
            'number': '1',
            'meaning': 'The Compassionate',
            'tawil': '📿 SHARĪ\'A: Legal meaning',
            'reference': 'Surah Al-Fatiha (1:1)',
            'verse': 'بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ',
            'dhikr': 'Yā Raḥmān',
            'pronunciation': 'ar-rah-maan',
            'phonetics': 'ar-raḥ-mān'
        }]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_path = Path(f.name)
        
        try:
            writer = csv_handler.AsmaCSVWriter()
            writer.write_notion_format(data, temp_path)
            
            # Verify file was written
            assert temp_path.exists()
            
            # Read back and verify
            reader = csv_handler.AsmaCSVReader()
            written_data = reader.read_raw(temp_path)
            
            assert len(written_data) == 2  # Header + 1 row
            assert len(written_data[0]) == 9  # 9 columns
            assert written_data[1][0] == 'Al-Rahman (الرحمن)'
        finally:
            if temp_path.exists():
                temp_path.unlink()
    
    def test_write_raw_data(self):
        """Test writing raw data"""
        data = [
            ['col1', 'col2', 'col3'],
            ['val1', 'val2', 'val3']
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_path = Path(f.name)
        
        try:
            writer = csv_handler.AsmaCSVWriter()
            writer.write_raw(data, temp_path)
            
            # Verify file was written
            assert temp_path.exists()
            
            # Read back and verify
            with open(temp_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert 'col1' in content
                assert 'val1' in content
        finally:
            if temp_path.exists():
                temp_path.unlink()


class TestCSVValidator:
    """Test CSVValidator class"""
    
    def test_class_exists(self):
        """Test that CSVValidator class exists"""
        assert hasattr(csv_handler, 'CSVValidator')
    
    def test_instantiation(self):
        """Test that CSVValidator can be instantiated"""
        validator = csv_handler.CSVValidator()
        assert validator is not None
    
    def test_validate_columns_method_exists(self):
        """Test that validate_columns method exists"""
        validator = csv_handler.CSVValidator()
        assert hasattr(validator, 'validate_columns')
    
    def test_validate_content_method_exists(self):
        """Test that validate_content method exists"""
        validator = csv_handler.CSVValidator()
        assert hasattr(validator, 'validate_content')
    
    def test_validate_columns_correct_count(self):
        """Test validating correct number of columns"""
        validator = csv_handler.CSVValidator()
        row = [''] * 9  # 9 empty strings
        assert validator.validate_columns(row) is True
    
    def test_validate_columns_incorrect_count(self):
        """Test validating incorrect number of columns"""
        validator = csv_handler.CSVValidator()
        row = [''] * 5  # Only 5 columns
        assert validator.validate_columns(row) is False
    
    def test_validate_content_valid_data(self):
        """Test validating valid content"""
        validator = csv_handler.CSVValidator()
        data = {
            'name': 'Al-Rahman (الرحمن)',
            'number': '1',
            'meaning': 'The Compassionate'
        }
        errors = validator.validate_content(data)
        assert len(errors) == 0
    
    def test_validate_content_missing_name(self):
        """Test validating content with missing name"""
        validator = csv_handler.CSVValidator()
        data = {
            'number': '1',
            'meaning': 'The Compassionate'
        }
        errors = validator.validate_content(data)
        assert len(errors) > 0
        assert any('name' in error.lower() for error in errors)
    
    def test_validate_content_invalid_number(self):
        """Test validating content with invalid number"""
        validator = csv_handler.CSVValidator()
        data = {
            'name': 'Al-Rahman',
            'number': 'not-a-number',
            'meaning': 'The Compassionate'
        }
        errors = validator.validate_content(data)
        assert len(errors) > 0
        assert any('number' in error.lower() for error in errors)