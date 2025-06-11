import pandas as pd
import streamlit as st

from src.sql_analysis import albums_by_artist, albums_by_decade, albums_by_genre

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
