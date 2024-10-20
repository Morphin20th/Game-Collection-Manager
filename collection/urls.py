from django.urls import path

from collection.views import (
    index,
    GamerCollectionListView,
    CollectionListView,
    CollectionDetailView,
    CollectionCreateView,
    CollectionUpdateView,
    CollectionDeleteView,
    GamerListView,
    GamerDetailView,
    GameListView,
    GameDetailView,
    GenreListView,
    GameByGenreListView,
    GenreCreateView,
    GenreUpdateView,
    GenreDeleteView,
)

urlpatterns = [
    path("", index, name="index"),
    path("my-collections/", GamerCollectionListView.as_view(), name="my-collection-list"),
    path("collections/", CollectionListView.as_view(), name="collection-list"),
    path("collections/<int:pk>/", CollectionDetailView.as_view(), name="collection-detail"),
    path("collections/create/", CollectionCreateView.as_view(), name="collection-create"),
    path("collections/<int:pk>/update/", CollectionUpdateView.as_view(), name="collection-update"),
    path("collections/<int:pk>/delete/", CollectionDeleteView.as_view(), name="collection-delete"),
    path("gamers/", GamerListView.as_view(), name="gamer-list"),
    path("gamers/<int:pk>", GamerDetailView.as_view(), name="gamer-detail"),
    path("games/", GameListView.as_view(), name="game-list"),
    path("games/<int:pk>", GameDetailView.as_view(), name="game-detail"),
    path("genres/", GenreListView.as_view(), name="genre-list"),
    path("genres/<int:pk>/games/", GameByGenreListView.as_view(), name="genre-games"),
    path("genres/create/", GenreCreateView.as_view(), name="genre-create"),
    path("genres/<int:pk>/update/", GenreUpdateView.as_view(), name="genre-update"),
    path("genres/<int:pk>/delete/", GenreDeleteView.as_view(), name="genre-delete")
]

app_name = "collection"
