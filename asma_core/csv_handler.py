"""CSV file operations for Asma al-Husna data"""
import csv
from pathlib import Path
from typing import List, Dict, Any
from .constants import COLUMN_HEADERS, CSV_COLUMN_COUNT


class AsmaCSVReader:
    """Read and parse CSV files"""
    
    def __init__(self, encoding: str = 'utf-8'):
        """
        Initialize CSV reader.
        
        Args:
            encoding: File encoding (default: utf-8)
        """
        self.encoding = encoding
    
    def read_names(self, filepath: Path) -> List[Dict[str, str]]:
        """
        Read and parse names from CSV file.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            List of dictionaries with parsed name data
        """
        if not filepath.exists():
            raise FileNotFoundError(f"CSV file not found: {filepath}")
        
        names = []
        with open(filepath, 'r', encoding=self.encoding) as f:
            reader = csv.reader(f)
            headers = next(reader, None)  # Skip header row
            
            for row in reader:
                if len(row) >= CSV_COLUMN_COUNT:
                    name_data = {
                        'name': row[0],
                        'number': row[1],
                        'meaning': row[2],
                        'tawil': row[3],
                        'reference': row[4],
                        'verse': row[5],
                        'dhikr': row[6],
                        'pronunciation': row[7],
                        'phonetics': row[8]
                    }
                    names.append(name_data)
        
        return names
    
    def read_raw(self, filepath: Path) -> List[List[str]]:
        """
        Read raw CSV data as list of lists.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            List of lists with raw CSV data
        """
        if not filepath.exists():
            raise FileNotFoundError(f"CSV file not found: {filepath}")
        
        data = []
        with open(filepath, 'r', encoding=self.encoding) as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)
        
        return data


class AsmaCSVWriter:
    """Write CSV files with proper formatting"""
    
    def __init__(self, encoding: str = 'utf-8'):
        """
        Initialize CSV writer.
        
        Args:
            encoding: File encoding (default: utf-8)
        """
        self.encoding = encoding
    
    def write_notion_format(self, data: List[Dict[str, Any]], filepath: Path) -> None:
        """
        Write data in Notion-compatible CSV format.
        
        Args:
            data: List of dictionaries with name data
            filepath: Path to write CSV file
        """
        with open(filepath, 'w', encoding=self.encoding, newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            
            # Write header
            writer.writerow(COLUMN_HEADERS)
            
            # Write data rows
            for item in data:
                row = [
                    item.get('name', ''),
                    item.get('number', ''),
                    item.get('meaning', ''),
                    item.get('tawil', ''),
                    item.get('reference', ''),
                    item.get('verse', ''),
                    item.get('dhikr', ''),
                    item.get('pronunciation', ''),
                    item.get('phonetics', '')
                ]
                writer.writerow(row)
    
    def write_raw(self, data: List[List[str]], filepath: Path) -> None:
        """
        Write raw CSV data.
        
        Args:
            data: List of lists with raw data
            filepath: Path to write CSV file
        """
        with open(filepath, 'w', encoding=self.encoding, newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            for row in data:
                writer.writerow(row)


class CSVValidator:
    """Validate CSV data integrity"""
    
    def validate_columns(self, row: List[str]) -> bool:
        """
        Validate that row has correct number of columns.
        
        Args:
            row: CSV row to validate
            
        Returns:
            True if valid column count
        """
        return len(row) == CSV_COLUMN_COUNT
    
    def validate_content(self, data: Dict[str, str]) -> List[str]:
        """
        Validate content of parsed name data.
        
        Args:
            data: Dictionary with name data
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Check required fields
        if not data.get('name'):
            errors.append("Name is required")
        
        # Check number is valid
        number = data.get('number', '')
        if number and not number.isdigit():
            try:
                int(number)
            except ValueError:
                errors.append(f"Invalid number format: {number}")
        
        # Could add more validation rules here
        
        return errors