from statistics import mean

from django.contrib.auth.models import User
from django.test import TestCase
from beers.models import Category, Beer, Review


class ReviewTestCase(TestCase):
    def setUp(self) -> None:
        self.c_lager = Category.objects.create(name='Lager')
        self.user = User.objects.create_user('Admin', 'email@example.com', 'password')
        self.beer_1 = Beer.objects.create(name='Perła',
                                          description='foobar',
                                          category=self.c_lager,
                                          created_by=self.user)

        self.beer_2 = Beer.objects.create(name='Warka',
                                          description='barfoo',
                                          category=self.c_lager,
                                          created_by=self.user)

        self.beer_1.save()
        self.beer_2.save()

    def test_create_review(self):
        review = Review.objects.create(title='Good beer',
                                       content='foo bar',
                                       author=self.user,
                                       beer=self.beer_1,
                                       rating=10)
        review.save()

        self.assertEqual(review.title, 'Good beer')
        self.assertEqual(review.content, 'foo bar')
        self.assertEqual(review.author, self.user)
        self.assertEqual(review.beer, self.beer_1)
        self.assertEqual(review.rating, 10)

    def test_calculate_beer_mean_rating_after_create(self):
        ratings = [1, 3, 10]

        for rating in ratings:
            review = Review.objects.create(title='Good beer',
                                           content='foo bar',
                                           author=self.user,
                                           beer=self.beer_1,
                                           rating=rating)
            review.save()

        beer = Beer.objects.get(name='Perła')
        beer_2 = Beer.objects.get(name='Warka')
        expected_rating = round(mean(ratings), 2)
        self.assertAlmostEqual(beer.rating.__float__(), expected_rating)
        self.assertIsNone(beer_2.rating)

    def test_calculate_beer_mean_rating_after_delete(self):
        ratings = [1, 3, 10]

        for rating in ratings:
            review = Review.objects.create(title='Good beer',
                                           content='foo bar',
                                           author=self.user,
                                           beer=self.beer_1,
                                           rating=rating)
            review.save()

        Review.objects.get(rating=10).delete()
        beer = Beer.objects.get(name='Perła')
        beer_2 = Beer.objects.get(name='Warka')
        expected_rating = 2
        self.assertAlmostEqual(beer.rating.__float__(), expected_rating)
        self.assertIsNone(beer_2.rating)

        Review.objects.get(rating=1).delete()
        beer = Beer.objects.get(name='Perła')
        beer_2 = Beer.objects.get(name='Warka')
        expected_rating = 3
        self.assertAlmostEqual(beer.rating.__float__(), expected_rating)
        self.assertIsNone(beer_2.rating)

        Review.objects.get(rating=3).delete()
        beer = Beer.objects.get(name='Perła')
        beer_2 = Beer.objects.get(name='Warka')
        self.assertIsNone(beer.rating)
        self.assertIsNone(beer_2.rating)
