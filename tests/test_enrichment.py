import os
import sqlite3

from src.db_manager import DB_PATH, db_connection
from src.enrichment import add_columns_to_table


def test_add_columns_to_table(tmp_path):
    """Testa se as colunas extras são adicionadas corretamente."""

    # Cria um caminho de banco de teste temporário
    test_db = tmp_path / "test_albums.db"
    os.environ["DB_PATH"] = str(test_db)

    # Cria tabela base sem as colunas extras
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS albums;")
        cursor.execute(
            """
            CREATE TABLE albums (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                artista TEXT NOT NULL,
                genero TEXT NOT NULL,
                ano INTEGER NOT NULL
            )
        """
        )
        conn.commit()

        # Aponta o contexto do DB para o banco de teste
        original_db_path = DB_PATH
        from src import db_manager

        db_manager.DB_PATH = str(test_db)

        # Executa a função a ser testada
        add_columns_to_table()

        # Verifica se as colunas extras existem
        with sqlite3.connect(test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(albums);")
            columns = [col[1] for col in cursor.fetchall()]

        assert "popularidade" in columns
        assert "total_faixas" in columns
        assert "spotify_url" in columns

        db_manager.DB_PATH = original_db_path  # Restaura o caminho original do DB_PATH
