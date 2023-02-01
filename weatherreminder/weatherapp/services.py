import requests
import datetime

from rest_framework import status

from django.db import IntegrityError

from weatherreminderproject.settings import API_KEY

from weatherapp.models import MyUser, Subscription
from weatherapp.serializers import UserSerializer, SubscriptionSerializer


class WeatherReport:
    url = 'http://api.openweathermap.org/data/2.5/weather'

    @classmethod
    def get_weather(cls, cities):
        report = {}

        for city in cities:
            params = {'q': city.city, 'appid': API_KEY, 'units': 'metric'}
            r = requests.get(url=cls.url, params=params)
            result = r.json()
            city_report = {}

            if result['cod'] == 200:
                city_report['city'] = result['name']
                city_report['weather'] = result['weather'][0]['main']
                city_report['description'] = result['weather'][0]['description']
                city_report['temp'] = result['main']['temp']
            elif result['cod'] == '404':
                city_report['city'] = None
            elif result['cod'] == 401:
                city_report['error'] = "wrong api key"

            report[city.city] = city_report

        return report

    @classmethod
    def add_subscription(cls, cityname, notification, user):
        params = {'q': cityname, 'appid': API_KEY, 'units': 'metric'}
        r = requests.get(url=cls.url, params=params)
        result = r.json()
        context = {}

        if notification not in [1, 3, 6, 12]:
            context["status"] = status.HTTP_400_BAD_REQUEST
            context["data"] = {"message": "you can set notification frequency only to 1, 3, 6 or 12 hours"}

        elif result['cod'] == '404':
            context["status"] = status.HTTP_404_NOT_FOUND
            context["data"] = {"message": "enter valid city name"}

        else:
            try:
                subscription = Subscription(user=user, city=cityname, notification=notification)
                subscription_data = SubscriptionSerializer(subscription).data
                subscription.save()
                user = MyUser.objects.get(id=user.id)

                serialized = UserSerializer(user)
                context["status"] = status.HTTP_200_OK
                context["data"] = serialized.data
                # email_data = {
                #    'email': user.email,
                #    'city': subscription_data['city'],
                #    'notification': subscription_data['notification'],
                #    'weather': cls.get_weather([subscription])[subscription_data['city']]
                # }

            except IntegrityError:
                context["status"] = status.HTTP_400_BAD_REQUEST
                context["data"] = {"message": "you have already subscribed to {}".format(cityname)}

        return context

    @classmethod
    def edit_subscription(cls, cityname, notification, user):
        context = {}
        cities = [city['city'] for city in UserSerializer(MyUser.objects.get(id=user.id)).data['cities']]
        if cityname in cities:
            if notification not in [1, 3, 6, 12]:
                context["status"] = status.HTTP_400_BAD_REQUEST
                context["data"] = {"message": "you can set notification frequency only to 1, 3, 6 or 12 hours"}
            else:
                subscription = Subscription.objects.get(user=user, city=cityname)
                subscription.notification = notification
                subscription.save()
                serialized = UserSerializer(user)
                context["status"] = status.HTTP_200_OK
                context["data"] = serialized.data
        else:
            context["status"] = status.HTTP_404_NOT_FOUND
            context["data"] = {"message": "you need to subscribe to {} first".format(cityname)}

        return context

