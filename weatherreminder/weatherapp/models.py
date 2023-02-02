from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class MyUserManager(BaseUserManager):

    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **other_fields)

    def create_user(self, email=None, password=None, **other_fields):
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email


class Subscription(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='cities')
    city = models.CharField(max_length=150, unique=True)
    notification = models.IntegerField(default=1)

    objects = models.Manager()

    def __str__(self):
        return self.city


class Weather(models.Model):
    city = models.CharField(max_length=150, unique=True)
    weather = models.CharField(max_length=500)
    description = models.CharField(max_length=10000)
    temperature = models.FloatField()

    objects = models.Manager()

    def __str__(self):
        return '{}, weather {}'.format(self.city, self.weather)

