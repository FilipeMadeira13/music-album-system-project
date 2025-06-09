import json
import os
import sqlite3

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "albums.db")
)
JSON_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "albums.json")
)


def create_table() -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS albums (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        artista TEXT NOT NULL,
        genero TEXT NOT NULL,
        ano INTEGER NOT NULL
    );
    """
    )
    conn.commit()
    conn.close()
    print("✅ Tabela 'albums' criada ou já existente.")


def migrate_json_data_to_sqlite() -> None:
    if not os.path.exists(JSON_PATH):
        print("❌ Arquivo albums.json não encontrado.")
        return

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        albums = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for album in albums:
        cursor.execute(
            """
            INSERT INTO albums (nome, artista, genero, ano)
            VALUES (?, ?, ?, ?)
        """,
            (album["nome"], album["artista"], album["genero"], album["ano"]),
        )

    conn.commit()
    conn.close()
    print(f"✅ {len(albums)} álbuns migrados com sucesso para SQLite.")
