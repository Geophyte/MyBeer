from rest_framework import status
from rest_framework.test import APITestCase
from .helpers import set_up_database


class CategoryEndpointTestCase(APITestCase):
    """
    GET all     - AUTHENTICATED
    GET one     - AUTHENTICATED
    POST        - ADMIN
    PATCH       - ADMIN
    DELETE - ADMIN
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

    def test_get_categories_all_by_not_authenticated_user(self):
        response = self.client.get('/api/v1/categories/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_categories_all_by_authenticated_user(self):
        token = self.get_token(self.user_1)
        response = self.client.get('/api/v1/categories/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category_one_by_not_authenticated_user(self):
        response = self.client.get(f'/api/v1/categories/{self.category_1.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_category_one_by_authenticated_user(self):
        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/categories/{self.category_1.id}/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_category_by_not_authenticated_user(self):
        new_category = {'name': 'Test name'}
        response = self.client.post(f'/api/v1/categories/', data=new_category)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_category_by_authenticated_user(self):
        token = self.get_token(self.user_1)
        new_category = {'name': 'Test name'}
        response = self.client.post(f'/api/v1/categories/', data=new_category,
                                    **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_category_by_admin_user(self):
        token = self.get_token(self.admin)
        new_category = {'name': 'Test name'}
        response = self.client.post(f'/api/v1/categories/', data=new_category,
                                    **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_category_by_not_authenticated_user(self):
        new_category = {'name': 'Test name'}
        response = self.client.patch(f'/api/v1/categories/{self.category_1.id}/', data=new_category)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_category_by_authenticated_user(self):
        token = self.get_token(self.user_1)
        new_category = {'name': 'Test name'}
        response = self.client.patch(f'/api/v1/categories/{self.category_1.id}/', data=new_category,
                                     **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_category_by_admin_user(self):
        token = self.get_token(self.admin)
        new_category = {'name': 'Test name'}
        response = self.client.patch(f'/api/v1/categories/{self.category_1.id}/', data=new_category,
                                     **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category_by_not_authenticated_user(self):
        response = self.client.delete(f'/api/v1/categories/{self.category_1.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_category_by_authenticated_user(self):
        token = self.get_token(self.user_1)
        response = self.client.delete(f'/api/v1/categories/{self.category_1.id}/',
                                      **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_category_by_admin_user(self):
        token = self.get_token(self.admin)
        category_id = self.category_1.id
        response = self.client.delete(f'/api/v1/categories/{category_id}/',
                                      **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
