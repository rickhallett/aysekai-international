# Aysekai International - Islamic Meditation CLI

A modern, architecturally sophisticated command-line application for Islamic meditation using the 99 Beautiful Names of Allah (الأسماء الحسنى). Built with enterprise-grade patterns including dependency injection, comprehensive error handling, and extensive test coverage.

## ✨ Features

- 🎲 **Ultra-Random Selection**: Cryptographically secure randomness with multiple entropy sources
- 🏗️ **Modern Architecture**: Clean separation of concerns with dependency injection
- 🛡️ **Security-First**: Input validation, secure logging, and hardened error handling  
- 🌙 **Beautiful Terminal UI**: Rich formatting with Arabic text support
- 📖 **Four Levels of Ta'wīl**: Sharī'a, Ṭarīqa, Ḥaqīqa, and Ma'rifa interpretations
- 📿 **Dhikr Practices**: Traditional meditation formulas for each name
- 🗣️ **Pronunciation Guides**: Phonetic assistance for proper recitation
- ✅ **98% Test Coverage**: Comprehensive test suite with TDD methodology
- 📊 **Data Processing**: Export-ready CSV files for Notion integration

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/yourusername/aysekai-international.git
cd aysekai-international

# Install dependencies  
pip install -r requirements.txt

# Run meditation session
python -m src.aysekai.cli.main meditate

# List the Beautiful Names
python -m src.aysekai.cli.main list-names

# Show application info
python -m src.aysekai.cli.main about
```

## 🏗️ Architecture

This project demonstrates enterprise-grade Python architecture patterns:

- **🔧 Dependency Injection**: Clean service boundaries and testability
- **📦 Package Structure**: Modern `src/` layout with clear separation
- **🛡️ Error Boundaries**: User-friendly error handling throughout
- **🧪 Test-Driven Development**: Comprehensive test suite driving design
- **🔒 Security Hardening**: Input validation and secure practices
- **📊 Structured Logging**: Detailed logging for debugging and monitoring

**→ [View detailed architecture documentation](ARCHITECTURE.md)**

## 📁 Project Structure

```
aysekai-international/
├── src/aysekai/           # Main application package
│   ├── cli/              # Command-line interface
│   ├── core/             # Domain models and business logic
│   ├── di/               # Dependency injection system
│   ├── utils/            # Utility functions and helpers
│   └── config/           # Configuration management
├── scripts/              # Data processing utilities
├── data/                 # CSV data files
│   ├── source/          # Original source data
│   └── processed/       # Generated files for Notion
├── tests/               # Comprehensive test suite
│   ├── unit/           # Unit tests by component
│   └── integration/    # Integration tests
└── docs/               # Documentation and specifications
```

## 🧪 Development

### Running Tests

```bash
# Run all tests with coverage
pytest tests/ -v --cov=src/aysekai --cov-report=term-missing

# Run specific test suites
pytest tests/unit/test_di/ -v           # Dependency injection tests
pytest tests/unit/test_cli/ -v          # CLI tests  
pytest tests/unit/test_package/ -v      # Package structure tests

# Run linting and type checking
ruff check src/
mypy src/ --ignore-missing-imports
```

### Development Commands

```bash
# Data processing scripts
python scripts/extract_all_99_names.py     # Extract names from source
python scripts/create_remaining_names.py   # Create Notion-ready CSV
python scripts/fix_csv_for_notion.py      # Fix CSV formatting

# CLI development  
python -m src.aysekai.cli.main meditate --entropy  # Show randomness report
python -m src.aysekai.cli.main meditate --number 33 # Select specific name
python -m src.aysekai.cli.main list-names 1 10     # List range
```

## 🔧 Configuration

The application supports flexible configuration through environment variables:

```bash
# Data file location
export AYSEKAI_DATA_PATH="/path/to/data"

# Logging configuration
export AYSEKAI_LOG_LEVEL="INFO"
export AYSEKAI_LOG_PATH="/path/to/logs"

# Security settings  
export AYSEKAI_MAX_PROMPT_LENGTH="1000"
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed configuration options.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Code Standards

- **Architecture**: Follow dependency injection and clean architecture patterns
- **Testing**: Write tests first (TDD approach), maintain 95%+ coverage  
- **Security**: All inputs must be validated, no hardcoded secrets
- **Documentation**: Update architecture docs for significant changes
- **Respect**: Maintain reverent treatment of sacred Islamic content

### Development Workflow

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes (TDD)
4. Implement the feature
5. Ensure all tests pass and coverage is maintained
6. Run linting: `ruff check src/` and `mypy src/`
7. Commit changes (`git commit -m 'Add amazing feature'`)
8. Push to branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## 📊 Data Structure

Each of the 99 Beautiful Names includes:

- **Arabic Name & Transliteration**: Original text with precise romanization
- **Number**: Traditional ordering (1-99) with alternative Al-Ghazali numbering
- **Brief Meaning**: Concise English translation
- **Four Levels of Ta'wīl**: 
  - **Sharī'a**: Legal/exoteric interpretation
  - **Ṭarīqa**: Spiritual path interpretation  
  - **Ḥaqīqa**: Mystical reality interpretation
  - **Ma'rifa**: Direct gnosis interpretation
- **Quranic References**: Relevant verses with context
- **Dhikr Formulas**: Traditional recitation practices
- **Pronunciation Guide**: Detailed phonetic assistance

## 🔒 Security Features

- **Input Validation**: All user inputs sanitized and validated
- **Error Boundaries**: Graceful error handling without information leakage
- **Secure Logging**: Sensitive information excluded from logs
- **Path Traversal Protection**: Safe file system operations
- **Dependency Injection**: Reduced coupling and improved security boundaries

## 📈 Performance

- **Lazy Loading**: Services instantiated only when needed
- **Efficient Randomness**: Optimized entropy collection and processing
- **Memory Management**: Proper resource cleanup and lifecycle management
- **Fast Startup**: Minimal dependencies loaded at startup

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- The 99 Beautiful Names of Allah from Islamic tradition
- Built with [Typer](https://typer.tiangolo.com/), [Rich](https://rich.readthedocs.io/), and [Pydantic](https://pydantic.dev/)
- Inspired by the intersection of spiritual practice and modern technology
- Contributors who maintain respectful treatment of sacred content

---

*"And to Allah belong the best names, so invoke Him by them."* - Quran 7:180

**[📖 Technical Architecture →](ARCHITECTURE.md)** | **[🤝 Contributing →](CONTRIBUTING.md)** | **[🔧 Development Setup →](docs/development.md)**