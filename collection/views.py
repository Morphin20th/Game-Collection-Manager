from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from collection.forms import CollectionForm
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
        context["title"] = "All collections"
        return context


class CollectionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Collection
    template_name = "collection/collections/collection_detail.html"


class CollectionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Collection
    success_url = reverse_lazy("collection:collection-list")
    template_name = "collection/collections/collection_form.html"
    form_class = CollectionForm

    def form_valid(self, form):
        form.instance.gamer = self.request.user
        return super().form_valid(form)


class CollectionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Collection
    form_class = CollectionForm
    success_url = reverse_lazy("collection:collection-list")
    template_name = "collection/collections/collection_form.html"


class GamerListView(LoginRequiredMixin, generic.ListView):
    model = Gamer
    template_name = "collection/gamer/gamer_list.html"
    paginate_by = 5


class GamerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Gamer
    template_name = "collection/gamer/gamer_detail.html"


class GameListView(LoginRequiredMixin, generic.ListView):
    model = Game
    template_name = "collection/game/game_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "All games"
        return context


class GameDetailView(LoginRequiredMixin, generic.DetailView):
    model = Game
    template_name = "collection/game/game_detail.html"


class GenreListView(LoginRequiredMixin, generic.ListView):
    model = Genre
    template_name = "collection/genre/genre_list.html"
    paginate_by = 5


class GameByGenreListView(LoginRequiredMixin, generic.ListView):
    model = Game
    template_name = "collection/game/game_list.html"
    paginate_by = 5

    def get_queryset(self):
        genre_pk = self.kwargs.get("pk")
        genre = get_object_or_404(Genre, pk=genre_pk)
        games = Game.objects.filter(genre=genre)
        return games

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre = get_object_or_404(Genre, id=self.kwargs.get("pk"))
        context["title"] = f"Games with genre {genre.name}"
        context["game_list"] = context["object_list"]
        context["genre"] = genre
        return context


class GenreCreateView(LoginRequiredMixin, generic.CreateView):
    model = Genre
    fields = "__all__"
    success_url = reverse_lazy("collection:genre-list")
    template_name = "collection/genre/genre_form.html"


class GenreUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Genre
    fields = "__all__"
    success_url = reverse_lazy("collection:genre-list")
    template_name = "collection/genre/genre_form.html"
