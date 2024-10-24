from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from collection.models import Genre, Game, Collection, Gamer

COLLECTION_URL = reverse("collection:collection-list")
MY_COLLECTION_URL = reverse("collection:my-collection-list")
GAMER_URL = reverse("collection:gamer-list")
GAME_URL = reverse("collection:game-list")
GENRE_URL = reverse("collection:genre-list")


class PublicTest(TestCase):
    def test_login_required_for_collection_list_page(self):
        response = self.client.get(COLLECTION_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_my_collection_list_page(self):
        response = self.client.get(MY_COLLECTION_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_gamer_list_page(self):
        response = self.client.get(GAMER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_game_list_page(self):
        response = self.client.get(GAME_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_genre_list_page(self):
        response = self.client.get(GENRE_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.genre1 = Genre.objects.create(name="Test Genre1")
        cls.genre2 = Genre.objects.create(name="Test Genre2")

        cls.game1 = Game.objects.create(
            title="Test Game1",
            price=10.99,
            genre=cls.genre1
        )
        cls.game2 = Game.objects.create(
            title="Test Game2",
            price=11.99,
            genre=cls.genre2
        )

        cls.gamer1 = get_user_model().objects.create_user(
            username="test_gamer1",
            password="Password1!",
        )
        cls.gamer2 = get_user_model().objects.create_user(
            username="test_gamer2",
            password="Password2!",
        )

        cls.collection1 = Collection.objects.create(
            name="Test Collection1",
            gamer=cls.gamer2,
        )
        cls.collection1.game.set([cls.game1, cls.game2])

        cls.collection2 = Collection.objects.create(
            name="Test Collection2",
            gamer=cls.gamer1
        )
        cls.collection2.game.set([cls.game2])

    def setUp(self):
        self.client.force_login(self.gamer1)

    def test_retrieve_collections(self):
        response = self.client.get(COLLECTION_URL)
        collections = Collection.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "collection/collections/collection_list.html")
        self.assertEqual(
            list(response.context["collections"]),
            list(collections)
        )

    def test_retrieve_gamer_collections(self):
        response = self.client.get(MY_COLLECTION_URL)
        collections = Collection.objects.filter(gamer=self.gamer1)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "collection/collections/collection_list.html")
        self.assertEqual(
            list(response.context["collections"]),
            list(collections)
        )

    def test_retrieve_games(self):
        response = self.client.get(GAME_URL)
        games = Game.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "collection/game/game_list.html")
        self.assertEqual(
            list(response.context["game_list"]),
            list(games)
        )

    def test_retrieve_gamers(self):
        response = self.client.get(GAMER_URL)
        gamers = Gamer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "collection/gamer/gamer_list.html")
        self.assertEqual(
            list(response.context["gamer_list"]),
            list(gamers)
        )

    def test_retrieve_genres(self):
        response = self.client.get(GENRE_URL)
        genres = Genre.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "collection/genre/genre_list.html")
        self.assertEqual(
            list(response.context["genre_list"]),
            list(genres)
        )

    def test_copy_collection(self):
        response = self.client.post(reverse("collection:collection-copy", args=[self.collection2.pk]))

        self.assertEqual(response.status_code, 302)

        copied_collection = Collection.objects.get(name=f"Copy of {self.collection2.name}")
        self.assertEqual(copied_collection.gamer, self.gamer1)

        self.assertEqual(
            list(copied_collection.game.all()),
            list(self.collection2.game.all())
        )
