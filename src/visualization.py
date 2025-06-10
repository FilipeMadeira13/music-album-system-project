from pathlib import Path

import pandas as pd
import plotly.express as px


def plot_releases_by_genre(df: pd.DataFrame) -> None:
    img_dir = ensure_image_folder()

    genre_count = df["genero"].value_counts().reset_index()
    genre_count.columns = ["Gênero", "Quantidade"]

    fig = px.bar(genre_count, x="Gênero", y="Quantidade", title="🎶 Álbuns por Gênero")
    fig.show()
    fig.write_image(img_dir / "plot_genero.png")


def plot_releases_by_artist(df: pd.DataFrame) -> None:
    img_dir = ensure_image_folder()

    artist_count = df["artista"].value_counts().reset_index()
    artist_count.columns = ["Artista", "Quantidade"]

    fig = px.bar(
        artist_count, x="Artista", y="Quantidade", title="🎤 Álbuns por Artista"
    )
    fig.show()
    fig.write_image(img_dir / "plot_artista.png")


def plot_releases_by_year(df: pd.DataFrame) -> None:
    img_dir = ensure_image_folder()

    fig = px.histogram(
        df,
        x="ano",
        nbins=30,
        title="📅 Lançamentos por Ano",
        labels={"ano": "Ano de Lançamento"},
    )
    fig.update_layout(xaxis_title="Ano", yaxis_title="Quantidade de Álbuns")
    fig.show()
    fig.write_image(img_dir / "plot_ano.png")


def plot_releases_by_decade(df: pd.DataFrame) -> None:
    img_dir = ensure_image_folder()

    df["decada"] = (df["ano"] // 10) * 10
    decade_count = df["decada"].value_counts().sort_index().reset_index()
    decade_count.columns = ["Década", "Quantidade"]

    fig = px.bar(
        decade_count,
        x="Década",
        y="Quantidade",
        title="📆 Lançamentos por Década",
        labels={"Quantidade": "Qtd. de Álbuns"},
    )
    fig.show()
    fig.write_image(img_dir / "plot_decada.png")


def ensure_image_folder() -> Path:
    project_root = Path.cwd().parent
    img_dir = project_root / "img"

    img_dir.mkdir(exist_ok=True)
    return img_dir
