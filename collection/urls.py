from django.urls import path

from collection.views import index, GamerCollectionListView, CollectionListView

urlpatterns = [
    path("", index, name="index"),
    path("my-collections/", GamerCollectionListView.as_view(), name="my-collections"),
    path("collections/", CollectionListView.as_view(), name="collections"),
]

app_name = "collection"