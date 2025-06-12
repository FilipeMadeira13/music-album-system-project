import os
import sqlite3

from src.db_manager import DB_PATH, db_connection


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

        query = "SELECT nome, artista, genero, ano FROM albums"
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
            {"nome": r[0], "artista": r[1], "genero": r[2], "ano": r[3]} for r in rows
        ]


def filter_albums(term: str) -> list[dict[str, str | int]]:
    with db_connection() as conn:
        cursor = conn.cursor()

        query = """
        SELECT nome, artista, genero, ano FROM albums
        WHERE lower(nome) LIKE ?
        OR lower(artista) LIKE ?
        OR lower(genero) LIKE ?
        OR cast(ano as TEXT) LIKE ?
        """

        term_like = f"%{term}%"
        cursor.execute(query, (term_like, term_like, term_like, term_like))
        rows = cursor.fetchall()

        return [
            {"nome": r[0], "artista": r[1], "genero": r[2], "ano": r[3]} for r in rows
        ]


def remove_album_by_name(name: str) -> bool:
    with db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM albums WHERE lower(nome) = ?", (name.lower(),)
        )
        count = cursor.fetchone()[0]

        if count == 0:
            conn.close()
            return False

        cursor.execute("DELETE FROM albums WHERE lower(nome) = ?", (name.lower(),))
        conn.commit()
        return True


def display_albums(albums: list[dict[str, str | int]]) -> None:
    print("\n🎶 Suas álbuns são:")
    print("-" * 70)

    for i, music in enumerate(albums, start=1):
        print(
            f"{i}. Nome: {music['nome']:<20} | Artista: {music['artista']:<20} | Gênero: {music['genero']:<15} | Ano: {music['ano']}"
        )

    print("-" * 70)
