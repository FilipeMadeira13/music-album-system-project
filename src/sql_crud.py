import random

from src.db_manager import db_connection


def add_album(album: dict[str, str | int]) -> None:
    with db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO albums (nome, artista, genero, ano)
            VALUES (?, ?, ?, ?)
            """,
            (album["nome"], album["artista"], album["genero"], album["ano"]),
        )

        conn.commit()
        print("✅ Álbum adicionado com sucesso.")


def list_albums(
    order_name=False, order_artist=False, order_year=False
) -> list[dict[str, str | int]]:
    with db_connection() as conn:
        cursor = conn.cursor()

        query = "SELECT nome, artista, genero, ano, favorito FROM albums"
        order_clauses = []

        if order_name:
            order_clauses.append("nome")
        if order_artist:
            order_clauses.append("artista")
        if order_year:
            order_clauses.append("ano")

        if order_clauses:
            query += " ORDER BY " + ", ".join(order_clauses)

        cursor.execute(query)
        rows = cursor.fetchall()

        return [
            {
                "nome": r[0],
                "artista": r[1],
                "genero": r[2],
                "ano": r[3],
                "favorito": r[4],
            }
            for r in rows
        ]


def filter_albums(term: str) -> list[dict[str, str | int]]:
    with db_connection() as conn:
        cursor = conn.cursor()

        query = """
        SELECT nome, artista, genero, ano, favorito FROM albums
        WHERE lower(nome) LIKE ?
        OR lower(artista) LIKE ?
        OR lower(genero) LIKE ?
        OR cast(ano as TEXT) LIKE ?
        """

        term_like = f"%{term}%"
        cursor.execute(query, (term_like, term_like, term_like, term_like))
        rows = cursor.fetchall()

        return [
            {
                "nome": r[0],
                "artista": r[1],
                "genero": r[2],
                "ano": r[3],
                "favorito": r[4],
            }
            for r in rows
        ]


def remove_album_by_name(name: str, artist: str) -> bool:
    with db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM albums WHERE lower(nome) = ? AND lower(artista) = ?",
            (name.lower(), artist.lower()),
        )
        count = cursor.fetchone()[0]

        if count == 0:
            conn.close()
            return False

        cursor.execute(
            "DELETE FROM albums WHERE lower(nome) = ? AND lower(artista) = ?",
            (name.lower(), artist.lower()),
        )
        conn.commit()
        return True


def update_album_favorite(name: str, artist: str, favorite: bool) -> bool:
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE albums SET favorito = ? WHERE lower(nome) = ? AND lower(artista) = ?",
            (int(favorite), name.lower(), artist.lower()),
        )
        conn.commit()
        return cursor.rowcount > 0


def list_favorites() -> list[dict[str, str | int]]:
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT nome, artista, genero, ano, favorito FROM albums WHERE favorito = 1"
        )
        rows = cursor.fetchall()
        return [
            {
                "nome": r[0],
                "artista": r[1],
                "genero": r[2],
                "ano": r[3],
                "favorito": r[4],
            }
            for r in rows
        ]


def get_random_album(favorites_only=False) -> dict[str, str | int] | None:
    with db_connection() as conn:
        cursor = conn.cursor()
        if favorites_only:
            cursor.execute(
                "SELECT nome, artista, genero, ano, favorito FROM albums WHERE favorito = 1"
            )
        else:
            cursor.execute("SELECT nome, artista, genero, ano, favorito FROM albums")
        rows = cursor.fetchall()
        if not rows:
            return None

        chosen = random.choice(rows)
        return {
            "nome": chosen[0],
            "artista": chosen[1],
            "genero": chosen[2],
            "ano": chosen[3],
            "favorito": chosen[4],
        }


def edit_album(
    current_name: str,
    current_artist: str,
    new_name: str | None,
    new_artist: str | None,
    new_genre: str | None,
    new_year: int | None,
) -> bool:
    with db_connection() as conn:
        cursor = conn.cursor()

        updates = []
        params = []

        if new_name:
            updates.append("nome = ?")
            params.append(new_name)
        if new_artist:
            updates.append("artista = ?")
            params.append(new_artist)
        if new_genre:
            updates.append("genero = ?")
            params.append(new_genre)
        if new_year:
            updates.append("ano = ?")
            params.append(new_year)

        if not updates:
            print("⚠️ Nenhum campo para atualizar.")
            return False

        params.extend([current_name.lower(), current_artist.lower()])
        query = f"""
        UPDATE albums
        SET {', '.join(updates)}
        WHERE lower(nome) = ? AND lower(artista) = ?
        """

        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount > 0


def display_albums(albums: list[dict[str, str | int]]) -> None:
    print("\n🎶 Suas álbuns são:")
    print("-" * 70)

    for i, album in enumerate(albums, start=1):
        if "favorito" in album and album["favorito"] == 1:
            print(f"⭐️ {i}. ", end="")
        else:
            print(f"{i}. ", end="")
        print(
            f"🎵 {album['nome']} - 🎤 {album['artista']} - 🎧 {album['genero']} - 📅 {album['ano']}"
        )

    print("-" * 70)
