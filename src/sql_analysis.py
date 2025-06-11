import sqlite3

import pandas as pd

from src.db_manager import DB_PATH


def load_dataframe() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM albums", conn)
    conn.close()
    return df


def albums_by_genre() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT genero, COUNT(*) AS quantidade
    FROM albums
    GROUP BY genero
    ORDER BY quantidade DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def albums_by_decade() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT (ano / 10) * 10 AS decada, COUNT(*) AS quantidade
    FROM albums
    GROUP BY decada
    ORDER BY decada
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def albums_by_artist() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT artista, COUNT(*) AS quantidade
    FROM albums
    GROUP BY artista
    ORDER BY quantidade DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def albums_by_decade_range(start_year: int, end_year: int) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT nome, artista, genero, ano
    FROM albums
    WHERE ano BETWEEN ? AND ?
    ORDER BY ano
    """
    df = pd.read_sql_query(query, conn, params=(start_year, end_year))
    conn.close()
    return df
