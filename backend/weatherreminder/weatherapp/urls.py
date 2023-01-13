from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from .views import MyTokenObtainPairView

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('user/subscriptions/', views.SubscriptionsView.as_view(), name='subscriptions'),

    path('register/', views.RegisterView.as_view(), name='register'),


    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]