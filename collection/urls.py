from django.urls import path

from collection.views import index, GamerCollectionListView, CollectionListView, GamerListView, GameListView

urlpatterns = [
    path("", index, name="index"),
    path("my-collections/", GamerCollectionListView.as_view(), name="my-collections"),
    path("collections/", CollectionListView.as_view(), name="collections"),
    path("gamers/", GamerListView.as_view(), name="gamers"),
    path("games/", GameListView.as_view(), name="games"),
]

app_name = "collection"