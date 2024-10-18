from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from collection.models import Gamer, Collection


def index(request:HttpRequest) -> HttpResponse:
    context = {
        "num_gamers": Gamer.objects.count(),
        "num_collections": Collection.objects.count(),
    }
    return render(request, "collection/index.html", context=context)