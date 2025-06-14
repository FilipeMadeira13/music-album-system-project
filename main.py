import src.analysis as analysis
import src.handlers as hd
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


def main():

    while True:
        option = show_menu()

        if option == "1":
            hd.handle_add_album_from_spotify()
        elif option == "2":
            hd.handle_list_albums()
        elif option == "3":
            hd.handle_filter_albums()
        elif option == "4":
            hd.handle_remove_album()
        elif option == "5":
            analysis.basic_statistics_sql()
        elif option == "6":
            hd.handle_enrich_album()
        elif option == "7":
            hd.handle_toggle_favorite()
        elif option == "8":
            hd.handle_random_album()
        elif option == "9":
            hd.handle_edit_album()
        elif option == "10":
            print("🎼 Você saiu do sistema de músicas.")
            break
        else:
            print("Escolha uma opção válida.")


if __name__ == "__main__":
    main()
