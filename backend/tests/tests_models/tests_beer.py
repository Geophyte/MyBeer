from django.test import TestCase
from django.contrib.auth.models import User
from beers.models import Category, Beer


class BeerTestCase(TestCase):
    def setUp(self) -> None:
        self.c_lager = Category.objects.create(name='Lager')
        self.c_porter = Category.objects.create(name='Porter')
        self.user = User.objects.create_user('admin', 'email@example.com', 'password')

    def test_create_beer(self):
        beer = Beer.objects.create(name='Perła',
                                   description='foobar',
                                   category=self.c_lager,
                                   created_by=self.user,
                                   image_url='test_image.png')

        beer.save()

        self.assertIsNotNone(beer.id)
        self.assertEqual(beer.name, 'Perła')
        self.assertEqual(beer.description, 'foobar')
        self.assertEqual(beer.category, self.c_lager)
        self.assertEqual(beer.created_by, self.user)
        self.assertIsNotNone(beer.image_url)
        self.assertNotEqual(beer.image_url.url, '/media/images/default.png')
        self.assertFalse(beer.active)

    def test_create_beer_no_img_url(self):
        beer = Beer.objects.create(name='Perła',
                                   description='foobar',
                                   created_by=self.user,
                                   category=self.c_lager)

        beer.save()

        self.assertIsNotNone(beer.id)
        self.assertEqual(beer.name, 'Perła')
        self.assertEqual(beer.description, 'foobar')
        self.assertEqual(beer.category, self.c_lager)
        self.assertEqual(beer.created_by, self.user)
        self.assertEqual(beer.image_url.url, '/media/images/default.png')
        self.assertFalse(beer.active)
