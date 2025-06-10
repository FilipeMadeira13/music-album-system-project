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
