"""Session logging for meditation sessions"""

import csv
from datetime import datetime
from pathlib import Path
from typing import Optional
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from asma_core.csv_handler import AsmaCSVWriter


class SessionLogger:
    """Log meditation sessions to CSV file"""
    
    def __init__(self, log_dir: Path):
        """
        Initialize session logger.
        
        Args:
            log_dir: Directory to store log files
        """
        self.log_dir = log_dir
        self.log_file = log_dir / "meditation_sessions.csv"
        self.csv_writer = AsmaCSVWriter()
        self._ensure_log_file()
        
    def _ensure_log_file(self) -> None:
        """Create log file with headers if it doesn't exist"""
        if not self.log_file.exists():
            headers = ["Date", "Time", "User", "Prompt", "Name_Number", "Name_Transliteration"]
            with open(self.log_file, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
    
    def _get_daily_session_count(self, date_str: str) -> int:
        """
        Count sessions for a given date.
        
        Args:
            date_str: Date string in YYYY-MM-DD format
            
        Returns:
            Number of sessions on that date
        """
        count = 0
        if self.log_file.exists():
            with open(self.log_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("Date") == date_str:
                        count += 1
        return count
    
    def log_session(self, prompt: str, name_number: int, name_transliteration: str) -> None:
        """
        Log a meditation session.
        
        Args:
            prompt: User's intention/prompt
            name_number: Number of the selected divine name (1-99)
            name_transliteration: Transliteration of the selected name
        """
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        # Determine user based on daily session count
        session_count = self._get_daily_session_count(date_str)
        user = "Ayse" if session_count == 0 else "Kai"
        
        # Prepare row data
        row = [
            date_str,
            time_str,
            user,
            prompt,
            str(name_number),
            name_transliteration
        ]
        
        # Append to CSV file
        with open(self.log_file, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)