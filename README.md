# Aysekai International - Asma al-Husna CLI

A beautifully crafted command-line application for Islamic meditation using the 99 Beautiful Names of Allah (الأسماء الحسنى). This project combines spiritual practice with modern technology, featuring ultra-random selection algorithms and a rich terminal user interface.

## Features

- 🎲 **Ultra-Random Selection**: Combines cryptographic randomness, time-based entropy, and hardware sources
- 🌙 **Beautiful Terminal UI**: Rich formatting with Arabic text support
- 📖 **Four Levels of Interpretation**: Each name includes Sharī'a, Ṭarīqa, Ḥaqīqa, and Ma'rifa levels
- 📿 **Dhikr Formulas**: Traditional recitation practices for each name
- 🗣️ **Pronunciation Guides**: Phonetic assistance for proper recitation
- 📊 **Notion Integration**: Export-ready CSV files for database import

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/aysekai-international.git
cd aysekai-international

# Install dependencies
pip install -r asma_al_husna_cli/requirements.txt

# Optional: Install for Arabic text support
pip install python-bidi pyfiglet
```

## Usage

### CLI Application

```bash
# Navigate to the CLI directory
cd asma_al_husna_cli

# Interactive meditation session
python main.py meditate

# List all 99 names
python main.py list-names

# List a specific range
python main.py list-names --start 1 --end 10

# Show application information
python main.py about
```

### Data Processing Scripts

```bash
# Extract names from source CSV (excludes names already in Notion)
python scripts/extract_all_99_names.py

# Create CSV for Notion import
python scripts/create_remaining_names.py

# Fix CSV formatting issues
python scripts/fix_csv_for_notion.py
```

## Project Structure

```
aysekai-international/
├── asma_core/              # Core shared modules
│   ├── constants.py        # Configuration and constants
│   ├── content.py          # Text processing functions
│   ├── csv_handler.py      # CSV operations
│   ├── parser.py           # Name parsing utilities
│   └── validators.py       # Data validation
├── asma_al_husna_cli/      # Main CLI application
│   ├── main.py             # CLI entry point
│   ├── data_loader.py      # Data management
│   ├── randomizer.py       # Random selection algorithm
│   ├── ui.py               # Terminal UI components
│   └── ascii_art.py        # Visual elements
├── scripts/                # Data processing utilities
├── data/                   # CSV data files
│   ├── source/            # Original data
│   └── processed/         # Generated files
└── tests/                  # Unit tests
```

## Development

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=asma_core --cov-report=term-missing
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write tests for new functionality
- Maintain respectful treatment of sacred content

## Data Structure

Each of the 99 names includes:
- **Arabic Name & Transliteration**: Original text with romanization
- **Number**: Traditional ordering (1-99)
- **Brief Meaning**: English translation
- **Ta'wīl (Interpretation)**: Four mystical levels
- **Quranic References**: Relevant verses
- **Dhikr Formulas**: Meditation practices
- **Pronunciation Guide**: Phonetic assistance

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- The 99 Beautiful Names of Allah from Islamic tradition
- Built with [Typer](https://typer.tiangolo.com/) and [Rich](https://rich.readthedocs.io/)
- Inspired by the need for modern tools in spiritual practice

---

*"He is Allah, the Creator, the Inventor, the Fashioner; to Him belong the best names."* - Quran 59:24