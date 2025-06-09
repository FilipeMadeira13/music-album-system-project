from datetime import datetime

import src.analysis as analysis
import src.crud as ms
from src.db_manager import create_table, migrate_json_data_to_sqlite


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
    6 - Migrar para SQlite
    7 - Sair
"""
    )
    return input("Escolha o número da opção acima: ").strip()


def main():

    while True:
        option = show_menu()

        if option == "1":
            name = input("Nome do álbum: ").strip().title()
            artist = input("Artista: ").strip().title()
            genre = input("Gênero: ").strip().title()

            while True:
                try:
                    year = int(input("Ano de lançamento: ").strip())

                    if 1900 <= year <= datetime.now().year:
                        break
                    else:
                        print("⚠️ Ano fora do intervalo esperado.")

                except ValueError:
                    print("⚠️ Ano inválido. Digite um número inteiro.")

            if name and artist and genre:
                ms.add_music_album(
                    {"nome": name, "artista": artist, "genero": genre, "ano": year}
                )
            else:
                print(
                    "⚠️ Existem campos que não foram digitados. Por favor, tente novamente."
                )
        elif option == "2":
            order_name = (
                input("Deseja ordenar por nome? (s/n): ").strip().lower() == "s"
            )
            order_artist = (
                input("Deseja ordenar por artista? (s/n): ").strip().lower() == "s"
            )
            order_year = input("Deseja ordenar por ano? (s/n): ").strip().lower() == "s"
            albums = ms.list_music_albums(order_name, order_artist, order_year)
            if albums:
                ms.display_music_albums(albums)
            else:
                print("❌ A lista de álbuns está vazia.")
        elif option == "3":
            filter = (
                input("Digite o filtro para exibir a lista filtrada: ").strip().lower()
            )
            filtered_music = ms.filter_music(filter)
            if filtered_music:
                ms.display_music_albums(filtered_music)
            else:
                print("❌ Nenhuma álbum foi encontrado.")
        elif option == "4":
            album = input("Digite o álbum que deseja excluir: ").strip().lower()

            confirmation = (
                input(f"Tem certeza que deseja excluir {album}? (s/n): ")
                .strip()
                .lower()
                == "s"
            )

            if confirmation:
                albums = ms.remove_music_album(album)
            else:
                print("❌ Exclusão de álbum cancelado!")
        elif option == "5":
            df = analysis.load_data_to_dataframe()
            if not df.empty:
                analysis.basic_statistics_sql()
        elif option == "6":
            create_table()
            migrate_json_data_to_sqlite()
        elif option == "7":
            print("🎼 Você saiu do sistema de músicas.")
            break
        else:
            print("Escolha uma opção válida.")


if __name__ == "__main__":
    main()
