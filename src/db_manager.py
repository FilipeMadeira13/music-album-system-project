import os
import sqlite3
from contextlib import contextmanager

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "albums.db")
)


def create_table() -> None:
    with db_connection as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS albums (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            artista TEXT NOT NULL,
            genero TEXT NOT NULL,
            ano INTEGER NOT NULL
        );
        """
        )
        conn.commit()
        print("✅ Tabela 'albums' criada ou já existente.")


@contextmanager
def db_connection():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()
