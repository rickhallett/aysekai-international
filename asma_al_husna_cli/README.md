# Asma al-Husna Interactive CLI 🕌

A mystical command-line application for daily meditation on the 99 Beautiful Names of Allah, featuring ultra-random selection based on personal intention.

## Features ✨

- **Ultra-Random Selection**: Combines multiple entropy sources for true randomness
- **Beautiful UI**: Rich terminal interface with Arabic text support
- **Four Levels of Interpretation**: Complete Ta'wīl for each divine name
- **Interactive Experience**: Personal intention shapes the selection
- **Complete Information**: Includes pronunciation, dhikr formulas, and Quranic references

## Installation 📦

1. Clone or download this repository
2. Navigate to the application directory:
```bash
cd asma_al_husna_cli
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage 🚀

### Basic meditation session:
```bash
python main.py meditate
```

### Show Baghdad art instead of mosque:
```bash
python main.py meditate --baghdad
```

### View entropy report:
```bash
python main.py meditate --entropy
```

### Select specific name by number:
```bash
python main.py meditate --number 99
```

### List all names:
```bash
python main.py list-names
```

### List a range of names:
```bash
python main.py list-names --start 1 --end 10
```

### About the application:
```bash
python main.py about
```

## How It Works 🔮

1. **Launch**: Beautiful ASCII art of a mosque or Baghdad
2. **Intention**: Share your thought, feeling, or intention for the day
3. **Processing**: The app combines your intention with multiple entropy sources
4. **Selection**: One of the 99 names is selected using ultra-random algorithms
5. **Display**: The name is presented with full details in a beautiful format

## Randomness Sources 🎲

The selection algorithm combines:
- Cryptographically secure random (secrets module)
- Nanosecond-precision timestamps
- SHA-256 hash of your intention
- OS-level entropy
- Hardware random generation
- Process and memory randomization

All sources are mixed using XOR operations and Fisher-Yates shuffling for maximum randomness.

## Data Structure 📚

Each divine name includes:
- Arabic name and transliteration
- Number (1-99)
- Brief meaning
- Ta'wīl (four levels of mystical interpretation)
- Quranic references
- Dhikr formulas
- Pronunciation guide

## Color Scheme 🎨

- **Purple**: Headers and primary text
- **Gold**: Arabic text and highlights
- **Emerald Green**: Quranic references
- **White**: General text

## Requirements ⚙️

- Python 3.7+
- Terminal with Unicode support
- CSV data files with the 99 names

## Notes 📝

- Ensure the CSV files are in the parent directory or update the path in `main.py`
- For best experience, use a terminal with good Unicode and color support
- The application respects the sacred nature of the content with appropriate styling

May your journey through the Beautiful Names bring peace and enlightenment. 🌟