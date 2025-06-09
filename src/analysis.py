import json
import os

import pandas as pd

from sql_analysis import albums_by_decade, albums_by_genre, load_dataframe
from src.crud import FILE_PATH


def load_data_to_dataframe() -> pd.DataFrame:
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
        return pd.DataFrame(data)

    print("❌ Arquivo de dados não encontrado.")
    return pd.DataFrame()


def basic_statistics_sql() -> None:
    df = load_dataframe()
    print(f"\n🎯 Total de álbuns: {len(df)}\n")

    print("🎧 Álbuns por Gênero:")
    print(albums_by_genre(), "\n")

    print("📅 Álbuns por Década:")
    print(albums_by_decade(), "\n")


def basic_statistics(df: pd.DataFrame) -> None:
    print("\n🔍 Estatísticas básicas:")
    print(f"Total de álbuns: {len(df)}\n")

    print("\n🎧 Álbuns por Gênero:")
    print(df["genero"].value_counts(), "\n")

    print("\n🎤 Álbuns por artista:")
    print(df["artista"].value_counts(), "\n")

    print("🎶 Álbuns por Nome (ocorrências repetidas):")
    print(df["nome"].value_counts(), "\n")

    print("📋 Álbuns por ano:")
    print(df["ano"].value_counts())
