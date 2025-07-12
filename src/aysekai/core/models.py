"""Core data models for Aysekai application"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DivineName:
    """Represents one of the 99 Beautiful Names of Allah"""
    
    number: int
    arabic: str
    transliteration: str
    brief_meaning: str
    level_1_sharia: str
    level_2_tariqa: str
    level_3_haqiqa: str
    level_4_marifa: str
    quranic_references: str
    dhikr_formulas: str
    pronunciation_guide: str
    
    def __post_init__(self):
        """Validate divine name data"""
        if not 1 <= self.number <= 99:
            raise ValueError(f"Divine name number must be 1-99, got {self.number}")
        
        if not self.arabic or not self.transliteration:
            raise ValueError("Arabic name and transliteration are required")
    
    @property
    def display_name(self) -> str:
        """Get formatted display name"""
        return f"{self.number}. {self.arabic} ({self.transliteration})"
    
    @property
    def meaning_summary(self) -> str:
        """Get brief meaning summary"""
        return f"{self.transliteration}: {self.brief_meaning}"
    
    def get_level_interpretation(self, level: int) -> Optional[str]:
        """Get interpretation for specific level (1-4)"""
        level_map = {
            1: self.level_1_sharia,
            2: self.level_2_tariqa, 
            3: self.level_3_haqiqa,
            4: self.level_4_marifa,
        }
        return level_map.get(level)


@dataclass 
class MeditationSession:
    """Represents a meditation session"""
    
    divine_name: DivineName
    start_time: str
    user_intention: Optional[str] = None
    session_id: Optional[str] = None
    
    def __post_init__(self):
        """Validate session data"""
        if not isinstance(self.divine_name, DivineName):
            raise ValueError("divine_name must be a DivineName instance")