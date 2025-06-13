import src.analysis as analysis
import src.sql_crud as sc
from src.enrichment import add_columns_to_table, enrich_album_data
from src.spotify_client import search_album_from_spotify
from src.utils.utils import album_exists, validate_year


def show_menu():
    print("=" * 50)
    print(f"🔷 ADMINISTRADOR DE MÚSICAS 🔷")
    print("=" * 50)
    print(
        """
    1 - Adicionar álbum (Via Spotify)
    2 - Listar álbuns
    3 - Filtrar álbuns
    4 - Remover álbum
    5 - Analisar dados
    6 - Atualizar álbum com dados do Spotify
    7 - Marcar álbum como favorito
    8 - Sortear álbum aleatório
    9 - Editar álbum
    10 - Sair
"""
    )
    return input("Escolha o número da opção acima: ").strip()


def handle_add_album_from_spotify():
    name = input("Nome do álbum: ").strip().title()
    artist = input("Artista: ").strip().title()

    if album_exists(name, artist):
        print("⚠️ Álbum já cadastrado.")
        return

    print("🔍 Buscando informações do álbum no Spotify...")
    data = search_album_from_spotify(name, artist)

    if not data:
        print("❌ Álbum não encontrado no Spotify.")
        return

    print("🎶 Álbum encontrado:")
    print(f"🎵 Nome: {data['nome']}")
    print(f"🎤 Artista: {data['artista']}")
    print(f"📅 Lançamento: {data['lancamento']}")
    print(f"🎼 Total de Faixas: {data['total_faixas']}")
    print(f"📈 Popularidade: {data['popularidade']}")
    print(f"🔗 Spotify: {data['spotify_url']}")

    confirm = (
        input("Deseja adicionar este álbum ao sistema? (s/n): ").strip().lower() == "s"
    )

    if confirm:
        year = int(data["lancamento"].split("-")[0])
        sc.add_album(
            {
                "nome": data["nome"],
                "artista": data["artista"],
                "genero": data.get("genero", "Desconhecido"),
                "ano": year,
                "spotify_url": data["spotify_url"],
            }
        )
    else:
        print("❌ Cadastro cancelado.")


def handle_list_albums():
    only_favs = input("Listar apenas álbuns favoritos? (s/n): ").strip().lower() == "s"
    if only_favs:
        albums = sc.list_favorites()
    else:
        print("Ordenar por:")
        order_name = input("Nome? (s/n): ").strip().lower() == "s"
        order_artist = input("Artista? (s/n): ").strip().lower() == "s"
        order_year = input("Ano? (s/n): ").strip().lower() == "s"

        albums = sc.list_albums(order_name, order_artist, order_year)
    if albums:
        sc.display_albums(albums)
    else:
        print("❌ A lista de álbuns está vazia.")


def handle_filter_albums():
    filter_term = (
        input("Digite o filtro para exibir a lista filtrada: ").strip().lower()
    )
    filtered_music = sc.filter_albums(filter_term)
    if filtered_music:
        sc.display_albums(filtered_music)
    else:
        print("❌ Nenhum álbum foi encontrado.")


def handle_remove_album():
    name = input("Digite o álbum que deseja excluir: ").strip().lower()
    artist = input("Digite o artista do álbum: ").strip().lower()
    if not name or not artist:
        print("⚠️ Nome do álbum e artista não podem ser vazios.")
        return
    confirmation = (
        input(f"Tem certeza que deseja excluir {name} do artista {artist}? (s/n): ")
        .strip()
        .lower()
        == "s"
    )
    if confirmation:
        album = sc.remove_album_by_name(name, artist)
        if album:
            print("✅ Álbum excluído com sucesso.")
        else:
            print("❌ Álbum não encontrado!")
    else:
        print("❌ Exclusão de álbum cancelada!")


def handle_enrich_album():
    name = input("Nome do álbum: ").strip().title()
    artist = input("Artista: ").strip().title()
    if name and artist:
        add_columns_to_table()
        enrich_album_data(name, artist)
    else:
        print("⚠️ Nome do álbum e artista não podem ser vazios.")


def handle_toggle_favorite():
    name = input("Nome do álbum: ").strip().title()
    artist = input("Artista: ").strip().title()
    is_fav = input("Marcar como favorito? (s/n): ").strip().lower() == "s"
    updated = sc.update_album_favorite(name, artist, is_fav)
    if updated:
        print("✅ Álbum atualizado com sucesso.")
    else:
        print("❌ Álbum não encontrado ou não atualizado.")


def handle_random_album():
    only_favs = (
        input("Escolher aleatóriamente apenas álbuns favoritos? (s/n): ")
        .strip()
        .lower()
        == "s"
    )
    album = sc.get_random_album(favorites_only=only_favs)

    if album:
        print("\n🎲 Álbum sorteado:")
        print(f"🎵 Nome: {album['nome']}")
        print(f"🎤 Artista: {album['artista']}")
        print(f"🎧 Gênero: {album['genero']}")
        print(f"📅 Ano: {album['ano']}")
    else:
        print("❌ Nenhum álbum encontrado para sortear.")


def handle_edit_album():
    print("🔧 Editar álbum")
    name = input("Nome do álbum: ").strip().title()
    artist = input("Artista: ").strip().title()

    if not album_exists(name, artist):
        print("❌ Álbum não encontrado.")
        return

    new_name = (
        input("Novo nome do álbum (deixe em branco para não alterar): ").strip().title()
    )
    new_artist = (
        input("Novo artista (deixe em branco para não alterar): ").strip().title()
    )
    new_genre = (
        input("Novo gênero (deixe em branco para não alterar): ").strip().title()
    )

    new_year_input = input("Novo ano (deixe em branco para não alterar): ").strip()
    new_year = None

    if new_year_input:
        try:
            new_year = int(new_year_input)
            if not validate_year(new_year):
                print("⚠️ Ano inválido.")
                return
        except ValueError:
            print("⚠️ Ano deve ser um número válido.")
            return

    updated = sc.edit_album(
        current_name=name,
        current_artist=artist,
        new_name=new_name if new_name else None,
        new_artist=new_artist if new_artist else None,
        new_genre=new_genre if new_genre else None,
        new_year=new_year,
    )

    if updated:
        print("✅ Álbum atualizado com sucesso.")
    else:
        print("❌ Não foi possível atualizar o álbum. Verifique os dados informados.")


def main():

    while True:
        option = show_menu()

        if option == "1":
            handle_add_album_from_spotify()
        elif option == "2":
            handle_list_albums()
        elif option == "3":
            handle_filter_albums()
        elif option == "4":
            handle_remove_album()
        elif option == "5":
            analysis.basic_statistics_sql()
        elif option == "6":
            handle_enrich_album()
        elif option == "7":
            handle_toggle_favorite()
        elif option == "8":
            handle_random_album()
        elif option == "9":
            handle_edit_album()
        elif option == "10":
            print("🎼 Você saiu do sistema de músicas.")
            break
        else:
            print("Escolha uma opção válida.")


if __name__ == "__main__":
    main()
