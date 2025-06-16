import builtins
from unittest.mock import patch

import pytest

import src.handlers  # noqa: E402
from src import handlers, sql_crud


@patch("src.handlers.search_album_from_spotify")
@patch("src.sql_crud.add_album")
@patch("builtins.input")
def test_handle_add_album_from_spotify_success(
    mock_input, mock_add_album, mock_search_album, capsys
):
    # Simula inputs do usuário
    mock_input.side_effect = ["Album Teste", "Artista Teste", "s"]

    # Simula retorno da API do Spotify
    mock_search_album.return_value = {
        "nome": "Test Album",
        "artista": "Test Artist",
        "lancamento": "2020-05-01",
        "total_faixas": 10,
        "popularidade": 75,
        "spotify_url": "https://spotify.com/album/test",
    }

    # Executa o handler
    handlers.handle_add_album_from_spotify()

    # Verifica se add_album foi chamado corretamente
    mock_add_album.assert_called_once_with(
        {
            "nome": "Test Album",
            "artista": "Test Artist",
            "genero": "Desconhecido",
            "ano": 2020,
            "spotify_url": "https://spotify.com/album/test",
        }
    )

    # Verifica a saída do terminal
    captured = capsys.readouterr()
    assert "🎶 Álbum encontrado:" in captured.out
    assert "✅" not in captured.out


@patch("src.sql_crud.display_albums")
@patch("src.sql_crud.list_favorites")
@patch("builtins.input", side_effect=["s"])
def test_handle_list_albums_favorites(mock_input, mock_list_fav, mock_display):
    mock_list_fav.return_value = [
        {
            "nome": "Album Favorito",
            "artista": "Artista Favorito",
            "genero": "Rock",
            "ano": 2020,
            "favorito": 1,
        }
    ]

    from src.handlers import handle_list_albums

    handle_list_albums()

    mock_list_fav.assert_called_once()
    mock_display.assert_called_once()


@patch("src.sql_crud.display_albums")
@patch("src.sql_crud.list_albums")
@patch("builtins.input", side_effect=["n", "s", "n", "s"])
def test_handle_list_albums_with_order(mock_input, mock_list, mock_display):
    mock_list.return_value = [
        {
            "nome": "Album Teste",
            "artista": "Artista Teste",
            "genero": "Rock",
            "ano": 2023,
            "favorito": 0,
        }
    ]

    from src.handlers import handle_list_albums

    handle_list_albums()
    mock_list.assert_called_once_with(True, False, True)
    mock_display.assert_called_once()


@patch("src.sql_crud.remove_album_by_name", return_value=True)
@patch("builtins.input", side_effect=["Album Teste", "Artista Teste", "s"])
def test_handle_remove_album_success(mock_input, mock_remove, capsys):
    handlers.handle_remove_album()

    captured = capsys.readouterr()
    assert "✅ Álbum excluído com sucesso." in captured.out


@patch("src.sql_crud.remove_album_by_name", return_value=False)
@patch("builtins.input", side_effect=["Album Inexistente", "Artista Inexistente", "s"])
def test_handle_remove_album_not_found(mock_input, mock_remove, capsys):
    handlers.handle_remove_album()

    captured = capsys.readouterr()
    assert "❌ Álbum não encontrado!" in captured.out


@patch("builtins.input", side_effect=["Album Teste", "Artista Teste", "n"])
def test_handle_remove_album_cancelled(mock_input, capsys):
    handlers.handle_remove_album()

    captured = capsys.readouterr()
    assert "❌ Exclusão de álbum cancelada!" in captured.out


@patch("builtins.input", side_effect=["", ""])
def test_handle_remove_album_empty_fields(mock_input, capsys):
    handlers.handle_remove_album()

    captured = capsys.readouterr()
    assert "⚠️ Nome do álbum e artista não podem ser vazios." in captured.out


@patch(
    "src.sql_crud.filter_albums",
    return_value=[
        {
            "nome": "Álbum X",
            "artista": "Artista Y",
            "genero": "Rock",
            "ano": 2022,
            "favorito": 0,
        }
    ],
)
@patch("src.sql_crud.display_albums")
@patch("builtins.input", return_value="rock")
def test_handle_filter_albums_found(mock_input, mock_display, mock_filter, capsys):
    handlers.handle_filter_albums()
    mock_display.assert_called_once()
    mock_filter.assert_called_once_with("rock")


@patch("src.sql_crud.filter_albums", return_value=[])
@patch("builtins.input", return_value="rock")
def test_handle_filter_albums_not_found(mock_input, mock_filter, capsys):
    handlers.handle_filter_albums()
    captured = capsys.readouterr()
    assert "❌ Nenhum álbum foi encontrado." in captured.out


@patch(
    "builtins.input",
    side_effect=[
        "Album Teste",
        "Artista Teste",  # busca álbum existente
        "Novo Álbum",
        "Novo Artista",
        "Novo Gênero",
        "2022",  # novos valores
    ],
)
@patch("src.handlers.album_exists", return_value=True)
@patch("src.sql_crud.edit_album", return_value=True)
def test_handle_edit_album_success(mock_edit, mock_exists, mock_input, capsys):
    handlers.handle_edit_album()
    captured = capsys.readouterr()
    assert "✅ Álbum atualizado com sucesso." in captured.out
    mock_edit.assert_called_once_with(
        current_name="Album Teste",
        current_artist="Artista Teste",
        new_name="Novo Álbum",
        new_artist="Novo Artista",
        new_genre="Novo Gênero",
        new_year=2022,
    )


@patch(
    "builtins.input",
    side_effect=["Album Teste", "Artista Teste", "", "", "", "3000"],  # ano inválido
)
@patch("src.handlers.album_exists", return_value=True)
def test_handle_edit_album_invalid_year(mock_exists, mock_input, capsys):
    handlers.handle_edit_album()
    captured = capsys.readouterr()
    assert "⚠️ Ano inválido." in captured.out


@patch("builtins.input", return_value="s")
@patch("src.sql_crud.get_random_album")
def test_handle_random_album_found(mock_get, mock_input, capsys):
    mock_get.return_value = {
        "nome": "Álbum Aleatório",
        "artista": "Artista Aleatório",
        "genero": "Pop",
        "ano": 2020,
    }
    handlers.handle_random_album()
    captured = capsys.readouterr()
    assert "🎲 Álbum sorteado:" in captured.out


@patch("builtins.input", return_value="s")
@patch("src.sql_crud.get_random_album", return_value=None)
def test_handle_random_album_not_found(mock_get, mock_input, capsys):
    handlers.handle_random_album()
    captured = capsys.readouterr()
    assert "❌ Nenhum álbum encontrado para sortear." in captured.out


def test_handle_toggle_favorite_album_updated(capsys):
    # Adiciona um álbum de teste
    sql_crud.add_album(
        {
            "nome": "Album Teste",
            "artista": "Artista Teste",
            "genero": "Rock",
            "ano": 2023,
        }
    )

    user_inputs = iter(["Album Teste", "Artista Teste", "s"])

    with patch.object(builtins, "input", lambda _: next(user_inputs)):
        handlers.handle_toggle_favorite()

    captured = capsys.readouterr()
    assert "✅ Álbum atualizado com sucesso." in captured.out


def test_handle_toggle_favorite_album_not_found(capsys):
    user_inputs = iter(["Album Inexistente", "Artista Inexistente", "s"])

    with patch.object(builtins, "input", lambda _: next(user_inputs)):
        with patch("src.sql_crud.update_album_favorite", return_value=False):
            handlers.handle_toggle_favorite()

    captured = capsys.readouterr()
    assert "❌ Álbum não encontrado ou não atualizado." in captured.out
