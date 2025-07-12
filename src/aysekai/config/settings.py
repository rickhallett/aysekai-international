"""Application settings with validation and security"""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Optional, List


class Settings(BaseSettings):
    """Application settings with validation and security"""

    # Data paths
    data_dir: Path = Field(
        default_factory=lambda: Path.home() / ".aysekai" / "data",
        description="Base data directory",
    )

    # Security settings
    max_prompt_length: int = Field(
        default=500, ge=1, le=1000, description="Maximum allowed prompt length"
    )

    allowed_csv_paths: List[str] = Field(
        default_factory=lambda: ["data/processed"],
        description="Allowed paths for CSV file access",
    )

    session_log_encryption: bool = Field(
        default=False, description="Enable session log encryption"
    )

    # Performance settings
    cache_enabled: bool = Field(default=True, description="Enable caching")

    cache_ttl: int = Field(default=3600, ge=0, description="Cache TTL in seconds")

    @field_validator("data_dir")
    def validate_data_dir(cls, v: Path) -> Path:
        """Ensure data directory is safe"""
        # Convert string to Path if needed
        if isinstance(v, str):
            v = Path(v)

        # Check for obvious directory traversal attacks
        original_str = str(v)
        # Block patterns like ../../ or ../../../ but allow single ../ in middle of path
        if original_str.startswith("../") or "../../" in original_str:
            raise ValueError("Invalid data directory")

        # Resolve to absolute path
        resolved = v.expanduser().resolve()

        return resolved

    model_config = SettingsConfigDict(
        env_prefix="AYSEKAI_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        frozen=True,
        extra="ignore",
    )


# Singleton pattern for settings
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get application settings (singleton)"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reset_settings() -> None:
    """Reset settings (for testing only)"""
    global _settings
    _settings = None
