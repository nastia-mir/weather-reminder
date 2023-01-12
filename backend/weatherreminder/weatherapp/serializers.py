from rest_framework import serializers
from .models import MyUser, City


class UserSerializer(serializers.ModelSerializer):
    cities = serializers.StringRelatedField(many=True)

    class Meta:
        model = MyUser
        fields = ['id', 'email', 'is_staff', 'cities']