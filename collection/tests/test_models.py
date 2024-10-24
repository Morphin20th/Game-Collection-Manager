from django.test import TestCase

from collection.models import Collection, Gamer, Game, Genre


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "test_username"
        cls.password = "Password1!"
        cls.first_name = "test_first_name"
        cls.last_name = "test_last_name"
        cls.collection_name = "test_collection_name"
        cls.genre_name = "test_genre_name"
        cls.title = "test_game_title"
        cls.price = 10.99
        cls.genre = Genre.objects.create(name=cls.genre_name)
        cls.gamer = Gamer.objects.create(
            username=cls.username,
            password=cls.password,
            first_name=cls.first_name,
            last_name=cls.last_name,
        )

    def test_gamer_str(self):
        self.assertEqual(str(self.gamer), f"{self.username} - {self.first_name} {self.last_name}")

    def test_game_str(self):
        game = Game.objects.create(title=self.title, price=self.price, genre=self.genre)
        self.assertEqual(str(game), f"{self.title} ({self.genre}) Price: {self.price}")

    def test_collection_str(self):
        collection = Collection.objects.create(
            name=self.collection_name,
            gamer=self.gamer,
        )
        self.assertEqual(str(collection), f"{self.collection_name} Creator: {self.gamer.username}")

    def test_genre_str(self):
        self.assertEqual(str(self.genre), self.genre_name)
