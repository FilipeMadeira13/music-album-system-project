import sqlite3

from src.db_manager import db_connection
from src.spotify_client import search_album_from_spotify


def add_columns_to_table() -> None:
    """Adiciona colunas extras se ainda não existirem."""
    with db_connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute("ALTER TABLE albums ADD COLUMN popularidade INTEGER")
        except sqlite3.OperationalError:
            pass  # Coluna já existe

        try:
            cursor.execute("ALTER TABLE albums ADD COLUMN total_faixas INTEGER")
        except sqlite3.OperationalError:
            pass

        try:
            cursor.execute("ALTER TABLE albums ADD COLUMN spotify_url TEXT")
        except sqlite3.OperationalError:
            pass

        conn.commit()


def enrich_album_data(name: str, artist: str) -> None:
    """Busca um álbum por nome e atualiza dados via Spotify API."""

    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM albums WHERE lower(nome) = ? AND lower(artista) = ?",
            (name.lower(), artist.lower()),
        )
        result = cursor.fetchone()

        if not result:
            print(f"❌ Álbum '{name}' de {artist} não encontrado na base de dados.")
            return

        album_id = result[0]
        print(f"🔍 Buscando informações no Spotify para: {name} de {artist}")
        spotify_data = search_album_from_spotify(name, artist)

        if not spotify_data:
            print(f"⚠️ Nenhuma informação encontrada na API.")
            return

        cursor.execute(
            """
            UPDATE albums
            SET popularidade = ?, total_faixas = ?, spotify_url = ?
            WHERE id = ?
            """,
            (
                spotify_data["popularidade"],
                spotify_data["total_faixas"],
                spotify_data["spotify_url"],
                album_id,
            ),
        )

        print(f"📊 Dados obtidos:")
        for k, v in spotify_data.items():
            print(f"  {k.capitalize()}: {v}")
        conn.commit()
        print(f"✅ Dados do álbum '{name}' atualizados com sucesso.")
