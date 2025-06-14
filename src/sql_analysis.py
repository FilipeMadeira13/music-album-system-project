import pandas as pd

from src.db_manager import db_connection


def load_dataframe() -> pd.DataFrame:
    with db_connection() as conn:
        df = pd.read_sql_query("SELECT * FROM albums", conn)
        return df


def albums_by_genre() -> pd.DataFrame:
    with db_connection() as conn:
        query = """
        SELECT genero, COUNT(*) AS quantidade
        FROM albums
        GROUP BY genero
        ORDER BY quantidade DESC
        """
        df = pd.read_sql_query(query, conn)
        return df


def albums_by_decade() -> pd.DataFrame:
    with db_connection() as conn:
        query = """
        SELECT (ano / 10) * 10 AS decada, COUNT(*) AS quantidade
        FROM albums
        GROUP BY decada
        ORDER BY decada
        """
        df = pd.read_sql_query(query, conn)
        return df


def albums_by_artist() -> pd.DataFrame:
    with db_connection() as conn:
        query = """
        SELECT artista, COUNT(*) AS quantidade
        FROM albums
        GROUP BY artista
        ORDER BY quantidade DESC
        """
        df = pd.read_sql_query(query, conn)
        return df


def albums_by_decade_range(start_year: int, end_year: int) -> pd.DataFrame:
    with db_connection() as conn:
        query = """
        SELECT nome, artista, genero, ano
        FROM albums
        WHERE ano BETWEEN ? AND ?
        ORDER BY ano
        """
        df = pd.read_sql_query(query, conn, params=(start_year, end_year))
        return df
