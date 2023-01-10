from rest_framework import status
from rest_framework.test import APITestCase

from beers.models import Beer
from .helpers import set_up_database, activate


class BeerEndpointTestCase(APITestCase):
    """
    GET all                     - AUTHENTICATED
    GET one                     - AUTHENTICATED
    GET filtered by category    - AUTHENTICATED
    GET filtered by name        - AUTHENTICATED
    POST                        - ADMIN
    PATCH                       - ADMIN
    DELETE                      - ADMIN
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

    def test_get_beers_all_by_not_authenticated_user(self):
        response = self.client.get('/api/v1/beers/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_beers_all_not_active_by_authenticated_user(self):
        token = self.get_token(self.user_1)
        response = self.client.get('/api/v1/beers/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_beers_all_active_by_authenticated_user(self):
        activate(Beer)
        token = self.get_token(self.user_1)
        response = self.client.get('/api/v1/beers/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_get_beer_one_by_not_authenticated_user(self):
        response = self.client.get(f'/api/v1/beers/{self.beer_1.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_beer_one_not_active_by_authenticated_user(self):
        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/beers/{self.beer_1.id}/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_beer_one_active_by_authenticated_user(self):
        activate(Beer)
        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/beers/{self.beer_1.id}/',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_beer_filtered_by_category_by_not_authenticated_user(self):
        response = self.client.get(f'/api/v1/beers/?category=Lager')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_beer_not_active_filtered_by_category_by_authenticated_user(self):
        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/beers/?category=Lager',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_beer_active_filtered_by_category_by_authenticated_user(self):
        activate(Beer)
        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/beers/?category=Lager',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_beer_filtered_by_name_by_not_authenticated_user(self):
        response = self.client.get(f'/api/v1/beers/?name=Perła')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_beer_not_active_filtered_by_name_by_authenticated_user(self):
        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/beers/?name=Perła',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_beer_active_filtered_by_name_by_authenticated_user(self):
        activate(Beer)
        token = self.get_token(self.user_1)
        response = self.client.get(f'/api/v1/beers/?name=Perła',
                                   **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_beer_by_not_authenticated_user(self):
        new_beer = {'name': 'Test name',
                    'description': 'test description',
                    'category': self.category_1
                    }
        response = self.client.post(f'/api/v1/beers/', data=new_beer)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_beer_without_active_by_authenticated_user(self):
        token = self.get_token(self.user_1)
        new_beer = {'name': 'Test name',
                    'description': 'test description',
                    'category': self.category_1.id
                    }
        response = self.client.post(f'/api/v1/beers/', data=new_beer,
                                    **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data['active'])

    def test_post_beer_with_active_set_true_by_authenticated_user(self):
        token = self.get_token(self.user_1)
        new_beer = {'name': 'Test name',
                    'description': 'test description',
                    'category': self.category_1.id,
                    'active': True
                    }
        response = self.client.post(f'/api/v1/beers/', data=new_beer,
                                    **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data['active'])

    def test_post_beer_without_active_by_admin(self):
        token = self.get_token(self.admin)
        new_beer = {'name': 'Test name',
                    'description': 'test description',
                    'category': self.category_1.id
                    }
        response = self.client.post(f'/api/v1/beers/', data=new_beer,
                                    **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data['active'])

    def test_post_beer_with_active_set_true_by_admin(self):
        token = self.get_token(self.admin)
        new_beer = {'name': 'Test name',
                    'description': 'test description',
                    'category': self.category_1.id,
                    'active': True
                    }
        response = self.client.post(f'/api/v1/beers/', data=new_beer,
                                    **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['active'])

    def test_patch_beer_by_not_authenticated_user(self):
        new_beer = {'active': True}
        response = self.client.patch(f'/api/v1/beers/{self.beer_1.id}/', data=new_beer)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        beer = Beer.objects.get(pk=self.beer_1.id)
        self.assertFalse(beer.active)

    def test_patch_beer_by_authenticated_user(self):
        token = self.get_token(self.user_1)
        new_beer = {'active': True}
        response = self.client.patch(f'/api/v1/beers/{self.beer_1.id}/', data=new_beer,
                                     **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        beer = Beer.objects.get(pk=self.beer_1.id)
        self.assertFalse(beer.active)

    def test_patch_beer_by_admin(self):
        token = self.get_token(self.admin)
        new_beer = {'active': True}
        response = self.client.patch(f'/api/v1/beers/{self.beer_1.id}/', data=new_beer,
                                     **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        beer = Beer.objects.get(pk=self.beer_1.id)
        self.assertTrue(beer.active)

        new_beer = {'active': False}
        response = self.client.patch(f'/api/v1/beers/{self.beer_1.id}/', data=new_beer,
                                     **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        beer = Beer.objects.get(pk=self.beer_1.id)
        self.assertFalse(beer.active)

    def test_delete_beer_by_not_authenticated_user(self):
        response = self.client.delete(f'/api/v1/beers/{self.beer_1.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_beer_by_authenticated_user(self):
        token = self.get_token(self.user_1)
        response = self.client.delete(f'/api/v1/beers/{self.beer_1.id}/',
                                      **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_beer_by_admin(self):
        token = self.get_token(self.admin)
        response = self.client.delete(f'/api/v1/beers/{self.beer_1.id}/',
                                      **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
