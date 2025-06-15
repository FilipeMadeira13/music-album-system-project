import builtins
from unittest.mock import patch

import pytest

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
