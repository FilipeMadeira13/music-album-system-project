import pandas as pd
import streamlit as st

from src.sql_analysis import (
    albums_by_artist,
    albums_by_decade,
    albums_by_decade_range,
    albums_by_genre,
)

st.title("🎵 Análise de Álbuns Musicais")

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
