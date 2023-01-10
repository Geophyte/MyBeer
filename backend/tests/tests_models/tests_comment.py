from django.contrib.auth.models import User
from django.test import TestCase
from beers.models import Category, Beer, Review, Comment


class CommentTestCase(TestCase):
    def setUp(self) -> None:
        self.c_lager = Category.objects.create(name='Lager')
        self.user1 = User.objects.create_user('user', 'email@example.com', 'password')
        self.user2 = User.objects.create_user('user2', 'email2@example.com', 'password')
        self.beer1 = Beer.objects.create(name='Perła',
                                         description='foobar',
                                         category=self.c_lager,
                                         created_by=self.user1)
        self.beer2 = Beer.objects.create(name='Warka',
                                         description='foobar',
                                         category=self.c_lager,
                                         created_by=self.user1)
        self.review1 = Review.objects.create(title='Good beer',
                                             content='foo bar',
                                             author=self.user2,
                                             beer=self.beer1,
                                             rating=10)
        self.review2 = Review.objects.create(title='Good beer',
                                             content='foo bar',
                                             author=self.user2,
                                             beer=self.beer2,
                                             rating=10)

    def test_create_comment(self):
        comment = Comment.objects.create(author=self.user1,
                                         review=self.review1,
                                         content='agree')

        self.assertEqual(comment.author, self.user1)
        self.assertEqual(comment.review, self.review1)
        self.assertEqual(comment.content, 'agree')
        self.assertTrue(comment.active)

    def test_delete_review_with_comments(self):
        for i in range(3):
            comment = Comment.objects.create(author=self.user1,
                                             review=self.review1,
                                             content='agree')
            comment.save()

        self.assertEqual(len(Comment.objects.all()), 3)
        review = Review.objects.get(id=self.review1.id)
        review.delete()

        self.assertEqual(len(Comment.objects.all()), 0)

    def test_delete_beer_with_review_and_comments(self):
        for i in range(3):
            comment = Comment.objects.create(author=self.user1,
                                             review=self.review1,
                                             content='agree')
            comment.save()
        comment = Comment.objects.create(author=self.user1,
                                         review=self.review2,
                                         content='agree')
        comment.save()

        self.assertEqual(len(Comment.objects.all()), 4)

        beer = Beer.objects.get(id=self.beer1.id)
        beer.delete()
        self.assertEqual(len(Comment.objects.all()), 1)

        beer = Beer.objects.get(id=self.beer2.id)
        beer.delete()
        self.assertEqual(len(Comment.objects.all()), 0)