from langchain_core.tools import tool
from src.database import save_flashcard_record

@tool
def save_flashcard(target_lang: str, front: str, back: str, example_sentence: str) -> str:
    """
    Save a new vocabulary word or phrase as a flashcard.
    Args:
        target_lang: Language being learned (e.g., Spanish, German).
        front: The target language word/phrase.
        back: English translation.
        example_sentence: Short example sentence using the word.
    """
    return save_flashcard_record(target_lang, front, back, example_sentence)