from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('user/subscriptions/', views.SubscriptionsView.as_view(), name='subscriptions'),

    path('register/', views.RegisterView.as_view(), name='register'),
    path('delete_user/', views.DeleteUserView.as_view(), name='delete user'),

    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]