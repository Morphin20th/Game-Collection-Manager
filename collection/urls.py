from django.urls import path

from collection.views import (
    index,
    GamerCollectionListView,
    CollectionListView,
    GamerListView,
    GameListView,
    GenreListView, CollectionDetailView,
)

urlpatterns = [
    path("", index, name="index"),
    path("my-collections/", GamerCollectionListView.as_view(), name="my-collection-list"),
    path("collections/", CollectionListView.as_view(), name="collection-list"),
    path("collections/<int:pk>", CollectionDetailView.as_view(), name="collection-detail"),
    path("gamers/", GamerListView.as_view(), name="gamer-list"),
    path("games/", GameListView.as_view(), name="game-list"),
    path("genres/", GenreListView.as_view(), name="genre-list"),
]

app_name = "collection"
