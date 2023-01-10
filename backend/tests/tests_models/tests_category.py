from django.db import IntegrityError, DataError
from django.test import TestCase
from beers.models import Category


class CategoryTestCase(TestCase):
    def test_create_category(self):
        category = Category.objects.create(name='Lager')
        category.save()
        self.assertIsNotNone(category.id)
        self.assertEqual(category.name, 'Lager')

    def test_create_category_with_exist_name(self):
        Category.objects.create(name='Lager').save()
        with self.assertRaises(IntegrityError):
            Category.objects.create(name='Lager').save()

    def test_create_category_with_no_name(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(name=None)

    def test_create_category_with_too_long_name(self):
        name = 'f' * 51
        with self.assertRaises(DataError):
            Category.objects.create(name=name)
