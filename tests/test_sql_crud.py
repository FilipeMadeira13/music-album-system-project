import os
import sqlite3

import pytest

from src import sql_crud
from src.db_manager import DB_PATH

TEST_DB_PATH = "test_albums.db"


@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch):
    # Use banco isolado
    monkeypatch.setattr("src.db_manager.DB_PATH", TEST_DB_PATH)

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
    os.remove(TEST_DB_PATH)


def test_add_and_list_album():
    album = {
        "nome": "Test Album",
        "artista": "Test Artist",
        "genero": "Test Genre",
        "ano": 2023,
    }
    sql_crud.add_album(album)
    result = sql_crud.list_albums()

    assert any(a["nome"] == "Test Album" for a in result)
    assert any(a["artista"] == "Test Artist" for a in result)
    assert isinstance(result, list)
    assert len(result) == 1


def test_add_album():
    pass


def test_remove_album_by_name():
    pass


def test_get_random_album():
    pass


def test_update_album_favorite():
    pass
