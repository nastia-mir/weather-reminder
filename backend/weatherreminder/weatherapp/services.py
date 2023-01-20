import requests
import datetime
from weatherreminder.settings import API_KEY


def get_weather(cityname):
    url = 'http://api.openweathermap.org/data/2.5/weather'
    # params = {'q': city.city, 'appid': API_KEY, 'units': 'metric'}
    params = {'q': cityname, 'appid': API_KEY, 'units': 'metric'}
    r = requests.get(url=url, params=params)
    result = r.json()
    city_context = {}

    if result['cod'] == 200:
        city_context['city'] = result['name']
        city_context['weather'] = result['weather'][0]['main']
        city_context['description'] = result['weather'][0]['description']
        city_context['temp'] = result['main']['temp']
        city_context['date'] = datetime.date.today()
    elif result['cod'] == '404':
        city_context['city'] = None

    return city_context
