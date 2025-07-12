"""Tests for asma_core.constants module"""

import pytest
from asma_core import constants


class TestColumnHeaders:
    """Test column header constants"""

    def test_column_headers_exist(self):
        """Test that COLUMN_HEADERS constant exists"""
        assert hasattr(constants, "COLUMN_HEADERS")

    def test_column_headers_is_list(self):
        """Test that COLUMN_HEADERS is a list"""
        assert isinstance(constants.COLUMN_HEADERS, list)

    def test_column_headers_count(self):
        """Test that COLUMN_HEADERS has 9 columns"""
        assert len(constants.COLUMN_HEADERS) == 9

    def test_column_headers_content(self):
        """Test that COLUMN_HEADERS contains expected values"""
        expected = [
            "The Beautiful Name / الاسم الحسن",
            "Number / الرقم",
            "Brief Meaning / المعنى المختصر",
            "Ta'wil / التأويل",
            "Quranic Reference / المرجع القرآني",
            "Verse → Ayah / الآية",
            "Dhikr Formula / صيغة الذكر",
            "Pronunciation",
            "Phonetics",
        ]
        assert constants.COLUMN_HEADERS == expected


class TestExistingNotionNames:
    """Test existing Notion names constants"""

    def test_existing_notion_names_exist(self):
        """Test that EXISTING_NOTION_NAMES constant exists"""
        assert hasattr(constants, "EXISTING_NOTION_NAMES")

    def test_existing_notion_names_is_set(self):
        """Test that EXISTING_NOTION_NAMES is a set"""
        assert isinstance(constants.EXISTING_NOTION_NAMES, set)

    def test_existing_notion_names_count(self):
        """Test that EXISTING_NOTION_NAMES has 5 names"""
        assert len(constants.EXISTING_NOTION_NAMES) == 5

    def test_existing_notion_names_content(self):
        """Test that EXISTING_NOTION_NAMES contains expected values"""
        expected = {
            "Al-Bāqī (الباقي)",
            "Al-Khabīr (الخبير)",
            "Ar-Raqīb (الرقيب)",
            "Al-Matīn (المتين)",
            "Al-Mu'īd (المعيد)",
        }
        assert constants.EXISTING_NOTION_NAMES == expected


class TestTawilLevels:
    """Test Ta'wil level constants"""

    def test_tawil_levels_exist(self):
        """Test that TAWIL_LEVELS constant exists"""
        assert hasattr(constants, "TAWIL_LEVELS")

    def test_tawil_levels_is_dict(self):
        """Test that TAWIL_LEVELS is a dictionary"""
        assert isinstance(constants.TAWIL_LEVELS, dict)

    def test_tawil_levels_keys(self):
        """Test that TAWIL_LEVELS has correct keys"""
        expected_keys = {"sharia", "tariqa", "haqiqa", "marifa"}
        assert set(constants.TAWIL_LEVELS.keys()) == expected_keys

    def test_tawil_levels_structure(self):
        """Test that each TAWIL_LEVEL has emoji and name"""
        for level, data in constants.TAWIL_LEVELS.items():
            assert "emoji" in data
            assert "name" in data
            assert isinstance(data["emoji"], str)
            assert isinstance(data["name"], str)

    def test_tawil_levels_values(self):
        """Test specific TAWIL_LEVELS values"""
        assert constants.TAWIL_LEVELS["sharia"] == {"emoji": "📿", "name": "SHARĪ'A"}
        assert constants.TAWIL_LEVELS["tariqa"] == {"emoji": "🚶", "name": "ṬARĪQA"}
        assert constants.TAWIL_LEVELS["haqiqa"] == {"emoji": "💎", "name": "ḤAQĪQA"}
        assert constants.TAWIL_LEVELS["marifa"] == {"emoji": "🌟", "name": "MA'RIFA"}


class TestTawilPatterns:
    """Test Ta'wil regex patterns"""

    def test_tawil_patterns_exist(self):
        """Test that TAWIL_PATTERNS constant exists"""
        assert hasattr(constants, "TAWIL_PATTERNS")

    def test_tawil_patterns_is_list(self):
        """Test that TAWIL_PATTERNS is a list"""
        assert isinstance(constants.TAWIL_PATTERNS, list)

    def test_tawil_patterns_length(self):
        """Test that TAWIL_PATTERNS has 4 patterns"""
        assert len(constants.TAWIL_PATTERNS) == 4

    def test_tawil_patterns_structure(self):
        """Test that each pattern is a tuple with regex and label"""
        for pattern in constants.TAWIL_PATTERNS:
            assert isinstance(pattern, tuple)
            assert len(pattern) == 2
            assert isinstance(pattern[0], str)  # regex pattern
            assert isinstance(pattern[1], str)  # label


class TestFilePaths:
    """Test file path constants"""

    def test_default_csv_filename(self):
        """Test default CSV filename constant"""
        assert hasattr(constants, "DEFAULT_CSV_FILENAME")
        assert constants.DEFAULT_CSV_FILENAME == "names.csv"

    def test_data_directories(self):
        """Test data directory constants"""
        assert hasattr(constants, "DATA_DIR")
        assert constants.DATA_DIR == "data"
        assert hasattr(constants, "SOURCE_DATA_DIR")
        assert constants.SOURCE_DATA_DIR == "data/source"
        assert hasattr(constants, "PROCESSED_DATA_DIR")
        assert constants.PROCESSED_DATA_DIR == "data/processed"


class TestNumericConstants:
    """Test numeric constants"""

    def test_total_names_count(self):
        """Test total number of divine names"""
        assert hasattr(constants, "TOTAL_NAMES")
        assert constants.TOTAL_NAMES == 99

    def test_csv_column_count(self):
        """Test expected number of CSV columns"""
        assert hasattr(constants, "CSV_COLUMN_COUNT")
        assert constants.CSV_COLUMN_COUNT == 9
