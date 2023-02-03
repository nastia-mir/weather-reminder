import requests

from rest_framework import status

from django.db import IntegrityError

from weatherreminderproject.settings import API_KEY

from weatherapp.models import MyUser, Subscription, Weather
from weatherapp.serializers import UserSerializer, SubscriptionSerializer, WeatherSerializer


class WeatherReport:
    url = 'http://api.openweathermap.org/data/2.5/weather'

    @classmethod
    def get_weather(cls, cities):
        report = {}

        for city in cities:
            weather = Weather.objects.get(city=city.city)
            serialized = WeatherSerializer(weather)
            report[city.city] = serialized.data

        return report

    @classmethod
    def update_weather(cls):
        cities = Weather.objects.all()
        for city in cities:
            try:
                subscription = Subscription.objects.get(city=city.cityname)
            except:
                city.delete()

            params = {'q': city.city, 'appid': API_KEY, 'units': 'metric'}
            r = requests.get(url=cls.url, params=params)
            result = r.json()
            city.weather = result['weather'][0]['main']
            city.description = result['weather'][0]['description']
            city.temperature = result['main']['temp']
            city.save()

    @classmethod
    def add_subscription(cls, cityname, notification_frequency, user, url):
        params = {'q': cityname, 'appid': API_KEY, 'units': 'metric'}
        r = requests.get(url=cls.url, params=params)
        result = r.json()
        context = {}

        if notification_frequency not in [1, 3, 6, 12]:
            context["status"] = status.HTTP_400_BAD_REQUEST
            context["data"] = {"message": "you can set notification frequency only to 1, 3, 6 or 12 hours"}

        elif result['cod'] == '404':
            context["status"] = status.HTTP_404_NOT_FOUND
            context["data"] = {"message": "enter valid city name"}

        else:
            try:
                if url:
                    subscription = Subscription(user=user,
                                                city=cityname,
                                                notification_frequency=notification_frequency,
                                                url=url)
                else:
                    subscription = Subscription(user=user,
                                                city=cityname,
                                                notification_frequency=notification_frequency)
                subscription.save()
                user = MyUser.objects.get(id=user.id)

                try:
                    weather = Weather.objects.get(city=cityname)
                except:
                    weather = Weather(city=cityname,
                                      weather=result['weather'][0]['main'],
                                      description=result['weather'][0]['description'],
                                      temperature=result['main']['temp'])
                    weather.save()

                serialized = UserSerializer(user)
                context["status"] = status.HTTP_200_OK
                context["data"] = serialized.data

            except IntegrityError:
                context["status"] = status.HTTP_400_BAD_REQUEST
                context["data"] = {"message": "you have already subscribed to {}".format(cityname)}

        return context

    @classmethod
    def edit_subscription(cls, cityname, notification_frequency, user):
        context = {}
        cities = [city['city'] for city in UserSerializer(MyUser.objects.get(id=user.id)).data['cities']]
        if cityname in cities:
            if notification_frequency not in [1, 3, 6, 12]:
                context["status"] = status.HTTP_400_BAD_REQUEST
                context["data"] = {"message": "you can set notification frequency only to 1, 3, 6 or 12 hours"}
            else:
                subscription = Subscription.objects.get(user=user, city=cityname)
                subscription.notification_frequency = notification_frequency
                subscription.save()
                serialized = UserSerializer(user)
                context["status"] = status.HTTP_200_OK
                context["data"] = serialized.data
        else:
            context["status"] = status.HTTP_404_NOT_FOUND
            context["data"] = {"message": "you need to subscribe to {} first".format(cityname)}

        return context

