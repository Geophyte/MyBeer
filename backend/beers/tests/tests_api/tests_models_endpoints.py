from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APITestCase

from beers.models import Beer, Category


class NotAuthenticatedUserTestCase(APITestCase):
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


class AuthenticatedUserTestCase(APITestCase):
    def setUp(self) -> None:
        self.register_url = '/api/v1/auth/register'
        self.login_url = '/api/v1/auth/login'
        self.register_data = {'username': 'username',
                              'password': 'wordpass',
                              'email': 'foo@bar.com',
                              'first_name': 'foo',
                              'last_name': 'bar'}
        self.login_data = {'username': 'username',
                           'password': 'wordpass'}
        self.client.post(self.register_url, self.register_data)
        self.token = self.client.post(self.login_url, data=self.login_data).json()['token']


    def test_beer_list(self):
        response = self.client.get('/api/v1/beers/', **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, 200)

    def test_beer_detail(self):
        response = self.client.get('/api/v1/beers/1/', **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, 404)

    def test_beer_filter(self):
        response = self.client.get('/api/v1/beers/?category=Lager', **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, 200)

    def test_category_list(self):
        response = self.client.get('/api/v1/categories/', **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, 200)

    def test_category_detail(self):
        response = self.client.get('/api/v1/categories/1/', **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, 404)

    def test_review_list(self):
        response = self.client.get('/api/v1/reviews/', **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, 200)

    def test_review_detail(self):
        response = self.client.get('/api/v1/reviews/1/', **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, 404)

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
        self.assertEqual(response.status_code, 404)

    def test_comment_filter_review_id(self):
        response = self.client.get('/api/v1/comments/?review=1', **{"HTTP_AUTHORIZATION": f"Token {self.token}"})
        self.assertEqual(response.status_code, 200)