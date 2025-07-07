# Aysekai International - Code Restructuring and Modularization Plan

## Overview
This plan outlines the restructuring and modularization of the aysekai-international codebase to improve organization, reduce code duplication, and enhance maintainability.

## Current Issues
1. **Root directory clutter**: Utility scripts and data files mixed in root
2. **Code duplication**: Common functions repeated across multiple scripts
3. **No clear separation**: Data files mixed with code files
4. **Missing abstractions**: Direct CSV manipulation without proper interfaces
5. **Inconsistent patterns**: Each script implements its own cleaning logic

## Proposed Structure

```
aysekai-international/
├── README.md                    # Project overview
├── CLAUDE.md                    # Claude Code guidance
├── requirements.txt             # Project-wide dependencies
├── setup.py                     # Package setup for proper imports
│
├── asma_core/                   # Core shared modules
│   ├── __init__.py
│   ├── constants.py            # All constants and configurations
│   ├── content.py              # Content processing functions
│   ├── csv_handler.py          # CSV reading/writing operations
│   ├── parser.py               # Name parsing utilities
│   └── validators.py           # Data validation functions
│
├── asma_al_husna_cli/          # CLI application (existing)
│   ├── __init__.py
│   ├── main.py
│   ├── data_loader.py          # Refactor to use asma_core
│   ├── randomizer.py
│   ├── ui.py
│   ├── ascii_art.py
│   └── requirements.txt
│
├── scripts/                     # Data processing scripts
│   ├── __init__.py
│   ├── extract_all_names.py    # Refactored to use asma_core
│   ├── create_remaining_names.py
│   ├── fix_csv_for_notion.py
│   ├── parse_all_names.py
│   └── reconstruct_csv.py
│
├── data/                        # All data files
│   ├── source/                 # Original data
│   │   └── names.csv
│   ├── processed/              # Generated/processed data
│   │   ├── all_remaining_names_for_notion.csv
│   │   ├── asma_al_husna_notion_ready.csv
│   │   └── names_fixed_for_notion.csv
│   └── cache/                  # Temporary files if needed
│
└── tests/                       # Unit tests
    ├── __init__.py
    ├── test_content.py
    ├── test_csv_handler.py
    ├── test_parser.py
    └── test_integration.py
```

## Core Modules Design

### 1. `asma_core/constants.py`
```python
# Column definitions
COLUMN_HEADERS = [
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

# Names already in Notion
EXISTING_NOTION_NAMES = {
    "Al-Bāqī (الباقي)",
    "Al-Khabīr (الخبير)",
    "Ar-Raqīb (الرقيب)",
    "Al-Matīn (المتين)",
    "Al-Mu'īd (المعيد)",
}

# Ta'wil section patterns
TAWIL_LEVELS = {
    'sharia': {'emoji': '📿', 'name': 'SHARĪ\'A'},
    'tariqa': {'emoji': '🚶', 'name': 'ṬARĪQA'},
    'haqiqa': {'emoji': '💎', 'name': 'ḤAQĪQA'},
    'marifa': {'emoji': '🌟', 'name': 'MA\'RIFA'},
}
```

### 2. `asma_core/content.py`
```python
"""Content processing utilities for Asma al-Husna data"""

def clean_multiline_content(content: str, preserve_structure: bool = True) -> str:
    """Clean and format multiline content"""

def process_tawil_sections(content: str) -> str:
    """Process Ta'wil content with proper emoji sections"""

def format_dhikr_content(content: str) -> str:
    """Format Dhikr formulas for display"""

def normalize_arabic_text(text: str) -> str:
    """Normalize Arabic text for consistent display"""
```

### 3. `asma_core/csv_handler.py`
```python
"""CSV file operations for Asma al-Husna data"""

class AsmaCSVReader:
    """Read and parse CSV files"""
    def read_names(self, filepath: Path) -> List[Dict[str, str]]
    def read_raw(self, filepath: Path) -> List[List[str]]

class AsmaCSVWriter:
    """Write CSV files with proper formatting"""
    def write_notion_format(self, data: List[Dict], filepath: Path)
    def write_raw(self, data: List[List[str]], filepath: Path)

class CSVValidator:
    """Validate CSV data integrity"""
    def validate_columns(self, row: List[str]) -> bool
    def validate_content(self, data: Dict[str, str]) -> List[str]
```

### 4. `asma_core/parser.py`
```python
"""Name parsing and extraction utilities"""

def parse_name_with_arabic(text: str) -> Tuple[str, str]
def extract_name_number(text: str) -> Optional[int]
def is_existing_name(name: str) -> bool
def parse_quranic_reference(ref: str) -> Dict[str, str]
```

## Migration Steps

### Phase 1: Setup Core Infrastructure
1. Create `asma_core` package structure
2. Implement core modules with shared functionality
3. Add comprehensive unit tests
4. Create setup.py for proper package installation

### Phase 2: Refactor Scripts
1. Update each script to import from `asma_core`
2. Remove duplicated functions
3. Standardize error handling
4. Add proper logging

### Phase 3: Reorganize Files
1. Create directory structure
2. Move data files to `data/` directory
3. Move scripts to `scripts/` directory
4. Update all file paths in code

### Phase 4: Update CLI Application
1. Refactor `data_loader.py` to use `asma_core`
2. Update file paths for new structure
3. Add configuration management
4. Test all CLI commands

### Phase 5: Documentation and Testing
1. Update CLAUDE.md with new structure
2. Create comprehensive README
3. Add integration tests
4. Document all modules and functions

## Benefits

1. **Reduced Duplication**: Common functions in one place
2. **Better Organization**: Clear separation of concerns
3. **Easier Testing**: Modular components can be tested independently
4. **Improved Maintainability**: Changes in one place affect all scripts
5. **Professional Structure**: Standard Python package layout
6. **Extensibility**: Easy to add new features or scripts

## Implementation Priority

1. **High Priority**:
   - Create `asma_core` package
   - Move common functions
   - Create data directory structure

2. **Medium Priority**:
   - Refactor existing scripts
   - Add comprehensive tests
   - Update documentation

3. **Low Priority**:
   - Add advanced features (caching, parallel processing)
   - Create GUI version
   - Add API endpoints

## Next Steps

1. Review and approve this plan
2. Create feature branch for restructuring
3. Implement Phase 1 (Core Infrastructure)
4. Test thoroughly before proceeding
5. Migrate incrementally to avoid breaking changes