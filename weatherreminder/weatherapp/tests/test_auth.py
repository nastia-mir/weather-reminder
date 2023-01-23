from django.urls import reverse

from rest_framework.test import APITestCase


class TestAuth(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.correct_data = {"email": "test@gmail.com",
                             "password": "password"}
        self.email_only = {"email": "test@gmail.com"}
        self.password_only = {"password": "password"}
        return super().setUp()

    def test_register_POST_correct_data(self):
        response = self.client.post(self.register_url, self.correct_data)
        self.assertEqual(response.status_code, 200)
        assert 'id' in response.data

    def test_register_POST_used_email(self):
        self.client.post(self.register_url, self.correct_data)
        response = self.client.post(self.register_url, self.correct_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], 'user with given email already exists')

    def test_register_POST_email_only(self):
        response = self.client.post(self.register_url, self.email_only)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["password"][0], 'This field is required.')

    def test_register_POST_password_only(self):
        response = self.client.post(self.register_url, self.password_only)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["email"][0], 'This field is required.')