import os
import sqlite3

import pandas as pd
import pytest

from src import sql_analysis

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
    cursor.executemany(
        """
        INSERT INTO albums (nome, artista, genero, ano) VALUES (?, ?, ?, ?)
        """,
        [
            ("Album A", "Artista A", "Rock", 1994),
            ("Album B", "Artista B", "Pop", 2005),
            ("Album C", "Artista C", "Jazz", 2010),
            ("Album D", "Artista D", "Rock", 2022),
        ],
    )
    conn.commit()
    yield
    conn.close()
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


def test_load_dataframe():
    df = sql_analysis.load_dataframe()

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 4


def test_albums_by_genre():
    df = sql_analysis.albums_by_genre()

    assert "genero" in df.columns
    assert "quantidade" in df.columns
    assert df[df["genero"] == "Rock"]["quantidade"].iloc[0] == 2


def test_albums_by_decade():
    df = sql_analysis.albums_by_decade()
    decades = df["decada"].to_list()

    assert 1990 in decades
    assert 2000 in decades
    assert 2010 in decades
    assert 2020 in decades


def test_albums_by_artist():
    df = sql_analysis.albums_by_artist()

    assert df[df["artista"] == "Artista A"]["quantidade"].iloc[0] == 1


def test_albums_by_decade_range():
    df = sql_analysis.albums_by_decade_range(2000, 2020)

    assert len(df) == 2
    assert df["ano"].min() >= 2000
    assert df["ano"].max() <= 2020
