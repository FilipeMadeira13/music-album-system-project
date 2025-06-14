import os

import spotipy
import streamlit as st
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET:
    raise EnvironmentError(
        "Variáveis de ambiente SPOTIFY_CLIENT_ID ou SPOTIFY_CLIENT_SECRET não definidas."
    )

auth_manager = SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET
)

sp = spotipy.Spotify(auth_manager=auth_manager)


def search_album_from_spotify(album_name: str, artist_name: str) -> dict:
    query = f"album:{album_name} artist:{artist_name}"
    result = sp.search(q=query, type="album", limit=1)

    if result["albums"]["items"]:
        album = result["albums"]["items"][0]

        full_album = sp.album(album["id"])

        return {
            "nome": full_album["name"],
            "artista": full_album["artists"][0]["name"],
            "total_faixas": full_album["total_tracks"],
            "popularidade": full_album["popularity"],
            "lancamento": full_album["release_date"],
            "spotify_url": full_album["external_urls"]["spotify"],
            "imagem": full_album["images"][0]["url"] if full_album["images"] else None,
        }

    return {}
