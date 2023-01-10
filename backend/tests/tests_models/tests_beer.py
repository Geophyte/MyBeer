from io import StringIO
from PIL import Image
from django.core.files.base import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.contrib.auth.models import User
from beers.models import Category, Beer, Review


class BeerTestCase(TestCase):
    @staticmethod
    def get_image_file(name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
        file_obj = StringIO()
        image = Image.new("RGB", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def setUp(self) -> None:
        self.c_lager = Category.objects.create(name='Lager')
        self.c_porter = Category.objects.create(name='Porter')
        self.user = User.objects.create_user('admin', 'email@example.com', 'password')

    def test_create_beer(self):
        beer = Beer.objects.create(name='Perła',
                                   description='foobar',
                                   category=self.c_lager,
                                   image_url='test_image.png')

        beer.save()

        self.assertIsNotNone(beer.id)
        self.assertEqual(beer.name, 'Perła')
        self.assertEqual(beer.description, 'foobar')
        self.assertEqual(beer.category, self.c_lager)
        self.assertEqual(beer.created_by.id, 1)
        self.assertIsNotNone(beer.image_url)
        self.assertNotEqual(beer.image_url.url, '/media/images/default.png')
        self.assertFalse(beer.active)

    def test_create_beer_no_img_url(self):
        beer = Beer.objects.create(name='Perła',
                                   description='foobar',
                                   category=self.c_lager)

        beer.save()

        self.assertIsNotNone(beer.id)
        self.assertEqual(beer.name, 'Perła')
        self.assertEqual(beer.description, 'foobar')
        self.assertEqual(beer.category, self.c_lager)
        self.assertEqual(beer.created_by.id, 1)
        self.assertEqual(beer.image_url.url, '/media/images/default.png')
        self.assertFalse(beer.active)
