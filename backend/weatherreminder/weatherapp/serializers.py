from rest_framework import serializers
from .models import MyUser, City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city', 'notification']


class UserSerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True)

    class Meta:
        model = MyUser
        fields = ['id', 'email', 'cities']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = MyUser.objects.create_user(validated_data['email'], validated_data['password'])
        return user
