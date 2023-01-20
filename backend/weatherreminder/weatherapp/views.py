from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import date, time
import requests
from .models import MyUser, Subscription
from .serializers import UserSerializer, RegisterSerializer
from .services import get_weather
from weatherreminder.settings import API_KEY



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(self, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class HomeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        cities = list(Subscription.objects.filter(user=request.user).all())
        context = {}

        for city in cities:
            city_context = get_weather(city.city)
            context[city.city] = city_context

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

        notification = int(request.data['notification'])
        if notification not in [1, 3, 6, 12]:
            return Response({"message": "you can set notification frequency only to 1, 3, 6 or 12 hours"})

        if result['cod'] == '404':
            return Response({"message": "enter valid city name"})
        else:
            try:
                subscription = Subscription(user=request.user, city=city, notification=time(notification, 0, 0))
                subscription.save()
                user = MyUser.objects.get(id=request.user.id)
                serialized = UserSerializer(user)
                return Response(serialized.data)
            except IntegrityError:
                return Response({"message": "you have already subscribed to {}".format(city)})

    def put(self, request):
        city = request.data['city']
        notification = int(request.data['notification'])
        user = MyUser.objects.get(id=request.user.id)
        cities = [city['city'] for city in UserSerializer(user).data['cities']]

        if city in cities:
            if notification not in [1, 3, 6, 12]:
                return Response({"message": "you can set notification frequency only to 1, 3, 6 or 12 hours"})

            subscription = Subscription.objects.get(user=request.user, city=city)
            subscription.notification = time(notification, 0, 0)
            subscription.save()
            serialized = UserSerializer(user)
            return Response(serialized.data)
        else:
            return Response({"message": "you need to subscribe to {} first".format(city)})

    def delete(self, request):
        city = request.data['city']
        try:
            subscription = Subscription.objects.get(user=request.user, city=city)
            subscription.delete()
            return Response({city: "deleted"})
        except:
            return Response({"message": "subscription not found"})


class RegisterView(APIView):
    def post(self, request):
        try:
            existing_user = MyUser.objects.get(email=request.data["email"])
        except:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            serialized = UserSerializer(user)
            return Response(serialized.data)

        return Response({"message": "user with given email already exists"})


class DeleteUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        email = request.data["email"]
        try:
            user = MyUser.objects.get(email=email)
            if user == request.user:
                user.delete()
                return Response({"email": email,
                                 "message": 'deleted'})
            else:
                return Response({"message": "you can not delete someone else's user"})
        except:
            return Response({"message": "user does not exist"})




