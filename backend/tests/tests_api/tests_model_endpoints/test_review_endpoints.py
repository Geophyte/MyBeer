from rest_framework import status
from rest_framework.test import APITestCase

from beers.models import Review, Beer, Comment
from .helpers import set_up_database, activate, deactivate


class ReviewEndpointTestCase(APITestCase):
    """
    GET all                     - AUTHENTICATED
    GET one                     - AUTHENTICATED
    GET filtered by beer_name   - AUTHENTICATED
    GET filtered by beer_id     - AUTHENTICATED
    POST                        - AUTHENTICATED
    PATCH                       - AUTHOR
    DELETE                      - AUTHOR
    """

    @classmethod
    def setUpClass(cls):
        cls.login_url = '/api/v1/auth/login'
        cls.user_1_data = {'username': 'user_1',
                           'password': 'password'}
        cls.user_2_data = {'username': 'user_2',
                           'password': 'password'}
        cls.admin_data = {'username': 'admin',
                          'password': 'admin'}

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        set_up_database(self)

    def get_token(self, user):
        if user == self.user_1:
            data = {'username': 'user_1',
                    'password': 'password'}
        if user == self.user_2:
            data = {'username': 'user_2',
                    'password': 'password'}
        if user == self.admin:
            data = {'username': 'admin',
                    'password': 'admin'}
        token = self.client.post(self.login_url, data=data).json()['token']
        return token


    def test_get_reviews_all_by_not_authenticated_user(self):
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_reviews_all_not_active_beer_not_active_review_by_authenticated_user(self):
        deactivate(Beer)
        deactivate(Review)

        token = self.get_token(self.user_1)
        response = self.client.get('/api/v1/reviews/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_reviews_all_not_active_beer_active_review_by_authenticated_user(self):
        deactivate(Beer)
        activate(Review)

        token = self.get_token(self.user_1)
        response = self.client.get('/api/v1/reviews/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_reviews_all_active_beer_not_active_review_by_authenticated_user(self):
        activate(Beer)
        deactivate(Review)

        token = self.get_token(self.user_1)
        response = self.client.get('/api/v1/reviews/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_reviews_all_active_beer_active_review_by_authenticated_user(self):
        activate(Beer)
        activate(Review)
        token = self.get_token(self.user_1)
        response = self.client.get('/api/v1/reviews/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_get_review_one_by_not_authenticated_user(self):
        response = self.client.get(f'/api/v1/reviews/{self.review_1.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_review_one_not_active_beer_not_active_review_by_authenticated_user(self):
        deactivate(Beer)
        deactivate(Review)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/reviews/{self.review_1.id}/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_review_one_not_active_beer_active_review_by_authenticated_user(self):
        activate(Beer)
        deactivate(Review)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/reviews/{self.review_1.id}/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_review_one_active_beer_not_active_review_by_authenticated_user(self):
        deactivate(Beer)
        activate(Review)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/reviews/{self.review_1.id}/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_review_one_active_beer_active_review_by_authenticated_user(self):
        activate(Beer)
        activate(Review)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/reviews/{self.review_1.id}/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_reviews_filtered_by_beer_name_by_not_authenticated_user(self):
        response = self.client.get(f'/api/v1/reviews/?beer_name=Perła')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_reviews_not_active_beer_not_active_review_filtered_by_beer_name_by_authenticated_user(self):
        deactivate(Beer)
        deactivate(Review)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/reviews/?beer_name=Perła',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_reviews_not_active_beer_active_review_filtered_by_beer_name_by_authenticated_user(self):
        deactivate(Beer)
        activate(Review)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/reviews/?beer_name=Perła',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_reviews_active_beer_not_active_review_filtered_by_beer_name_by_authenticated_user(self):
        activate(Beer)
        deactivate(Review)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/reviews/?beer_name=Perła',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_reviews_active_beer_active_review_by_filtered_by_beer_name_authenticated_user(self):
        activate(Beer)
        activate(Review)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/reviews/?beer_name=Perła',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_reviews_filtered_by_beer_id_by_not_authenticated_user(self):
        response = self.client.get(f'/api/v1/reviews/?beer_id={self.beer_1.id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_reviews_not_active_beer_not_active_review_filtered_by_beer_id_by_authenticated_user(self):
        deactivate(Beer)
        deactivate(Review)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/reviews/?beer_id={self.beer_1.id}',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_reviews_not_active_beer_active_review_filtered_by_beer_id_by_authenticated_user(self):
        deactivate(Beer)
        activate(Review)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/reviews/?beer_id={self.beer_1.id}',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_reviews_active_beer_not_active_review_filtered_by_beer_id_by_authenticated_user(self):
        activate(Beer)
        deactivate(Review)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/reviews/?beer_id={self.beer_1.id}',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_reviews_active_beer_active_review_by_filtered_by_beer_id_authenticated_user(self):
        activate(Beer)
        activate(Review)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/reviews/?beer_id={self.beer_1.id}',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_post_review_by_not_authenticated_user(self):
        new_review = {'title': 'Test title',
                      'content': 'test content',
                      'beer': self.beer_1,
                      'rating': 5}
        response = self.client.post(f'/api/v1/reviews/', data=new_review)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_review_without_active_by_authenticated_user(self):
        token = self.get_token(self.user_1)
        new_review = {'title': 'Test title',
                      'content': 'test content',
                      'beer': self.beer_1.id,
                      'rating': 5}

        response = self.client.post('/api/v1/reviews/', data=new_review,
                                    **{"HTTP_AUTHORIZATION": f"Token {token}"})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['active'])

    def test_post_review_with_active_set_false_by_authenticated_user(self):
        token = self.get_token(self.user_1)
        new_review = {'title': 'Test title',
                      'content': 'test content',
                      'beer': self.beer_1.id,
                      'rating': 5,
                      'active': False}

        response = self.client.post('/api/v1/reviews/', data=new_review,
                                    **{"HTTP_AUTHORIZATION": f"Token {token}"})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['active'])

    def test_post_review_without_active_by_admin(self):
        token = self.get_token(self.admin)
        new_review = {'title': 'Test title',
                      'content': 'test content',
                      'beer': self.beer_1.id,
                      'rating': 5}

        response = self.client.post(f'/api/v1/reviews/', data=new_review,
                                    **{"HTTP_AUTHORIZATION": f"Token {token}"})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['active'])

    def test_post_review_with_active_set_false_by_admin(self):
        token = self.get_token(self.admin)
        new_review = {'title': 'Test title',
                      'content': 'test content',
                      'beer': self.beer_1.id,
                      'rating': 5,
                      'active': False}

        response = self.client.post('/api/v1/reviews/', data=new_review,
                                    **{"HTTP_AUTHORIZATION": f"Token {token}"})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['active'])

    def test_patch_review_by_not_authenticated_user(self):
        new_review = {'active': False}
        response = self.client.patch(f'/api/v1/reviews/{self.review_1.id}/', data=new_review)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        review = Review.objects.get(pk=self.review_1.id)
        self.assertTrue(review.active)

    def test_patch_review_by_authenticated_not_author(self):
        token = self.get_token(self.user_2)
        new_review = {'active': False}
        response = self.client.patch(f'/api/v1/reviews/{self.review_1.id}/', data=new_review,
                                     **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        review = Review.objects.get(pk=self.review_1.id)
        self.assertTrue(review.active)

    def test_patch_review_by_author(self):
        token = self.get_token(self.user_1)
        new_review = {'active': False}
        response = self.client.patch(f'/api/v1/reviews/{self.review_1.id}/', data=new_review,
                                     **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        review = Review.objects.get(pk=self.review_1.id)
        self.assertFalse(review.active)

    def test_patch_review_by_admin(self):
        token = self.get_token(self.admin)
        new_review = {'active': False}
        response = self.client.patch(f'/api/v1/reviews/{self.review_1.id}/', data=new_review,
                                     **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        review = Review.objects.get(pk=self.review_1.id)
        self.assertFalse(review.active)

    def test_delete_review_by_not_authenticated_user(self):
        response = self.client.delete(f'/api/v1/reviews/{self.review_1.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_review_by_authenticated_not_author(self):
        token = self.get_token(self.user_2)
        response = self.client.delete(f'/api/v1/reviews/{self.review_1.id}/',
                                      **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_review_by_author(self):
        token = self.get_token(self.user_1)
        response = self.client.delete(f'/api/v1/reviews/{self.review_1.id}/',
                                      **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Comment.objects.filter(review=self.review_1.id)), 0)

    def test_delete_review_by_admin(self):
        token = self.get_token(self.user_1)
        response = self.client.delete(f'/api/v1/reviews/{self.review_1.id}/',
                                      **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Comment.objects.filter(review=self.review_1.id)), 0)