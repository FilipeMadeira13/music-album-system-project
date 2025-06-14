import os
import sqlite3

import pytest

from src.utils.utils import album_exists, validate_year

TEST_DB_PATH = "test_albums.db"


@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch):
    monkeypatch.setenv("DB_PATH", TEST_DB_PATH)

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
    cursor.execute(
        """
        INSERT INTO albums (nome, artista, genero, ano)
        VALUES ('Existing Album', 'Known Artist', 'Test Genre', 2023)
    """
    )
    conn.commit()
    yield
    conn.close()

    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


def test_album_exists_found():
    assert album_exists("Existing Album", "Known Artist") is True


def test_album_exists_not_found():
    assert album_exists("Nonexistent Album", "Unknown Artist") is False


def test_validate_year_valid():
    assert validate_year(2023) is True
    assert validate_year(1900) is True


def test_validate_year_invalid():
    assert validate_year(1899) is False
    assert validate_year(3000) is False
