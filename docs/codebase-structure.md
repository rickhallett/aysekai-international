# Codebase Structure - Aysekai International

## Overview
The Aysekai International project is a Python CLI application for Islamic meditation using the 99 Beautiful Names of Allah (Asma al-Husna). The codebase follows a modular architecture with clear separation of concerns.

## Directory Structure

```
aysekai-international/
├── asma_al_husna_cli/      # Main CLI application
│   ├── __init__.py         # Package initialization
│   ├── main.py             # Entry point with Typer CLI commands
│   ├── data_loader.py      # CSV data loading and DivineName model
│   ├── randomizer.py       # Ultra-random selection algorithm
│   ├── ui.py               # Rich terminal UI components
│   ├── ascii_art.py        # ASCII art and visual elements
│   ├── session_logger.py   # Session logging functionality
│   ├── demo_randomness.py  # Randomness demonstration script
│   ├── test_app.py         # Basic application tests
│   ├── requirements.txt    # CLI-specific dependencies
│   └── specs/              # Specifications and PRDs
│
├── asma_core/              # Core shared library
│   ├── __init__.py         # Package initialization
│   ├── constants.py        # Shared constants and configurations
│   ├── content.py          # Content processing utilities
│   ├── csv_handler.py      # CSV reading/writing operations
│   ├── parser.py           # Name parsing utilities
│   └── validators.py       # Data validation functions
│
├── data/                   # Data files
│   ├── source/             # Original source data
│   │   └── names.csv       # Source CSV with 99 names
│   ├── processed/          # Processed data files
│   │   ├── all_remaining_names_for_notion.csv
│   │   ├── asma_al_husna_notion_ready.csv
│   │   └── names_fixed_for_notion.csv
│   ├── logs/               # Application logs
│   │   └── meditation_sessions.csv
│   └── cache/              # Cache directory
│
├── scripts/                # Data processing scripts
│   ├── __init__.py
│   ├── extract_all_99_names.py    # Extract names from source
│   ├── create_remaining_names.py  # Create remaining names CSV
│   ├── fix_csv_for_notion.py      # Fix CSV for Notion import
│   ├── parse_all_names.py         # Parse all names
│   ├── reconstruct_csv.py         # Reconstruct CSV data
│   └── original_versions/         # Backup of original scripts
│
├── tests/                  # Unit tests
│   ├── __init__.py
│   ├── test_constants.py   # Test constants module
│   ├── test_content.py     # Test content processing
│   ├── test_csv_handler.py # Test CSV operations
│   └── test_parser.py      # Test parsing utilities
│
├── .claude/                # Claude Code configuration
│   ├── commands/           # Custom Claude commands
│   ├── hooks/              # Development hooks
│   ├── mcp.json           # MCP server config
│   └── settings.local.json # Local settings
│
├── setup.py                # Package setup configuration
├── pytest.ini              # Pytest configuration
├── requirements-dev.txt    # Development dependencies
├── README.md              # Project documentation
├── CLAUDE.md              # Claude Code instructions
├── RESTRUCTURING_PLAN.md  # Architecture planning
├── .gitignore             # Git ignore rules
└── .env                   # Environment variables (ignored)
```

## Architecture Overview

### 1. **asma_al_husna_cli** - Main Application Layer
- **Purpose**: User-facing CLI application
- **Key Components**:
  - `main.py`: CLI command definitions using Typer
  - `data_loader.py`: Loads and manages divine names data
  - `randomizer.py`: Implements complex randomization algorithm
  - `ui.py`: Rich terminal UI with formatting and colors
  - `session_logger.py`: Tracks meditation sessions

### 2. **asma_core** - Core Library Layer
- **Purpose**: Shared utilities and business logic
- **Key Components**:
  - `constants.py`: Central configuration and constants
  - `content.py`: Text processing and Ta'wil handling
  - `csv_handler.py`: Robust CSV operations
  - `parser.py`: Name and reference parsing
  - `validators.py`: Data integrity checks

### 3. **data** - Data Layer
- **Purpose**: Data storage and management
- **Structure**:
  - Source data (original CSV)
  - Processed data (Notion-ready CSVs)
  - Logs (meditation sessions)
  - Cache (temporary data)

### 4. **scripts** - Data Processing Layer
- **Purpose**: ETL and data transformation scripts
- **Usage**: Convert source data to various formats

### 5. **tests** - Testing Layer
- **Purpose**: Unit tests for core functionality
- **Coverage**: Core modules (not CLI layer)

## Key Design Patterns

1. **Separation of Concerns**: Clear separation between CLI, core logic, and data
2. **Modular Architecture**: Reusable components in asma_core
3. **Data Pipeline**: Scripts for data transformation workflow
4. **Configuration Management**: Centralized constants and settings
5. **Rich UI**: Terminal-based UI with color coding and formatting

## Dependencies

### Core Dependencies (asma_core)
- Standard library only (no external dependencies)

### CLI Dependencies (asma_al_husna_cli)
- `typer`: CLI framework
- `rich`: Terminal formatting
- `python-bidi`: Arabic text support (optional)
- `pyfiglet`: ASCII art (optional)

### Development Dependencies
- `pytest`: Testing framework
- `pytest-cov`: Coverage reporting

## Data Flow

1. Source CSV → Scripts → Processed CSVs
2. Processed CSVs → DataLoader → DivineName objects
3. DivineName objects → Randomizer → Selected name
4. Selected name → UI → Terminal display
5. Session data → SessionLogger → CSV logs