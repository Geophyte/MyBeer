from rest_framework import status
from rest_framework.test import APITestCase

from beers.models import Review, Beer, Comment
from .helpers import set_up_database, activate, deactivate


class CommentEndpointTestCase(APITestCase):
    """
    GET all                     - AUTHENTICATED
    GET one                     - AUTHENTICATED
    GET filtered by review_id   - AUTHENTICATED
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

    def test_get_comments_all_by_not_authenticated_user(self):
        response = self.client.get('/api/v1/comments/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_comments_all_not_active_beer_by_authenticated_user(self):
        deactivate(Beer)
        activate(Review)
        activate(Comment)

        token = self.get_token(self.user_1)
        response = self.client.get('/api/v1/comments/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_comments_all_not_active_review_by_authenticated_user(self):
        activate(Beer)
        deactivate(Review)
        activate(Comment)

        token = self.get_token(self.user_1)
        response = self.client.get('/api/v1/comments/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_comments_all_not_active_comments_by_authenticated_user(self):
        activate(Beer)
        activate(Review)
        deactivate(Comment)

        token = self.get_token(self.user_1)
        response = self.client.get('/api/v1/comments/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_comments_all_only_active_beer_by_authenticated_user(self):
        activate(Beer)
        deactivate(Review)
        deactivate(Comment)

        token = self.get_token(self.user_1)
        response = self.client.get('/api/v1/comments/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_comments_all_only_active_review_by_authenticated_user(self):
        deactivate(Beer)
        activate(Review)
        deactivate(Comment)

        token = self.get_token(self.user_1)
        response = self.client.get('/api/v1/comments/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_comments_all_only_active_comments_by_authenticated_user(self):
        deactivate(Beer)
        deactivate(Review)
        activate(Comment)

        token = self.get_token(self.user_1)
        response = self.client.get('/api/v1/comments/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_comments_all_active_all_by_authenticated_user(self):
        activate(Beer)
        activate(Review)
        activate(Comment)

        token = self.get_token(self.user_1)
        response = self.client.get('/api/v1/comments/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_get_comment_one_by_not_authenticated_user(self):
        response = self.client.get(f'/api/v1/comments/{self.comment_1.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_comment_one_not_active_beer_by_authenticated_user(self):
        deactivate(Beer)
        activate(Review)
        activate(Comment)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/comments/{self.comment_1.id}/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_comment_one_not_active_review_by_authenticated_user(self):
        activate(Beer)
        deactivate(Review)
        activate(Comment)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/comments/{self.comment_1.id}/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_comment_one_not_active_comments_by_authenticated_user(self):
        activate(Beer)
        activate(Review)
        deactivate(Comment)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/comments/{self.comment_1.id}/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_comment_one_only_active_beer_by_authenticated_user(self):
        activate(Beer)
        deactivate(Review)
        deactivate(Comment)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/comments/{self.comment_1.id}/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_comment_one_only_active_review_by_authenticated_user(self):
        deactivate(Beer)
        activate(Review)
        deactivate(Comment)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/comments/{self.comment_1.id}/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_comment_one_only_active_comments_by_authenticated_user(self):
        deactivate(Beer)
        deactivate(Review)
        activate(Comment)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/comments/{self.comment_1.id}/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_comment_one_all_active_by_authenticated_user(self):
        activate(Beer)
        activate(Review)
        activate(Comment)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/comments/{self.comment_1.id}/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_comments_filtered_by_review_id_by_not_authenticated_user(self):
        response = self.client.get(f'/api/v1/comments/?review={self.review_1.id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_comments_not_active_beer_filtered_by_review_id_by_authenticated_user(self):
        deactivate(Beer)
        activate(Review)
        activate(Comment)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/comments/?review={self.review_1.id}',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_comments_not_active_review_filtered_by_review_id_by_authenticated_user(self):
        activate(Beer)
        deactivate(Review)
        activate(Comment)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/comments/?review={self.review_1.id}',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_comments_not_active_comments_filtered_by_review_id_by_authenticated_user(self):
        activate(Beer)
        activate(Review)
        deactivate(Comment)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/comments/?review={self.review_1.id}',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_comments_only_active_beer_filtered_by_review_id_by_authenticated_user(self):
        activate(Beer)
        deactivate(Review)
        deactivate(Comment)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/comments/?review={self.review_1.id}',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_comments_only_active_review_filtered_by_review_id_by_authenticated_user(self):
        deactivate(Beer)
        activate(Review)
        deactivate(Comment)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/comments/?review={self.review_1.id}',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_comments_only_active_comments_filtered_by_review_id_by_authenticated_user(self):
        deactivate(Beer)
        deactivate(Review)
        activate(Comment)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/comments/?review={self.review_1.id}',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_comments_all_active_filtered_by_review_id_by_authenticated_user(self):
        activate(Beer)
        activate(Review)
        activate(Comment)

        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/comments/?review={self.review_2.id}',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_post_comment_by_not_authenticated_user(self):
        new_comment = {'content': 'test content',
                       'review': self.review_1.id}

        response = self.client.post(f'/api/v1/comments/', data=new_comment)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_comment_without_active_by_authenticated_user(self):
        token = self.get_token(self.user_1)
        new_comment = {'content': 'test content',
                       'review': self.review_1.id}

        response = self.client.post(f'/api/v1/comments/', data=new_comment,
                                    **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['active'])

    def test_post_comment_with_active_set_false_by_authenticated_user(self):
        token = self.get_token(self.user_1)
        new_comment = {'content': 'test content',
                       'review': self.review_1.id,
                       'active': False}

        response = self.client.post(f'/api/v1/comments/', data=new_comment,
                                    **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['active'])

    def test_post_comment_without_active_by_admin(self):
        token = self.get_token(self.admin)
        new_comment = {'content': 'test content',
                       'review': self.review_1.id}

        response = self.client.post(f'/api/v1/comments/', data=new_comment,
                                    **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['active'])

    def test_post_comment_with_active_set_false_by_admin(self):
        token = self.get_token(self.admin)
        new_comment = {'content': 'test content',
                       'review': self.review_1.id,
                       'active': False}

        response = self.client.post(f'/api/v1/comments/', data=new_comment,
                                    **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['active'])

    def test_patch_comment_by_not_authenticated_user(self):
        new_comment = {'active': False}
        response = self.client.patch(f'/api/v1/comments/{self.comment_1.id}/', data=new_comment)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        comment = Comment.objects.get(pk=self.comment_1.id)
        self.assertTrue(comment.active)

    def test_patch_comment_by_authenticated_not_author(self):
        token = self.get_token(self.user_2)
        new_comment = {'active': False}
        response = self.client.patch(f'/api/v1/comments/{self.comment_1.id}/', data=new_comment,
                                     **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        comment = Comment.objects.get(pk=self.comment_1.id)
        self.assertTrue(comment.active)

    def test_patch_comment_by_author(self):
        token = self.get_token(self.user_1)
        new_comment = {'active': False}
        response = self.client.patch(f'/api/v1/comments/{self.comment_1.id}/', data=new_comment,
                                     **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        comment = Comment.objects.get(pk=self.comment_1.id)
        self.assertFalse(comment.active)

    def test_patch_comment_by_admin(self):
        token = self.get_token(self.admin)
        new_comment = {'active': False}
        response = self.client.patch(f'/api/v1/comments/{self.comment_1.id}/', data=new_comment,
                                     **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        comment = Comment.objects.get(pk=self.comment_1.id)
        self.assertFalse(comment.active)

    def test_delete_comment_by_not_authenticated_user(self):
        response = self.client.delete(f'/api/v1/comments/{self.comment_1.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_comment_by_authenticated_not_author(self):
        token = self.get_token(self.user_2)
        response = self.client.delete(f'/api/v1/comments/{self.comment_1.id}/',
                                      **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete_comment_by_author(self):
        token = self.get_token(self.user_1)
        response = self.client.delete(f'/api/v1/comments/{self.comment_1.id}/',
                                      **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_delete_comment_by_admin(self):
        token = self.get_token(self.admin)
        response = self.client.delete(f'/api/v1/comments/{self.comment_1.id}/',
                                      **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
