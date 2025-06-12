import src.analysis as analysis
import src.sql_crud as sc
from src.enrichment import add_columns_to_table, enrich_album_data
from src.utils.utils import album_exists, validate_year


def show_menu():
    print("=" * 50)
    print(f"🔷 ADMINISTRADOR DE MÚSICAS 🔷")
    print("=" * 50)
    print(
        """
    1 - Adicionar álbum
    2 - Listar álbuns
    3 - Filtrar álbuns
    4 - Remover álbum
    5 - Analisar dados
    6 - Atualizar álbum com dados do Spotify
    7 - Sair
"""
    )
    return input("Escolha o número da opção acima: ").strip()


def handle_add_album():
    name = input("Nome do álbum: ").strip().title()

    if album_exists(name):
        print("⚠️ Álbum já cadastrado.")
        return

    artist = input("Artista: ").strip().title()
    genre = input("Gênero: ").strip().title()

    while True:
        try:
            year = int(input("Ano de lançamento: ").strip())

            if validate_year(year):
                break
            else:
                print("⚠️ Ano fora do intervalo esperado.")

        except ValueError:
            print("⚠️ Ano inválido. Digite um número inteiro.")

    if name and artist and genre:
        sc.add_album({"nome": name, "artista": artist, "genero": genre, "ano": year})
    else:
        print("⚠️ Existem campos que não foram digitados. Por favor, tente novamente.")


def handle_list_albums():
    order_name = input("Deseja ordenar por nome? (s/n): ").strip().lower() == "s"
    order_artist = input("Deseja ordenar por artista? (s/n): ").strip().lower() == "s"
    order_year = input("Deseja ordenar por ano? (s/n): ").strip().lower() == "s"
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
    confirmation = (
        input(f"Tem certeza que deseja excluir {name}? (s/n): ").strip().lower() == "s"
    )
    if confirmation:
        album = sc.remove_album_by_name(name)
        if album:
            print("✅ Álbum excluído com sucesso.")
        else:
            print("❌ Álbum não encontrado!")
    else:
        print("❌ Exclusão de álbum cancelado!")


def handle_enrich_album():
    album_name = input("Digite o nome do álbum que deseja enriquecer: ").strip().title()
    if album_name:
        add_columns_to_table()
        enrich_album_data(album_name)
    else:
        print("⚠️ Nome do álbum não pode ser vazio.")


def main():

    while True:
        option = show_menu()

        if option == "1":
            handle_add_album()
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
            print("🎼 Você saiu do sistema de músicas.")
            break
        else:
            print("Escolha uma opção válida.")


if __name__ == "__main__":
    main()
