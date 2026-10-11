import datetime
from src.database import get_connection

def calculate_sm2(quality: int, repetitions: int, previous_interval: int, previous_ease: float):
    """
    Implements the standard SM-2 algorithm.
    quality: Response rating from 0 (complete blackout) to 5 (perfect recall).
    """
    if quality < 3:
        repetitions = 0
        interval = 1
    else:
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 6
        else:
            interval = int(previous_interval * previous_ease)
        repetitions += 1

    ease_factor = previous_ease + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    if ease_factor < 1.3:
        ease_factor = 1.3

    return repetitions, interval, ease_factor

def review_flashcard(card_id: int, quality: int):
    """Updates flashcard SRS parameters after a user study review."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT repetition, interval, ease_factor FROM flashcards WHERE id = ?", (card_id,))
        row = cursor.fetchone()
        if not row:
            return "Card not found."

        reps, prev_interval, prev_ease = row
        new_reps, new_interval, new_ease = calculate_sm2(quality, reps, prev_interval, prev_ease)
        
        next_date = datetime.date.today() + datetime.timedelta(days=new_interval)
        
        cursor.execute("""
            UPDATE flashcards 
            SET repetition = ?, interval = ?, ease_factor = ?, next_review_date = ?
            WHERE id = ?
        """, (new_reps, new_interval, new_ease, next_date, card_id))
        conn.commit()
    return f"Updated! Next review in {new_interval} day(s)."