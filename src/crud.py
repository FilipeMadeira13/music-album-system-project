import json
import os

FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "albums.json")
FILE_PATH = os.path.abspath(FILE_PATH)


def add_music_album(album: dict[str, str]) -> None:
    albums = load_music_data()

    albums.append(album)

    save_music_data(albums)
    print("🎶 Álbum adicionado com sucesso.")


def list_music_albums(
    order_name: bool, order_artist: bool, order_year: bool
) -> list[dict[str, str]]:
    albums = load_music_data()

    if order_name and order_artist and order_year:
        return sorted(albums, key=lambda x: (x["nome"], x["artista"], x["ano"]))
    elif order_name and order_artist:
        return sorted(albums, key=lambda x: (x["nome"], x["artista"]))
    elif order_name and order_year:
        return sorted(albums, key=lambda x: (x["nome"], x["ano"]))
    elif order_artist and order_year:
        return sorted(albums, key=lambda x: (x["artista"], x["ano"]))
    elif order_name:
        return sorted(albums, key=lambda x: x["nome"])
    elif order_artist:
        return sorted(albums, key=lambda x: x["artista"])
    elif order_year:
        return sorted(albums, key=lambda x: x["ano"])

    return albums


def filter_music(filter: str) -> list[dict[str, str]]:
    musics = load_music_data()

    return [
        music
        for music in musics
        if (
            filter in music["nome"].lower()
            or filter in music["artista"].lower()
            or filter in music["genero"].lower()
            or filter in str(music["ano"]).lower()
        )
    ]


def remove_music_album(name: str) -> list[dict[str, str]]:
    albums = load_music_data()

    filtered_music = [m for m in albums if m["nome"].lower() != name.lower()]

    if len(albums) == len(filtered_music):
        print(f'❌ Álbum "{name.title()}" não encontrado.')
    else:
        save_music_data(filtered_music)
        print(f'✅ Álbum "{name.title()}" removido com sucesso.')


def display_music_albums(albums: list[dict[str, str]]) -> None:
    print("\n🎶 Suas álbuns são:")
    print("-" * 70)

    for i, music in enumerate(albums, start=1):
        print(
            f"{i}. Nome: {music['nome']:<20} | Artista: {music['artista']:<20} | Gênero: {music['genero']:<15} | Ano: {music['ano']}"
        )

    print("-" * 70)


def load_music_data() -> list[dict[str, str]]:
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    return []


def save_music_data(musics: list[dict[str, str]]) -> None:
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(musics, file, indent=4, ensure_ascii=False)
