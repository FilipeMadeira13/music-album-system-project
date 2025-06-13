import streamlit as st
from dotenv import load_dotenv

from src.spotify_client import search_album_from_spotify
from src.sql_analysis import (
    albums_by_artist,
    albums_by_decade,
    albums_by_decade_range,
    albums_by_genre,
)

load_dotenv()


@st.cache_data
def cached_search_album_from_spotify(album_name: str, artist_name: str) -> dict:
    return search_album_from_spotify(album_name, artist_name)


st.title("🎵 Análise de Álbuns Musicais")

st.subheader("🔍 Buscar Álbum no Spotify")

album_name = st.text_input("Digite o nome do álbum: ").title().strip()
artist = st.text_input("Digite o nome do artista: ").title().strip()

if album_name and artist:
    album_sp = cached_search_album_from_spotify(album_name, artist)

    if album_sp:
        st.image(album_sp["imagem"], width=250)
        st.markdown(
            f"[Ouvir no Spotify]({album_sp['spotify_url']})", unsafe_allow_html=True
        )

        st.markdown(f"**Artista**: {album_sp['artista']}")
        st.markdown(f"**Data de Lançamento**: {album_sp['lancamento']}")
        st.markdown(f"**Total de Faixas**: {album_sp['total_faixas']}")
        st.markdown(f"**Popularidade**: {album_sp['popularidade']}")
    else:
        st.warning("Nenhum resultado encontado para esse álbum.")

st.subheader("Álbuns por Gênero")
df_genre = albums_by_genre()
st.bar_chart(df_genre.set_index("genero")["quantidade"])

st.subheader("Álbuns por Artista")
df_artist = albums_by_artist()
st.bar_chart(df_artist.set_index("artista")["quantidade"])

st.subheader("Álbuns por Década")
df_decade = albums_by_decade()
st.bar_chart(df_decade.set_index("decada")["quantidade"])

st.subheader("🔎 Filtrar por Intervalo de Anos")

start = st.number_input("Ano inicial", min_value=1900, max_value=2025, value=1990)
end = st.number_input("Ano final", min_value=1900, max_value=2025, value=1999)

if start <= end:
    df_range = albums_by_decade_range(start, end)
    st.write(f"🎯 Álbuns lançados entre {start} e {end}: {len(df_range)} encontrados.")
    st.dataframe(df_range)
else:
    st.warning("O ano final deve ser maior ou igual ao ano inicial.")
