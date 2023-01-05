from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APITestCase

from beers.models import Beer, Category, Review, Comment


def set_up_database(test_class):
    # INIT TEST DATABASE
    test_class.user_1 = User.objects.create_user('user_1', 'user_1@example.com', 'password')
    test_class.user_2 = User.objects.create_user('user_2', 'user_2@example.com', 'password')

    test_class.category_1 = Category.objects.create(name='Lager')
    test_class.category_1.save()
    test_class.category_2 = Category.objects.create(name='Porter')
    test_class.category_2.save()

    test_class.beer_1 = Beer.objects.create(name='Perła',
                                            description='foobar',
                                            category=test_class.category_1,
                                            created_by=test_class.user_1)
    test_class.beer_2 = Beer.objects.create(name='Warka',
                                            description='barfoo',
                                            category=test_class.category_1,
                                            created_by=test_class.user_2)
    test_class.beer_3 = Beer.objects.create(name='Żywiec porter',
                                            description='foobar',
                                            category=test_class.category_2,
                                            created_by=test_class.user_1)
    test_class.beer_4 = Beer.objects.create(name='inny porter',
                                            description='barfoo',
                                            category=test_class.category_2,
                                            created_by=test_class.user_2)
    test_class.beer_1.save()
    test_class.beer_2.save()
    test_class.beer_3.save()
    test_class.beer_4.save()

    test_class.review_1 = Review.objects.create(title='good',
                                                content='foo bar',
                                                author=test_class.user_1,
                                                beer=test_class.beer_1,
                                                rating=7)

    test_class.review_2 = Review.objects.create(title='not good',
                                                content='foo bar',
                                                author=test_class.user_2,
                                                beer=test_class.beer_1,
                                                rating=2)

    test_class.review_3 = Review.objects.create(title='very good',
                                                content='foo bar',
                                                author=test_class.user_1,
                                                beer=test_class.beer_3,
                                                rating=10)

    test_class.review_4 = Review.objects.create(title='normal',
                                                content='foo bar',
                                                author=test_class.user_2,
                                                beer=test_class.beer_4,
                                                rating=5)
    test_class.review_1.save()
    test_class.review_2.save()
    test_class.review_3.save()
    test_class.review_4.save()

    test_class.comment_1 = Comment.objects.create(author=test_class.user_1,
                                                  review=test_class.review_2,
                                                  content='agree')
    test_class.comment_2 = Comment.objects.create(author=test_class.user_2,
                                                  review=test_class.review_2,
                                                  content='thanks')
    test_class.comment_3 = Comment.objects.create(author=test_class.user_1,
                                                  review=test_class.review_3,
                                                  content='ok')
    test_class.comment_4 = Comment.objects.create(author=test_class.user_1,
                                                  review=test_class.review_4,
                                                  content='kk')

    test_class.comment_1.save()
    test_class.comment_2.save()
    test_class.comment_3.save()
    test_class.comment_4.save()


class NotAuthenticatedUserTestCase(APITestCase):
    def setUp(self) -> None:
        # INIT TEST DATABASE
        set_up_database(self)

    def test_api_root(self):
        response = self.client.get('/api/v1/')
        self.assertEqual(response.status_code, 200)

    def test_beer_list(self):
        response = self.client.get('/api/v1/beers/')
        self.assertEqual(response.status_code, 401)

    def test_beer_detail(self):
        response = self.client.get('/api/v1/beers/1/')
        self.assertEqual(response.status_code, 401)

    def test_beer_filter(self):
        response = self.client.get('/api/v1/beers/?category=Lager')
        self.assertEqual(response.status_code, 401)

    def test_category_list(self):
        response = self.client.get('/api/v1/categories/')
        self.assertEqual(response.status_code, 401)

    def test_category_detail(self):
        response = self.client.get('/api/v1/categories/1/')
        self.assertEqual(response.status_code, 401)

    def test_review_list(self):
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 401)

    def test_review_detail(self):
        response = self.client.get('/api/v1/reviews/1/')
        self.assertEqual(response.status_code, 401)

    def test_review_filter_beer_name(self):
        response = self.client.get('/api/v1/reviews/?beer_name=Perła')
        self.assertEqual(response.status_code, 401)

    def test_review_filter_beer_id(self):
        response = self.client.get('/api/v1/reviews/?beer_id=1')
        self.assertEqual(response.status_code, 401)

    def test_comment_list(self):
        response = self.client.get('/api/v1/comments/')
        self.assertEqual(response.status_code, 401)

    def test_comment_detail(self):
        response = self.client.get('/api/v1/comments/1/')
        self.assertEqual(response.status_code, 401)

    def test_comment_filter_review_id(self):
        response = self.client.get('/api/v1/comments/?review=1')
        self.assertEqual(response.status_code, 401)

    def test_post_category(self):
        new_category = {
            "name": "APA"}

        response = self.client.post('/api/v1/categories/', new_category)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_beer(self):
        new_beer = {
            "name": "Heineken",
            "description": "Very interesting and long description.",
            "category": self.category_1.id}

        response = self.client.post('/api/v1/beers/', new_beer)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_review(self):
        new_review = {"title": "test",
                      "content": 'foobar',
                      "beer": self.beer_2.id,
                      "rating": 10}

        response = self.client.post('/api/v1/reviews/', new_review)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_comment(self):
        new_comment = {"content": "please work",
                       "review": self.review_1.id}
        response = self.client.post('/api/v1/comments/', new_comment)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserTestCase(APITestCase):
    def setUp(self) -> None:
        self.register_url = '/api/v1/auth/register'
        self.login_url = '/api/v1/auth/login'
        self.register_data = {'username': 'user',
                              'password': 'word',
                              'email': 'foo@bar.com',
                              'first_name': 'foo',
                              'last_name': 'bar'}
        self.login_data = {'username': 'user',
                           'password': 'word'}
        self.client.post(self.register_url, self.register_data)
        self.token = self.client.post(self.login_url, data=self.login_data).json()['token']

        # INIT TEST DATABASE
        set_up_database(self)

    def test_beer_list(self):
        response = self.client.get('/api/v1/beers/', **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, 200)

    def test_beer_detail(self):
        response = self.client.get('/api/v1/beers/1/', **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertIn(response.status_code, (200, 404))

    def test_beer_filter(self):
        response = self.client.get('/api/v1/beers/?category=Lager', **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, 200)

    def test_category_list(self):
        response = self.client.get('/api/v1/categories/', **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, 200)

    def test_category_detail(self):
        response = self.client.get('/api/v1/categories/1/', **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertIn(response.status_code, (200, 404))

    def test_review_list(self):
        response = self.client.get('/api/v1/reviews/', **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, 200)

    def test_review_detail(self):
        response = self.client.get('/api/v1/reviews/1/', **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertIn(response.status_code, (200, 404))

    def test_review_filter_beer_name(self):
        response = self.client.get('/api/v1/reviews/?beer_name=Perła', **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, 200)

    def test_review_filter_beer_id(self):
        response = self.client.get('/api/v1/reviews/?beer_id=1', **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, 200)

    def test_comment_list(self):
        response = self.client.get('/api/v1/comments/', **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, 200)

    def test_comment_detail(self):
        response = self.client.get('/api/v1/comments/1/', **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertIn(response.status_code, (200, 404))

    def test_comment_filter_review_id(self):
        response = self.client.get('/api/v1/comments/?review=1', **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, 200)

    def test_post_category(self):
        new_category = {
            "name": "APA"}

        response = self.client.post('/api/v1/categories/', new_category,
                                    **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_beer(self):
        new_beer = {
            "name": "Heineken",
            "description": "Very interesting and long description.",
            "category": self.category_1.id}

        response = self.client.post('/api/v1/beers/', new_beer, **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, 201)

    def test_post_review(self):
        new_review = {"title": "test",
                      "content": 'foobar',
                      "beer": self.beer_2.id,
                      "rating": 10}

        response = self.client.post('/api/v1/reviews/', new_review, **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, 201)

    def test_post_comment(self):
        new_comment = {"content": "please work",
                       "review": self.review_1.id}
        response = self.client.post('/api/v1/comments/', new_comment, **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, 201)

    def test_delete_category(self):
        category_id = self.category_1.id
        response = self.client.delete(f'/api/v1/categories/{category_id}/',
                                      **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_beer(self):
        beer_id = self.beer_1.id
        response = self.client.delete(f'/api/v1/beers/{beer_id}/', **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_review(self):
        review_id = self.review_1.id
        response = self.client.delete(f'/api/v1/reviews/{review_id}/', **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment(self):
        comment_id = self.comment_1.id
        response = self.client.delete(f'/api/v1/comments/{comment_id}/',
                                      **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_category(self):
        new_category = {
            "name": "new_name"}
        category_id = self.category_1.id
        response = self.client.put(f'/api/v1/categories/{category_id}/', new_category,
                                   **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_beer(self):
        new_beer = {
            "name": "new_name",
            "description": "new_desc",
            "category": self.category_2.id}
        beer_id = self.beer_1.id
        response = self.client.put(f'/api/v1/beers/{beer_id}/', new_beer,
                                   **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_review(self):
        new_review = {"title": "new_title",
                      "content": 'new_content',
                      "beer": self.beer_1.id,
                      "rating": 1}
        review_id = self.review_1.id
        response = self.client.put(f'/api/v1/reviews/{review_id}/', new_review,
                                   **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_comment(self):
        new_comment = {"content": "new_content",
                       "review": self.review_1.id}
        comment_id = self.comment_1.id
        response = self.client.put(f'/api/v1/comments/{comment_id}/', new_comment,
                                   **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_review_by_its_author(self):
        token = self.client.post(self.login_url, data={'username': 'user_1',
                                                       'password': 'password'}).json()['token']
        new_review = {"title": "new_title",
                      "content": 'new_content',
                      "rating": 1}
        review_id = self.review_1.id
        response = self.client.put(f'/api/v1/reviews/{review_id}/', new_review,
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        beer_id = response.data.get('beer')
        self.assertEqual(beer_id, self.beer_1.id)

    def test_put_comment_by_its_author(self):
        token = self.client.post(self.login_url, data={'username': 'user_1',
                                                       'password': 'password'}).json()['token']
        new_comment = {"content": 'new_content'}
        comment_id = self.comment_1.id
        response = self.client.put(f'/api/v1/comments/{comment_id}/', new_comment,
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        review_id = response.data.get('review')
        self.assertEqual(review_id, self.review_2.id)

    def test_delete_review_by_its_author(self):
        token = self.client.post(self.login_url, data={'username': 'user_1',
                                                       'password': 'password'}).json()['token']
        review_id = self.review_1.id
        response = self.client.delete(f'/api/v1/reviews/{review_id}/', **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_comment_by_its_author(self):
        token = self.client.post(self.login_url, data={'username': 'user_1',
                                                       'password': 'password'}).json()['token']
        comment_id = self.comment_1.id
        response = self.client.delete(f'/api/v1/comments/{comment_id}/',
                                      **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_try_to_change_review_parent_beer(self):
        token = self.client.post(self.login_url, data={'username': 'user_1',
                                                       'password': 'password'}).json()['token']
        new_review = {"title": "new_title",
                      "beer": self.beer_2,
                      "content": 'new_content',
                      "rating": 1}
        review_id = self.review_1.id
        response = self.client.put(f'/api/v1/reviews/{review_id}/', new_review,
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        beer_id = response.data.get('beer')
        self.assertNotEqual(beer_id, self.beer_2.id)
        self.assertEqual(beer_id, self.beer_1.id)

    def test_try_to_change_comment_parent_review(self):
        token = self.client.post(self.login_url, data={'username': 'user_1',
                                                       'password': 'password'}).json()['token']
        new_comment = {"content": "new_content",
                       "review": self.review_1}
        comment_id = self.comment_1.id
        response = self.client.put(f'/api/v1/comments/{comment_id}/', new_comment,
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        review_id = response.data.get('review')
        self.assertNotEqual(review_id, self.review_1.id)
        self.assertEqual(review_id, self.review_2.id)
