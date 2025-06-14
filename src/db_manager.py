import os
import sqlite3
from contextlib import contextmanager


def get_db_path():
    return os.getenv(
        "DB_PATH",
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "data", "albums.db")
        ),
    )


def create_table() -> None:
    with db_connection() as conn:
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


def add_favorito_column() -> None:
    with db_connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
            ALTER TABLE albums
            ADD COLUMN favorito BOOLEAN DEFAULT 0;
            """
            )
            print("✅ Coluna 'favorito' adicionada à tabela 'albums'.")
        except sqlite3.OperationalError:
            print("⚠️ Coluna 'favorito' já existe na tabela 'albums'.")


@contextmanager
def db_connection():
    conn = sqlite3.connect(get_db_path())
    try:
        yield conn
    finally:
        conn.close()
