"""Path resolution without hardcoded paths"""

from pathlib import Path
from typing import Optional, List

from ..config import get_settings
from ..core.exceptions import ConfigurationError
from ..utils.validators import InputValidator


class PathResolver:
    """Resolve paths using configuration instead of hardcoded values"""
    
    def __init__(self):
        """Initialize path resolver with configuration"""
        self.settings = get_settings()
        self.base_dir = self.settings.data_dir
    
    def get_data_files_path(self, require_files: bool = False) -> Path:
        """
        Get the path to CSV data files.
        
        Args:
            require_files: If True, raise error if files don't exist
            
        Returns:
            Path to data directory
            
        Raises:
            ConfigurationError: If require_files=True and files missing
        """
        data_path = self.base_dir
        
        if require_files and not self.validate_data_files(data_path):
            raise ConfigurationError(
                f"Could not find CSV data files in {data_path}. "
                "Please ensure the data files are in the correct location."
            )
        
        return data_path
    
    def validate_data_files(self, data_path: Path) -> bool:
        """
        Validate that required CSV files exist.
        
        Args:
            data_path: Base data directory
            
        Returns:
            True if at least one required CSV exists
        """
        required_files = [
            "processed/all_remaining_names_for_notion.csv",
            "processed/asma_al_husna_notion_ready.csv",
        ]
        
        for file_path in required_files:
            if (data_path / file_path).exists():
                return True
        
        return False
    
    def get_csv_path(self, filename: str) -> Path:
        """
        Get path to a specific CSV file.
        
        Args:
            filename: Name of the CSV file
            
        Returns:
            Full path to the CSV file
        """
        return self.base_dir / "processed" / filename
    
    def get_log_directory(self) -> Path:
        """
        Get the log directory path.
        
        Returns:
            Path to logs directory
        """
        return self.base_dir / "logs"
    
    def get_cache_directory(self) -> Path:
        """
        Get the cache directory path.
        
        Returns:
            Path to cache directory
        """
        return self.base_dir / "cache"
    
    def ensure_directories(self) -> None:
        """Create all required directories if they don't exist"""
        directories = [
            self.base_dir / "processed",
            self.base_dir / "logs",
            self.base_dir / "cache",
            self.base_dir / "source",
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def is_path_allowed(self, path: Path) -> bool:
        """
        Check if a path is within allowed directories.
        
        Args:
            path: Path to validate
            
        Returns:
            True if path is allowed
        """
        allowed_dirs = [
            str(self.base_dir),
            str(self.get_log_directory()),
            str(self.get_cache_directory()),
        ]
        
        return InputValidator.validate_file_path(path, allowed_dirs)
    
    def list_available_csvs(self) -> List[Path]:
        """
        List all available CSV files.
        
        Returns:
            List of paths to CSV files
        """
        processed_dir = self.base_dir / "processed"
        if not processed_dir.exists():
            return []
        
        return list(processed_dir.glob("*.csv"))


# Global instance for convenience
_resolver: Optional[PathResolver] = None


def get_path_resolver() -> PathResolver:
    """Get global path resolver instance"""
    global _resolver
    if _resolver is None:
        _resolver = PathResolver()
    return _resolver