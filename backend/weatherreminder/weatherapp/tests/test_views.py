from rest_framework.test import APITestCase
from django.urls import reverse


class TestViewsLoggedIn(APITestCase):

    def setUp(self):
        self.home_url = reverse('home')
        self.subscriptions_url = reverse('subscriptions')
        self.delete_user_url = reverse('delete user')
        self.token_obtain_pair_url = reverse('token_obtain_pair')

        # authentication
        self.user_data = {"email": "test@gmail.com",
                          "password": "password"}
        self.client.post(reverse("register"), self.user_data)
        response = self.client.post(reverse('token_obtain_pair'), self.user_data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        self.other_user_data = {"email": "other@gmail.com",
                                "password": "password"}
        self.client.post(reverse("register"), self.other_user_data)

        return super().setUp()

    def test_home_GET(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)

    def test_subscriptions_GET(self):
        response = self.client.get(self.subscriptions_url)
        self.assertEqual(response.status_code, 200)
        assert 'cities' in response.data

    def test_subscriptions_POST_correct(self):
        response = self.client.post(self.subscriptions_url, {"city": "kyiv",
                                                             "notification": 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["cities"][len(response.data["cities"])-1]["city"], "kyiv")

    def test_subscriptions_POST_invalid_city(self):
        response = self.client.post(self.subscriptions_url, {"city": "somecity",
                                                             "notification": 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], 'enter valid city name')

    def test_subscriptions_POST_invalid_notification(self):
        response = self.client.post(self.subscriptions_url, {"city": "kyiv",
                                                             "notification": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], 'you can set notification frequency only to 1, 3, 6 or 12 hours')

    def test_subscriptions_POST_already_subscribed(self):
        self.client.post(self.subscriptions_url, {"city": "kyiv",
                                                  "notification": 1})
        response = self.client.post(self.subscriptions_url, {"city": "kyiv",
                                                             "notification": 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], 'you have already subscribed to kyiv')

    def test_subscriptions_PUT_correct(self):
        self.client.post(self.subscriptions_url, {"city": "kyiv",
                                                  "notification": 1})
        response = self.client.put(self.subscriptions_url, {"city": "kyiv",
                                                            "notification": 3})
        for city in response.data["cities"]:
            if city["city"] == 'kyiv':
                notification = city["notification"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(notification, '03:00:00')

    def test_subscriptions_PUT_invalid_notification(self):
        self.client.post(self.subscriptions_url, {"city": "kyiv",
                                                  "notification": 1})
        response = self.client.put(self.subscriptions_url, {"city": "kyiv",
                                                            "notification": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], 'you can set notification frequency only to 1, 3, 6 or 12 hours')

    def test_subscriptions_PUT_not_subscribed(self):
        response = self.client.put(self.subscriptions_url, {"city": "kyiv",
                                                             "notification": 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], 'you need to subscribe to kyiv first')

    def test_subscriptions_DELETE_correct(self):
        self.client.post(self.subscriptions_url, {"city": "kyiv",
                                                  "notification": 1})
        response = self.client.delete(self.subscriptions_url, {"city": "kyiv"})
        self.assertEqual(response.status_code, 200)

    def test_subscriptions_DELETE_not_subscribed(self):
        response = self.client.delete(self.subscriptions_url, {"city": "kyiv"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], 'subscription not found')

    def test_delete_user_DELETE_correct(self):
        response = self.client.delete(self.delete_user_url, {"email": "test@gmail.com"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], 'deleted')

    def test_delete_user_DELETE_incorrect_email(self):
        response = self.client.delete(self.delete_user_url, {"email": "other@gmail.com"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "you can not delete someone else's user")

    def test_delete_user_DELETE_not_exist(self):
        response = self.client.delete(self.delete_user_url, {"email": "notexist@gmail.com"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "user does not exist")


class TestViewsNotLoggedIn(APITestCase):
    def setUp(self):
        self.home_url = reverse('home')
        self.subscriptions_url = reverse('subscriptions')
        self.delete_user_url = reverse('delete user')
        self.token_obtain_pair_url = reverse('token_obtain_pair')
        return super().setUp()

    def test_home_GET(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_subscriptions_GET(self):
        response = self.client.get(self.subscriptions_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_subscriptions_POST(self):
        response = self.client.post(self.subscriptions_url, {"city": "kyiv",
                                                             "notification": 1})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_subscriptions_PUT(self):
        response = self.client.put(self.subscriptions_url, {"city": "kyiv",
                                                            "notification": 1})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_subscriptions_DELETE(self):
        response = self.client.put(self.subscriptions_url, {"city": "kyiv"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_delete_user_DELETE(self):
        response = self.client.put(self.delete_user_url, {"email": "test@gmail.com"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
