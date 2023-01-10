from django.shortcuts import render
from django.http import HttpResponse
import requests
from datetime import date

API_KEY = '31ee71338fd9a262442351ab26c5707e'


def home(request):
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'appid': API_KEY, 'units': 'metric'}
    context = {}

    if request.POST:
        params['q'] = request.POST['city']

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

    else:
        context['city'] = None

    return render(request, 'home.html', context)


