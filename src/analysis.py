import pandas as pd

from src.sql_analysis import albums_by_decade, albums_by_genre, load_dataframe


def load_data_to_dataframe() -> pd.DataFrame:
    return load_dataframe()


def basic_statistics_sql() -> None:
    df = load_dataframe()
    print(f"\n🎯 Total de álbuns: {len(df)}\n")

    print("🎧 Álbuns por Gênero:")
    print(albums_by_genre(), "\n")

    print("📅 Álbuns por Década:")
    print(albums_by_decade(), "\n")
