from weatherapp import views

from django.urls import reverse, resolve

from rest_framework.test import APITestCase
from rest_framework_simplejwt.views import TokenRefreshView


class TestUrls(APITestCase):
    def test_home(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.__name__, views.HomeView.as_view().__name__)

    def test_subscriptions(self):
        url = reverse('subscriptions')
        self.assertEqual(resolve(url).func.__name__, views.SubscriptionsView.as_view().__name__)

    def test_delete_user(self):
        url = reverse('delete user')
        self.assertEqual(resolve(url).func.__name__, views.DeleteUserView.as_view().__name__)

    def test_token_obtain_pair(self):
        url = reverse('token_obtain_pair')
        self.assertEqual(resolve(url).func.__name__, views.MyTokenObtainPairView.as_view().__name__)

    def test_token_refresh(self):
        url = reverse('token_refresh')
        self.assertEqual(resolve(url).func.__name__, TokenRefreshView.as_view().__name__)
