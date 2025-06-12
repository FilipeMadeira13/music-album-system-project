from datetime import datetime

from src.db_manager import db_connection


def validate_year(year: int) -> bool:
    return 1900 <= year <= datetime.now().year


def album_exists(name: str) -> bool:
    """Verifica se um álbum existe na base de dados."""
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM albums WHERE lower(nome) = ?", (name.lower(),)
        )
        return cursor.fetchone()[0] > 0
