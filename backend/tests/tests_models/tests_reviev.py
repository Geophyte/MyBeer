from statistics import mean

from django.contrib.auth.models import User
from django.test import TestCase
from beers.models import Category, Beer, Review


class ReviewTestCase(TestCase):
    def setUp(self) -> None:
        self.c_lager = Category.objects.create(name='Lager')
        self.user = User.objects.create_user('admin', 'email@example.com', 'password')
        self.beer_1 = Beer.objects.create(name='Perła',
                                          description='foobar',
                                          category=self.c_lager,
                                          created_by=self.user)

        self.beer_2 = Beer.objects.create(name='Warka',
                                          description='barfoo',
                                          category=self.c_lager,
                                          created_by=self.user)

        assert self.beer_2.active is False
        assert self.beer_2.rating == 0

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

    def test_calculate_not_active_beer_mean_rating_after_create(self):
        ratings = [1, 3, 10]

        for rating in ratings:
            review = Review.objects.create(title='Good beer',
                                           content='foo bar',
                                           author=self.user,
                                           beer=self.beer_1,
                                           rating=rating)
            review.save()
        beer_1 = Beer.objects.get(name='Perła')
        beer_2 = Beer.objects.get(name='Warka')
        self.assertAlmostEqual(beer_1.rating.__float__(), 0)
        self.assertAlmostEqual(beer_2.rating.__float__(), 0)

    def test_calculate_active_beer_mean_rating_after_create(self):
        self.beer_1.active = True
        self.beer_2.active = True
        self.beer_1.save()
        self.beer_2.save()
        ratings = [1, 3, 10]

        for rating in ratings:
            review = Review.objects.create(title='Good beer',
                                           content='foo bar',
                                           author=self.user,
                                           beer=self.beer_1,
                                           rating=rating)
            review.save()
        beer_1 = Beer.objects.get(name='Perła')
        beer_2 = Beer.objects.get(name='Warka')
        expected_rating = round(mean(ratings), 2)
        self.assertAlmostEqual(beer_1.rating.__float__(), expected_rating)
        self.assertAlmostEqual(beer_2.rating.__float__(), 0)

    def test_calculate_not_active_beer_mean_rating_after_delete(self):
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
        self.assertAlmostEqual(beer.rating.__float__(), 0)
        self.assertAlmostEqual(beer_2.rating.__float__(), 0)

        Review.objects.get(rating=1).delete()
        beer = Beer.objects.get(name='Perła')
        beer_2 = Beer.objects.get(name='Warka')
        self.assertAlmostEqual(beer.rating.__float__(), 0)
        self.assertAlmostEqual(beer_2.rating.__float__(), 0)

        Review.objects.get(rating=3).delete()
        beer = Beer.objects.get(name='Perła')
        beer_2 = Beer.objects.get(name='Warka')
        self.assertAlmostEqual(beer.rating.__float__(), 0)
        self.assertAlmostEqual(beer_2.rating.__float__(), 0)

    def test_calculate_active_beer_mean_rating_after_delete(self):
        self.beer_1.active = True
        self.beer_2.active = True
        self.beer_1.save()
        self.beer_2.save()

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
        self.assertAlmostEqual(beer.rating.__float__(), 2)
        self.assertAlmostEqual(beer_2.rating.__float__(), 0)

        Review.objects.get(rating=1).delete()
        beer = Beer.objects.get(name='Perła')
        beer_2 = Beer.objects.get(name='Warka')
        self.assertAlmostEqual(beer.rating.__float__(), 3)
        self.assertAlmostEqual(beer_2.rating.__float__(), 0)

        Review.objects.get(rating=3).delete()
        beer = Beer.objects.get(name='Perła')
        beer_2 = Beer.objects.get(name='Warka')
        self.assertAlmostEqual(beer.rating.__float__(), 0)
        self.assertAlmostEqual(beer_2.rating.__float__(), 0)

    def test_calculate_beer_mean_rating_after_set_review_not_active(self):
        self.beer_1.active = True
        self.beer_2.active = True
        self.beer_1.save()
        self.beer_2.save()

        ratings = [1, 3, 10]
        for rating in ratings:
            review = Review.objects.create(title='Good beer',
                                           content='foo bar',
                                           author=self.user,
                                           beer=self.beer_1,
                                           rating=rating)
            review.save()

        r = Review.objects.get(rating=10)
        r.active = False
        r.save()

        beer = Beer.objects.get(name='Perła')
        beer_2 = Beer.objects.get(name='Warka')
        self.assertAlmostEqual(beer.rating.__float__(), 2)
        self.assertAlmostEqual(beer_2.rating.__float__(), 0)

        r = Review.objects.get(rating=1)
        r.active = False
        r.save()

        beer = Beer.objects.get(name='Perła')
        beer_2 = Beer.objects.get(name='Warka')
        self.assertAlmostEqual(beer.rating.__float__(), 3)
        self.assertAlmostEqual(beer_2.rating.__float__(), 0)

        r = Review.objects.get(rating=3)
        r.active = False
        r.save()
        beer = Beer.objects.get(name='Perła')
        beer_2 = Beer.objects.get(name='Warka')
        self.assertAlmostEqual(beer.rating.__float__(), 0)
        self.assertAlmostEqual(beer_2.rating.__float__(), 0)

    def test_delete_beers_with_reviews(self):
        ratings = [1, 3, 10]
        for rating in ratings:
            review_1 = Review.objects.create(title='Good beer',
                                           content='foo bar',
                                           author=self.user,
                                           beer=self.beer_1,
                                           rating=rating)

            review_2 = Review.objects.create(title='Good beer',
                                           content='foo bar',
                                           author=self.user,
                                           beer=self.beer_2,
                                           rating=rating)
            review_1.save()
            review_2.save()

        self.assertEqual(len(Review.objects.all()), 6)

        beer = Beer.objects.get(name='Perła')
        beer.delete()

        self.assertEqual(len(Review.objects.all()), 3)

        beer = Beer.objects.get(name='Warka')
        beer.delete()

        self.assertEqual(len(Review.objects.all()), 0)
