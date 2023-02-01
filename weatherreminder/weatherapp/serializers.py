from rest_framework import serializers

from weatherapp.models import MyUser, Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['city', 'notification']


class UserSerializer(serializers.ModelSerializer):
    cities = SubscriptionSerializer(many=True)

    class Meta:
        model = MyUser
        fields = ['email', 'cities']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = MyUser.objects.create_user(validated_data['email'], validated_data['password'])
        return user
