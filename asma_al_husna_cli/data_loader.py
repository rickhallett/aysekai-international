import csv
import os
import sys
from typing import List, Dict, Any
from dataclasses import dataclass
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from asma_core import csv_handler, content


@dataclass
class DivineName:
    """Represents one of the 99 Beautiful Names of Allah"""

    name_arabic: str
    number: int
    brief_meaning: str
    tawil: str
    quranic_reference: str
    verse_ayah: str
    dhikr_formula: str
    pronunciation: str
    phonetics: str


class DataLoader:
    """Loads and manages the 99 Names of Allah from CSV files"""

    def __init__(self, base_path: Path = None):
        if base_path is None:
            base_path = Path(__file__).parent.parent
        self.base_path = base_path
        self.names: List[DivineName] = []

    def load_all_names(self) -> List[DivineName]:
        """Load all 99 names from both CSV files"""
        # Load from processed data directory
        csv1_path = (
            self.base_path / "data" / "processed" / "all_remaining_names_for_notion.csv"
        )
        csv2_path = (
            self.base_path / "data" / "processed" / "asma_al_husna_notion_ready.csv"
        )

        self.names = []

        # Process first CSV
        if csv1_path.exists():
            self._load_csv(csv1_path)

        # Process second CSV
        if csv2_path.exists():
            self._load_csv(csv2_path)

        # Sort by number to ensure proper order
        self.names.sort(key=lambda x: x.number)

        return self.names

    def _load_csv(self, csv_path: Path) -> None:
        """Load names from a single CSV file"""
        reader = csv_handler.AsmaCSVReader()

        try:
            # Use our CSV reader to load the data
            names_data = reader.read_names(csv_path)

            for row in names_data:
                try:
                    # Extract number
                    number_str = row.get("number", "0").strip()
                    number = int(number_str) if number_str.isdigit() else 0

                    if number == 0:  # Skip invalid entries
                        continue

                    # Create DivineName object
                    name = DivineName(
                        name_arabic=row.get("name", "").strip(),
                        number=number,
                        brief_meaning=row.get("meaning", "").strip(),
                        tawil=row.get("tawil", "").strip(),
                        quranic_reference=row.get("reference", "").strip(),
                        verse_ayah=row.get("verse", "").strip(),
                        dhikr_formula=row.get("dhikr", "").strip(),
                        pronunciation=row.get("pronunciation", "").strip(),
                        phonetics=row.get("phonetics", "").strip(),
                    )

                    self.names.append(name)

                except (ValueError, KeyError) as e:
                    # Skip malformed entries
                    continue

        except FileNotFoundError:
            # CSV file doesn't exist, skip silently
            pass

    def get_name_by_number(self, number: int) -> DivineName:
        """Get a specific name by its number (1-99)"""
        for name in self.names:
            if name.number == number:
                return name
        raise ValueError(f"Name with number {number} not found")

    def get_all_names(self) -> List[DivineName]:
        """Return all loaded names"""
        if not self.names:
            self.load_all_names()
        return self.names
