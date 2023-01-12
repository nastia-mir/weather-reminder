from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

import requests
from datetime import date

from .models import MyUser, City
from .serializers import UserSerializer, CitySerializer
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
        params = {'q': 'kyiv', 'appid': API_KEY, 'units': 'metric'}
        context = {}

        r = requests.get(url=url, params=params)
        result = r.json()

        if result['cod'] == 200:
            context['city'] = result['name']
            context['weather'] = result['weather'][0]['main']
            context['description'] = result['weather'][0]['description']
            # context['icon'] = result['weather'][0]['icon']
            context['temp'] = result['main']['temp']
            context['date'] = date.today()
        elif result['cod'] == 404:
            context['city'] = None

        return Response(context)

    def post(self, request):
        url = 'http://api.openweathermap.org/data/2.5/weather'
        params = {'appid': API_KEY, 'units': 'metric', 'q': request.data["city"]}

        r = requests.get(url=url, params=params)
        result = r.json()
        context = {}

        if result['cod'] == 200:
            context['city'] = result['name']
            context['weather'] = result['weather'][0]['main']
            context['description'] = result['weather'][0]['description']
            # context['icon'] = result['weather'][0]['icon']
            context['temp'] = result['main']['temp']
            context['date'] = date.today()
        elif result['cod'] == 404:
            context['city'] = None

        return Response(context)


class SubscriptionsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        users = MyUser.objects.get(id=request.user.id)
        serialized = UserSerializer(users)
        return Response(serialized.data)

    def post(self, request):
        city = request.data['city']
        subsctiption = City(user=request.user, city=city)
        subsctiption.save()
        users = MyUser.objects.get(id=request.user.id)
        serialized = UserSerializer(users)
        return Response(serialized.data)


