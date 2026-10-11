import sqlite3
import os
from pathlib import Path

# Use project root data directory
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

LANG_DB_PATH = DATA_DIR / "syntext_language.db"

def get_connection():
    return sqlite3.connect(LANG_DB_PATH)

def init_db():
    """Initializes tables for flashcards and SRS tracking."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS flashcards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_lang TEXT NOT NULL,
                front TEXT NOT NULL,
                back TEXT NOT NULL,
                example_sentence TEXT,
                interval INTEGER DEFAULT 1,
                ease_factor REAL DEFAULT 2.5,
                repetition INTEGER DEFAULT 0,
                next_review_date DATE DEFAULT CURRENT_DATE
            )
        """)
        conn.commit()

def save_flashcard_record(target_lang: str, front: str, back: str, example_sentence: str) -> str:
    """Inserts a new flashcard into the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO flashcards (target_lang, front, back, example_sentence) 
               VALUES (?, ?, ?, ?)""",
            (target_lang, front, back, example_sentence)
        )
        conn.commit()
    return f"Saved flashcard: '{front}' ({back})"

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {LANG_DB_PATH}")