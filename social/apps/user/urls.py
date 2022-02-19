from email.mime import base
from django.urls import path
from rest_framework import routers
from .views import LoginView, UserProfile, UserView
from rest_framework_simplejwt.views import TokenRefreshView

router = routers.DefaultRouter()
router.register('users/profiles', UserProfile, basename='profile')
router.register('users', UserView, basename='users')

urlpatterns = [
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

] + router.urls
