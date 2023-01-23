from django.urls import reverse

from rest_framework.test import APITestCase

from weatherapp import serializers
from weatherapp.models import MyUser, City


class TestUserSerializer(APITestCase):
    def setUp(self):
        self.user_data = {"email": "test@gmail.com",
                          "password": "password"}
        self.client.post(reverse("register"), self.user_data)

        self.user_serialized_data = {
            "id": 1,
            "email": "test@gmail.com",
            "cities": []
        }
        self.serializer = serializers.UserSerializer(MyUser.objects.get(id=1))
        return super().setUp()

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'email', "cities"})

    def test_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['id'], self.user_serialized_data['id'])
        self.assertEqual(data['email'], self.user_serialized_data['email'])
        self.assertEqual(data['cities'], self.user_serialized_data['cities'])


class TestCitySerializer(APITestCase):
    def setUp(self):
        # authentication
        self.user_data = {"email": "test@gmail.com",
                          "password": "password"}
        self.client.post(reverse("register"), self.user_data)
        response = self.client.post(reverse('token_obtain_pair'), self.user_data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        self.city_data = {"city": "kyiv",
                          "notification": 1}
        self.client.post(reverse("subscriptions"), self.city_data)

        self.city_serialized_data = {
            "city": "kyiv",
            "notification": "01:00:00"
        }
        self.serializer = serializers.CitySerializer(City.objects.get(city="kyiv"))
        return super().setUp()

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'city', 'notification'})

    def test_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['city'], self.city_serialized_data['city'])
        self.assertEqual(data['notification'], self.city_serialized_data['notification'])


class TestRegisterSerializer(APITestCase):
    def setUp(self):
        self.user_data = {"email": "test@gmail.com",
                          "password": "password"}
        self.serializer = serializers.RegisterSerializer(data=self.user_data)
        self.serializer.is_valid(raise_exception=True)
        self.serializer.save()
        self.serialized_data = {"id": 1,
                                "email": "test@gmail.com"}
        return super().setUp()

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'email'})

    def test_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['id'], self.serialized_data['id'])
        self.assertEqual(data['email'], self.serialized_data['email'])
