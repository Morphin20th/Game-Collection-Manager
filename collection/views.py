from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from collection.models import Gamer, Collection, Game, Genre


@login_required
def index(request: HttpRequest) -> HttpResponse:
    context = {
        "num_gamers": Gamer.objects.count(),
        "num_collections": Collection.objects.count(),
    }
    return render(request, "collection/index.html", context=context)


class GamerCollectionListView(LoginRequiredMixin, generic.ListView):
    model = Collection
    template_name = "collection/collections/collection_list.html"
    context_object_name = "collections"
    paginate_by = 5

    def get_queryset(self):
        return Collection.objects.filter(gamer=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "My collections"
        return context


class CollectionListView(LoginRequiredMixin, generic.ListView):
    model = Collection
    template_name = "collection/collections/collection_list.html"
    context_object_name = "collections"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "All collections"
        return context


class GamerListView(LoginRequiredMixin, generic.ListView):
    model = Gamer
    template_name = "collection/gamer/gamer_list.html"
    paginate_by = 5


class GameListView(LoginRequiredMixin, generic.ListView):
    model = Game
    template_name = "collection/game/game_list.html"
    paginate_by = 5


class GenreListView(LoginRequiredMixin, generic.ListView):
    model = Genre
    template_name = "collection/genre/genre_list.html"
    paginate_by = 5
