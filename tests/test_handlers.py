import builtins
from unittest.mock import patch

import pytest

from src import handlers, sql_crud


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
