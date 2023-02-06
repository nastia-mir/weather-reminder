from django.contrib import admin
from .models import MyUser, Subscription, Weather

admin.site.register(MyUser)
admin.site.register(Subscription)
admin.site.register(Weather)
