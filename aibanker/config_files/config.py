from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


DATA_DIR = BASE_DIR / "data"
DB_FILE_CREDENTIALS = DATA_DIR / "app.db"
DB_EXPENSE_FILE = DATA_DIR / "app_.db"



OPTION_DICT = {
    "Food and Drinks": '#4ACFAC',  # PAS_GREEN
    "Entertainment": '#f97c7c',  # PAS_RED
    "Transportation": '#7E8CE0',  # PAS_PURPLE
    "Shopping": '#f0c58c',  # PAS_ORANGE
    "Bills and Utilities": '#ffe8c7',  # PAS_ORANGE_LIGHT
    "Travel": '#83c5c6',  # PAS_LIGHT_BLUE
    "Healthcare": '#bad594',  # ANOTHER_PAS_GREEN
    "Personal Care": '#e5a978',  # PEACH
    "Education": '#dccde4',  # VERY_LIGHT_PURPLE
    "Miscellaneous": '#f9c7ff'  # GRAPE
}
CURRENCY_DICT = {
    'US Dollar': '$',
    'British Pound': '£',
    'Euro': '€',
    'Japanese Yen': '¥',
    'Ukrainian Hryvnia': '₴'
}
