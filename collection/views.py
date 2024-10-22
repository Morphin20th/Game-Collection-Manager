from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from collection.models import Gamer, Collection, Game, Genre
from collection.forms import (
    CollectionForm,
    GamerCreationForm,
    GamerBioUpdateForm,
    CollectionSearchForm,
    GamerSearchForm,
    GameSearchForm,
    GenreSearchForm,
)


# ListView classes
# can be deleted
class GamerCollectionListView(LoginRequiredMixin, generic.ListView):
    model = Collection
    template_name = "collection/collections/collection_list.html"
    context_object_name = "collections"
    paginate_by = 5

    def get_queryset(self):
        queryset = Collection.objects.select_related("gamer").filter(gamer=self.request.user)
        form = CollectionSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data["name"]
            if name:
                queryset = queryset.filter(name__icontains=name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["search_form"] = CollectionSearchForm(
            initial={"name": name}
        )
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
        name = self.request.GET.get("name", "")
        context["search_form"] = CollectionSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Collection.objects.select_related("gamer").all()
        form = CollectionSearchForm(self.request.GET)

        if form.is_valid():
            name = form.cleaned_data.get("name")
            if name:
                queryset = queryset.filter(name__icontains=name)
        return queryset


class GamerListView(LoginRequiredMixin, generic.ListView):
    model = Gamer
    template_name = "collection/gamer/gamer_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = Gamer.objects.all()
        form = GamerSearchForm(self.request.GET)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            if username:
                queryset = queryset.filter(username__icontains=username)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username")
        context["search_form"] = GamerSearchForm(initial={"username": username})
        return context


class GameListView(LoginRequiredMixin, generic.ListView):
    model = Game
    template_name = "collection/game/game_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get("title")
        context["search_form"] = GameSearchForm(initial={"title": title})
        context["page_title"] = "All games"
        return context

    def get_queryset(self):
        queryset = Game.objects.select_related("genre")
        form = GameSearchForm(self.request.GET)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            if title:
                queryset = queryset.filter(title__icontains=title)
        return queryset


class GameByGenreListView(LoginRequiredMixin, generic.ListView):
    model = Game
    template_name = "collection/game/game_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get("title")
        context["search_form"] = GameSearchForm(initial={"title": title})
        context["page_title"] = f"Games with genre {self.genre.name}"
        context["genre"] = self.genre
        return context

    def get_queryset(self):
        genre_pk = self.kwargs.get("pk")
        self.genre = get_object_or_404(Genre, pk=genre_pk)
        queryset = Game.objects.select_related("genre").filter(genre=self.genre)
        form = GameSearchForm(self.request.GET)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            if title:
                queryset = queryset.filter(title__icontains=title)
        return queryset


class GenreListView(LoginRequiredMixin, generic.ListView):
    model = Genre
    template_name = "collection/genre/genre_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = Genre.objects.all()
        form = GenreSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            if name:
                queryset = Genre.objects.filter(name__icontains=name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", )
        context["search_form"] = GenreSearchForm(
            initial={"name": name}
        )
        return context


# DetailView classes
class CollectionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Collection
    template_name = "collection/collections/collection_detail.html"
    queryset = Collection.objects.select_related("gamer").prefetch_related("game", "game__genre")


class GamerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Gamer
    template_name = "collection/gamer/gamer_detail.html"
    queryset = Gamer.objects.prefetch_related("collections")


class GameDetailView(LoginRequiredMixin, generic.DetailView):
    model = Game
    template_name = "collection/game/game_detail.html"
    queryset = Game.objects.select_related("genre")


# CreateView classes
class CollectionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Collection
    template_name = "collection/collections/collection_form.html"
    form_class = CollectionForm

    def form_valid(self, form):
        form.instance.gamer = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("collection:collection-detail", kwargs={"pk": self.object.pk})


class GamerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Gamer
    form_class = GamerCreationForm
    template_name = "collection/gamer/gamer_form.html"

    def get_success_url(self):
        return reverse_lazy("collection:gamer-detail", kwargs={"pk": self.object.pk})


class GameCreateView(LoginRequiredMixin, generic.CreateView):
    model = Game
    fields = "__all__"
    template_name = "collection/game/game_form.html"

    def get_success_url(self):
        return reverse_lazy("collection:game-detail", kwargs={"pk": self.object.pk})


class GenreCreateView(LoginRequiredMixin, generic.CreateView):
    model = Genre
    fields = "__all__"
    success_url = reverse_lazy("collection:genre-list")
    template_name = "collection/genre/genre_form.html"


# UpdateView classes
class CollectionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Collection
    form_class = CollectionForm
    template_name = "collection/collections/collection_form.html"

    def get_success_url(self):
        return reverse_lazy("collection:collection-detail", kwargs={"pk": self.object.pk})


class CollectionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Collection
    success_url = reverse_lazy("collection:my-collection-list")
    template_name = "collection/collections/collection_confirm_delete.html"


class GamerBioUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Gamer
    success_url = reverse_lazy("collection:gamer-list")
    form_class = GamerBioUpdateForm
    template_name = "collection/gamer/gamer_form.html"


class GameUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Game
    fields = "__all__"
    template_name = "collection/game/game_form.html"

    def get_success_url(self):
        return reverse_lazy("collection:game-detail", kwargs={"pk": self.object.pk})


class GenreUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Genre
    fields = "__all__"
    success_url = reverse_lazy("collection:genre-list")
    template_name = "collection/genre/genre_form.html"


# DeleteView classes
class GamerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Gamer
    success_url = reverse_lazy("collection:gamer-list")
    template_name = "collection/gamer/gamer_confirm_delete.html"


class GameDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Game
    success_url = reverse_lazy("collection:game-list")
    template_name = "collection/game/game_confirm_delete.html"


class GenreDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Genre
    success_url = reverse_lazy("collection:genre-list")
    template_name = "collection/genre/genre_confirm_delete.html"


@login_required
def index(request: HttpRequest) -> HttpResponse:
    context = {
        "num_gamers": Gamer.objects.count(),
        "num_collections": Collection.objects.count(),
    }
    return render(request, "collection/index.html", context=context)


@login_required
def copy_collection(request, pk):
    original_collection = get_object_or_404(Collection, pk=pk)
    new_collection = Collection.objects.create(
        name=f"Copy of {original_collection.name}",
        gamer=request.user
    )
    new_collection.game.set(original_collection.game.all())
    new_collection.save()
    return HttpResponseRedirect(reverse_lazy("collection:collection-detail", args=[new_collection.pk]))
