import builtins
from unittest import mock

import src.analysis as analysis


def test_basic_statistics_sql_output(monkeypatch):
    # Mock print para capturar a saída
    printed = []

    def fake_print(*args, **kwargs):
        printed.append(" ".join(str(arg) for arg in args))

    monkeypatch.setattr(builtins, "print", fake_print)

    analysis.basic_statistics_sql()

    assert any("🎯 Total de álbuns:" in line for line in printed)
    assert any("🎧 Álbuns por Gênero:" in line for line in printed)
    assert any("🎤 Álbuns por Artista:" in line for line in printed)
    assert any("📅 Álbuns por Década:" in line for line in printed)
