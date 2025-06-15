import os
import sqlite3

import pytest

TEST_DB_PATH = "test_albums.db"


@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch):
    monkeypatch.setenv("DB_PATH", TEST_DB_PATH)

    # Cria tabela antes do teste
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS albums (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            artista TEXT NOT NULL,
            genero TEXT NOT NULL,
            ano INTEGER NOT NULL,
            favorito BOOLEAN DEFAULT 0
        )
        """
    )
    conn.commit()
    yield
    conn.close()
    # Remove o banco de dados após o teste
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
