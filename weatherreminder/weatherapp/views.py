import datetime
import requests

from django.db import IntegrityError

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status

from weatherapp.models import MyUser, Subscription
from weatherapp.serializers import UserSerializer, RegisterSerializer
from weatherapp.services import WeatherReport


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
        context = WeatherReport.get_weather(cities)
        return Response(context)


class SubscriptionsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serialized = UserSerializer(request.user)
        return Response(serialized.data)

    def post(self, request):
        city = request.data['city']
        notification_frequency = int(request.data['notification_frequency'])
        context = WeatherReport.add_subscription(city, notification_frequency, request.user)
        return Response(status=context["status"],
                        data=context["data"])

    def put(self, request):
        city = request.data['city']
        notification_frequency = int(request.data['notification_frequency'])
        context = WeatherReport.edit_subscription(city, notification_frequency, request.user)
        return Response(status=context["status"],
                        data=context["data"])

    def delete(self, request):
        city = request.data['city']
        Subscription.objects.filter(user=request.user, city=city).delete()
        return Response({city: "deleted"})


class RegisterView(APIView):
    def post(self, request):
        try:
            existing_user = MyUser.objects.get(email=request.data["email"])
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"message": "user with given email already exists"})
        except:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            serialized = UserSerializer(user)
            return Response(serialized.data)


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
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={"message": "you can not delete someone else's user"})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"message": "user does not exist"})
