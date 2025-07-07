# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python CLI application for Islamic meditation using the 99 Beautiful Names of Allah (Asma al-Husna). The application provides an interactive terminal interface for spiritual practice with rich formatting and ultra-random selection algorithms.

## Development Commands

### Setup and Installation
```bash
# Install dependencies
pip install -r asma_al_husna_cli/requirements.txt

# Install with optional Arabic support
pip install python-bidi pyfiglet
```

### Running the Application
```bash
# Run the main application (from asma_al_husna_cli directory)
cd asma_al_husna_cli
python main.py

# Common commands
python main.py meditate              # Interactive meditation session
python main.py list-names            # Display all names
python main.py list-names 1 10       # Display names 1-10
python main.py about                 # Show application info

# With options
python main.py meditate --baghdad    # Use Al-Ghazali numbering
python main.py meditate --entropy    # Show entropy visualization
python main.py meditate --number 33  # Select specific name
```

### Testing
```bash
# Run all unit tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=asma_core --cov-report=term-missing

# Run specific test module
pytest tests/test_content.py -v

# Run basic CLI tests (from asma_al_husna_cli directory)
python test_app.py
```

### Data Processing Scripts
```bash
# Extract all names from source CSV (excludes names already in Notion)
python scripts/extract_all_99_names.py

# Create remaining names CSV for Notion import
python scripts/create_remaining_names.py

# Fix CSV formatting for Notion import
python scripts/fix_csv_for_notion.py
```

## Architecture Overview

### Project Structure

```
aysekai-international/
├── asma_core/              # Core shared modules
│   ├── constants.py        # All constants and configurations
│   ├── content.py          # Content processing functions
│   ├── csv_handler.py      # CSV reading/writing operations
│   ├── parser.py           # Name parsing utilities
│   └── validators.py       # Data validation functions
├── asma_al_husna_cli/      # CLI application
│   ├── main.py             # Entry point and CLI commands
│   ├── data_loader.py      # CSV data management (uses asma_core)
│   ├── randomizer.py       # Ultra-random selection algorithm
│   ├── ui.py               # Terminal UI components
│   └── ascii_art.py        # Intro screens and visual elements
├── scripts/                # Data processing scripts
│   ├── extract_all_99_names.py
│   ├── create_remaining_names.py
│   └── fix_csv_for_notion.py
├── data/                   # Data files
│   ├── source/            # Original source data
│   └── processed/         # Generated CSV files
└── tests/                  # Unit tests
```

### Core Components

1. **asma_core package**: Shared functionality used across the project
   - **constants.py**: Column headers, existing names, Ta'wil patterns
   - **content.py**: Text cleaning, Ta'wil processing, Dhikr formatting
   - **csv_handler.py**: CSV reading/writing with proper encoding
   - **parser.py**: Name parsing, number extraction, Quranic reference parsing
   - **validators.py**: Data validation and integrity checks

2. **asma_al_husna_cli/main.py**: Entry point and CLI command definitions
   - Defines all CLI commands (meditate, list-names, about)
   - Handles command-line arguments and options

3. **asma_al_husna_cli/data_loader.py**: CSV data management
   - Loads divine names from data/processed/ directory
   - Uses asma_core.csv_handler for file operations

4. **randomizer.py**: Ultra-random selection algorithm
   - Combines multiple entropy sources (cryptographic, time-based, hardware)
   - Implements the core meditation selection logic

5. **ui.py**: Terminal UI components using Rich library
   - Renders beautiful formatted output with colors
   - Handles Arabic text display and alignment
   - Creates interactive prompts and panels

### Data Structure

The application uses CSV files containing structured data for each of the 99 names:
- **Number**: 1-99 (or alternative Al-Ghazali numbering)
- **Arabic Name**: Original Arabic text
- **Transliteration**: Romanized version
- **Brief Meaning**: Short English translation
- **Four Levels of Ta'wīl**: Sharī'a, Ṭarīqa, Ḥaqīqa, Ma'rifa interpretations
- **Quranic References**: Relevant verses
- **Dhikr Formulas**: Meditation practices
- **Pronunciation Guide**: Phonetic assistance

### Key Design Principles

1. **Respectful Presentation**: All sacred content is displayed with appropriate reverence and formatting
2. **Ultra-Randomness**: The selection algorithm combines multiple entropy sources to ensure true randomness for meditation
3. **Rich Terminal Experience**: Extensive use of colors, boxes, and formatting for beautiful CLI output
4. **Modular Structure**: Clear separation between data loading, UI, randomization, and CLI logic

### Color Scheme

The application uses a specific color palette defined in ui.py:
- Sacred text (Arabic): Special formatting with careful alignment
- Interpretations: Color-coded by level (Sharī'a, Ṭarīqa, Ḥaqīqa, Ma'rifa)
- UI elements: Consistent theming throughout

## Important Notes

- The application handles sacred Islamic content - maintain respectful treatment in all modifications
- Arabic text rendering may require BiDi support (python-bidi package)  
- The randomization algorithm is intentionally complex to ensure meaningful selection
- Data files are organized: source files in data/source/, processed files in data/processed/
- The asma_core package provides reusable functionality - use it instead of duplicating code
- All scripts in scripts/ directory use the core modules for consistency