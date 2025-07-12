"""Service interfaces and protocols for dependency injection"""

from typing import Protocol, List, Dict, Any
from pathlib import Path

from ..core.models import DivineName


class DataReader(Protocol):
    """Protocol for reading divine name data from various sources"""
    
    def read_all_names(self) -> List[DivineName]:
        """Read all divine names from the data source"""
        ...
    
    def get_name_by_number(self, number: int) -> DivineName:
        """Get specific divine name by number (1-99)"""
        ...


class RandomSelector(Protocol):
    """Protocol for random selection of divine names"""
    
    def select_random_name(self, names: List[DivineName], intention: str) -> DivineName:
        """Select a random divine name based on intention"""
        ...
    
    def get_entropy_report(self) -> Dict[str, Any]:
        """Get report of entropy sources used for selection"""
        ...


class PathResolver(Protocol):
    """Protocol for resolving file paths and data locations"""
    
    def get_data_path(self) -> Path:
        """Get the path to data files directory"""
        ...
    
    def list_csv_files(self) -> List[Path]:
        """List all available CSV files in data directory"""
        ...
    
    def resolve_path(self, relative_path: str) -> Path:
        """Resolve a relative path to absolute path"""
        ...


class SessionLogger(Protocol):
    """Protocol for logging meditation sessions"""
    
    def log_session(self, intention: str, name_number: int, transliteration: str) -> None:
        """Log a meditation session"""
        ...
    
    def get_session_history(self) -> List[Dict[str, Any]]:
        """Get history of meditation sessions"""
        ...