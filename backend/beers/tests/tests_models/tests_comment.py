from django.contrib.auth.models import User
from django.test import TestCase
from beers.models import Category, Beer, Review, Comment


class CommentTestCase(TestCase):
    def setUp(self) -> None:
        self.c_lager = Category.objects.create(name='Lager')
        self.user1 = User.objects.create_user('user', 'email@example.com', 'password')
        self.user2 = User.objects.create_user('user2', 'email2@example.com', 'password')
        self.beer = Beer.objects.create(name='Perła',
                                        description='foobar',
                                        category=self.c_lager,
                                        created_by=self.user1)
        self.review = Review.objects.create(title='Good beer',
                                            content='foo bar',
                                            author=self.user2,
                                            beer=self.beer,
                                            rating=10)

    def test_create_comment(self):
        comment = Comment.objects.create(author=self.user1,
                                         review=self.review,
                                         content='agree')

        self.assertEqual(comment.author, self.user1)
        self.assertEqual(comment.review, self.review)
        self.assertEqual(comment.content, 'agree')
