from src import sql_crud


def test_add_and_list_album():
    album = {
        "nome": "Test Album",
        "artista": "Test Artist",
        "genero": "Test Genre",
        "ano": 2023,
    }
    sql_crud.add_album(album)
    result = sql_crud.list_albums()

    assert any(a["nome"] == "Test Album" for a in result)
    assert any(a["artista"] == "Test Artist" for a in result)
    assert isinstance(result, list)
    assert len(result) == 1


def test_remove_album_by_name():
    sql_crud.add_album(
        {
            "nome": "Album to Remove",
            "artista": "Artist",
            "genero": "Genre",
            "ano": 2023,
        }
    )
    removed = sql_crud.remove_album_by_name("Album to Remove", "Artist")
    albums = sql_crud.list_albums()

    assert removed is True
    assert all(a["nome"] != "Album to Remove" for a in albums)


def test_get_random_album():
    sql_crud.add_album(
        {
            "nome": "Random Album",
            "artista": "Random Artist",
            "genero": "Random Genre",
            "ano": 2023,
        }
    )
    album = sql_crud.get_random_album()

    assert album is not None
    assert album["nome"] == "Random Album"


def test_update_album_favorite():
    sql_crud.add_album(
        {
            "nome": "Album to Update",
            "artista": "Artist",
            "genero": "Genre",
            "ano": 2023,
        }
    )
    updated = sql_crud.update_album_favorite("Album to Update", "Artist", True)
    favs = sql_crud.list_favorites()

    assert updated is True
    assert len(favs) == 1
    assert favs[0]["favorito"] == 1
