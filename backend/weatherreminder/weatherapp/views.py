from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from datetime import date

from .models import MyUser
from .serializers import UserSerializer


API_KEY = '31ee71338fd9a262442351ab26c5707e'


@api_view(['GET'])
def home(request):
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': 'kyiv', 'appid': API_KEY, 'units': 'metric'}
    context = {}

    # if request.POST:
    #     params['q'] = request.POST['city']

    r = requests.get(url=url, params=params)
    result = r.json()

    if result['cod'] == 200:
        context['city'] = result['name']
        context['weather'] = result['weather'][0]['main']
        context['description'] = result['weather'][0]['description']
        context['icon'] = result['weather'][0]['icon']
        context['temp'] = result['main']['temp']
        context['date'] = date.today()
    elif result['cod'] == 404:
        context['city'] = None


    # else:
    #     context['city'] = None

    return Response(context)


@api_view(['GET'])
def users(request):
    users = MyUser.objects.all()
    serialized = UserSerializer(users, many = True)
    return Response(serialized.data)
