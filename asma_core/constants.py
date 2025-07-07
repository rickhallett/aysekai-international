"""Constants for Asma al-Husna data processing"""

# Column headers for CSV files
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

# Names already existing in Notion
EXISTING_NOTION_NAMES = {
    "Al-Bāqī (الباقي)",
    "Al-Khabīr (الخبير)",
    "Ar-Raqīb (الرقيب)",
    "Al-Matīn (المتين)",
    "Al-Mu'īd (المعيد)",
}

# Ta'wil levels with their emojis and names
TAWIL_LEVELS = {
    'sharia': {'emoji': '📿', 'name': 'SHARĪ\'A'},
    'tariqa': {'emoji': '🚶', 'name': 'ṬARĪQA'},
    'haqiqa': {'emoji': '💎', 'name': 'ḤAQĪQA'},
    'marifa': {'emoji': '🌟', 'name': 'MA\'RIFA'},
}

# Ta'wil regex patterns for content extraction
TAWIL_PATTERNS = [
    (r"📿\s*SHARĪ\'A[^🚶💎🌟]*", "📿 SHARĪ'A"),
    (r"🚶\s*ṬARĪQA[^📿💎🌟]*", "🚶 ṬARĪQA"),
    (r"💎\s*ḤAQĪQA[^📿🚶🌟]*", "💎 ḤAQĪQA"),
    (r"🌟\s*MA\'RIFA[^📿🚶💎]*", "🌟 MA'RIFA"),
]

# File paths and directories
DEFAULT_CSV_FILENAME = 'names.csv'
DATA_DIR = 'data'
SOURCE_DATA_DIR = 'data/source'
PROCESSED_DATA_DIR = 'data/processed'

# Numeric constants
TOTAL_NAMES = 99
CSV_COLUMN_COUNT = 9