from rest_framework.test import APITestCase


class AuthorizationTestCase(APITestCase):
    def setUp(self) -> None:
        self.register_url = '/api/v1/auth/register'
        self.login_url = '/api/v1/auth/login'
        self.userdata_url = '/api/v1/auth/user'
        self.logout_url = '/api/v1/auth/logout'

        self.register_data = {'username': 'username',
                              'password': 'wordpass',
                              'email': 'foo@bar.com',
                              'first_name': 'foo',
                              'last_name': 'bar'}

        self.login_data = {'username': 'username',
                           'password': 'wordpass'}

        self.client.post(self.register_url, self.register_data)

    def test_register(self):
        user_data = {'username': 'beer_enjoyer',
                     'password': 'password',
                     'email': 'beer_enjoyer@bar.com',
                     'first_name': 'foo',
                     'last_name': 'bar'}
        response = self.client.post(self.register_url, user_data)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post(self.login_url, data=self.login_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json()['token'])

    def test_get_user_data(self):
        token = self.client.post(self.login_url, data=self.login_data).json()['token']
        response = self.client.get(self.userdata_url, **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, 200)

        user_data = response.data.get('user_info')

        user_id = user_data.get('id')
        username = user_data.get('username')
        email = user_data.get('email')
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')

        self.assertEqual(1, user_id)
        self.assertEqual(self.register_data.get('username'), username)
        self.assertEqual(self.register_data.get('email'), email)
        self.assertEqual(self.register_data.get('first_name'), first_name)
        self.assertEqual(self.register_data.get('last_name'), last_name)

    def test_logout(self):
        token = self.client.post(self.login_url, data=self.login_data).json()['token']
        response = self.client.post(self.logout_url, **{"HTTP_AUTHORIZATION": f"Token {token}"})
        self.assertEqual(response.status_code, 204)
