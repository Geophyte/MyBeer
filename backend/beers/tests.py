from django.test import TestCase
from beers.models import Category, Beer, Review, Comment


class CategoryModelTest(TestCase):
    def setUp(self) -> None:
        self.category1 = Category.objects.create(
            name="Pilzner"
        )

    def test_create(self):
        self.assertEqual(self.category1.name, "Pilzner")
        self.assertEqual(self.category1.id, 1)


class BeerModelTestCase(TestCase):
    pass


class ReviewModelTestCase(TestCase):
    pass


class CommentModelTestCase(TestCase):
    pass
