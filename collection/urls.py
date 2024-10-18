from django.contrib import admin
from django.shortcuts import render
from django.urls import path

from collection.views import index

urlpatterns = [
    path("", index, name="index")
]

app_name = "collection"