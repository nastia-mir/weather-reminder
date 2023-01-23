from rest_framework.test import APITestCase

from weatherapp.services import get_weather
from weatherreminder.settings import API_KEY

class TestServices(APITestCase):
    def setUp(self):
        self.correct_cityname = "kyiv"
        self.incorrect_cityname = 'somecity'
        self.correct_api_key = API_KEY
        self.incorrect_aoi_key = "13vjglesiblsedjbskhnhtl"

        return super().setUp()

    def test_get_weather_correct(self):
        result = get_weather(self.correct_cityname, self.correct_api_key)
        self.assertEqual(result['city'].lower(), self.correct_cityname)

    def test_get_weather_incorrect_city(self):
        result = get_weather(self.incorrect_cityname, self.correct_api_key)
        self.assertEqual(result['city'], None)

    def test_get_weather_incorrect_api_key(self):
        result = get_weather(self.correct_cityname, self.incorrect_api_key)
        self.assertEqual(result['error'], "wrong api key")



