from rest_framework import serializers
from .models import MyUser


class UserSerializer(serializers.ModelSerializer):
    cities = serializers.StringRelatedField(many=True)

    class Meta:
        model = MyUser
        fields = ['id', 'email', 'cities']