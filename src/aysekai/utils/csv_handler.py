"""CSV handling utilities for Aysekai application"""

import csv
from pathlib import Path
from typing import List, Optional, Dict

from ..core.models import DivineName
from ..core.exceptions import DataError


class AsmaCSVReader:
    """Reader for Asma al-Husna CSV files"""
    
    def __init__(self, csv_path: Path):
        """
        Initialize CSV reader.
        
        Args:
            csv_path: Path to CSV file
        """
        self.csv_path = Path(csv_path)
        if not self.csv_path.exists():
            raise DataError(f"CSV file not found: {csv_path}")
    
    def read_all(self) -> List[DivineName]:
        """
        Read all divine names from CSV.
        
        Returns:
            List of DivineName objects
        """
        names = []
        
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = self._row_to_divine_name(row)
                    if name:
                        names.append(name)
        except Exception as e:
            raise DataError(f"Error reading CSV file {self.csv_path}: {e}")
        
        return names
    
    def _row_to_divine_name(self, row: Dict[str, str]) -> Optional[DivineName]:
        """Convert CSV row to DivineName object"""
        try:
            return DivineName(
                number=int(row.get('Number', 0)),
                arabic=row.get('Arabic', '').strip(),
                transliteration=row.get('Transliteration', '').strip(),
                brief_meaning=row.get('Brief Meaning', '').strip(),
                level_1_sharia=row.get('Level 1 - Shari\'a', '').strip(),
                level_2_tariqa=row.get('Level 2 - Tariqa', '').strip(), 
                level_3_haqiqa=row.get('Level 3 - Haqiqa', '').strip(),
                level_4_marifa=row.get('Level 4 - Ma\'rifa', '').strip(),
                quranic_references=row.get('Quranic References', '').strip(),
                dhikr_formulas=row.get('Dhikr Formulas', '').strip(),
                pronunciation_guide=row.get('Pronunciation Guide', '').strip(),
            )
        except (ValueError, KeyError):
            # Log warning but don't fail entire import
            return None


class AsmaCSVWriter:
    """Writer for Asma al-Husna CSV files"""
    
    def __init__(self, csv_path: Path):
        """
        Initialize CSV writer.
        
        Args:
            csv_path: Path where CSV will be written
        """
        self.csv_path = Path(csv_path)
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
    
    def write_all(self, names: List[DivineName]) -> None:
        """
        Write divine names to CSV.
        
        Args:
            names: List of DivineName objects to write
        """
        fieldnames = [
            'Number', 'Arabic', 'Transliteration', 'Brief Meaning',
            'Level 1 - Shari\'a', 'Level 2 - Tariqa', 
            'Level 3 - Haqiqa', 'Level 4 - Ma\'rifa',
            'Quranic References', 'Dhikr Formulas', 'Pronunciation Guide'
        ]
        
        try:
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for name in names:
                    writer.writerow(self._divine_name_to_row(name))
        except Exception as e:
            raise DataError(f"Error writing CSV file {self.csv_path}: {e}")
    
    def _divine_name_to_row(self, name: DivineName) -> Dict[str, str]:
        """Convert DivineName object to CSV row"""
        return {
            'Number': str(name.number),
            'Arabic': name.arabic,
            'Transliteration': name.transliteration,
            'Brief Meaning': name.brief_meaning,
            'Level 1 - Shari\'a': name.level_1_sharia,
            'Level 2 - Tariqa': name.level_2_tariqa,
            'Level 3 - Haqiqa': name.level_3_haqiqa,
            'Level 4 - Ma\'rifa': name.level_4_marifa,
            'Quranic References': name.quranic_references,
            'Dhikr Formulas': name.dhikr_formulas,
            'Pronunciation Guide': name.pronunciation_guide,
        }