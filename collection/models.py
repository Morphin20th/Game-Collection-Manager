from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=255, unique=True)
    platform = models.CharField(max_length=100, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name="games",
    )

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return f"{self.title} ({self.genre}) Price: {self.price}"


class Gamer(AbstractUser):
    bio = models.TextField(blank=True)

    class Meta:
        verbose_name = "Gamer"
        verbose_name_plural = "Gamers"

    def __str__(self) -> str:
        return f"{self.username} - {self.first_name} {self.last_name}"


class Collection(models.Model):
    name = models.CharField(max_length=100)
    gamer = models.ForeignKey(
        Gamer,
        on_delete=models.CASCADE,
        related_name="collections",
    )
    game = models.ManyToManyField(Game, related_name="collections")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name", ]

    def __str__(self) -> str:
        return f"{self.name} Creator: {self.gamer.username}"

    def get_absolute_url(self):
        return reverse("collection:collection-detail", args=[str(self.id)])
