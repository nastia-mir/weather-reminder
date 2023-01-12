from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

import requests
from datetime import date

from .models import MyUser, City
from .serializers import UserSerializer
API_KEY = '31ee71338fd9a262442351ab26c5707e'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['first_name'] = user.first_name
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class HomeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        url = 'http://api.openweathermap.org/data/2.5/weather'
        user = MyUser.objects.get(id=request.user.id)
        cities = UserSerializer(user).data['cities']
        context = {}

        for city in cities:
            params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
            r = requests.get(url=url, params=params)
            result = r.json()
            city_context = {}

            if result['cod'] == 200:
                city_context['city'] = result['name']
                city_context['weather'] = result['weather'][0]['main']
                city_context['description'] = result['weather'][0]['description']
                # city_context['icon'] = result['weather'][0]['icon']
                city_context['temp'] = result['main']['temp']
                city_context['date'] = date.today()
            elif result['cod'] == '404':
                city_context['city'] = None

            context[city] = city_context

        return Response(context)


class SubscriptionsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        users = MyUser.objects.get(id=request.user.id)
        serialized = UserSerializer(users)
        return Response(serialized.data)

    def post(self, request):
        url = 'http://api.openweathermap.org/data/2.5/weather'
        city = request.data['city']

        params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
        r = requests.get(url=url, params=params)
        result = r.json()

        if result['cod'] == '404':
            return Response({"message": "enter valid city name"})
        else:
            subscription = City(user=request.user, city=city)
            subscription.save()
            user = MyUser.objects.get(id=request.user.id)
            serialized = UserSerializer(user)
            return Response(serialized.data)

    def delete(self, request):
        city = request.data['city']
        user = MyUser.objects.get(id=request.user.id)
        if city in UserSerializer(user).data['cities']:

            subscription = City.objects.get(user=request.user, city=city)
            subscription.delete()
            user = MyUser.objects.get(id=request.user.id)
            serialized = UserSerializer(user)
            return Response(serialized.data)

        else:
            return Response({"message": "subscription not found"})
