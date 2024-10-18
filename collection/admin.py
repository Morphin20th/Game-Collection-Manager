from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from collection.models import Genre, Game, Gamer, Collection

admin.site.register(Genre)
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "genre",
        "price",
        "release_date",
    ]
    list_filter = ["genre",]
    search_fields = ["title",]


@admin.register(Gamer)
class GamerAdmin(admin.ModelAdmin):
    list_display = UserAdmin.list_display

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["name", "gamer", "created_at",]
    list_filter = ["gamer",]
    search_fields = ["name",]